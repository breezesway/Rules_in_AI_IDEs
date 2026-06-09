package com.example.todoapp.service;

import com.example.todoapp.dto.TodoRequestDto;
import com.example.todoapp.dto.TodoResponseDto;

import java.util.List;

public interface TodoService {

    List<TodoResponseDto> getAllTodos();

    TodoResponseDto getTodoById(Long id);

    TodoResponseDto createTodo(TodoRequestDto todoRequestDto);

    TodoResponseDto updateTodo(Long id, TodoRequestDto todoRequestDto);

    TodoResponseDto toggleTodoStatus(Long id);

    void deleteTodo(Long id);
}
