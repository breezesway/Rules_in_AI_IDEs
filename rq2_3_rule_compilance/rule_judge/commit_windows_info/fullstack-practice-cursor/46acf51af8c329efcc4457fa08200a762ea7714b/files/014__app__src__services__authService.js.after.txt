import apiClient, { tokenStorage } from "./apiClient";

// Define authService object first
const authService = {
  login: async (credentials) => {
    const response = await apiClient.post("/auth/login", credentials);
    return response.data;
  },

  register: async (userData) => {
    const response = await apiClient.post("/auth/register", userData);
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await apiClient.get("/auth/me");
    return response.data;
  },

  logout: async () => {
    try {
      await apiClient.post("/auth/logout");
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      tokenStorage.clearTokens();
    }
  },

  verifyEmail: async (verificationData) => {
    const response = await apiClient.post(
      "/auth/verify-email",
      verificationData
    );
    return response.data;
  },

  resendVerification: async (emailData) => {
    const response = await apiClient.post(
      "/auth/resend-verification",
      emailData
    );
    return response.data;
  },
};

// Export the authService object
export default authService;

// Export individual functions for direct use
export const login = authService.login;
export const register = authService.register;
export const getCurrentUser = authService.getCurrentUser;
export const logout = authService.logout;
export const verifyEmail = authService.verifyEmail;
export const resendVerification = authService.resendVerification;

// Export token storage utilities
export { tokenStorage };
