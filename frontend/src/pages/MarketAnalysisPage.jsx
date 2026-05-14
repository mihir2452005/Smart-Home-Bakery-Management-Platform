import { useState, useEffect } from 'react';
import { useStore } from '../services/store';
import { marketRatesAPI } from '../services/api';
import toast from 'react-hot-toast';
import { Globe, TrendingUp, Search, BarChart3 } from 'lucide-react';

const MarketAnalysisPage = () => {
  const { user } = useStore();
  const [rates, setRates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [analysis, setAnalysis] = useState(null);
  const [query, setQuery] = useState({
    cake_type: 'Chocolate',
    weight: '1kg',
    user_cake_cost: ''
  });

  useEffect(() => {
    fetchRates();
  }, [user?.id]);

  const fetchRates = async () => {
    if (!user?.id) return;
    setLoading(true);
    try {
      const response = await marketRatesAPI.getMarketRates(user.id);
      setRates(response?.items || []);
    } catch (error) {
      toast.error('Failed to load market rates');
    } finally {
      setLoading(false);
    }
  };

  const handleScrape = async () => {
    try {
      await marketRatesAPI.scrapeRates({
        user_id: user.id,
        location: user.location || 'Bangalore',
        cake_types: ['Chocolate', 'Vanilla', 'Red Velvet']
      });
      toast.success('Market rates updated!');
      fetchRates();
    } catch (error) {
      toast.error('Scraping failed');
    }
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!query.user_cake_cost) {
      toast.error('Please enter your cake cost');
      return;
    }
    try {
      const result = await marketRatesAPI.analyzeRates(user.id, {
        cake_type: query.cake_type,
        weight: query.weight,
        user_cake_cost: Number(query.user_cake_cost)
      });
      setAnalysis(result);
      toast.success('Analysis complete!');
    } catch (error) {
      toast.error('Analysis failed');
    }
  };

  if (loading) return <div className="text-center py-8">Loading market data...</div>;

  return (
    <div className="space-y-6 animate-fadeIn">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Market Analysis</h1>
          <p className="text-gray-600 dark:text-gray-400">Analyze competitor pricing and optimize your margins</p>
        </div>
        <button onClick={handleScrape} className="btn btn-primary flex items-center gap-2">
          <Search size={18} /> Update Market Rates
        </button>
      </div>

      <div className="grid grid-1 lg:grid-3 gap-6">
        <div className="lg:col-span-1 card">
          <h3 className="font-bold text-lg mb-4 flex items-center gap-2">
            <BarChart3 size={20} className="text-pink-500" /> Pricing Analyzer
          </h3>
          <form onSubmit={handleAnalyze} className="space-y-4">
            <div>
              <label className="form-label">Cake Type</label>
              <select 
                className="form-select" 
                value={query.cake_type} 
                onChange={e => setQuery({...query, cake_type: e.target.value})}
              >
                <option value="Chocolate">Chocolate</option>
                <option value="Vanilla">Vanilla</option>
                <option value="Red Velvet">Red Velvet</option>
                <option value="Fruit Cake">Fruit Cake</option>
              </select>
            </div>
            <div>
              <label className="form-label">Weight</label>
              <select 
                className="form-select" 
                value={query.weight} 
                onChange={e => setQuery({...query, weight: e.target.value})}
              >
                <option value="500g">500g</option>
                <option value="1kg">1kg</option>
                <option value="2kg">2kg</option>
                <option value="3kg">3kg</option>
              </select>
            </div>
            <div>
              <label className="form-label">Your Cost (₹)</label>
              <input 
                type="number" 
                className="form-input" 
                value={query.user_cake_cost} 
                onChange={e => setQuery({...query, user_cake_cost: e.target.value})} 
                placeholder="e.g. 250"
              />
            </div>
            <button type="submit" className="btn btn-primary w-full">Analyze Now</button>
          </form>

          {analysis && (
            <div className="mt-6 p-4 bg-pink-50 dark:bg-pink-900/20 rounded-lg border-l-4 border-pink-500 animate-fadeIn">
              <p className="text-sm text-gray-500">Recommended Price</p>
              <p className="text-2xl font-bold text-pink-600">₹{analysis.recommended_price}</p>
              <div className="mt-3 space-y-2 text-sm">
                <div className="flex justify-between">
                  <span>Market Avg:</span>
                  <span className="font-semibold">₹{analysis.market_average}</span>
                </div>
                <div className="flex justify-between">
                  <span>Min Price:</span>
                  <span className="font-semibold">₹{analysis.market_min}</span>
                </div>
                <div className="flex justify-between">
                  <span>Max Price:</span>
                  <span className="font-semibold">₹{analysis.market_max}</span>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="lg:col-span-2 card overflow-x-auto">
          <h3 className="font-bold text-lg mb-4 flex items-center gap-2">
            <Globe size={20} className="text-pink-500" /> Competitor Rates
          </h3>
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400">
                <th className="p-4 font-semibold">Bakery</th>
                <th className="p-4 font-semibold">Cake Type</th>
                <th className="p-4 font-semibold">Weight</th>
                <th className="p-4 font-semibold">Price</th>
              </tr>
            </thead>
            <tbody>
              {rates.length > 0 ? rates.map((rate) => (
                <tr key={rate.id} className="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                  <td className="p-4 font-medium">{rate.bakery_name || 'Unknown Bakery'}</td>
                  <td className="p-4">{rate.cake_type}</td>
                  <td className="p-4">{rate.weight}</td>
                  <td className="p-4 font-semibold">₹{rate.price}</td>
                </tr>
              )) : (
                <tr>
                  <td colSpan="4" className="p-8 text-center text-gray-500">No market data available. Click "Update Market Rates" to scrape.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default MarketAnalysisPage;
