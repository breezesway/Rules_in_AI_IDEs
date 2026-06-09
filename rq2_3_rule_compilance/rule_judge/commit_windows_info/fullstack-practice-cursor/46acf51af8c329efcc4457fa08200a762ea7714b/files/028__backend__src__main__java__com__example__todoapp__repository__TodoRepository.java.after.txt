package com.example.todoapp.repository;

import com.example.todoapp.entity.Todo;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface TodoRepository extends JpaRepository<Todo, Long> {
    
    // Basic user-specific queries
    List<Todo> findByUserIdOrderByCreatedAtDesc(Long userId);
    List<Todo> findByUserIdAndCompletedOrderByCreatedAtDesc(Long userId, Boolean completed);
    long countByUserId(Long userId);
    long countByUserIdAndCompleted(Long userId, Boolean completed);
    Optional<Todo> findByIdAndUserId(Long id, Long userId);
    boolean existsByIdAndUserId(Long id, Long userId);
    
    // Deadline-specific queries - Fixed method names
    @Query("SELECT t FROM Todo t WHERE t.user.id = :userId ORDER BY CASE WHEN t.deadline IS NULL THEN 1 ELSE 0 END, t.deadline ASC")
    List<Todo> findByUserIdOrderByDeadlineAscNullsLast(@Param("userId") Long userId);
    
    List<Todo> findByUserIdAndDeadlineIsNotNullOrderByDeadlineAsc(Long userId);
    List<Todo> findByUserIdAndDeadlineIsNullOrderByCreatedAtDesc(Long userId);
    
    // Overdue and due soon queries
    @Query("SELECT t FROM Todo t WHERE t.user.id = :userId AND t.deadline < :now AND t.completed = false ORDER BY t.deadline ASC")
    List<Todo> findOverdueTodosByUserId(@Param("userId") Long userId, @Param("now") LocalDateTime now);
    
    @Query("SELECT t FROM Todo t WHERE t.user.id = :userId AND t.deadline BETWEEN :now AND :dueSoon AND t.completed = false ORDER BY t.deadline ASC")
    List<Todo> findDueSoonTodosByUserId(@Param("userId") Long userId, @Param("now") LocalDateTime now, @Param("dueSoon") LocalDateTime dueSoon);
    
    // Deadline range queries
    @Query("SELECT t FROM Todo t WHERE t.user.id = :userId AND t.deadline BETWEEN :startDate AND :endDate ORDER BY t.deadline ASC")
    List<Todo> findTodosByUserIdAndDeadlineBetween(@Param("userId") Long userId, @Param("startDate") LocalDateTime startDate, @Param("endDate") LocalDateTime endDate);
    
    // Statistics queries
    @Query("SELECT COUNT(t) FROM Todo t WHERE t.user.id = :userId AND t.deadline < :now AND t.completed = false")
    long countOverdueTodosByUserId(@Param("userId") Long userId, @Param("now") LocalDateTime now);
    
    @Query("SELECT COUNT(t) FROM Todo t WHERE t.user.id = :userId AND t.deadline IS NOT NULL")
    long countTodosWithDeadlineByUserId(@Param("userId") Long userId);
    
    // Search queries
    @Query("SELECT t FROM Todo t WHERE t.user.id = :userId AND (LOWER(t.title) LIKE LOWER(CONCAT('%', :keyword, '%')) OR LOWER(t.description) LIKE LOWER(CONCAT('%', :keyword, '%')))")
    List<Todo> searchTodosByUserIdAndKeyword(@Param("userId") Long userId, @Param("keyword") String keyword);
}
