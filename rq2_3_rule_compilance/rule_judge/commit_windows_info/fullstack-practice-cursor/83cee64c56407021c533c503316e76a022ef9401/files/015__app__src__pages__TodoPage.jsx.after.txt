import React from 'react';
import Header from '../components/layout/Header';
import { useAuth } from '../context/AuthContext';

const TodoPage = () => {
  const { user } = useAuth();

  return (
    <div>
      <Header />
      <div style={{
        maxWidth: '1200px',
        margin: '0 auto',
        padding: '40px 20px'
      }}>
        <h1>Welcome to Your Todo App!</h1>
        <p>Hello, {user?.firstName || user?.username}!</p>
        <p>You are successfully logged in. This is where your todos will be displayed.</p>
        <p>Todo functionality will be implemented in the next phase.</p>
      </div>
    </div>
  );
};

export default TodoPage;
