/**
 * Layout Component
 * Main layout with sidebar and header
 */

import { useState } from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { Menu, X, LogOut, Settings, Sun, Moon } from 'lucide-react';
import { useStore } from '../services/store';
import toast from 'react-hot-toast';

const Layout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const { user, darkMode, setDarkMode, logout } = useStore();
  const location = useLocation();

  const menuItems = [
    { label: 'Dashboard', path: '/dashboard', icon: '📊' },
    { label: 'Recipe Generator', path: '/recipes/generator', icon: '🎂' },
    { label: 'Inventory', path: '/inventory', icon: '📦' },
    { label: 'Orders', path: '/orders', icon: '🛒' },
    { label: 'AI Features', path: '/ai-features', icon: '🤖' },
    { label: 'Market Analysis', path: '/market-analysis', icon: '💹' },
    { label: 'Expenses', path: '/expenses', icon: '💰' },
    { label: 'Settings', path: '/settings', icon: '⚙️' },
  ];

  const handleLogout = () => {
    logout();
    localStorage.removeItem('userToken');
    toast.success('Logged out successfully');
  };

  const isActive = (path) => location.pathname === path;

  return (
    <div className="flex h-screen bg-light dark:bg-dark">
      {/* Sidebar */}
      <aside
        className={`${
          sidebarOpen ? 'w-64' : 'w-0'
        } bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 transition-all duration-300 overflow-hidden`}
      >
        <div className="h-full flex flex-col">
          {/* Logo */}
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <h1 className="text-2xl font-bold bg-gradient-to-r from-pink-500 to-yellow-400 bg-clip-text text-transparent">
              🎂 Cake Hub
            </h1>
          </div>

          {/* Navigation */}
          <nav className="flex-1 overflow-y-auto p-4">
            <ul className="space-y-2">
              {menuItems.map((item) => (
                <li key={item.path}>
                  <Link
                    to={item.path}
                    className={`flex items-center space-x-3 px-4 py-2 rounded-lg transition-all ${
                      isActive(item.path)
                        ? 'bg-pink-500 text-white'
                        : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                    }`}
                  >
                    <span className="text-xl">{item.icon}</span>
                    <span>{item.label}</span>
                  </Link>
                </li>
              ))}
            </ul>
          </nav>

          {/* User Info */}
          <div className="p-4 border-t border-gray-200 dark:border-gray-700">
            <div className="text-sm text-gray-600 dark:text-gray-400">
              <p className="font-semibold">{user?.bakery_name || 'My Bakery'}</p>
              <p className="truncate">{user?.email}</p>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 px-6 py-4">
          <div className="flex items-center justify-between">
            {/* Toggle Sidebar */}
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
            >
              {sidebarOpen ? <X size={24} /> : <Menu size={24} />}
            </button>

            {/* Right Side Controls */}
            <div className="flex items-center space-x-4">
              {/* Dark Mode Toggle */}
              <button
                onClick={() => setDarkMode(!darkMode)}
                className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
              >
                {darkMode ? <Sun size={20} /> : <Moon size={20} />}
              </button>

              {/* Settings */}
              <Link
                to="/settings"
                className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
              >
                <Settings size={20} />
              </Link>

              {/* Logout */}
              <button
                onClick={handleLogout}
                className="p-2 hover:bg-red-100 dark:hover:bg-red-900 text-red-600 rounded-lg transition-colors"
              >
                <LogOut size={20} />
              </button>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;
