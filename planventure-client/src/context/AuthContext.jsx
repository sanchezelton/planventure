import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import api from '../services/api';

const AuthContext = createContext(null);

const TOKEN_KEY = 'planventure_token';

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState(localStorage.getItem(TOKEN_KEY));
  const [loading, setLoading] = useState(true);

  // Initialize authentication state from stored token
  useEffect(() => {
    const initAuth = async () => {
      const storedToken = localStorage.getItem(TOKEN_KEY);
      if (storedToken) {
        try {
          // Validate token with backend
          api.setAuthToken(storedToken);
          await api.get('/auth/verify');
          setIsAuthenticated(true);
          setToken(storedToken);
        } catch (error) {
          console.error('Token validation failed:', error);
          logout();
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = useCallback(async (email, password) => {
    try {
      const response = await api.post('/auth/login', { email, password });
      const { token: newToken } = response;
      
      if (!newToken) {
        throw new Error('No token received from server');
      }

      // Set token in localStorage and state
      localStorage.setItem(TOKEN_KEY, newToken);
      api.setAuthToken(newToken);
      setToken(newToken);
      setIsAuthenticated(true);

      return response;
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  }, []);

  const register = useCallback(async (email, password) => {
    try {
      const response = await api.post('/auth/register', { email, password });
      const { token: newToken } = response;

      if (!newToken) {
        throw new Error('No token received from server');
      }

      // Set token in localStorage and state
      localStorage.setItem(TOKEN_KEY, newToken);
      api.setAuthToken(newToken);
      setToken(newToken);
      setIsAuthenticated(true);

      return response;
    } catch (error) {
      console.error('Registration failed:', error);
      throw error;
    }
  }, []);

  const logout = useCallback(() => {
    // Clear token from localStorage and state
    localStorage.removeItem(TOKEN_KEY);
    api.setAuthToken(null);
    setToken(null);
    setIsAuthenticated(false);
  }, []);

  const value = {
    isAuthenticated,
    token,
    loading,
    login,
    register,
    logout
  };

  if (loading) {
    // You might want to show a loading spinner here
    return null;
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};