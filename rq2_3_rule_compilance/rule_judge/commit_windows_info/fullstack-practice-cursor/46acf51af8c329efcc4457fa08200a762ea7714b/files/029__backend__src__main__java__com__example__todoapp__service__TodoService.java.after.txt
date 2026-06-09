package com.example.todoapp.service;

import com.example.todoapp.dto.TodoRequestDto;
import com.example.todoapp.dto.TodoResponseDto;
import com.example.todoapp.dto.TodoDeadlineStatsDto;
import com.example.todoapp.dto.TodoFilterDto;

import java.time.LocalDateTime;
import java.util.List;

public interface TodoService {

    // Basic CRUD operations for current user
    List<TodoResponseDto> getCurrentUserTodos();
    TodoResponseDto getCurrentUserTodoById(Long todoId);
    TodoResponseDto createTodoForCurrentUser(TodoRequestDto todoRequest);
    TodoResponseDto updateCurrentUserTodo(Long todoId, TodoRequestDto todoRequest);
    void deleteCurrentUserTodo(Long todoId);
    TodoResponseDto toggleCurrentUserTodoCompletion(Long todoId);
    
    // Deadline-specific operations
    List<TodoResponseDto> getCurrentUserTodosSortedByDeadline();
    List<TodoResponseDto> getCurrentUserTodosWithDeadlines();
    List<TodoResponseDto> getCurrentUserTodosWithoutDeadlines();
    List<TodoResponseDto> getCurrentUserOverdueTodos();
    List<TodoResponseDto> getCurrentUserDueSoonTodos();
    List<TodoResponseDto> getCurrentUserTodosByDateRange(LocalDateTime startDate, LocalDateTime endDate);
    
    // Deadline management
    TodoResponseDto setTodoDeadline(Long todoId, LocalDateTime deadline);
    TodoResponseDto removeTodoDeadline(Long todoId);
    
    // Statistics and analytics
    TodoDeadlineStatsDto getCurrentUserTodoStats();
    
    // Search and filter
    List<TodoResponseDto> searchCurrentUserTodos(String keyword);
    List<TodoResponseDto> filterCurrentUserTodos(TodoFilterDto filter);
}
