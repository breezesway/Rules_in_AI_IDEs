package com.example.todoapp.service.impl;

import com.example.todoapp.dto.auth.AuthResponseDto;
import com.example.todoapp.dto.auth.LoginRequestDto;
import com.example.todoapp.dto.auth.RegisterRequestDto;
import com.example.todoapp.dto.auth.UserProfileDto;
import com.example.todoapp.entity.Role;
import com.example.todoapp.entity.User;
import com.example.todoapp.repository.RoleRepository;
import com.example.todoapp.repository.UserRepository;
import com.example.todoapp.security.UserPrincipal;
import com.example.todoapp.service.AuthService;
import com.example.todoapp.service.EmailVerificationService;
import com.example.todoapp.service.JwtService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.HashSet;
import java.util.Set;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class AuthServiceImpl implements AuthService {

    private final UserRepository userRepository;
    private final RoleRepository roleRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;
    private final AuthenticationManager authenticationManager;
    private final EmailVerificationService emailVerificationService;

    @Override
    public AuthResponseDto register(RegisterRequestDto request) {
        log.info("Starting registration process for user: {}", request.getUsername());
        
        try {
            // Check if username or email already exists
            if (userRepository.existsByUsername(request.getUsername())) {
                log.warn("Username already exists: {}", request.getUsername());
                throw new RuntimeException("Username already exists");
            }
            if (userRepository.existsByEmail(request.getEmail())) {
                log.warn("Email already exists: {}", request.getEmail());
                throw new RuntimeException("Email already exists");
            }
            
            // Check if user with same first name and last name already exists
            if (request.getFirstName() != null && request.getLastName() != null && 
                userRepository.existsByFirstNameAndLastName(request.getFirstName(), request.getLastName())) {
                log.warn("User with same name already exists: {} {}", request.getFirstName(), request.getLastName());
                throw new RuntimeException("User already exists");
            }

            log.info("Creating new user: {}", request.getUsername());
            
            // Create new user
            User user = new User();
            user.setUsername(request.getUsername());
            user.setEmail(request.getEmail());
            user.setPassword(passwordEncoder.encode(request.getPassword()));
            user.setFirstName(request.getFirstName());
            user.setLastName(request.getLastName());
            user.setEmailVerified(false);
            user.setEnabled(false); // User must verify email first

            // Assign default role
            Role userRole = roleRepository.findByName("ROLE_USER")
                    .orElseThrow(() -> new RuntimeException("Default role not found"));
            user.setRoles(new HashSet<>(Set.of(userRole)));

            User savedUser = userRepository.save(user);
            log.info("User saved successfully with ID: {}", savedUser.getId());

            // Send verification email
            log.info("Sending verification email to: {}", savedUser.getEmail());
            emailVerificationService.sendVerificationCode(savedUser.getEmail(), savedUser.getFirstName());

            // Create user profile
            UserProfileDto userProfile = UserProfileDto.builder()
                    .id(savedUser.getId())
                    .username(savedUser.getUsername())
                    .email(savedUser.getEmail())
                    .firstName(savedUser.getFirstName())
                    .lastName(savedUser.getLastName())
                    .enabled(savedUser.getEnabled())
                    .emailVerified(savedUser.getEmailVerified())
                    .roles(savedUser.getRoles().stream().map(Role::getName).collect(Collectors.toSet()))
                    .createdAt(savedUser.getCreatedAt())
                    .build();

            log.info("Registration completed successfully for user: {}", savedUser.getUsername());
            
            // Return response without tokens (user must verify email first)
            return new AuthResponseDto(
                null, // No access token until email is verified
                null, // No refresh token until email is verified
                null, // No token type until email is verified
                0L,   // No expiration until email is verified
                userProfile
            );
            
        } catch (Exception e) {
            log.error("Registration failed for user: {}", request.getUsername(), e);
            throw e;
        }
    }

    @Override
    public AuthResponseDto login(LoginRequestDto request) {
        // Authenticate user
        Authentication authentication = authenticationManager.authenticate(
            new UsernamePasswordAuthenticationToken(request.getUsernameOrEmail(), request.getPassword())
        );

        SecurityContextHolder.getContext().setAuthentication(authentication);

        UserPrincipal userPrincipal = (UserPrincipal) authentication.getPrincipal();
        User user = userPrincipal.getUser();

        // Check if email is verified
        if (!user.getEmailVerified()) {
            throw new RuntimeException("Please verify your email before logging in");
        }

        // Check if user is enabled
        if (!user.getEnabled()) {
            throw new RuntimeException("Account is disabled. Please contact support.");
        }

        // Generate tokens
        String accessToken = jwtService.generateAccessToken(user);
        String refreshToken = jwtService.generateRefreshToken(user);

        return createAuthResponse(user, accessToken, refreshToken);
    }

    @Override
    public UserProfileDto getCurrentUser() {
        UserPrincipal userPrincipal = (UserPrincipal) SecurityContextHolder.getContext()
                .getAuthentication().getPrincipal();
        User user = userPrincipal.getUser();

        return UserProfileDto.builder()
                .id(user.getId())
                .username(user.getUsername())
                .email(user.getEmail())
                .firstName(user.getFirstName())
                .lastName(user.getLastName())
                .enabled(user.getEnabled())
                .emailVerified(user.getEmailVerified())
                .roles(user.getRoles().stream().map(Role::getName).collect(Collectors.toSet()))
                .createdAt(user.getCreatedAt())
                .build();
    }

    @Override
    public void logout() {
        SecurityContextHolder.clearContext();
    }

    private AuthResponseDto createAuthResponse(User user, String accessToken, String refreshToken) {
        UserProfileDto userProfile = UserProfileDto.builder()
                .id(user.getId())
                .username(user.getUsername())
                .email(user.getEmail())
                .firstName(user.getFirstName())
                .lastName(user.getLastName())
                .enabled(user.getEnabled())
                .emailVerified(user.getEmailVerified())
                .roles(user.getRoles().stream().map(Role::getName).collect(Collectors.toSet()))
                .createdAt(user.getCreatedAt())
                .build();

        return new AuthResponseDto(
            accessToken,
            refreshToken,
            "Bearer",
            900000L, // 15 minutes
            userProfile
        );
    }
}
