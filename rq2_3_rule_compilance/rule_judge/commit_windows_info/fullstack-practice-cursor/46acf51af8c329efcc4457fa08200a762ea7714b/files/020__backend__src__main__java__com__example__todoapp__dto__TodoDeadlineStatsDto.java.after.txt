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
public class TodoDeadlineStatsDto {
    private long totalTodos;
    private long todosWithDeadlines;
    private long todosWithoutDeadlines;
    private long overdueTodos;
    private long dueSoonTodos;
    private long completedWithDeadlines;
    private double deadlineCompletionRate;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime nextDeadline;
    private long todosThisWeek;
    private long todosThisMonth;
}
