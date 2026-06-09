package com.example.todoapp.controller;

import com.example.todoapp.dto.TodoRequestDto;
import com.example.todoapp.dto.TodoResponseDto;
import com.example.todoapp.dto.TodoDeadlineStatsDto;
import com.example.todoapp.dto.TodoFilterDto;
import com.example.todoapp.service.TodoService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;

@RestController
@RequestMapping("/api/todos")
@RequiredArgsConstructor
@CrossOrigin(origins = "http://localhost:3000")
public class TodoController {

    private final TodoService todoService;

    // Basic CRUD operations for current user
    @GetMapping
    public ResponseEntity<List<TodoResponseDto>> getCurrentUserTodos() {
        List<TodoResponseDto> todos = todoService.getCurrentUserTodos();
        return ResponseEntity.ok(todos);
    }

    @GetMapping("/{id}")
    public ResponseEntity<TodoResponseDto> getCurrentUserTodoById(@PathVariable Long id) {
        TodoResponseDto todo = todoService.getCurrentUserTodoById(id);
        return ResponseEntity.ok(todo);
    }

    @PostMapping
    public ResponseEntity<TodoResponseDto> createTodoForCurrentUser(@Valid @RequestBody TodoRequestDto todoRequestDto) {
        TodoResponseDto createdTodo = todoService.createTodoForCurrentUser(todoRequestDto);
        return ResponseEntity.status(HttpStatus.CREATED).body(createdTodo);
    }

    @PutMapping("/{id}")
    public ResponseEntity<TodoResponseDto> updateCurrentUserTodo(
            @PathVariable Long id,
            @Valid @RequestBody TodoRequestDto todoRequestDto) {
        TodoResponseDto updatedTodo = todoService.updateCurrentUserTodo(id, todoRequestDto);
        return ResponseEntity.ok(updatedTodo);
    }

    @PatchMapping("/{id}/toggle")
    public ResponseEntity<TodoResponseDto> toggleCurrentUserTodoCompletion(@PathVariable Long id) {
        TodoResponseDto toggledTodo = todoService.toggleCurrentUserTodoCompletion(id);
        return ResponseEntity.ok(toggledTodo);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteCurrentUserTodo(@PathVariable Long id) {
        todoService.deleteCurrentUserTodo(id);
        return ResponseEntity.noContent().build();
    }

    // Deadline-specific endpoints
    @GetMapping("/sorted-by-deadline")
    public ResponseEntity<List<TodoResponseDto>> getCurrentUserTodosSortedByDeadline() {
        List<TodoResponseDto> todos = todoService.getCurrentUserTodosSortedByDeadline();
        return ResponseEntity.ok(todos);
    }

    @GetMapping("/with-deadlines")
    public ResponseEntity<List<TodoResponseDto>> getCurrentUserTodosWithDeadlines() {
        List<TodoResponseDto> todos = todoService.getCurrentUserTodosWithDeadlines();
        return ResponseEntity.ok(todos);
    }

    @GetMapping("/without-deadlines")
    public ResponseEntity<List<TodoResponseDto>> getCurrentUserTodosWithoutDeadlines() {
        List<TodoResponseDto> todos = todoService.getCurrentUserTodosWithoutDeadlines();
        return ResponseEntity.ok(todos);
    }

    @GetMapping("/overdue")
    public ResponseEntity<List<TodoResponseDto>> getCurrentUserOverdueTodos() {
        List<TodoResponseDto> todos = todoService.getCurrentUserOverdueTodos();
        return ResponseEntity.ok(todos);
    }

    @GetMapping("/due-soon")
    public ResponseEntity<List<TodoResponseDto>> getCurrentUserDueSoonTodos() {
        List<TodoResponseDto> todos = todoService.getCurrentUserDueSoonTodos();
        return ResponseEntity.ok(todos);
    }

    @GetMapping("/by-date-range")
    public ResponseEntity<List<TodoResponseDto>> getCurrentUserTodosByDateRange(
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime startDate,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime endDate) {
        List<TodoResponseDto> todos = todoService.getCurrentUserTodosByDateRange(startDate, endDate);
        return ResponseEntity.ok(todos);
    }

    // Deadline management
    @PatchMapping("/{id}/deadline")
    public ResponseEntity<TodoResponseDto> setTodoDeadline(
            @PathVariable Long id,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime deadline) {
        TodoResponseDto updatedTodo = todoService.setTodoDeadline(id, deadline);
        return ResponseEntity.ok(updatedTodo);
    }

    @DeleteMapping("/{id}/deadline")
    public ResponseEntity<TodoResponseDto> removeTodoDeadline(@PathVariable Long id) {
        TodoResponseDto updatedTodo = todoService.removeTodoDeadline(id);
        return ResponseEntity.ok(updatedTodo);
    }

    // Statistics and analytics
    @GetMapping("/stats")
    public ResponseEntity<TodoDeadlineStatsDto> getCurrentUserTodoStats() {
        TodoDeadlineStatsDto stats = todoService.getCurrentUserTodoStats();
        return ResponseEntity.ok(stats);
    }

    // Search and filter
    @GetMapping("/search")
    public ResponseEntity<List<TodoResponseDto>> searchCurrentUserTodos(@RequestParam String keyword) {
        List<TodoResponseDto> todos = todoService.searchCurrentUserTodos(keyword);
        return ResponseEntity.ok(todos);
    }

    @PostMapping("/filter")
    public ResponseEntity<List<TodoResponseDto>> filterCurrentUserTodos(@RequestBody TodoFilterDto filter) {
        List<TodoResponseDto> todos = todoService.filterCurrentUserTodos(filter);
        return ResponseEntity.ok(todos);
    }
}
