import axios from "axios";

const API_BASE_URL = "http://localhost:8080/api";

// Token utility functions
const tokenStorage = {
  setTokens: (accessToken, refreshToken) => {
    try {
      if (accessToken && accessToken.trim() !== "") {
        localStorage.setItem("accessToken", accessToken);
        console.log("Access token saved to localStorage");
      } else {
        console.warn("Attempting to save empty access token");
      }

      if (refreshToken && refreshToken.trim() !== "") {
        localStorage.setItem("refreshToken", refreshToken);
        console.log("Refresh token saved to localStorage");
      } else {
        console.warn("Attempting to save empty refresh token");
      }
    } catch (error) {
      console.error("Error saving tokens to localStorage:", error);
    }
  },

  getAccessToken: () => {
    try {
      const token = localStorage.getItem("accessToken");
      console.log(
        "Retrieved access token from localStorage:",
        token ? "present" : "null"
      );
      return token;
    } catch (error) {
      console.error("Error retrieving access token from localStorage:", error);
      return null;
    }
  },

  getRefreshToken: () => {
    try {
      const token = localStorage.getItem("refreshToken");
      console.log(
        "Retrieved refresh token from localStorage:",
        token ? "present" : "null"
      );
      return token;
    } catch (error) {
      console.error("Error retrieving refresh token from localStorage:", error);
      return null;
    }
  },

  clearTokens: () => {
    try {
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      console.log("Tokens cleared from localStorage");
    } catch (error) {
      console.error("Error clearing tokens from localStorage:", error);
    }
  },
};

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add request interceptor to include auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = tokenStorage.getAccessToken();
    console.log(
      "API Request Interceptor - Token from localStorage:",
      token ? "present" : "null"
    );

    if (token && token.trim() !== "") {
      config.headers.Authorization = `Bearer ${token}`;
      console.log("Authorization header set with token");
    } else {
      console.log(
        "No valid token found, request will be sent without authorization"
      );
    }

    console.log("Request config:", {
      url: config.url,
      method: config.method,
      hasAuthHeader: !!config.headers.Authorization,
    });

    return config;
  },
  (error) => {
    console.error("Request interceptor error:", error);
    return Promise.reject(error);
  }
);

// Add response interceptor to handle token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = tokenStorage.getRefreshToken();
        if (refreshToken) {
          // Try to refresh the token
          const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
            refreshToken,
          });

          const { accessToken } = response.data.data;
          tokenStorage.setTokens(accessToken, refreshToken);

          // Retry the original request
          originalRequest.headers.Authorization = `Bearer ${accessToken}`;
          return apiClient(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, redirect to login
        tokenStorage.clearTokens();
        window.location.href = "/login";
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;
export { tokenStorage };
