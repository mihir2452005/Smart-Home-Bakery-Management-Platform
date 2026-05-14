import { useState } from 'react';
import { useStore } from '../services/store';
import { aiAPI } from '../services/api';
import toast from 'react-hot-toast';
import { Brain, Palette, TrendingUp, AlertCircle, Image as ImageIcon, Sparkles } from 'lucide-react';

const AIFeaturesPage = () => {
  const { user } = useStore();
  const [activeTab, setActiveTab] = useState('diagnose');
  const [loading, setLoading] = useState(false);
  const [input, setInput] = useState('');
  const [result, setResult] = useState(null);

  const handleAIAction = async (type, payload) => {
    setLoading(true);
    setResult(null);
    try {
      let response;
      switch (type) {
        case 'diagnose':
          response = await aiAPI.diagnoseBakingMistake({ 
            problem_description: input, 
            cake_type: 'General' 
          });
          break;
        case 'decorate':
          response = await aiAPI.getDecorationRecommendations({ 
            user_id: user.id, 
            cake_weight: '1kg', 
            style: input || 'Elegant' 
          });
          break;
        case 'optimize':
          response = await aiAPI.optimizeProfit({ 
            user_id: user.id, 
            ingredient_costs: 200, 
            selling_price: 500, 
            cake_type: 'Chocolate', 
            market_rate: 600 
          });
          break;
        case 'image':
          response = await aiAPI.generateImage({ 
            user_id: user.id, 
            prompt: input 
          });
          break;
        default:
          return;
      }
      setResult(response?.data || response);
      toast.success('AI response received!');
    } catch (error) {
      toast.error(error?.message || 'AI service failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">AI Baking Assistant</h1>
        <p className="text-gray-600 dark:text-gray-400">Professional AI tools to perfect your cakes and business</p>
      </div>

      <div className="flex gap-2 overflow-x-auto pb-2">
        {[
          { id: 'diagnose', label: 'Diagnose Mistake', icon: <AlertCircle size={18} /> },
          { id: 'decorate', label: 'Decoration Ideas', icon: <Palette size={18} /> },
          { id: 'optimize', label: 'Profit Optimizer', icon: <TrendingUp size={18} /> },
          { id: 'image', label: 'Design Preview', icon: <ImageIcon size={18} /> },
        ].map(tab => (
          <button 
            key={tab.id}
            onClick={() => { setActiveTab(tab.id); setResult(null); setInput(''); }}
            className={`btn flex items-center gap-2 whitespace-nowrap ${activeTab === tab.id ? 'btn-primary' : 'btn-outline'}`}
          >
            {tab.icon} {tab.label}
          </button>
        ))}
      </div>

      <div className="grid grid-1 lg:grid-2 gap-6">
        <div className="card">
          <h3 className="font-bold text-lg mb-4 flex items-center gap-2">
            <Brain size={20} className="text-pink-500" /> 
            {activeTab === 'diagnose' && 'What went wrong?'}
            {activeTab === 'decorate' && 'Decoration Style'}
            {activeTab === 'optimize' && 'Business Optimization'}
            {activeTab === 'image' && 'Cake Design Prompt'}
          </h3>
          
          <div className="space-y-4">
            <textarea 
              className="form-textarea" 
              rows="4" 
              placeholder={
                activeTab === 'diagnose' ? "e.g. My cake sank in the middle after taking it out of the oven..." :
                activeTab === 'decorate' ? "e.g. Elegant wedding style with white cream and gold drip..." :
                activeTab === 'image' ? "e.g. A 3-tier chocolate cake with strawberry drips and macarons on top..." :
                "Enter details for optimization..."
              }
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
            <button 
              onClick={() => handleAIAction(activeTab, input)} 
              className="btn btn-primary w-full flex items-center justify-center gap-2"
              disabled={loading}
            >
              {loading ? 'AI is thinking...' : <><Sparkles size={18} /> Ask AI Assistant</>}
            </button>
          </div>
        </div>

        <div className="card min-h-[400px]">
          <h3 className="font-bold text-lg mb-4">AI Response</h3>
          {!result && !loading && (
            <div className="flex flex-col items-center justify-center h-64 text-gray-500">
              <Brain size={48} className="mb-4 opacity-20" />
              <p>Enter your query and click "Ask AI Assistant"</p>
            </div>
          )}
          {loading && (
            <div className="flex flex-col items-center justify-center h-64 space-y-4">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-pink-500"></div>
              <p className="text-gray-500">Consulting AI experts...</p>
            </div>
          )}
          {result && (
            <div className="space-y-4 animate-fadeIn">
              {activeTab === 'diagnose' && (
                <div className="space-y-4">
                  <div className="p-4 bg-red-50 dark:bg-red-900/20 rounded-lg border-l-4 border-red-500">
                    <p className="font-bold text-red-600">Likely Cause:</p>
                    <p className="text-gray-700 dark:text-gray-300">{result.likely_cause || 'Unknown'}</p>
                  </div>
                  <div>
                    <p className="font-bold mb-2">Solutions:</p>
                    <ul className="list-disc list-inside space-y-2 text-gray-700 dark:text-gray-300">
                      {result.solutions?.map((s, i) => <li key={i}>{s}</li>)}
                    </ul>
                  </div>
                  <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border-l-4 border-green-500">
                    <p className="font-bold text-green-600">Prevention Tips:</p>
                    <p className="text-gray-700 dark:text-gray-300">{result.prevention_tips || 'N/A'}</p>
                  </div>
                </div>
              )}

              {activeTab === 'decorate' && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <p className="text-sm text-gray-500">Cream Quantity</p>
                    <p className="text-xl font-bold">{result.cream_quantity_grams}g</p>
                  </div>
                  <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <p className="text-sm text-gray-500">Piping Style</p>
                    <p className="text-xl font-bold">{result.piping_style}</p>
                  </div>
                  <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <p className="text-sm text-gray-500">Difficulty</p>
                    <p className="text-xl font-bold">{result.difficulty_level}</p>
                  </div>
                  <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <p className="text-sm text-gray-500">Estimated Time</p>
                    <p className="text-xl font-bold">{result.estimated_time_hours}h</p>
                  </div>
                </div>
              )}

              {activeTab === 'optimize' && (
                <div className="p-4 bg-pink-50 dark:bg-pink-900/20 rounded-lg border-l-4 border-pink-500">
                  <p className="font-bold text-pink-600">Recommended Price: ₹{result.recommended_price}</p>
                  <p className="text-gray-700 dark:text-gray-300 mt-2">{result.competitive_analysis?.summary || 'Optimize your pricing based on market rates.'}</p>
                </div>
              )}

              {activeTab === 'image' && (
                <div className="text-center space-y-4">
                  <img 
                    src={result.image_url} 
                    alt="AI Generated Cake" 
                    className="w-full h-auto rounded-lg shadow-lg border border-gray-200 dark:border-gray-700"
                  />
                  <a href={result.image_url} target="_blank" rel="noreferrer" className="btn btn-outline w-full">
                    Open Full Image
                  </a>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AIFeaturesPage;
