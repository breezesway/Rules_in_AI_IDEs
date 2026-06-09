package com.example.todoapp.service.impl;

import com.example.todoapp.dto.TodoRequestDto;
import com.example.todoapp.dto.TodoResponseDto;
import com.example.todoapp.dto.TodoDeadlineStatsDto;
import com.example.todoapp.dto.TodoFilterDto;
import com.example.todoapp.entity.Todo;
import com.example.todoapp.entity.User;
import com.example.todoapp.exception.AuthorizationException;
import com.example.todoapp.exception.ResourceNotFoundException;
import com.example.todoapp.repository.TodoRepository;
import com.example.todoapp.repository.UserRepository;
import com.example.todoapp.service.TodoService;
import com.example.todoapp.util.SecurityUtil;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Transactional
@Slf4j
public class TodoServiceImpl implements TodoService {

    private final TodoRepository todoRepository;
    private final UserRepository userRepository;

    @Override
    @Transactional(readOnly = true)
    public List<TodoResponseDto> getCurrentUserTodos() {
        Long userId = getCurrentUserId();
        log.debug("Fetching todos for user ID: {}", userId);
        
        List<Todo> todos = todoRepository.findByUserIdOrderByCreatedAtDesc(userId);
        return todos.stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public TodoResponseDto getCurrentUserTodoById(Long todoId) {
        Long userId = getCurrentUserId();
        log.debug("Fetching todo ID: {} for user ID: {}", todoId, userId);
        
        Todo todo = todoRepository.findByIdAndUserId(todoId, userId)
                .orElseThrow(() -> new ResourceNotFoundException("Todo not found with id: " + todoId));
        
        return convertToDto(todo);
    }

    @Override
    public TodoResponseDto createTodoForCurrentUser(TodoRequestDto todoRequest) {
        Long userId = getCurrentUserId();
        log.debug("Creating todo for user ID: {}", userId);
        
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));
        
        Todo todo = new Todo();
        todo.setTitle(todoRequest.getTitle());
        todo.setDescription(todoRequest.getDescription());
        todo.setCompleted(todoRequest.getCompleted() != null ? todoRequest.getCompleted() : false);
        todo.setDeadline(todoRequest.getDeadline());
        todo.setUser(user);
        
        Todo savedTodo = todoRepository.save(todo);
        log.info("Created todo ID: {} for user ID: {}", savedTodo.getId(), userId);
        
