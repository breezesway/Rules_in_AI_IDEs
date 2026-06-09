package com.example.todoapp.security;

import com.example.todoapp.service.JwtService;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;

@Component
@RequiredArgsConstructor
@Slf4j
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private final JwtService jwtService;
    private final UserDetailsService userDetailsService;

    @Override
    protected void doFilterInternal(
            HttpServletRequest request,
            HttpServletResponse response,
            FilterChain filterChain
    ) throws ServletException, IOException {
        
        final String authHeader = request.getHeader("Authorization");
        
        // Authorization 헤더가 없거나 Bearer로 시작하지 않으면 다음 필터로 진행
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            log.debug("No Authorization header or not Bearer token for request: {}", request.getRequestURI());
            filterChain.doFilter(request, response);
            return;
        }
        
        // Bearer 토큰 추출
        final String jwt = authHeader.substring(7);
        
        // JWT 토큰이 null이거나 비어있으면 다음 필터로 진행
        if (jwt == null || jwt.trim().isEmpty()) {
            log.debug("JWT token is null or empty for request: {}", request.getRequestURI());
            filterChain.doFilter(request, response);
            return;
        }
        
        log.debug("Processing JWT token for request: {}", request.getRequestURI());
        
        try {
            final String username = jwtService.extractUsername(jwt);
            
            if (username != null && SecurityContextHolder.getContext().getAuthentication() == null) {
                UserDetails userDetails = this.userDetailsService.loadUserByUsername(username);
                
                if (jwtService.isTokenValid(jwt, userDetails)) {
                    UsernamePasswordAuthenticationToken authToken = new UsernamePasswordAuthenticationToken(
                        userDetails,
                        null,
                        userDetails.getAuthorities()
                    );
                    authToken.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
                    SecurityContextHolder.getContext().setAuthentication(authToken);
                    log.debug("Authentication set for user: {}", username);
                } else {
                    log.debug("JWT token is invalid for user: {}", username);
                }
            }
        } catch (Exception e) {
            log.debug("Error processing JWT token: {}", e.getMessage());
            // JWT 처리 중 오류가 발생해도 요청을 계속 진행 (인증되지 않은 상태로)
        }
        
        filterChain.doFilter(request, response);
    }
}
