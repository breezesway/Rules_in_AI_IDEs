import axios from "axios";

const API_BASE_URL = "http://localhost:8080/api/todos";

const todoService = {
  // Get all todos
  async getAllTodos() {
    try {
      const response = await axios.get(API_BASE_URL);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || "Failed to fetch todos");
    }
  },

  // Get todo by ID
  async getTodoById(id) {
    try {
      const response = await axios.get(`${API_BASE_URL}/${id}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || "Failed to fetch todo");
    }
  },

  // Create new todo
  async createTodo(todoData) {
    try {
      const response = await axios.post(API_BASE_URL, todoData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || "Failed to create todo");
    }
  },

  // Update todo
  async updateTodo(id, todoData) {
    try {
      const response = await axios.put(`${API_BASE_URL}/${id}`, todoData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || "Failed to update todo");
    }
  },

  // Toggle todo completion status
  async toggleTodoStatus(id) {
    try {
      const response = await axios.patch(`${API_BASE_URL}/${id}/toggle`);
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
      await axios.delete(`${API_BASE_URL}/${id}`);
      return true;
    } catch (error) {
      throw new Error(error.response?.data?.message || "Failed to delete todo");
    }
  },
};

export default todoService;
