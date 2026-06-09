import apiClient from "./apiClient";

const todoService = {
  // Basic CRUD operations
  getCurrentUserTodos: () => apiClient.get("/todos"),
  getCurrentUserTodoById: (id) => apiClient.get(`/todos/${id}`),
  createTodoForCurrentUser: (todoData) => apiClient.post("/todos", todoData),
  updateCurrentUserTodo: (id, todoData) =>
    apiClient.put(`/todos/${id}`, todoData),
  deleteCurrentUserTodo: (id) => apiClient.delete(`/todos/${id}`),
  toggleCurrentUserTodoCompletion: (id) =>
    apiClient.patch(`/todos/${id}/toggle`),

  // Deadline-specific operations
  getCurrentUserTodosSortedByDeadline: () =>
    apiClient.get("/todos/sorted-by-deadline"),
  getCurrentUserTodosWithDeadlines: () =>
    apiClient.get("/todos/with-deadlines"),
  getCurrentUserTodosWithoutDeadlines: () =>
    apiClient.get("/todos/without-deadlines"),
  getCurrentUserOverdueTodos: () => apiClient.get("/todos/overdue"),
  getCurrentUserDueSoonTodos: () => apiClient.get("/todos/due-soon"),
  getCurrentUserTodosByDateRange: (startDate, endDate) =>
    apiClient.get("/todos/by-date-range", {
      params: { startDate, endDate },
    }),

  // Deadline management
  setTodoDeadline: (id, deadline) =>
    apiClient.patch(`/todos/${id}/deadline`, null, {
      params: { deadline },
    }),
  removeTodoDeadline: (id) => apiClient.delete(`/todos/${id}/deadline`),

  // Statistics and analytics
  getCurrentUserTodoStats: () => apiClient.get("/todos/stats"),

  // Search and filter
  searchCurrentUserTodos: (keyword) =>
    apiClient.get("/todos/search", { params: { keyword } }),
  filterCurrentUserTodos: (filter) => apiClient.post("/todos/filter", filter),
};

export default todoService;