        return convertToDto(savedTodo);
    }

    @Override
    public TodoResponseDto updateCurrentUserTodo(Long todoId, TodoRequestDto todoRequest) {
        Long userId = getCurrentUserId();
        log.debug("Updating todo ID: {} for user ID: {}", todoId, userId);
        
        Todo todo = todoRepository.findByIdAndUserId(todoId, userId)
                .orElseThrow(() -> new ResourceNotFoundException("Todo not found with id: " + todoId));
        
        todo.setTitle(todoRequest.getTitle());
        todo.setDescription(todoRequest.getDescription());
        todo.setCompleted(todoRequest.getCompleted() != null ? todoRequest.getCompleted() : todo.getCompleted());
        todo.setDeadline(todoRequest.getDeadline());
        
        Todo updatedTodo = todoRepository.save(todo);
        log.info("Updated todo ID: {} for user ID: {}", todoId, userId);
        
        return convertToDto(updatedTodo);
    }

    @Override
    public void deleteCurrentUserTodo(Long todoId) {
        Long userId = getCurrentUserId();
        log.debug("Deleting todo ID: {} for user ID: {}", todoId, userId);
        
        if (!todoRepository.existsByIdAndUserId(todoId, userId)) {
            throw new ResourceNotFoundException("Todo not found with id: " + todoId);
        }
        
        todoRepository.deleteById(todoId);
        log.info("Deleted todo ID: {} for user ID: {}", todoId, userId);
    }

    @Override
    public TodoResponseDto toggleCurrentUserTodoCompletion(Long todoId) {
        Long userId = getCurrentUserId();
        log.debug("Toggling completion for todo ID: {} for user ID: {}", todoId, userId);
        
        Todo todo = todoRepository.findByIdAndUserId(todoId, userId)
                .orElseThrow(() -> new ResourceNotFoundException("Todo not found with id: " + todoId));
        
        todo.setCompleted(!todo.getCompleted());
        Todo updatedTodo = todoRepository.save(todo);
        
        log.info("Toggled completion for todo ID: {} for user ID: {}", todoId, userId);
        return convertToDto(updatedTodo);
    }

    @Override
    @Transactional(readOnly = true)
    public List<TodoResponseDto> getCurrentUserTodosSortedByDeadline() {
        Long userId = getCurrentUserId();
        List<Todo> todos = todoRepository.findByUserIdOrderByDeadlineAscNullsLast(userId);
        return todos.stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public List<TodoResponseDto> getCurrentUserTodosWithDeadlines() {
        Long userId = getCurrentUserId();
        List<Todo> todos = todoRepository.findByUserIdAndDeadlineIsNotNullOrderByDeadlineAsc(userId);
        return todos.stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public List<TodoResponseDto> getCurrentUserTodosWithoutDeadlines() {
        Long userId = getCurrentUserId();
        List<Todo> todos = todoRepository.findByUserIdAndDeadlineIsNullOrderByCreatedAtDesc(userId);
        return todos.stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public List<TodoResponseDto> getCurrentUserOverdueTodos() {
        Long userId = getCurrentUserId();
        LocalDateTime now = LocalDateTime.now();
        List<Todo> todos = todoRepository.findOverdueTodosByUserId(userId, now);
        return todos.stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public List<TodoResponseDto> getCurrentUserDueSoonTodos() {
        Long userId = getCurrentUserId();
        LocalDateTime now = LocalDateTime.now();
        LocalDateTime dueSoon = now.plusDays(1);
        List<Todo> todos = todoRepository.findDueSoonTodosByUserId(userId, now, dueSoon);
        return todos.stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public List<TodoResponseDto> getCurrentUserTodosByDateRange(LocalDateTime startDate, LocalDateTime endDate) {
        Long userId = getCurrentUserId();
        List<Todo> todos = todoRepository.findTodosByUserIdAndDeadlineBetween(userId, startDate, endDate);
        return todos.stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());
    }

    @Override
    public TodoResponseDto setTodoDeadline(Long todoId, LocalDateTime deadline) {
        Long userId = getCurrentUserId();
        log.debug("Setting deadline for todo ID: {} for user ID: {}", todoId, userId);
        
        Todo todo = todoRepository.findByIdAndUserId(todoId, userId)
                .orElseThrow(() -> new ResourceNotFoundException("Todo not found with id: " + todoId));
        
        todo.setDeadline(deadline);
        Todo updatedTodo = todoRepository.save(todo);
        
        log.info("Set deadline for todo ID: {} for user ID: {}", todoId, userId);
        return convertToDto(updatedTodo);
    }

    @Override
    public TodoResponseDto removeTodoDeadline(Long todoId) {
        Long userId = getCurrentUserId();
        log.debug("Removing deadline for todo ID: {} for user ID: {}", todoId, userId);
        
        Todo todo = todoRepository.findByIdAndUserId(todoId, userId)
                .orElseThrow(() -> new ResourceNotFoundException("Todo not found with id: " + todoId));
        
        todo.setDeadline(null);
        Todo updatedTodo = todoRepository.save(todo);
        
        log.info("Removed deadline for todo ID: {} for user ID: {}", todoId, userId);
        return convertToDto(updatedTodo);
    }

    @Override
    @Transactional(readOnly = true)
    public TodoDeadlineStatsDto getCurrentUserTodoStats() {
        Long userId = getCurrentUserId();
        LocalDateTime now = LocalDateTime.now();
        
        long totalTodos = todoRepository.countByUserId(userId);
        long todosWithDeadlines = todoRepository.countTodosWithDeadlineByUserId(userId);
        long overdueTodos = todoRepository.countOverdueTodosByUserId(userId, now);
        long dueSoonTodos = todoRepository.findDueSoonTodosByUserId(userId, now, now.plusDays(1)).size();
        
        double deadlineCompletionRate = todosWithDeadlines > 0 ? 
            (double) todoRepository.countByUserIdAndCompleted(userId, true) / todosWithDeadlines * 100 : 0.0;
        
        return TodoDeadlineStatsDto.builder()
                .totalTodos(totalTodos)
                .todosWithDeadlines(todosWithDeadlines)
                .todosWithoutDeadlines(totalTodos - todosWithDeadlines)
                .overdueTodos(overdueTodos)
                .dueSoonTodos(dueSoonTodos)
                .deadlineCompletionRate(deadlineCompletionRate)
                .build();
    }

    @Override
    @Transactional(readOnly = true)
    public List<TodoResponseDto> searchCurrentUserTodos(String keyword) {
        Long userId = getCurrentUserId();
        List<Todo> todos = todoRepository.searchTodosByUserIdAndKeyword(userId, keyword);
        return todos.stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public List<TodoResponseDto> filterCurrentUserTodos(TodoFilterDto filter) {
        Long userId = getCurrentUserId();
        List<Todo> todos = todoRepository.findByUserIdOrderByCreatedAtDesc(userId);
        
        // Apply filters
        return todos.stream()
                .filter(todo -> filter.getCompleted() == null || todo.getCompleted().equals(filter.getCompleted()))
                .filter(todo -> filter.getHasDeadline() == null || 
                    (filter.getHasDeadline() ? todo.hasDeadline() : !todo.hasDeadline()))
                .filter(todo -> filter.getOverdueOnly() == null || 
                    (filter.getOverdueOnly() ? todo.isOverdue() : true))
                .filter(todo -> filter.getDueSoonOnly() == null || 
                    (filter.getDueSoonOnly() ? todo.isDueSoon() : true))
                .map(this::convertToDto)
                .collect(Collectors.toList());
    }

    private Long getCurrentUserId() {
        Long userId = SecurityUtil.getCurrentUserId();
        if (userId == null) {
            throw new AuthorizationException("User not authenticated");
        }
        return userId;
    }

    private TodoResponseDto convertToDto(Todo todo) {
        String deadlineStatus = determineDeadlineStatus(todo);
        
        return new TodoResponseDto(
                todo.getId(),
                todo.getTitle(),
                todo.getDescription(),
                todo.getCompleted(),
                todo.getDeadline(),
                todo.hasDeadline(),
                todo.isOverdue(),
                todo.isDueSoon(),
                deadlineStatus,
                todo.getCreatedAt(),
                todo.getUpdatedAt()
        );
    }

    private String determineDeadlineStatus(Todo todo) {
        if (!todo.hasDeadline()) {
            return "NO_DEADLINE";
        }
        if (todo.isOverdue()) {
            return "OVERDUE";
        }
        if (todo.isDueSoon()) {
            return "DUE_SOON";
        }
        return "ON_TIME";
    }
}
