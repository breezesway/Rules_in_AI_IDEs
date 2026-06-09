package com.example.todoapp.repository;

import com.example.todoapp.entity.EmailVerification;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface EmailVerificationRepository extends JpaRepository<EmailVerification, Long> {

    Optional<EmailVerification> findByEmailAndVerificationCodeAndExpiryTimeAfter(
            String email, String verificationCode, LocalDateTime currentTime);

    Optional<EmailVerification> findByEmailAndExpiryTimeAfter(String email, LocalDateTime currentTime);

    @Query("SELECT COUNT(e) FROM EmailVerification e WHERE e.email = :email AND e.createdAt > :since")
    long countByEmailAndCreatedAtAfter(@Param("email") String email, @Param("since") LocalDateTime since);

    void deleteByEmailAndVerifiedTrue(String email);

    void deleteByExpiryTimeBefore(LocalDateTime expiryTime);
}
