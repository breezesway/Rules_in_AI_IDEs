package com.example.todoapp.service;

import com.example.todoapp.dto.auth.AuthResponseDto;
import com.example.todoapp.dto.auth.LoginRequestDto;
import com.example.todoapp.dto.auth.RegisterRequestDto;
import com.example.todoapp.dto.auth.UserProfileDto;

public interface AuthService {

    AuthResponseDto register(RegisterRequestDto request);
    
    AuthResponseDto login(LoginRequestDto request);
    
    UserProfileDto getCurrentUser();
    
    void logout();
}
