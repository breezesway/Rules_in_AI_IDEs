package com.example.todoapp.util;

import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

@Component
public class DateTimeUtil {

    public LocalDateTime getCurrentTime() {
        return LocalDateTime.now();
    }

    public LocalDateTime addMinutes(LocalDateTime dateTime, long minutes) {
        return dateTime.plusMinutes(minutes);
    }

    public boolean isExpired(LocalDateTime expiryTime) {
        return LocalDateTime.now().isAfter(expiryTime);
    }

    public long getMinutesUntilExpiry(LocalDateTime expiryTime) {
        LocalDateTime now = LocalDateTime.now();
        if (now.isAfter(expiryTime)) {
            return 0;
        }
        return java.time.Duration.between(now, expiryTime).toMinutes();
    }
}
