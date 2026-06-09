package com.example.todoapp.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Data
@Component
@ConfigurationProperties(prefix = "jwt")
public class JwtConfig {

    private String secret = "your-secret-key-should-be-very-long-and-secure-in-production";
    private long accessTokenExpiration = 900000; // 15 minutes in milliseconds
    private long refreshTokenExpiration = 604800000; // 7 days in milliseconds
    private String issuer = "todo-app";
}
