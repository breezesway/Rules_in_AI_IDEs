import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { verifyEmail, resendVerification, tokenStorage } from '../../services/authService';
import './AuthForms.css';

const EmailVerificationForm = () => {
    const [verificationCode, setVerificationCode] = useState(['', '', '', '', '', '']);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [resendDisabled, setResendDisabled] = useState(false);
    const [countdown, setCountdown] = useState(0);
    
    const navigate = useNavigate();
    const location = useLocation();
    const { user, updateUser } = useAuth();
    
    const email = location.state?.email || user?.email;

    useEffect(() => {
        if (!email) {
            navigate('/register');
            return;
        }
    }, [email, navigate]);

    useEffect(() => {
        let timer;
        if (countdown > 0) {
            timer = setTimeout(() => setCountdown(countdown - 1), 1000);
        } else {
            setResendDisabled(false);
        }
        return () => clearTimeout(timer);
    }, [countdown]);

    const handleCodeChange = (index, value) => {
        if (value.length > 1) return; // Only allow single digit
        
        const newCode = [...verificationCode];
        newCode[index] = value;
        setVerificationCode(newCode);
        
        // Auto-focus next input
        if (value && index < 5) {
            const nextInput = document.querySelector(`input[data-index="${index + 1}"]`);
            if (nextInput) nextInput.focus();
        }
    };

    const handleKeyDown = (index, e) => {
        if (e.key === 'Backspace' && !verificationCode[index] && index > 0) {
            const prevInput = document.querySelector(`input[data-index="${index - 1}"]`);
            if (prevInput) prevInput.focus();
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        const code = verificationCode.join('');
        if (code.length !== 6) {
            setError('Please enter the complete 6-digit verification code');
            return;
        }

        setIsLoading(true);
        setError('');
        setSuccess('');

        try {
            console.log('Submitting email verification with code:', code);
            const response = await verifyEmail({ email, verificationCode: code });
            
            console.log('Email verification response:', response);
            
            // Check if verification was successful and tokens were returned
            if (response.data && response.data.accessToken) {
                console.log('Tokens received from verification:', {
                    accessToken: response.data.accessToken ? 'present' : 'null',
                    refreshToken: response.data.refreshToken ? 'present' : 'null'
                });
                
                // Store tokens
                tokenStorage.setTokens(response.data.accessToken, response.data.refreshToken);
                
                console.log('Tokens saved to localStorage');
                
                setSuccess('Email verified successfully! Logging you in...');
                
                // Update user context with the returned user profile
                if (updateUser) {
                    console.log('Updating user context with:', response.data.user);
                    updateUser(response.data.user);
                }
                
                // Redirect to todos page after successful verification and login
                setTimeout(() => {
                    navigate('/todos', { 
                        state: { 
                            message: 'Email verified successfully! Welcome to Todo App!' 
                        } 
                    });
                }, 2000);
            } else {
                console.log('No tokens received from verification, redirecting to login');
                setSuccess('Email verified successfully! Redirecting to login...');
                
                // Update user context
                if (updateUser) {
                    updateUser({ ...user, emailVerified: true, enabled: true });
                }
                
                // Redirect to login after 2 seconds
                setTimeout(() => {
                    navigate('/login', { 
                        state: { 
                            message: 'Email verified successfully! Please log in to continue.' 
                        } 
                    });
                }, 2000);
            }
            
        } catch (err) {
            console.error('Email verification failed:', err);
            setError(err.response?.data?.message || 'Verification failed. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleResendCode = async () => {
        setIsLoading(true);
        setError('');
        setSuccess('');

        try {
            await resendVerification({ email });
            setSuccess('Verification code resent successfully!');
            setResendDisabled(true);
            setCountdown(60); // 60 second cooldown
        } catch (err) {
            setError(err.response?.data?.message || 'Failed to resend verification code.');
        } finally {
            setIsLoading(false);
        }
    };

    if (!email) {
        return null;
    }

    return (
        <div className="auth-container">
            <div className="auth-form-container">
                <div className="auth-header">
                    <h2>Verify Your Email</h2>
                    <p>We've sent a 6-digit verification code to:</p>
                    <p className="email-display">{email}</p>
                </div>

                <form onSubmit={handleSubmit} className="auth-form">
                    <div className="verification-code-container">
                        <label htmlFor="verification-code">Enter Verification Code:</label>
                        <div className="code-inputs">
                            {verificationCode.map((digit, index) => (
                                <input
                                    key={index}
                                    type="text"
                                    inputMode="numeric"
                                    pattern="[0-9]*"
                                    maxLength="1"
                                    value={digit}
                                    onChange={(e) => handleCodeChange(index, e.target.value)}
                                    onKeyDown={(e) => handleKeyDown(index, e)}
                                    data-index={index}
                                    className="code-input"
                                    placeholder="0"
                                    disabled={isLoading}
                                />
                            ))}
                        </div>
                    </div>

                    {error && <div className="error-message">{error}</div>}
                    {success && <div className="success-message">{success}</div>}

                    <button 
                        type="submit" 
                        className="auth-button primary"
                        disabled={isLoading || verificationCode.join('').length !== 6}
                    >
                        {isLoading ? 'Verifying...' : 'Verify Email'}
                    </button>

                    <div className="resend-section">
                        <p>Didn't receive the code?</p>
                        <button
                            type="button"
                            className="auth-button secondary"
                            onClick={handleResendCode}
                            disabled={resendDisabled || isLoading}
                        >
                            {resendDisabled 
                                ? `Resend in ${countdown}s` 
                                : 'Resend Code'
                            }
                        </button>
                    </div>

                    <div className="auth-links">
                        <button
                            type="button"
                            className="link-button"
                            onClick={() => navigate('/login')}
                        >
                            Back to Login
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default EmailVerificationForm;
