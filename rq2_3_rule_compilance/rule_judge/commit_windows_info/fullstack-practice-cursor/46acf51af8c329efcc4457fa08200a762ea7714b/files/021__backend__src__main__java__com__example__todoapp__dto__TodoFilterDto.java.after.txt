package com.example.todoapp.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TodoFilterDto {
    private Boolean completed;
    private Boolean hasDeadline;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime deadlineFrom;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime deadlineTo;
    
    private String sortBy; // "CREATED_AT", "DEADLINE", "TITLE"
    private String sortDirection; // "ASC", "DESC"
    private Boolean overdueOnly;
    private Boolean dueSoonOnly;
}
