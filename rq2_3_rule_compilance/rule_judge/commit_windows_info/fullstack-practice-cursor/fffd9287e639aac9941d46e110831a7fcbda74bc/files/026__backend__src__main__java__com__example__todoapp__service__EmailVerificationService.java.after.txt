package com.example.todoapp.service;

import com.example.todoapp.dto.auth.AuthResponseDto;
import com.example.todoapp.dto.auth.EmailVerificationRequestDto;
import com.example.todoapp.dto.auth.ResendVerificationRequestDto;

public interface EmailVerificationService {

    void sendVerificationCode(String email, String firstName);

    AuthResponseDto verifyEmail(EmailVerificationRequestDto request);

    void resendVerificationCode(ResendVerificationRequestDto request);

    void cleanupExpiredVerifications();
}
