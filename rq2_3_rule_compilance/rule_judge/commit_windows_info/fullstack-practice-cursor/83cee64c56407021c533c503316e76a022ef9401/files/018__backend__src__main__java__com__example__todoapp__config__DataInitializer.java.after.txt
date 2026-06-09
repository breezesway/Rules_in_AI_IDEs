package com.example.todoapp.config;

import com.example.todoapp.entity.Role;
import com.example.todoapp.entity.User;
import com.example.todoapp.repository.RoleRepository;
import com.example.todoapp.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.util.HashSet;
import java.util.Set;

@Component
@RequiredArgsConstructor
@Slf4j
public class DataInitializer implements CommandLineRunner {

    private final RoleRepository roleRepository;
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    @Override
    @Transactional
    public void run(String... args) throws Exception {
        log.info("Starting data initialization...");
        
        try {
            // First, check what's in the database
            log.info("Current role count: {}", roleRepository.count());
            log.info("Current user count: {}", userRepository.count());
            
            initializeRoles();
            initializeAdminUser();
            
            log.info("Data initialization completed successfully");
        } catch (Exception e) {
            log.error("Error during data initialization: ", e);
            throw e;
        }
    }

    private void initializeRoles() {
        log.info("Checking roles...");
        
        if (roleRepository.count() == 0) {
            log.info("No roles found, creating default roles...");
            
            try {
                Role userRole = new Role();
                userRole.setName("ROLE_USER");
                userRole.setDescription("Standard user role");
                Role savedUserRole = roleRepository.save(userRole);
                log.info("Saved user role with ID: {}", savedUserRole.getId());

                Role adminRole = new Role();
                adminRole.setName("ROLE_ADMIN");
                adminRole.setDescription("Administrator role");
                Role savedAdminRole = roleRepository.save(adminRole);
                log.info("Saved admin role with ID: {}", savedAdminRole.getId());

                log.info("Default roles initialized successfully");
            } catch (Exception e) {
                log.error("Error initializing roles: ", e);
                throw e;
            }
        } else {
            log.info("Roles already exist, skipping initialization");
            // List existing roles
            roleRepository.findAll().forEach(role -> 
                log.info("Existing role: {} - {}", role.getName(), role.getDescription())
            );
        }
    }

    private void initializeAdminUser() {
        log.info("Checking users...");
        
        if (userRepository.count() == 0) {
            log.info("No users found, creating default admin user...");
            
            try {
                // Verify roles exist
                Role adminRole = roleRepository.findByName("ROLE_ADMIN")
                        .orElseThrow(() -> new RuntimeException("Admin role not found"));
                log.info("Found admin role: {} - {}", adminRole.getId(), adminRole.getName());

                User adminUser = new User();
                adminUser.setUsername("admin");
                adminUser.setEmail("admin@todoapp.com");
                adminUser.setPassword(passwordEncoder.encode("Admin123!"));
                adminUser.setFirstName("Admin");
                adminUser.setLastName("User");
                adminUser.setEnabled(true);

                // Create a new set to avoid any potential issues
                Set<Role> roles = new HashSet<>();
                roles.add(adminRole);
                adminUser.setRoles(roles);

                log.info("About to save admin user: {}", adminUser.getUsername());
                User savedUser = userRepository.save(adminUser);
                log.info("Default admin user created successfully: {} / Admin123! (ID: {})", 
                        savedUser.getUsername(), savedUser.getId());
            } catch (Exception e) {
                log.error("Error creating admin user: ", e);
                throw e;
            }
        } else {
            log.info("Users already exist, skipping admin user creation");
            // List existing users
            userRepository.findAll().forEach(user -> 
                log.info("Existing user: {} - {}", user.getUsername(), user.getEmail())
            );
        }
    }
}
