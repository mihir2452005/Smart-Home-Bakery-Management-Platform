/**
 * Dashboard Page
 * Main analytics and profit dashboard
 */

import { useEffect, useState } from 'react';
import { useStore } from '../services/store';
import { dashboardAPI } from '../services/api';
import { TrendingUp, Package, ShoppingCart, DollarSign } from 'lucide-react';
import toast from 'react-hot-toast';

const DashboardPage = () => {
  const { user, dashboardData, setDashboardData } = useStore();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      if (!user?.id) return;

      try {
        setLoading(true);
        const data = await dashboardAPI.getSummary(user.id, 30);
        setDashboardData(data);
      } catch (error) {
        toast.error('Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, [user?.id, setDashboardData]);

  if (loading) {
    return <div className="text-center py-8">Loading dashboard...</div>;
  }

  const summary = dashboardData?.summary || {};

  const stats = [
    {
      title: 'Total Orders',
      value: summary.total_orders || 0,
      icon: ShoppingCart,
      color: 'bg-blue-500',
    },
    {
      title: 'Revenue',
      value: `₹${summary.total_revenue?.toFixed(2) || 0}`,
      icon: DollarSign,
      color: 'bg-green-500',
    },
    {
      title: 'Total Profit',
      value: `₹${summary.total_profit?.toFixed(2) || 0}`,
      icon: TrendingUp,
      color: 'bg-pink-500',
    },
    {
      title: 'Avg Profit/Cake',
      value: `₹${summary.average_profit_per_cake?.toFixed(2) || 0}`,
      icon: Package,
      color: 'bg-yellow-500',
    },
  ];

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
        <p className="text-gray-600 dark:text-gray-400">Welcome back, {user?.full_name}!</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div key={stat.title} className="card hover:shadow-lg transition-all">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 dark:text-gray-400 text-sm">{stat.title}</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white mt-2">
                    {stat.value}
                  </p>
                </div>
                <div className={`${stat.color} p-3 rounded-lg text-white`}>
                  <Icon size={24} />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Charts Section */}
      <div className="grid grid-1 lg:grid-cols-2 gap-6">
        {/* Profit Margin */}
        <div className="card">
          <h3 className="font-bold text-lg mb-4">Profit Margin</h3>
          <div className="text-center py-8">
            <p className="text-4xl font-bold text-pink-500">
              {dashboardData?.profit_margin?.toFixed(1) || 0}%
            </p>
            <p className="text-gray-600 dark:text-gray-400 mt-2">Status: {summary.profit_status}</p>
          </div>
        </div>

        {/* Most Selling Flavor */}
        <div className="card">
          <h3 className="font-bold text-lg mb-4">Most Selling</h3>
          <div className="text-center py-8">
            <p className="text-2xl font-bold text-yellow-500">{summary.most_selling_flavor || 'N/A'}</p>
            <p className="text-gray-600 dark:text-gray-400 mt-2">Flavor</p>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-4 flex-wrap">
        <button className="btn btn-primary">
          Create New Order
        </button>
        <button className="btn btn-secondary">
          Generate Recipe
        </button>
        <button className="btn btn-outline">
          View Reports
        </button>
      </div>
    </div>
  );
};

export default DashboardPage;
