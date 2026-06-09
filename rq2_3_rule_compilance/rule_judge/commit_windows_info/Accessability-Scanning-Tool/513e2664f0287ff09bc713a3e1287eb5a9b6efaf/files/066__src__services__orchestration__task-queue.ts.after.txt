import { EventEmitter } from 'events';
import {
  AnalysisTask,
  TaskQueue as TaskQueueInterface,
  TaskResult,
  Worker,
  WorkerMetrics,
} from '../../core/types/common.js';
import { BrowserManager } from '../../core/utils/browser-manager.js';
import { PerformanceMonitor } from '../../core/utils/performance-monitor.js';
import { AnalysisWorker } from './analysis-worker.js';

export class TaskQueue extends EventEmitter {
  private static instance: TaskQueue;
  private queue: TaskQueueInterface = {
    pending: [],
    processing: [],
    completed: [],
    failed: [],
  };
  private workers: Map<string, AnalysisWorker> = new Map();
  private maxConcurrentTasks: number = 5;
  private processingInterval: NodeJS.Timer | null = null;
  private performanceMonitor: PerformanceMonitor;
  private isShuttingDown: boolean = false;

  private constructor() {
    super();
    this.performanceMonitor = PerformanceMonitor.getInstance();
    this.initializeWorkers();
    this.startProcessing();
  }

  public static getInstance(): TaskQueue {
    if (!TaskQueue.instance) {
      TaskQueue.instance = new TaskQueue();
    }
    return TaskQueue.instance;
  }

  private async initializeWorkers(): Promise<void> {
    const browserManager = BrowserManager.getInstance();

    for (let i = 0; i < this.maxConcurrentTasks; i++) {
      const workerId = `worker-${i + 1}`;
      const worker = new AnalysisWorker(workerId, browserManager);
      this.workers.set(workerId, worker);

      worker.on('taskCompleted', (result: TaskResult) => {
        this.handleTaskCompletion(result);
      });

      worker.on('taskFailed', (result: TaskResult) => {
        this.handleTaskFailure(result);
      });
    }
  }

  public async addTask(task: AnalysisTask): Promise<string> {
    if (this.isShuttingDown) {
      throw new Error('Task queue is shutting down');
    }

    // Validate task
    if (!task.url || !task.type) {
      throw new Error('Invalid task: URL and type are required');
    }

    // Add to pending queue with priority sorting
    this.queue.pending.push(task);
    this.queue.pending.sort((a, b) => {
      const priorityOrder = { high: 3, medium: 2, low: 1 };
      return priorityOrder[b.priority] - priorityOrder[a.priority];
    });

    this.emit('taskAdded', task);
    this.performanceMonitor.recordMetric('queue_size', this.queue.pending.length);

    return task.id;
  }

  public async addBatch(tasks: AnalysisTask[]): Promise<string[]> {
    const taskIds: string[] = [];

    for (const task of tasks) {
      const taskId = await this.addTask(task);
      taskIds.push(taskId);
    }

    return taskIds;
  }

  private startProcessing(): void {
    this.processingInterval = setInterval(() => {
      this.processQueue();
    }, 1000); // Check every second
  }

  private async processQueue(): Promise<void> {
    if (this.isShuttingDown) {
      return;
    }

    const availableWorkers = Array.from(this.workers.values()).filter(worker =>
      worker.isAvailable()
    );

    if (availableWorkers.length === 0 || this.queue.pending.length === 0) {
      return;
    }

    const tasksToProcess = Math.min(availableWorkers.length, this.queue.pending.length);

    for (let i = 0; i < tasksToProcess; i++) {
      const task = this.queue.pending.shift()!;
      const worker = availableWorkers[i];

      task.startedAt = new Date();
      this.queue.processing.push(task);

      try {
        await worker.processTask(task);
        this.emit('taskStarted', task);
      } catch (error) {
        this.handleTaskFailure({
          taskId: task.id,
          success: false,
          error: error as Error,
          duration: Date.now() - task.startedAt!.getTime(),
          memoryUsage: process.memoryUsage().heapUsed,
          workerMetrics: worker.getMetrics(),
        });
      }
    }
  }

  private handleTaskCompletion(result: TaskResult): void {
    const taskIndex = this.queue.processing.findIndex(t => t.id === result.taskId);
    if (taskIndex !== -1) {
      const task = this.queue.processing.splice(taskIndex, 1)[0];
      task.completedAt = new Date();
      this.queue.completed.push(task);

      this.emit('taskCompleted', result);
      this.performanceMonitor.recordMetric('tasks_completed', this.queue.completed.length);
      this.performanceMonitor.recordMetric('processing_time', result.duration);
    }
  }

