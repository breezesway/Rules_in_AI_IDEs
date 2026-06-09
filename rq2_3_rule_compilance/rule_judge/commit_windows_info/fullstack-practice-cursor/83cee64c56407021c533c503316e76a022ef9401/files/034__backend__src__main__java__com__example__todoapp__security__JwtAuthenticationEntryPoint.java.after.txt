package com.example.todoapp.security;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.example.todoapp.dto.common.ErrorResponseDto;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.MediaType;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.web.AuthenticationEntryPoint;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.time.LocalDateTime;

@Component
@RequiredArgsConstructor
public class JwtAuthenticationEntryPoint implements AuthenticationEntryPoint {

    private final ObjectMapper objectMapper;

    @Override
    public void commence(
            HttpServletRequest request,
            HttpServletResponse response,
            AuthenticationException authException
    ) throws IOException, ServletException {
        
        response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
        response.setContentType(MediaType.APPLICATION_JSON_VALUE);
        response.setCharacterEncoding(StandardCharsets.UTF_8.name());
        
        ErrorResponseDto errorResponse = new ErrorResponseDto(
            "Unauthorized",
            "Authentication required",
            HttpServletResponse.SC_UNAUTHORIZED,
            LocalDateTime.now(),
            request.getRequestURI(),
            null
        );
        
        response.getWriter().write(objectMapper.writeValueAsString(errorResponse));
    }
}
