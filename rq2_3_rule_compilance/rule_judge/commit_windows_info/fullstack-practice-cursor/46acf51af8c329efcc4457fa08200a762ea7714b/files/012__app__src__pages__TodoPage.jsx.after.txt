import React, { useState } from 'react';
import Header from '../components/layout/Header';
import TodoForm from '../components/TodoForm';
import TodoList from '../components/TodoList';
import { useAuth } from '../context/AuthContext';
import { useTodo } from '../context/TodoContext';
import './TodoPage.css';

const TodoPage = () => {
  const { user } = useAuth();
  const { createTodo, loading } = useTodo();
  const [showForm, setShowForm] = useState(false);

  const handleCreateTodo = async (todoData) => {
    try {
      await createTodo(todoData);
      setShowForm(false);
    } catch (error) {
      // Error is handled by the TodoContext
      console.error('Failed to create todo:', error);
    }
  };

  return (
    <div className="todo-page">
      <Header />
      <div className="todo-page-container">
        <div className="todo-page-header">
          <div className="welcome-section">
            <h1>Welcome to Your Todo App!</h1>
            <p>Hello, {user?.firstName || user?.username}!</p>
            <p>Manage your tasks with deadlines and stay organized.</p>
          </div>
          
          <div className="action-section">
            <button
              className={`add-todo-btn ${showForm ? 'active' : ''}`}
              onClick={() => setShowForm(!showForm)}
            >
              {showForm ? 'Cancel' : '+ Add New Todo'}
            </button>
          </div>
        </div>

        {showForm && (
          <div className="form-section">
            <TodoForm 
              onSubmit={handleCreateTodo}
              loading={loading}
            />
          </div>
        )}

        <div className="todo-content">
          <TodoList />
        </div>
      </div>
    </div>
  );
};

export default TodoPage;
