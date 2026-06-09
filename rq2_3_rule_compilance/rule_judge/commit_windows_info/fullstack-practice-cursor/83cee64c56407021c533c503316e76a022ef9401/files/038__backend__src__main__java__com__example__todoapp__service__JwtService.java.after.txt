package com.example.todoapp.service;

import com.example.todoapp.entity.User;
import org.springframework.security.core.userdetails.UserDetails;

public interface JwtService {

    String generateAccessToken(User user);
    
    String generateRefreshToken(User user);
    
    String extractUsername(String token);
    
    boolean isTokenValid(String token, UserDetails userDetails);
    
    boolean isTokenExpired(String token);
}
