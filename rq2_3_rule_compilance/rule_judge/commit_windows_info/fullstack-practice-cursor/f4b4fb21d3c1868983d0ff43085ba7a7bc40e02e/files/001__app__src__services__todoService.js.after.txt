import axios from "axios";

// 여기! 환경별 API URL 설정 추가
const API_BASE_URL =
  process.env.REACT_APP_API_BASE_URL || "http://localhost:8080/api/todos";

// 여기! Axios 인스턴스 생성 및 기본 설정 추가
const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || "http://localhost:8080/api",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

// 여기! 요청 인터셉터 추가 (로깅용)
apiClient.interceptors.request.use(
  (config) => {
    console.log(
      `🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`
    );
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 여기! 응답 인터셉터 추가 (에러 처리 개선)
apiClient.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error(
      `❌ API Error: ${error.response?.status} ${error.config?.url}`,
      error
    );
    return Promise.reject(error);
  }
);

const todoService = {
  // 여기! 백엔드 연결 상태 확인 메서드 추가
  async checkBackendHealth() {
    try {
      const response = await apiClient.get("/todos/health");
      return {
        isConnected: true,
        status: response.data.status,
        timestamp: response.data.timestamp,
      };
    } catch (error) {
      return {
        isConnected: false,
        error: error.message,
        timestamp: Date.now(),
      };
    }
  },

  // Get all todos
  async getAllTodos() {
    try {
      const response = await apiClient.get("/todos");
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || "Failed to fetch todos");
    }
  },

  // Get todo by ID
  async getTodoById(id) {
    try {
      const response = await apiClient.get(`/todos/${id}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || "Failed to fetch todo");
    }
  },

  // Create new todo
  async createTodo(todoData) {
    try {
      const response = await apiClient.post("/todos", todoData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || "Failed to create todo");
    }
  },

  // Update todo
  async updateTodo(id, todoData) {
    try {
      const response = await apiClient.put(`/todos/${id}`, todoData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || "Failed to update todo");
    }
  },

  // Toggle todo completion status
  async toggleTodoStatus(id) {
    try {
      const response = await apiClient.patch(`/todos/${id}/toggle`);
      return response.data;
    } catch (error) {
      throw new Error(
        error.response?.data?.message || "Failed to toggle todo status"
      );
    }
  },

  // Delete todo
  async deleteTodo(id) {
    try {
      await apiClient.delete(`/todos/${id}`);
      return true;
    } catch (error) {
      throw new Error(error.response?.data?.message || "Failed to delete todo");
    }
  },
};

export default todoService;
