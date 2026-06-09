import React from "react";
import TodoForm from "./components/TodoForm";
import TodoList from "./components/TodoList";
import useTodos from "./hooks/useTodos";
import "./App.css";

function App() {
  const {
    todos,
    loading,
    error,
    createTodo,
    updateTodo,
    toggleTodoStatus,
    deleteTodo,
    clearError,
  } = useTodos();

  const handleCreateTodo = async (todoData) => {
    try {
      await createTodo(todoData);
    } catch (error) {
      console.error("Failed to create todo:", error);
    }
  };

  const handleUpdateTodo = async (id, todoData) => {
    try {
      await updateTodo(id, todoData);
    } catch (error) {
      console.error("Failed to update todo:", error);
    }
  };

  const handleToggleTodo = async (id) => {
    try {
      await toggleTodoStatus(id);
    } catch (error) {
      console.error("Failed to toggle todo:", error);
    }
  };

  const handleDeleteTodo = async (id) => {
    try {
      await deleteTodo(id);
    } catch (error) {
      console.error("Failed to delete todo:", error);
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <div className="container">
          <h1>📝 Todo App</h1>
          <p>Organize your tasks efficiently</p>
        </div>
      </header>

      <main className="app-main">
        <div className="container">
          {error && (
            <div className="error-banner" onClick={clearError}>
              <span>⚠️ {error}</span>
              <button className="close-error">×</button>
            </div>
          )}

          <TodoForm onSubmit={handleCreateTodo} loading={loading} />

          <TodoList
            todos={todos}
            loading={loading}
            onUpdate={handleUpdateTodo}
            onToggle={handleToggleTodo}
            onDelete={handleDeleteTodo}
          />
        </div>
      </main>

      <footer className="app-footer">
        <div className="container">
          <p>&copy; 2024 Todo App. Built with React & Spring Boot.</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
