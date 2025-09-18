const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

class ApiService {
  constructor() {
    this.baseUrl = BASE_URL;
    this.token = null;
  }

  setAuthToken(token) {
    this.token = token;
  }

  getHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    return headers;
  }

  async handleResponse(response) {
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.message || 'An error occurred');
    }
    
    return data;
  }

  // Auth specific methods
  async login(email, password) {
    try {
      const response = await this.post('/auth/login', { email, password });
      if (response.token) {
        this.setAuthToken(response.token);
      }
      return response;
    } catch (error) {
      throw new Error(error.message || 'Login failed. Please check your credentials.');
    }
  }

  async register(email, password) {
    try {
      const response = await this.post('/auth/register', { email, password });
      if (response.token) {
        this.setAuthToken(response.token);
      }
      return response;
    } catch (error) {
      throw new Error(error.message || 'Registration failed. Please try again.');
    }
  }

  async verifyToken() {
    try {
      return await this.get('/auth/verify');
    } catch (error) {
      throw new Error('Token verification failed');
    }
  }

  async get(endpoint) {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'GET',
      headers: this.getHeaders(),
    });
    return this.handleResponse(response);
  }

  async post(endpoint, data) {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(data),
    });
    return this.handleResponse(response);
  }

  async put(endpoint, data) {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'PUT',
      headers: this.getHeaders(),
      body: JSON.stringify(data),
    });
    return this.handleResponse(response);
  }

  async delete(endpoint) {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'DELETE',
      headers: this.getHeaders(),
    });
    return this.handleResponse(response);
  }
}

const api = new ApiService();
export default api;