  private handleTaskFailure(result: TaskResult): void {
    const taskIndex = this.queue.processing.findIndex(t => t.id === result.taskId);
    if (taskIndex !== -1) {
      const task = this.queue.processing.splice(taskIndex, 1)[0];

      // Retry logic
      if (task.retryCount < task.maxRetries) {
        task.retryCount++;
        task.startedAt = undefined;
        this.queue.pending.unshift(task); // Add to front for retry
        this.emit('taskRetry', task);
      } else {
        task.completedAt = new Date();
        this.queue.failed.push(task);
        this.emit('taskFailed', result);
        this.performanceMonitor.recordMetric('tasks_failed', this.queue.failed.length);
      }
    }
  }

  public getQueueStatus(): TaskQueueInterface {
    return {
      pending: [...this.queue.pending],
      processing: [...this.queue.processing],
      completed: [...this.queue.completed],
      failed: [...this.queue.failed],
    };
  }

  public getWorkerStatus(): Worker[] {
    return Array.from(this.workers.values()).map(worker => ({
      id: worker.getId(),
      isAvailable: worker.isAvailable(),
      currentTask: worker.getCurrentTask(),
      processedTasks: worker.getProcessedTaskCount(),
      totalProcessingTime: worker.getTotalProcessingTime(),
      lastActivity: worker.getLastActivity(),
      metrics: worker.getMetrics(),
    }));
  }

  public async getTaskResult(taskId: string): Promise<TaskResult | null> {
    const completedTask = this.queue.completed.find(t => t.id === taskId);
    if (completedTask) {
      return {
        taskId,
        success: true,
        duration: completedTask.completedAt!.getTime() - completedTask.startedAt!.getTime(),
        memoryUsage: process.memoryUsage().heapUsed,
        workerMetrics: this.getWorkerMetrics(),
      };
    }

    const failedTask = this.queue.failed.find(t => t.id === taskId);
    if (failedTask) {
      return {
        taskId,
        success: false,
        duration: failedTask.completedAt!.getTime() - failedTask.startedAt!.getTime(),
        memoryUsage: process.memoryUsage().heapUsed,
        workerMetrics: this.getWorkerMetrics(),
      };
    }

    return null;
  }

  private getWorkerMetrics(): WorkerMetrics {
    const workers = Array.from(this.workers.values());
    const totalTasks = workers.reduce((sum, w) => sum + w.getProcessedTaskCount(), 0);
    const totalTime = workers.reduce((sum, w) => sum + w.getTotalProcessingTime(), 0);

    return {
      tasksProcessed: totalTasks,
      averageProcessingTime: totalTasks > 0 ? totalTime / totalTasks : 0,
      memoryUsage: process.memoryUsage().heapUsed,
      errorRate:
        this.queue.failed.length /
        Math.max(1, this.queue.completed.length + this.queue.failed.length),
      uptime: process.uptime(),
    };
  }

  public async scaleWorkers(targetWorkers: number): Promise<void> {
    if (targetWorkers < 1 || targetWorkers > 20) {
      throw new Error('Worker count must be between 1 and 20');
    }

    const currentWorkers = this.workers.size;
    const browserManager = BrowserManager.getInstance();

    if (targetWorkers > currentWorkers) {
      // Scale up
      for (let i = currentWorkers; i < targetWorkers; i++) {
        const workerId = `worker-${i + 1}`;
        const worker = new AnalysisWorker(workerId, browserManager);
        this.workers.set(workerId, worker);

        worker.on('taskCompleted', (result: TaskResult) => {
          this.handleTaskCompletion(result);
        });

        worker.on('taskFailed', (result: TaskResult) => {
          this.handleTaskFailure(result);
        });
      }
    } else if (targetWorkers < currentWorkers) {
      // Scale down
      const workersToRemove = Array.from(this.workers.keys()).slice(targetWorkers);
      for (const workerId of workersToRemove) {
        const worker = this.workers.get(workerId);
        if (worker && worker.isAvailable()) {
          await worker.cleanup();
          this.workers.delete(workerId);
        }
      }
    }

    this.maxConcurrentTasks = targetWorkers;
    this.emit('workersScaled', { targetWorkers, currentWorkers: this.workers.size });
  }

  public async waitForCompletion(taskId: string, timeout: number = 30000): Promise<TaskResult> {
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        reject(new Error(`Task ${taskId} timed out after ${timeout}ms`));
      }, timeout);

      const checkCompletion = () => {
        const result = this.getTaskResult(taskId);
        if (result) {
          clearTimeout(timer);
          resolve(result);
        } else {
          setTimeout(checkCompletion, 1000);
        }
      };

      checkCompletion();
    });
  }

  public async shutdown(): Promise<void> {
    this.isShuttingDown = true;

    if (this.processingInterval) {
      clearInterval(this.processingInterval);
    }

    // Wait for processing tasks to complete
    while (this.queue.processing.length > 0) {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }

    // Cleanup workers
    for (const worker of this.workers.values()) {
      await worker.cleanup();
    }

    this.workers.clear();
    this.emit('shutdown');
  }
}
