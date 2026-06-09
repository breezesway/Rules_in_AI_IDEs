package com.example.todoapp.dto.common;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ErrorResponseDto {

    private String message;
    private String error;
    private int status;
    private LocalDateTime timestamp = LocalDateTime.now();
    private String path;
    private List<String> details;
}
