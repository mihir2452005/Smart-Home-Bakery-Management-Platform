/**
 * Placeholder Pages
 * These components need to be expanded with full functionality
 */

import React from 'react';

// LoginPage
export const LoginPage = () => (
  <div className="min-h-screen bg-gradient-to-br from-pink-500 to-yellow-400 flex items-center justify-center p-4">
    <div className="card w-full max-w-md">
      <h1 className="text-3xl font-bold mb-6">Login</h1>
      <form className="space-y-4">
        <input type="email" placeholder="Email" className="form-input" />
        <input type="password" placeholder="Password" className="form-input" />
        <button type="submit" className="btn btn-primary w-full">Login</button>
      </form>
    </div>
  </div>
);

// RegisterPage
export const RegisterPage = () => (
  <div className="min-h-screen bg-gradient-to-br from-pink-500 to-yellow-400 flex items-center justify-center p-4">
    <div className="card w-full max-w-md">
      <h1 className="text-3xl font-bold mb-6">Register</h1>
      <form className="space-y-4">
        <input type="text" placeholder="Full Name" className="form-input" />
        <input type="email" placeholder="Email" className="form-input" />
        <input type="password" placeholder="Password" className="form-input" />
        <input type="password" placeholder="Confirm Password" className="form-input" />
        <button type="submit" className="btn btn-primary w-full">Register</button>
      </form>
    </div>
  </div>
);

// HomePage
export const HomePage = () => (
  <div className="min-h-screen bg-gradient-to-br from-pink-500 to-yellow-400">
    <div className="container-main py-20">
      <h1 className="text-5xl font-bold text-white mb-6">Smart Home Bakery Platform</h1>
      <p className="text-xl text-white mb-8">Perfect your cake recipes and grow your home bakery business</p>
      <div className="space-x-4">
        <a href="/register" className="btn btn-primary">Get Started</a>
        <a href="/login" className="btn btn-secondary">Login</a>
      </div>
    </div>
  </div>
);

// RecipeGeneratorPage
export const RecipeGeneratorPage = () => (
  <div className="card">
    <h1 className="text-3xl font-bold mb-6">AI Recipe Generator</h1>
    <form className="grid grid-2 gap-4">
      <input type="text" placeholder="Cake Flavor" className="form-input" />
      <select className="form-select">
        <option>500g</option>
        <option>1kg</option>
        <option>2kg</option>
        <option>3kg</option>
      </select>
      <input type="number" placeholder="Budget" className="form-input" />
      <select className="form-select">
        <option>Gas Oven</option>
        <option>Microwave</option>
        <option>Electric Oven</option>
      </select>
      <button type="submit" className="btn btn-primary col-span-2">Generate Recipe</button>
    </form>
  </div>
);

// InventoryPage
export const InventoryPage = () => (
  <div className="space-y-6">
    <h1 className="text-3xl font-bold">Inventory Management</h1>
    <div className="card">
      <table className="w-full">
        <thead>
          <tr className="border-b">
            <th className="text-left p-3">Ingredient</th>
            <th className="text-left p-3">Stock</th>
            <th className="text-left p-3">Alert Level</th>
            <th className="text-left p-3">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr className="border-b hover:bg-gray-50 dark:hover:bg-gray-800">
            <td className="p-3">Flour</td>
            <td className="p-3">500g</td>
            <td className="p-3"><span className="badge badge-warning">Low</span></td>
            <td className="p-3">
              <button className="btn btn-outline text-sm">Reorder</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
);

// OrdersPage
export const OrdersPage = () => (
  <div className="space-y-6">
    <h1 className="text-3xl font-bold">Orders</h1>
    <div className="card">
      <p className="text-gray-600 dark:text-gray-400">No orders yet. Start creating orders!</p>
    </div>
  </div>
);

// AIFeaturesPage
export const AIFeaturesPage = () => (
  <div className="space-y-6">
    <h1 className="text-3xl font-bold">AI Features</h1>
    <div className="grid grid-3 gap-6">
      <div className="card text-center">
        <h3 className="font-bold mb-2">🤖 Diagnose Problems</h3>
        <p className="text-sm text-gray-600 dark:text-gray-400">Get AI help for baking issues</p>
      </div>
      <div className="card text-center">
        <h3 className="font-bold mb-2">🎨 Decoration Suggestions</h3>
        <p className="text-sm text-gray-600 dark:text-gray-400">Get design recommendations</p>
      </div>
      <div className="card text-center">
        <h3 className="font-bold mb-2">💰 Profit Optimization</h3>
        <p className="text-sm text-gray-600 dark:text-gray-400">Maximize your profits</p>
      </div>
    </div>
  </div>
);

// MarketAnalysisPage
export const MarketAnalysisPage = () => (
  <div className="space-y-6">
    <h1 className="text-3xl font-bold">Market Analysis</h1>
    <div className="card">
      <p className="text-gray-600 dark:text-gray-400">Analyze nearby bakery prices and set competitive pricing</p>
    </div>
  </div>
);

// ExpensesPage
export const ExpensesPage = () => (
  <div className="space-y-6">
    <h1 className="text-3xl font-bold">Expenses</h1>
    <div className="card">
      <p className="text-gray-600 dark:text-gray-400">Track your business expenses</p>
    </div>
  </div>
);

// SettingsPage
export const SettingsPage = () => (
  <div className="space-y-6">
    <h1 className="text-3xl font-bold">Settings</h1>
    <div className="card">
      <p className="text-gray-600 dark:text-gray-400">Manage your preferences</p>
    </div>
  </div>
);

// NotFoundPage
export const NotFoundPage = () => (
  <div className="min-h-screen flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-4xl font-bold mb-4">404</h1>
      <p className="text-gray-600 dark:text-gray-400 mb-4">Page not found</p>
      <a href="/" className="btn btn-primary">Go Home</a>
    </div>
  </div>
);

// RecipeDetailsPage
export const RecipeDetailsPage = () => (
  <div className="card">
    <h1 className="text-3xl font-bold mb-6">Recipe Details</h1>
    <p className="text-gray-600 dark:text-gray-400">Recipe information will be displayed here</p>
  </div>
);

// OrderDetailPage
export const OrderDetailPage = () => (
  <div className="card">
    <h1 className="text-3xl font-bold mb-6">Order Details</h1>
    <p className="text-gray-600 dark:text-gray-400">Order information will be displayed here</p>
  </div>
);
