import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import Header from '../components/layout/Header';
import TodoForm from '../components/TodoForm';
import TodoList from '../components/TodoList';
import { useAuth } from '../context/AuthContext';
import { useTodo } from '../context/TodoContext';
import './TodoPage.css';

const TodoPage = () => {
  const { t } = useTranslation('common');
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
            <h1>{t('home.title')}</h1>
            <p>{t('todo_page.hello')}, {user?.firstName || user?.username}님!</p>
            <p>{t('todo_page.manage_tasks')}</p>
          </div>
          
          <div className="action-section">
            <button
              className={`add-todo-btn ${showForm ? 'active' : ''}`}
              onClick={() => setShowForm(!showForm)}
            >
              {showForm ? t('cancel') : `+ ${t('todo_page.add_new_todo')}`}
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
