package com.example.todoapp.service.impl;

import com.example.todoapp.config.JwtConfig;
import com.example.todoapp.entity.User;
import com.example.todoapp.service.JwtService;
import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;

import javax.crypto.SecretKey;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class JwtServiceImpl implements JwtService {

    private final JwtConfig jwtConfig;

    @Override
    public String generateAccessToken(User user) {
        log.debug("Generating access token for user: {}", user.getUsername());
        String token = generateToken(user, jwtConfig.getAccessTokenExpiration());
        log.debug("Generated access token: {}", token != null ? token.substring(0, Math.min(token.length(), 20)) + "..." : "null");
        return token;
    }

    @Override
    public String generateRefreshToken(User user) {
        log.debug("Generating refresh token for user: {}", user.getUsername());
        String token = generateToken(user, jwtConfig.getRefreshTokenExpiration());
        log.debug("Generated refresh token: {}", token != null ? token.substring(0, Math.min(token.length(), 20)) + "..." : "null");
        return token;
    }

    @Override
    public String extractUsername(String token) {
        return extractClaim(token, Claims::getSubject);
    }

    @Override
    public boolean isTokenValid(String token, UserDetails userDetails) {
        final String username = extractUsername(token);
        return (username.equals(userDetails.getUsername()) && !isTokenExpired(token));
    }

    @Override
    public boolean isTokenExpired(String token) {
        return extractExpiration(token).before(new Date());
    }

    private String generateToken(User user, long expiration) {
        try {
            log.debug("Starting token generation for user: {}", user.getUsername());
            log.debug("JWT Config - Secret length: {}, Issuer: {}, Expiration: {}", 
                     jwtConfig.getSecret() != null ? jwtConfig.getSecret().length() : "null", 
                     jwtConfig.getIssuer(), expiration);
            
            Map<String, Object> claims = new HashMap<>();
            claims.put("roles", user.getRoles().stream()
                    .map(role -> role.getName())
                    .collect(Collectors.toList()));
            claims.put("userId", user.getId());
            
            log.debug("Claims prepared: {}", claims);
            
            SecretKey signingKey = getSigningKey();
            log.debug("Signing key generated: {}", signingKey != null ? signingKey.getAlgorithm() : "null");
            
            String token = Jwts.builder()
                    .setClaims(claims)
                    .setSubject(user.getUsername())
                    .setIssuer(jwtConfig.getIssuer())
                    .setIssuedAt(new Date(System.currentTimeMillis()))
                    .setExpiration(new Date(System.currentTimeMillis() + expiration))
                    .signWith(signingKey, Jwts.SIG.HS256)
                    .compact();
            
            log.debug("Token generated successfully: {}", token != null ? "not null" : "null");
            return token;
            
        } catch (Exception e) {
            log.error("Error generating JWT token for user: {}", user.getUsername(), e);
            throw e;
        }
    }

    private Date extractExpiration(String token) {
        return extractClaim(token, Claims::getExpiration);
    }

    private <T> T extractClaim(String token, java.util.function.Function<Claims, T> claimsResolver) {
        final Claims claims = extractAllClaims(token);
        return claimsResolver.apply(claims);
    }

    private Claims extractAllClaims(String token) {
        try {
            return Jwts.parser()
                    .verifyWith(getSigningKey())
                    .build()
                    .parseSignedClaims(token)
                    .getPayload();
        } catch (Exception e) {
            log.error("Error parsing JWT token: {}", token, e);
            throw e;
        }
    }

    private SecretKey getSigningKey() {
        try {
            String secret = jwtConfig.getSecret();
            if (secret == null || secret.trim().isEmpty()) {
                log.error("JWT secret is null or empty");
                throw new IllegalStateException("JWT secret cannot be null or empty");
            }
            
            byte[] keyBytes = secret.getBytes();
            log.debug("Secret key bytes length: {}", keyBytes.length);
            
            SecretKey key = Keys.hmacShaKeyFor(keyBytes);
            log.debug("Secret key generated successfully: {}", key.getAlgorithm());
            return key;
            
        } catch (Exception e) {
            log.error("Error generating signing key", e);
            throw e;
        }
    }
}
