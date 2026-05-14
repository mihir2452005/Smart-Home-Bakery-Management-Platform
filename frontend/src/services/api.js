/**
 * API Service
 * Handles all communication with the backend API
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add user token if available
    const token = localStorage.getItem('userToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error.response?.data || error);
  }
);

// Auth APIs
export const authAPI = {
  register: (userData) => api.post('/auth/register', userData),
  login: (credentials) => api.post('/auth/login', credentials),
  getProfile: (userId) => api.get(`/auth/profile/${userId}`),
  updateProfile: (userId, data) => api.put(`/auth/profile/${userId}`, data),
  getPreferences: (userId) => api.get(`/auth/preferences/${userId}`),
  updatePreferences: (userId, data) => api.put(`/auth/preferences/${userId}`, data),
};

// Recipe APIs
export const recipeAPI = {
  generateRecipe: (data) => api.post('/recipes/generate', data),
  getRecipes: (userId, page = 1) => api.get(`/recipes/${userId}?page=${page}`),
  getRecipe: (recipeId) => api.get(`/recipes/${recipeId}`),
  rateRecipe: (recipeId, data) => api.post(`/recipes/${recipeId}/rate`, data),
  deleteRecipe: (recipeId) => api.delete(`/recipes/${recipeId}`),
  searchRecipes: (params) => api.get('/recipes/search', { params }),
};

// Ingredient APIs
export const ingredientAPI = {
  getIngredients: (userId, page = 1, category = '') =>
    api.get(`/ingredients/${userId}?page=${page}&category=${category}`),
  addIngredient: (data) => api.post('/ingredients', data),
  getIngredient: (ingredientId) => api.get(`/ingredients/${ingredientId}`),
  updateIngredient: (ingredientId, data) => api.put(`/ingredients/${ingredientId}`, data),
  useIngredient: (ingredientId, data) => api.post(`/ingredients/${ingredientId}/use`, data),
  getAlerts: (userId) => api.get(`/ingredients/${userId}/alerts`),
  resolveAlert: (alertId) => api.post(`/ingredients/alerts/${alertId}/resolve`),
  deleteIngredient: (ingredientId) => api.delete(`/ingredients/${ingredientId}`),
};

// Order APIs
export const orderAPI = {
  createOrder: (data) => api.post('/orders', data),
  getOrders: (userId, page = 1, status = '') =>
    api.get(`/orders/${userId}?page=${page}&status=${status}`),
  getOrder: (orderId) => api.get(`/orders/${orderId}`),
  estimateCost: (orderId, data) => api.post(`/orders/${orderId}/estimate`, data),
  updateStatus: (orderId, data) => api.put(`/orders/${orderId}/status`, data),
  finalizeOrder: (orderId, data) => api.post(`/orders/${orderId}/finalize`, data),
  cancelOrder: (orderId) => api.delete(`/orders/${orderId}`),
};

// Dashboard APIs
export const dashboardAPI = {
  getSummary: (userId, days = 30) => api.get(`/dashboard/${userId}/summary?days=${days}`),
  getDailyProfit: (userId, days = 30) => api.get(`/dashboard/${userId}/daily-profit?days=${days}`),
  getRecipePerformance: (userId) => api.get(`/dashboard/${userId}/recipe-performance`),
  getExpenseBreakdown: (userId, days = 30) =>
    api.get(`/dashboard/${userId}/expense-breakdown?days=${days}`),
  getMonthlyTrend: (userId, months = 6) => api.get(`/dashboard/${userId}/monthly-trend?months=${months}`),
  generateReport: (userId) => api.post(`/dashboard/${userId}/generate-report`),
};

// AI APIs
export const aiAPI = {
  generateRecipe: (data) => api.post('/ai/recipe-generator', data),
  getDecorationRecommendations: (data) => api.post('/ai/decoration-recommendations', data),
  diagnoseBakingMistake: (data) => api.post('/ai/diagnose-mistake', data),
  optimizeProfit: (data) => api.post('/ai/optimize-profit', data),
  suggestCakes: (data) => api.post('/ai/suggest-cakes', data),
  generateImage: (data) => api.post('/ai/generate-image', data),
  calculateCost: (data) => api.post('/ai/calculate-cost', data),
  suggestPrice: (data) => api.post('/ai/suggest-price', data),
  getGeneratedImages: (userId) => api.get(`/ai/${userId}/generated-images`),
};

// Expense APIs
export const expenseAPI = {
  getExpenses: (userId, page = 1, category = '') =>
    api.get(`/expenses/${userId}?page=${page}&category=${category}`),
  addExpense: (data) => api.post('/expenses', data),
  getExpense: (expenseId) => api.get(`/expenses/${expenseId}`),
  updateExpense: (expenseId, data) => api.put(`/expenses/${expenseId}`, data),
  deleteExpense: (expenseId) => api.delete(`/expenses/${expenseId}`),
};

// Market Rates APIs
export const marketRatesAPI = {
  scrapeRates: (data) => api.post('/market-rates/scrape', data),
  getMarketRates: (userId, page = 1, location = '', cakeType = '') =>
    api.get(`/market-rates/${userId}?page=${page}&location=${location}&cake_type=${cakeType}`),
  analyzeRates: (userId, data) => api.post(`/market-rates/analyze/${userId}`, data),
  getLocations: (userId) => api.get(`/market-rates/locations/${userId}`),
  getDecorationRefs: (userId, page = 1, cakeWeight = '', style = '') =>
    api.get(`/market-rates/decoration-refs/${userId}?page=${page}&cake_weight=${cakeWeight}&style=${style}`),
  addDecorationRef: (data) => api.post('/market-rates/decoration-refs', data),
};

export default api;
