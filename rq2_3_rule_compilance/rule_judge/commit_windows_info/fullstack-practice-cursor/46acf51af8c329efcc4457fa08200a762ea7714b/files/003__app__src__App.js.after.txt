import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { TodoProvider } from "./context/TodoContext";
import ProtectedRoute from "./components/auth/ProtectedRoute";
import HomePage from "./pages/HomePage";
import LoginForm from "./components/auth/LoginForm";
import RegisterForm from "./components/auth/RegisterForm";
import LoginSuccessPage from "./pages/LoginSuccessPage";
import EmailVerificationPage from "./pages/EmailVerificationPage";
import TodoPage from "./pages/TodoPage";
import "./App.css";

function App() {
  return (
    <AuthProvider>
      <TodoProvider>
        <Router>
          <div className="App">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/login" element={<LoginForm />} />
              <Route path="/register" element={<RegisterForm />} />
              <Route path="/verify-email" element={<EmailVerificationPage />} />
              <Route
                path="/login-success"
                element={
                  <ProtectedRoute>
                    <LoginSuccessPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/todos"
                element={
                  <ProtectedRoute>
                    <TodoPage />
                  </ProtectedRoute>
                }
              />
            </Routes>
          </div>
        </Router>
      </TodoProvider>
    </AuthProvider>
  );
}

export default App;
