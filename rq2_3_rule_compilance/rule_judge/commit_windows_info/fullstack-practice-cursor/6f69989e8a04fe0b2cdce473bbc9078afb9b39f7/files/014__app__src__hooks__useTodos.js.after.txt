import { useState, useEffect, useCallback } from "react";
import todoService from "../services/todoService";

const useTodos = () => {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch all todos
  const fetchTodos = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await todoService.getAllTodos();
      setTodos(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  // Create new todo
  const createTodo = useCallback(async (todoData) => {
    try {
      setLoading(true);
      setError(null);
      const newTodo = await todoService.createTodo(todoData);
      setTodos((prev) => [...prev, newTodo]);
      return newTodo;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  // Update todo
  const updateTodo = useCallback(async (id, todoData) => {
    try {
      setLoading(true);
      setError(null);
      const updatedTodo = await todoService.updateTodo(id, todoData);
      setTodos((prev) =>
        prev.map((todo) => (todo.id === id ? updatedTodo : todo))
      );
      return updatedTodo;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  // Toggle todo completion status
  const toggleTodoStatus = useCallback(async (id) => {
    try {
      setLoading(true);
      setError(null);
      const toggledTodo = await todoService.toggleTodoStatus(id);
      setTodos((prev) =>
        prev.map((todo) => (todo.id === id ? toggledTodo : todo))
      );
      return toggledTodo;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  // Delete todo
  const deleteTodo = useCallback(async (id) => {
    try {
      setLoading(true);
      setError(null);
      await todoService.deleteTodo(id);
      setTodos((prev) => prev.filter((todo) => todo.id !== id));
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  // Clear error
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  // Load todos on component mount
  useEffect(() => {
    fetchTodos();
  }, [fetchTodos]);

  return {
    todos,
    loading,
    error,
    createTodo,
    updateTodo,
    toggleTodoStatus,
    deleteTodo,
    fetchTodos,
    clearError,
  };
};

export default useTodos;
