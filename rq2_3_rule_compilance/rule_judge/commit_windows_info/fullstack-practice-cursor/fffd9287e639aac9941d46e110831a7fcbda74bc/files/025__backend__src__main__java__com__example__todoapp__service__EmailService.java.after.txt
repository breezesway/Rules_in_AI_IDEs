package com.example.todoapp.service;

public interface EmailService {

    void sendVerificationEmail(String to, String firstName, String verificationCode);

    void sendPasswordResetEmail(String to, String firstName, String resetCode);

    void sendWelcomeEmail(String to, String firstName);
}
