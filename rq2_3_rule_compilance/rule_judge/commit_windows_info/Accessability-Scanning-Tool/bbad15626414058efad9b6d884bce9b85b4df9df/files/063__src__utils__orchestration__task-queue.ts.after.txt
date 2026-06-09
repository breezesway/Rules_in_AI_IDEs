import { EventEmitter } from 'events';
import {
  AnalysisTask,
  TaskQueue as TaskQueueInterface,
  TaskResult,
  Worker,
  WorkerMetrics,
} from '@/core/types/common.js';
import { BrowserManager } from '@/core/utils/browser-manager.js';
import { AnalysisWorker } from '@/utils/orchestration/analysis-worker.js';
import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { ConfigurationService } from '@/utils/services/configuration-service';

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
  private isShuttingDown: boolean = false;

  private constructor() {
    super();
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
      worker.getIsAvailable()
    );

    if (availableWorkers.length === 0 || this.queue.pending.length === 0) {
      return;
    }

    const tasksToProcess = Math.min(availableWorkers.length, this.queue.pending.length);

    for (let i = 0; i < tasksToProcess; i++) {
      const task = this.queue.pending.shift();
      const worker = availableWorkers[i];

      if (!task || !worker) continue;

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
      if (!task) return;

      task.completedAt = new Date();
      this.queue.completed.push(task);

      this.emit('taskCompleted', result);
    }
  }

  private handleTaskFailure(result: TaskResult): void {
    const taskIndex = this.queue.processing.findIndex(t => t.id === result.taskId);
    if (taskIndex !== -1) {
      const task = this.queue.processing.splice(taskIndex, 1)[0];
      if (!task) return;

      // Retry logic
      if (task.retryCount < task.maxRetries) {
        task.retryCount++;
        task.startedAt = undefined as any;
        this.queue.pending.unshift(task); // Add to front for retry
        this.emit('taskRetry', task);
      } else {
        task.completedAt = new Date();
        this.queue.failed.push(task);
        this.emit('taskFailed', result);
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
      isAvailable: worker.getIsAvailable(),
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
        this.emit('workerAdded', workerId);
      }
    } else if (targetWorkers < currentWorkers) {
      // Scale down
      const workersToShutdown = Array.from(this.workers.values()).slice(targetWorkers);

      for (const worker of workersToShutdown) {
        if (worker.getIsAvailable()) {
          this.workers.delete(worker.getId());
          this.emit('workerRemoved', worker.getId());
        } else {
          // Worker is busy, mark for shutdown after task completion
          worker.once('taskCompleted', () => {
            this.workers.delete(worker.getId());
            this.emit('workerRemoved', worker.getId());
          });
        }
      }
    }

    this.maxConcurrentTasks = targetWorkers;
    this.emit('scaled', this.maxConcurrentTasks);
  }

  public async waitForCompletion(taskId: string, timeout: number = 30000): Promise<TaskResult> {
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        reject(new Error(`Task ${taskId} timed out after ${timeout}ms`));
      }, timeout);

      const checkCompletion = async () => {
        const result = await this.getTaskResult(taskId);
        if (result === null) {
          // Task not found, check again later
          setTimeout(checkCompletion, 1000);
        } else {
          clearTimeout(timer);
          resolve(result);
        }
      };

      checkCompletion();
    });
  }

  public async shutdown(): Promise<void> {
    this.isShuttingDown = true;
    this.emit('shuttingDown');

    // Stop processing new tasks
    if (this.processingInterval) {
      clearInterval(this.processingInterval as unknown as number);
      this.processingInterval = null;
    }

    // Wait for ongoing tasks to complete
    const ongoingTasks = this.queue.processing.map(
      task =>
        new Promise(resolve => {
          this.once(`taskCompleted:${task.id}`, resolve);
          this.once(`taskFailed:${task.id}`, resolve);
        })
    );

    await Promise.all(ongoingTasks);

    // Cleanup workers
    for (const worker of this.workers.values()) {
      await worker.cleanup();
    }

    this.emit('shutdown');
  }
}
