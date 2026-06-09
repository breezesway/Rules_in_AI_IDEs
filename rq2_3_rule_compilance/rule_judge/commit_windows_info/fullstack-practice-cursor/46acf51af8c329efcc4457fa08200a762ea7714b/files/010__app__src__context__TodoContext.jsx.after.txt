import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { useAuth } from './AuthContext';
import todoService from '../services/todoService';

const TodoContext = createContext();

export const useTodo = () => {
  const context = useContext(TodoContext);
  if (!context) {
    throw new Error('useTodo must be used within a TodoProvider');
  }
  return context;
};

export const TodoProvider = ({ children }) => {
  const { user, isAuthenticated } = useAuth();
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState(null);

  // Load todos when user is authenticated
  useEffect(() => {
    if (isAuthenticated && user) {
      loadTodos();
      loadStats();
    } else {
      setTodos([]);
      setStats(null);
    }
  }, [isAuthenticated, user]);

  const loadTodos = useCallback(async () => {
    if (!isAuthenticated) return;
    
    setLoading(true);
    setError(null);
    try {
      const response = await todoService.getCurrentUserTodos();
      setTodos(response.data || []);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to load todos');
      console.error('Error loading todos:', err);
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated]);

  const loadStats = useCallback(async () => {
    if (!isAuthenticated) return;
    
    try {
      const response = await todoService.getCurrentUserTodoStats();
      setStats(response.data || null);
    } catch (err) {
      console.error('Error loading stats:', err);
    }
  }, [isAuthenticated]);

  const createTodo = useCallback(async (todoData) => {
    if (!isAuthenticated) return null;
    
    setError(null);
    try {
      const response = await todoService.createTodoForCurrentUser(todoData);
      const newTodo = response.data;
      setTodos(prev => [newTodo, ...prev]);
      await loadStats(); // Refresh stats
      return newTodo;
    } catch (err) {
      const errorMsg = err.response?.data?.message || 'Failed to create todo';
      setError(errorMsg);
      throw new Error(errorMsg);
    }
  }, [isAuthenticated, loadStats]);

  const updateTodo = useCallback(async (id, todoData) => {
    if (!isAuthenticated) return null;
    
    setError(null);
    try {
      const response = await todoService.updateCurrentUserTodo(id, todoData);
      const updatedTodo = response.data;
      setTodos(prev => prev.map(todo => 
        todo.id === id ? updatedTodo : todo
      ));
      await loadStats(); // Refresh stats
      return updatedTodo;
    } catch (err) {
      const errorMsg = err.response?.data?.message || 'Failed to update todo';
      setError(errorMsg);
      throw new Error(errorMsg);
    }
  }, [isAuthenticated, loadStats]);

  const deleteTodo = useCallback(async (id) => {
    if (!isAuthenticated) return false;
    
    setError(null);
    try {
      await todoService.deleteCurrentUserTodo(id);
      setTodos(prev => prev.filter(todo => todo.id !== id));
      await loadStats(); // Refresh stats
      return true;
    } catch (err) {
      const errorMsg = err.response?.data?.message || 'Failed to delete todo';
      setError(errorMsg);
      throw new Error(errorMsg);
    }
  }, [isAuthenticated, loadStats]);

  const toggleTodoCompletion = useCallback(async (id) => {
    if (!isAuthenticated) return null;
    
    setError(null);
    try {
      const response = await todoService.toggleCurrentUserTodoCompletion(id);
      const updatedTodo = response.data;
      setTodos(prev => prev.map(todo => 
        todo.id === id ? updatedTodo : todo
      ));
      await loadStats(); // Refresh stats
      return updatedTodo;
    } catch (err) {
      const errorMsg = err.response?.data?.message || 'Failed to toggle todo completion';
      setError(errorMsg);
      throw new Error(errorMsg);
    }
  }, [isAuthenticated, loadStats]);

  const setTodoDeadline = useCallback(async (id, deadline) => {
    if (!isAuthenticated) return null;
    
    setError(null);
    try {
      const response = await todoService.setTodoDeadline(id, deadline);
      const updatedTodo = response.data;
      setTodos(prev => prev.map(todo => 
        todo.id === id ? updatedTodo : todo
      ));
      await loadStats(); // Refresh stats
      return updatedTodo;
    } catch (err) {
      const errorMsg = err.response?.data?.message || 'Failed to set deadline';
      setError(errorMsg);
      throw new Error(errorMsg);
    }
  }, [isAuthenticated, loadStats]);

  const removeTodoDeadline = useCallback(async (id) => {
    if (!isAuthenticated) return null;
    
    setError(null);
    try {
      const response = await todoService.removeTodoDeadline(id);
      const updatedTodo = response.data;
      setTodos(prev => prev.map(todo => 
        todo.id === id ? updatedTodo : todo
      ));
      await loadStats(); // Refresh stats
      return updatedTodo;
    } catch (err) {
      const errorMsg = err.response?.data?.message || 'Failed to remove deadline';
      setError(errorMsg);
      throw new Error(errorMsg);
    }
  }, [isAuthenticated, loadStats]);

  const searchTodos = useCallback(async (keyword) => {
    if (!isAuthenticated) return [];
    
    setError(null);
    try {
      const response = await todoService.searchCurrentUserTodos(keyword);
      return response.data || [];
    } catch (err) {
      const errorMsg = err.response?.data?.message || 'Failed to search todos';
      setError(errorMsg);
      throw new Error(errorMsg);
    }
  }, [isAuthenticated]);

  const filterTodos = useCallback(async (filter) => {
    if (!isAuthenticated) return [];
    
    setError(null);
    try {
      const response = await todoService.filterCurrentUserTodos(filter);
      return response.data || [];
    } catch (err) {
      const errorMsg = err.response?.data?.message || 'Failed to filter todos';
      setError(errorMsg);
      throw new Error(errorMsg);
    }
  }, [isAuthenticated]);

  const getOverdueTodos = useCallback(async () => {
    if (!isAuthenticated) return [];
    
    setError(null);
    try {
      const response = await todoService.getCurrentUserOverdueTodos();
      return response.data || [];
    } catch (err) {
      const errorMsg = err.response?.data?.message || 'Failed to get overdue todos';
      setError(errorMsg);
      throw new Error(errorMsg);
    }
  }, [isAuthenticated]);

  const getDueSoonTodos = useCallback(async () => {
    if (!isAuthenticated) return [];
    
    setError(null);
    try {
      const response = await todoService.getCurrentUserDueSoonTodos();
      return response.data || [];
    } catch (err) {
      const errorMsg = err.response?.data?.message || 'Failed to get due soon todos';
      setError(errorMsg);
      throw new Error(errorMsg);
    }
  }, [isAuthenticated]);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const value = {
    todos,
    loading,
    error,
    stats,
    createTodo,
    updateTodo,
    deleteTodo,
    toggleTodoCompletion,
    setTodoDeadline,
    removeTodoDeadline,
    searchTodos,
    filterTodos,
    getOverdueTodos,
    getDueSoonTodos,
    loadTodos,
    loadStats,
    clearError
  };

  return (
    <TodoContext.Provider value={value}>
      {children}
    </TodoContext.Provider>
  );
};
