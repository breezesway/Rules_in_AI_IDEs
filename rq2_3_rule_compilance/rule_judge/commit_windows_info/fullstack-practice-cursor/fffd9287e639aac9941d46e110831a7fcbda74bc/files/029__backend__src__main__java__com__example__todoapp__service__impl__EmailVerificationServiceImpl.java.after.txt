package com.example.todoapp.service.impl;

import com.example.todoapp.dto.auth.AuthResponseDto;
import com.example.todoapp.dto.auth.EmailVerificationRequestDto;
import com.example.todoapp.dto.auth.ResendVerificationRequestDto;
import com.example.todoapp.dto.auth.UserProfileDto;
import com.example.todoapp.entity.EmailVerification;
import com.example.todoapp.entity.User;
import com.example.todoapp.repository.EmailVerificationRepository;
import com.example.todoapp.repository.UserRepository;
import com.example.todoapp.service.EmailService;
import com.example.todoapp.service.EmailVerificationService;
import com.example.todoapp.service.JwtService;
import com.example.todoapp.util.DateTimeUtil;
import com.example.todoapp.util.VerificationCodeGenerator;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class EmailVerificationServiceImpl implements EmailVerificationService {

    private final EmailVerificationRepository emailVerificationRepository;
    private final UserRepository userRepository;
    private final EmailService emailService;
    private final VerificationCodeGenerator codeGenerator;
    private final DateTimeUtil dateTimeUtil;
    private final JwtService jwtService;

    @Value("${app.email.verification.expiry-minutes:10}")
    private int expiryMinutes;

    @Value("${app.email.verification.max-attempts:5}")
    private int maxAttempts;

    @Value("${app.email.verification.rate-limit-minutes:1}")
    private int rateLimitMinutes;

    @Override
    @Transactional
    public void sendVerificationCode(String email, String firstName) {
        // Check rate limiting
        LocalDateTime since = dateTimeUtil.getCurrentTime().minusMinutes(rateLimitMinutes);
        long recentAttempts = emailVerificationRepository.countByEmailAndCreatedAtAfter(email, since);
        
        if (recentAttempts > 0) {
            throw new RuntimeException("Please wait before requesting another verification code");
        }

        // Generate verification code
        String verificationCode = codeGenerator.generateVerificationCode();
        LocalDateTime expiryTime = dateTimeUtil.addMinutes(dateTimeUtil.getCurrentTime(), expiryMinutes);

        // Save verification record
        EmailVerification verification = new EmailVerification();
        verification.setEmail(email);
        verification.setVerificationCode(verificationCode);
        verification.setExpiryTime(expiryTime);
        verification.setVerified(false);
        verification.setAttempts(0);

        emailVerificationRepository.save(verification);

        // Send email
        emailService.sendVerificationEmail(email, firstName, verificationCode);
        
        log.info("Verification code sent to: {}", email);
    }

    @Override
    @Transactional
    public AuthResponseDto verifyEmail(EmailVerificationRequestDto request) {
        LocalDateTime currentTime = dateTimeUtil.getCurrentTime();
        
        log.debug("Starting email verification for: {}", request.getEmail());
        
        // Find valid verification record
        EmailVerification verification = emailVerificationRepository
                .findByEmailAndVerificationCodeAndExpiryTimeAfter(
                        request.getEmail(), request.getVerificationCode(), currentTime)
                .orElseThrow(() -> new RuntimeException("Invalid or expired verification code"));

        // Check if already verified
        if (verification.getVerified()) {
            throw new RuntimeException("Email is already verified");
        }

        // Check attempts limit
        if (verification.getAttempts() >= maxAttempts) {
            throw new RuntimeException("Maximum verification attempts exceeded");
        }

        // Increment attempts
        verification.setAttempts(verification.getAttempts() + 1);

        // Check if code matches
        if (!verification.getVerificationCode().equals(request.getVerificationCode())) {
            emailVerificationRepository.save(verification);
            throw new RuntimeException("Invalid verification code");
        }

        // Mark as verified
        verification.setVerified(true);
        emailVerificationRepository.save(verification);

        // Update user
        User user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new RuntimeException("User not found"));
        
        user.setEmailVerified(true);
        user.setEnabled(true);
        userRepository.save(user);

        log.debug("User updated - Email verified: {}, Enabled: {}", user.getEmailVerified(), user.getEnabled());

        // Send welcome email
        emailService.sendWelcomeEmail(request.getEmail(), user.getFirstName());

        // Clean up old verifications for this email
        emailVerificationRepository.deleteByEmailAndVerifiedTrue(request.getEmail());

        // Generate JWT tokens for automatic login
        log.debug("Generating JWT tokens for user: {}", user.getUsername());
        String accessToken = jwtService.generateAccessToken(user);
        String refreshToken = jwtService.generateRefreshToken(user);
        
        log.debug("JWT tokens generated - Access token: {}, Refresh token: {}", 
                 accessToken != null ? "not null" : "null", 
                 refreshToken != null ? "not null" : "null");

        // Create user profile
        UserProfileDto userProfile = UserProfileDto.builder()
                .id(user.getId())
                .username(user.getUsername())
                .email(user.getEmail())
                .firstName(user.getFirstName())
                .lastName(user.getLastName())
                .enabled(user.getEnabled())
                .emailVerified(user.getEmailVerified())
                .roles(user.getRoles().stream().map(role -> role.getName()).collect(Collectors.toSet()))
                .createdAt(user.getCreatedAt())
                .build();

        log.info("Email verified successfully for: {}", request.getEmail());
        
        // Return auth response with tokens
        AuthResponseDto response = new AuthResponseDto(
            accessToken,
            refreshToken,
            "Bearer",
            900000L, // 15 minutes
            userProfile
        );
        
        log.debug("Auth response created with tokens: {}", response.getAccessToken() != null ? "tokens present" : "tokens missing");
        return response;
    }

    @Override
    @Transactional
    public void resendVerificationCode(ResendVerificationRequestDto request) {
        User user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new RuntimeException("User not found"));

        if (user.getEmailVerified()) {
            throw new RuntimeException("Email is already verified");
        }

        // Delete old unverified verifications
        emailVerificationRepository.deleteByEmailAndVerifiedTrue(request.getEmail());

        // Send new verification code
        sendVerificationCode(request.getEmail(), user.getFirstName());
        
        log.info("Verification code resent to: {}", request.getEmail());
    }

    @Override
    @Scheduled(fixedRate = 300000) // Run every 5 minutes
    @Transactional
    public void cleanupExpiredVerifications() {
        LocalDateTime currentTime = dateTimeUtil.getCurrentTime();
        emailVerificationRepository.deleteByExpiryTimeBefore(currentTime);
        log.debug("Cleaned up expired verification codes");
    }
}
