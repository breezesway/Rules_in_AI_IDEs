-- Create default roles
INSERT INTO roles (name, description) VALUES 
('ROLE_USER', 'Standard user role'),
('ROLE_ADMIN', 'Administrator role');

-- Create verified admin user (password: Admin123!)
INSERT INTO users (username, email, password, first_name, email_verified, enabled, created_at) VALUES 
('admin', 'admin@example.com', '$2a$12$LQv3c1yqBw2UKaOF.QiPp.8fJUh4vNI8ZRdkHOJqOg5z8.dNhCQOm', 'Admin', true, true, NOW());

-- Assign admin role
INSERT INTO user_roles (user_id, role_id) 
SELECT u.id, r.id FROM users u, roles r 
WHERE u.username = 'admin' AND r.name = 'ROLE_ADMIN';

INSERT INTO user_roles (user_id, role_id) 
SELECT u.id, r.id FROM users u, roles r 
WHERE u.username = 'admin' AND r.name = 'ROLE_USER';
