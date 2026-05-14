import { Link } from 'react-router-dom';
import { Cake, Sparkles, TrendingUp, Package } from 'lucide-react';

const HomePage = () => (
  <div className="min-h-screen bg-gradient-to-br from-pink-500 via-pink-400 to-yellow-400">
    {/* Hero Section */}
    <div className="container-main py-20 text-center animate-fadeIn">
      <div className="inline-block p-3 bg-white/20 backdrop-blur-md rounded-full mb-6">
        <Cake size={48} className="text-white" />
      </div>
      <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
        Smart Home <br />
        <span className="text-yellow-200">Bakery Platform</span>
      </h1>
      <p className="text-xl text-white/90 mb-10 max-w-2xl mx-auto">
        The all-in-one AI-powered assistant for home bakers. 
        Generate perfect recipes, track costs, and grow your business professionally.
      </p>
      <div className="flex flex-col sm:flex-row gap-4 justify-center">
        <Link to="/register" className="btn btn-primary text-lg px-8 py-4 shadow-xl">
          Start Baking Now
        </Link>
        <Link to="/login" className="btn btn-secondary text-lg px-8 py-4 shadow-xl">
          Baker Login
        </Link>
      </div>
    </div>

    {/* Features Grid */}
    <div className="container-main py-20 grid grid-1 md:grid-3 gap-8">
      <div className="card p-8 text-center space-y-4 hover:scale-105 transition-transform">
        <div className="w-16 h-16 bg-pink-100 dark:bg-pink-900/30 rounded-full flex items-center justify-center mx-auto text-pink-500">
          <Sparkles size={32} />
        </div>
        <h3 className="text-xl font-bold">AI Recipe Generator</h3>
        <p className="text-gray-600 dark:text-gray-400">
          Get professional eggless recipes tailored to your budget, oven, and serving size.
        </p>
      </div>

      <div className="card p-8 text-center space-y-4 hover:scale-105 transition-transform">
        <div className="w-16 h-16 bg-yellow-100 dark:bg-yellow-900/30 rounded-full flex items-center justify-center mx-auto text-yellow-500">
          <TrendingUp size={32} />
        </div>
        <h3 className="text-xl font-bold">Profit Intelligence</h3>
        <p className="text-gray-600 dark:text-gray-400">
          Calculate exact ingredient costs and set competitive market prices to maximize profit.
        </p>
      </div>

      <div className="card p-8 text-center space-y-4 hover:scale-105 transition-transform">
        <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center mx-auto text-blue-500">
          <Package size={32} />
        </div>
        <h3 className="text-xl font-bold">Inventory Tracking</h3>
        <p className="text-gray-600 dark:text-gray-400">
          Never run out of ingredients with smart low-stock alerts and supplier management.
        </p>
      </div>
    </div>

    {/* Footer */}
    <footer className="py-10 text-center text-white/70 text-sm">
      <p>© {new Date().getFullYear()} Cake Hub. Made with ❤️ for Home Bakers.</p>
    </footer>
  </div>
);

export default HomePage;
