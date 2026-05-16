import React from 'react';
import { Link } from 'react-router-dom';
import { Cake, Sparkles, TrendingUp, Package, Users, Zap, BarChart3, Coffee } from 'lucide-react';

const HomePage = () => (
  <div className="min-h-screen bg-white dark:bg-gray-900">
    {/* Navigation Bar */}
    <nav className="backdrop-blur-md bg-white/80 dark:bg-gray-900/80 sticky top-0 z-50 border-b border-pink-100 dark:border-pink-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <Cake className="text-pink-500" size={32} />
          <span className="text-2xl font-bold bg-gradient-to-r from-pink-500 to-yellow-500 bg-clip-text text-transparent">
            Cake Hub
          </span>
        </div>
        <div className="flex gap-4">
          <Link to="/login" className="px-6 py-2 text-gray-700 dark:text-gray-300 hover:text-pink-500 font-medium transition">
            Login
          </Link>
          <Link to="/register" className="px-6 py-2 bg-gradient-to-r from-pink-500 to-yellow-500 text-white rounded-full font-semibold hover:shadow-lg transition">
            Get Started
          </Link>
        </div>
      </div>
    </nav>

    {/* Hero Section */}
    <div className="relative overflow-hidden bg-gradient-to-b from-pink-50 via-white to-yellow-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 py-20 md:py-32">
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-pink-200 dark:bg-pink-900/20 rounded-full blur-3xl opacity-30"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-yellow-200 dark:bg-yellow-900/20 rounded-full blur-3xl opacity-30"></div>
      </div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
        <div className="inline-block mb-6 px-4 py-2 bg-pink-100 dark:bg-pink-900/30 rounded-full">
          <span className="text-pink-600 dark:text-pink-400 font-semibold text-sm">🚀 Trusted by 1000+ Home Bakers</span>
        </div>
        
        <h1 className="text-5xl md:text-7xl font-bold text-gray-900 dark:text-white mb-6 leading-tight">
          Turn Your <span className="bg-gradient-to-r from-pink-500 via-red-500 to-yellow-500 bg-clip-text text-transparent">Baking Passion</span> Into Profit
        </h1>
        
        <p className="text-lg md:text-xl text-gray-600 dark:text-gray-400 mb-12 max-w-3xl mx-auto leading-relaxed">
          The all-in-one AI-powered platform designed specifically for home bakers. Generate perfect eggless recipes, calculate exact costs, compete with nearby bakeries, and grow your business professionally.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
          <Link to="/register" className="px-8 py-4 bg-gradient-to-r from-pink-500 to-yellow-500 text-white rounded-full font-bold text-lg hover:shadow-2xl transition-all hover:scale-105">
            Start Free Today →
          </Link>
          <Link to="/login" className="px-8 py-4 border-2 border-pink-500 text-pink-600 dark:text-pink-400 rounded-full font-bold text-lg hover:bg-pink-50 dark:hover:bg-pink-900/20 transition">
            Already Have Account?
          </Link>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-8 max-w-2xl mx-auto">
          <div>
            <p className="text-3xl md:text-4xl font-bold text-pink-500">500+</p>
            <p className="text-gray-600 dark:text-gray-400 text-sm">Recipes AI Generated</p>
          </div>
          <div>
            <p className="text-3xl md:text-4xl font-bold text-yellow-500">98%</p>
            <p className="text-gray-600 dark:text-gray-400 text-sm">User Satisfaction</p>
          </div>
          <div>
            <p className="text-3xl md:text-4xl font-bold text-blue-500">24/7</p>
            <p className="text-gray-600 dark:text-gray-400 text-sm">Support Available</p>
          </div>
        </div>
      </div>
    </div>

    {/* Features Section */}
    <div className="py-20 md:py-32 bg-white dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">Powerful Features Built for You</h2>
          <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">Everything you need to succeed as a home baker in one beautiful, easy-to-use platform</p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Feature 1 */}
          <div className="group p-8 bg-gradient-to-br from-pink-50 to-pink-100 dark:from-pink-900/10 dark:to-pink-900/20 rounded-2xl border border-pink-200 dark:border-pink-800 hover:shadow-xl transition-all hover:scale-105">
            <div className="w-14 h-14 bg-pink-500 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition">
              <Sparkles size={28} className="text-white" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">AI Recipe Generator</h3>
            <p className="text-gray-700 dark:text-gray-400">Generate perfect eggless cake recipes tailored to your budget, oven capacity, and serving size in seconds.</p>
          </div>

          {/* Feature 2 */}
          <div className="group p-8 bg-gradient-to-br from-yellow-50 to-yellow-100 dark:from-yellow-900/10 dark:to-yellow-900/20 rounded-2xl border border-yellow-200 dark:border-yellow-800 hover:shadow-xl transition-all hover:scale-105">
            <div className="w-14 h-14 bg-yellow-500 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition">
              <TrendingUp size={28} className="text-white" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Profit Calculator</h3>
            <p className="text-gray-700 dark:text-gray-400">Calculate exact ingredient costs and automatically set competitive prices to maximize your profit margins.</p>
          </div>

          {/* Feature 3 */}
          <div className="group p-8 bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/10 dark:to-blue-900/20 rounded-2xl border border-blue-200 dark:border-blue-800 hover:shadow-xl transition-all hover:scale-105">
            <div className="w-14 h-14 bg-blue-500 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition">
              <Package size={28} className="text-white" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Smart Inventory</h3>
            <p className="text-gray-700 dark:text-gray-400">Track ingredients, get low-stock alerts, and manage suppliers efficiently without running out.</p>
          </div>

          {/* Feature 4 */}
          <div className="group p-8 bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900/10 dark:to-purple-900/20 rounded-2xl border border-purple-200 dark:border-purple-800 hover:shadow-xl transition-all hover:scale-105">
            <div className="w-14 h-14 bg-purple-500 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition">
              <BarChart3 size={28} className="text-white" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Analytics Dashboard</h3>
            <p className="text-gray-700 dark:text-gray-400">Track orders, profits, expenses, and customer trends with beautiful real-time analytics.</p>
          </div>

          {/* Feature 5 */}
          <div className="group p-8 bg-gradient-to-br from-red-50 to-red-100 dark:from-red-900/10 dark:to-red-900/20 rounded-2xl border border-red-200 dark:border-red-800 hover:shadow-xl transition-all hover:scale-105">
            <div className="w-14 h-14 bg-red-500 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition">
              <Zap size={28} className="text-white" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Market Analysis</h3>
            <p className="text-gray-700 dark:text-gray-400">See what nearby bakeries are charging and adjust your prices to stay competitive.</p>
          </div>

          {/* Feature 6 */}
          <div className="group p-8 bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/10 dark:to-green-900/20 rounded-2xl border border-green-200 dark:border-green-800 hover:shadow-xl transition-all hover:scale-105">
            <div className="w-14 h-14 bg-green-500 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition">
              <Users size={28} className="text-white" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Order Management</h3>
            <p className="text-gray-700 dark:text-gray-400">Manage customer orders, track orders, and keep clients happy with professional service.</p>
          </div>

          {/* Feature 7 */}
          <div className="group p-8 bg-gradient-to-br from-indigo-50 to-indigo-100 dark:from-indigo-900/10 dark:to-indigo-900/20 rounded-2xl border border-indigo-200 dark:border-indigo-800 hover:shadow-xl transition-all hover:scale-105">
            <div className="w-14 h-14 bg-indigo-500 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition">
              <Coffee size={28} className="text-white" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Decoration Ideas</h3>
            <p className="text-gray-700 dark:text-gray-400">Get AI-powered decoration suggestions with beautiful references for every cake style.</p>
          </div>

          {/* Feature 8 */}
          <div className="group p-8 bg-gradient-to-br from-orange-50 to-orange-100 dark:from-orange-900/10 dark:to-orange-900/20 rounded-2xl border border-orange-200 dark:border-orange-800 hover:shadow-xl transition-all hover:scale-105">
            <div className="w-14 h-14 bg-orange-500 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition">
              <Cake size={28} className="text-white" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Baking Guidance</h3>
            <p className="text-gray-700 dark:text-gray-400">Learn how to fix common baking mistakes and troubleshoot issues with AI-powered solutions.</p>
          </div>
        </div>
      </div>
    </div>

    {/* Pricing Section */}
    <div className="py-20 md:py-32 bg-gray-50 dark:bg-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">Simple, Transparent Pricing</h2>
          <p className="text-lg text-gray-600 dark:text-gray-400">Start free, upgrade anytime. No hidden fees.</p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          <div className="p-8 bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-700 text-center hover:shadow-lg transition">
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Hobby Baker</h3>
            <p className="text-gray-600 dark:text-gray-400 mb-6">Perfect to start</p>
            <p className="text-4xl font-bold text-gray-900 dark:text-white mb-6"><span className="text-lg">₹</span>0<span className="text-lg">/mo</span></p>
            <button className="w-full py-3 border-2 border-pink-500 text-pink-600 dark:text-pink-400 rounded-full font-bold hover:bg-pink-50 dark:hover:bg-pink-900/20 transition mb-6">
              Get Started
            </button>
            <ul className="space-y-3 text-left">
              <li className="text-gray-700 dark:text-gray-400">✓ 10 Recipe Generations</li>
              <li className="text-gray-700 dark:text-gray-400">✓ Cost Calculator</li>
              <li className="text-gray-700 dark:text-gray-400">✓ Basic Analytics</li>
            </ul>
          </div>

          <div className="p-8 bg-white dark:bg-gray-900 rounded-2xl border-2 border-pink-500 shadow-xl text-center transform scale-105">
            <div className="inline-block px-4 py-1 bg-pink-500 text-white rounded-full text-sm font-bold mb-4">Most Popular</div>
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Professional</h3>
            <p className="text-gray-600 dark:text-gray-400 mb-6">For growing businesses</p>
            <p className="text-4xl font-bold text-gray-900 dark:text-white mb-6"><span className="text-lg">₹</span>299<span className="text-lg">/mo</span></p>
            <button className="w-full py-3 bg-gradient-to-r from-pink-500 to-yellow-500 text-white rounded-full font-bold hover:shadow-lg transition mb-6">
              Start Free Trial
            </button>
            <ul className="space-y-3 text-left">
              <li className="text-gray-700 dark:text-gray-400">✓ Unlimited Recipes</li>
              <li className="text-gray-700 dark:text-gray-400">✓ Full Analytics</li>
              <li className="text-gray-700 dark:text-gray-400">✓ Market Analysis</li>
              <li className="text-gray-700 dark:text-gray-400">✓ Priority Support</li>
            </ul>
          </div>

          <div className="p-8 bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-700 text-center hover:shadow-lg transition">
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Enterprise</h3>
            <p className="text-gray-600 dark:text-gray-400 mb-6">For teams</p>
            <p className="text-4xl font-bold text-gray-900 dark:text-white mb-6">Custom</p>
            <button className="w-full py-3 border-2 border-pink-500 text-pink-600 dark:text-pink-400 rounded-full font-bold hover:bg-pink-50 dark:hover:bg-pink-900/20 transition mb-6">
              Contact Sales
            </button>
            <ul className="space-y-3 text-left">
              <li className="text-gray-700 dark:text-gray-400">✓ Everything in Pro</li>
              <li className="text-gray-700 dark:text-gray-400">✓ Custom Integration</li>
              <li className="text-gray-700 dark:text-gray-400">✓ Dedicated Support</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    {/* CTA Section */}
    <div className="py-20 md:py-32 bg-gradient-to-r from-pink-500 via-red-500 to-yellow-500">
      <div className="max-w-4xl mx-auto text-center px-4">
        <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">Ready to Grow Your Bakery?</h2>
        <p className="text-xl text-white/90 mb-8">Join thousands of home bakers already using Cake Hub to turn their passion into profit.</p>
        <Link to="/register" className="inline-block px-8 py-4 bg-white text-pink-600 rounded-full font-bold text-lg hover:shadow-2xl transition hover:scale-105">
          Start Your Free Account →
        </Link>
      </div>
    </div>

    {/* Footer */}
    <footer className="py-12 bg-gray-900 text-gray-400 border-t border-gray-800">
      <div className="max-w-7xl mx-auto px-4">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <Cake className="text-pink-500" size={24} />
              <span className="font-bold text-white">Cake Hub</span>
            </div>
            <p className="text-sm">Empowering home bakers to build professional businesses.</p>
          </div>
          <div>
            <h4 className="font-bold text-white mb-4">Product</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="#" className="hover:text-white transition">Features</a></li>
              <li><a href="#" className="hover:text-white transition">Pricing</a></li>
              <li><a href="#" className="hover:text-white transition">Security</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold text-white mb-4">Company</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="#" className="hover:text-white transition">About</a></li>
              <li><a href="#" className="hover:text-white transition">Blog</a></li>
              <li><a href="#" className="hover:text-white transition">Contact</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold text-white mb-4">Legal</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="#" className="hover:text-white transition">Privacy</a></li>
              <li><a href="#" className="hover:text-white transition">Terms</a></li>
              <li><a href="#" className="hover:text-white transition">Cookies</a></li>
            </ul>
          </div>
        </div>
        <div className="border-t border-gray-800 pt-8 text-center text-sm">
          <p>© {new Date().getFullYear()} Cake Hub. Made with ❤️ for Home Bakers. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
);

export default HomePage;
