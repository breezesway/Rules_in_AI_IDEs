import React, { createContext, useContext, useState, useEffect } from 'react';
import authService, { tokenStorage } from '../services/authService';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(() => {
    const storedToken = tokenStorage.getAccessToken();
    console.log('Initializing AuthContext with token:', storedToken ? 'present' : 'null');
    return storedToken;
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initializeAuth = async () => {
      console.log('Initializing auth with token:', token ? 'present' : 'null');
      
      if (token && token.trim() !== '') {
        try {
          console.log('Attempting to get current user with token');
          const userProfile = await authService.getCurrentUser();
          console.log('User profile retrieved:', userProfile);
          // Extract user profile from nested structure if needed
          const actualUserProfile = userProfile?.data || userProfile;
          setUser(actualUserProfile);
        } catch (error) {
          console.error('Failed to get current user:', error);
          console.log('Clearing invalid token and logging out');
          logout();
        }
      } else {
        console.log('No valid token found, user remains unauthenticated');
      }
      setLoading(false);
    };

    initializeAuth();
  }, [token]);

  const login = async (credentials) => {
    try {
      console.log('Attempting login with credentials');
      const response = await authService.login(credentials);
      const { accessToken, refreshToken, user: userProfile } = response.data;
      
      console.log('Login successful, tokens received:', {
        accessToken: accessToken ? 'present' : 'null',
        refreshToken: refreshToken ? 'present' : 'null'
      });
      
      console.log('Login response full data:', response.data);
      console.log('User profile from login:', userProfile);
      
      // 토큰 유효성 검사
      if (!accessToken || accessToken.trim() === '') {
        console.error('Invalid access token received');
        throw new Error('Invalid access token received from server');
      }
      
      // 토큰 저장 유틸리티 사용
      tokenStorage.setTokens(accessToken, refreshToken);
      
      setToken(accessToken);
      // Extract user profile from nested structure if needed
      const actualUserProfile = userProfile?.data || userProfile;
      setUser(actualUserProfile);
      
      console.log('User set in context after login:', actualUserProfile);
      
      return { success: true };
    } catch (error) {
      console.error('Login failed:', error);
      return { 
        success: false, 
        error: error.response?.data?.message || 'Login failed' 
      };
    }
  };

  const register = async (userData) => {
    try {
      console.log('Attempting registration with user data');
      const response = await authService.register(userData);
      const { accessToken, refreshToken, user: userProfile } = response.data;
      
      console.log('Registration successful, response:', {
        accessToken: accessToken ? 'present' : 'null',
        refreshToken: refreshToken ? 'present' : 'null',
        userProfile: userProfile ? 'present' : 'null'
      });
      
      // 등록 성공 시 사용자 정보만 저장 (토큰은 이메일 인증 후에 생성됨)
      if (userProfile) {
        setUser(userProfile);
        console.log('User profile set in context');
        
        // 토큰이 있는 경우에만 저장 (이메일 인증 후 자동 로그인 시)
        if (accessToken && accessToken.trim() !== '') {
          tokenStorage.setTokens(accessToken, refreshToken);
          setToken(accessToken);
          console.log('Tokens saved after registration');
        } else {
          console.log('No tokens received after registration (expected for email verification flow)');
        }
      }
      
      return { success: true };
    } catch (error) {
      console.error('Registration failed:', error);
      return { 
        success: false, 
        error: error.response?.data?.message || 'Registration failed' 
      };
    }
  };

  const logout = () => {
    console.log('Logging out, clearing tokens and user data');
    tokenStorage.clearTokens();
    setToken(null);
    setUser(null);
    console.log('Logout completed');
  };

  const value = {
    user,
    token,
    loading,
    login,
    register,
    logout,
    updateUser: setUser,
    isAuthenticated: !!token
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
