/**
 * Zustand Store
 * Global state management for the application
 */

import { create } from 'zustand';

export const useStore = create((set) => ({
  // User state
  user: null,
  isLoggedIn: false,
  preferences: {},

  setUser: (user) => set({ user, isLoggedIn: !!user }),
  setPreferences: (preferences) => set({ preferences }),
  logout: () => set({ user: null, isLoggedIn: false }),

  // UI state
  sidebarOpen: true,
  darkMode: localStorage.getItem('darkMode') === 'true',
  notifications: [],

  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  setDarkMode: (dark) => {
    localStorage.setItem('darkMode', dark);
    set({ darkMode: dark });
  },

  addNotification: (notification) =>
    set((state) => ({
      notifications: [...state.notifications, notification],
    })),

  removeNotification: (id) =>
    set((state) => ({
      notifications: state.notifications.filter((n) => n.id !== id),
    })),

  // Recipe state
  recipes: [],
  selectedRecipe: null,

  setRecipes: (recipes) => set({ recipes }),
  setSelectedRecipe: (recipe) => set({ selectedRecipe: recipe }),

  // Order state
  orders: [],
  selectedOrder: null,

  setOrders: (orders) => set({ orders }),
  setSelectedOrder: (order) => set({ selectedOrder: order }),

  // Ingredient state
  ingredients: [],

  setIngredients: (ingredients) => set({ ingredients }),

  // Dashboard state
  dashboardData: null,

  setDashboardData: (data) => set({ dashboardData: data }),
}));
