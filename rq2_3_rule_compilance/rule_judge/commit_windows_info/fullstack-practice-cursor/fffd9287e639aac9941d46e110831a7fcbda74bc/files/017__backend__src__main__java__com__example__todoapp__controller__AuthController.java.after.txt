package com.example.todoapp.controller;

import com.example.todoapp.dto.auth.AuthResponseDto;
import com.example.todoapp.dto.auth.EmailVerificationRequestDto;
import com.example.todoapp.dto.auth.LoginRequestDto;
import com.example.todoapp.dto.auth.RegisterRequestDto;
import com.example.todoapp.dto.auth.ResendVerificationRequestDto;
import com.example.todoapp.dto.auth.UserProfileDto;
import com.example.todoapp.dto.common.ApiResponseDto;
import com.example.todoapp.service.AuthService;
import com.example.todoapp.service.EmailVerificationService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
@CrossOrigin(origins = "http://localhost:3000")
public class AuthController {

    private final AuthService authService;
    private final EmailVerificationService emailVerificationService;

    @PostMapping("/register")
    public ResponseEntity<ApiResponseDto<AuthResponseDto>> register(@Valid @RequestBody RegisterRequestDto request) {
        AuthResponseDto response = authService.register(request);
        return ResponseEntity.ok(ApiResponseDto.success("User registered successfully", response));
    }

    @PostMapping("/login")
    public ResponseEntity<ApiResponseDto<AuthResponseDto>> login(@Valid @RequestBody LoginRequestDto request) {
        AuthResponseDto response = authService.login(request);
        return ResponseEntity.ok(ApiResponseDto.success("Login successful", response));
    }

    @GetMapping("/me")
    public ResponseEntity<ApiResponseDto<UserProfileDto>> getCurrentUser() {
        UserProfileDto userProfile = authService.getCurrentUser();
        return ResponseEntity.ok(ApiResponseDto.success("User profile retrieved", userProfile));
    }

    @PostMapping("/logout")
    public ResponseEntity<ApiResponseDto<Void>> logout() {
        authService.logout();
        return ResponseEntity.ok(ApiResponseDto.success("Logout successful"));
    }

    @PostMapping("/verify-email")
    public ResponseEntity<ApiResponseDto<AuthResponseDto>> verifyEmail(@Valid @RequestBody EmailVerificationRequestDto request) {
        AuthResponseDto response = emailVerificationService.verifyEmail(request);
        return ResponseEntity.ok(ApiResponseDto.success("Email verified successfully", response));
    }

    @PostMapping("/resend-verification")
    public ResponseEntity<ApiResponseDto<Void>> resendVerification(@Valid @RequestBody ResendVerificationRequestDto request) {
        emailVerificationService.resendVerificationCode(request);
        return ResponseEntity.ok(ApiResponseDto.success("Verification code resent successfully"));
    }
}
