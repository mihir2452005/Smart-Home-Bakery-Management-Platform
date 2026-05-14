import { useState, useEffect } from 'react';
import { useStore } from '../services/store';
import { authAPI } from '../services/api';
import toast from 'react-hot-toast';
import { User, Bell, Moon, Globe, CreditCard, Save } from 'lucide-react';

const SettingsPage = () => {
  const { user, preferences, setPreferences } = useStore();
  const [loading, setLoading] = useState(false);
  const [settings, setSettings] = useState({
    theme: 'light',
    language: 'en',
    currency: 'INR',
    notification_email: true,
    notification_sms: false,
    auto_low_stock_alert: true,
    weekly_profit_report: true,
    preferred_ai_provider: 'openai'
  });

  useEffect(() => {
    if (preferences && Object.keys(preferences).length > 0) {
      setSettings(preferences);
    }
  }, [preferences]);

  const handleSave = async () => {
    if (!user?.id) return;
    setLoading(true);
    try {
      const response = await authAPI.updatePreferences(user.id, settings);
      setPreferences(response?.data || response);
      toast.success('Preferences updated successfully!');
    } catch (error) {
      toast.error('Failed to update preferences');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Settings</h1>
        <button onClick={handleSave} className="btn btn-primary flex items-center gap-2" disabled={loading}>
          <Save size={18} /> {loading ? 'Saving...' : 'Save Changes'}
        </button>
      </div>

      <div className="grid grid-1 lg:grid-2 gap-6">
        <div className="card space-y-6">
          <h3 className="font-bold text-lg flex items-center gap-2 border-b pb-2">
            <User size={20} className="text-pink-500" /> Account Preferences
          </h3>
          
          <div className="space-y-4">
            <div className="form-group">
              <label className="form-label">Preferred Currency</label>
              <select 
                className="form-select" 
                value={settings.currency} 
                onChange={e => setSettings({...settings, currency: e.target.value})}
              >
                <option value="INR">INR (₹)</option>
                <option value="USD">USD ($)</option>
                <option value="EUR">EUR (€)</option>
                <option value="GBP">GBP (£)</option>
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Language</label>
              <select 
                className="form-select" 
                value={settings.language} 
                onChange={e => setSettings({...settings, language: e.target.value})}
              >
                <option value="en">English</option>
                <option value="hi">Hindi</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">AI Provider</label>
              <select 
                className="form-select" 
                value={settings.preferred_ai_provider} 
                onChange={e => setSettings({...settings, preferred_ai_provider: e.target.value})}
              >
                <option value="openai">OpenAI (GPT-4)</option>
                <option value="gemini">Google Gemini</option>
              </select>
            </div>
          </div>
        </div>

        <div className="card space-y-6">
          <h3 className="font-bold text-lg flex items-center gap-2 border-b pb-2">
            <Bell size={20} className="text-pink-500" /> Notifications & Alerts
          </h3>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-pink-100 dark:bg-pink-900/30 rounded-full text-pink-500">
                  <Bell size={18} />
                </div>
                <div>
                  <p className="font-medium">Email Notifications</p>
                  <p className="text-xs text-gray-500">Receive important alerts via email</p>
                </div>
              </div>
              <input 
                type="checkbox" 
                className="h-5 w-5 accent-pink-500" 
                checked={settings.notification_email} 
                onChange={e => setSettings({...settings, notification_email: e.target.checked})}
              />
            </div>

            <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-yellow-100 dark:bg-yellow-900/30 rounded-full text-yellow-500">
                  <AlertCircle size={18} />
                </div>
                <div>
                  <p className="font-medium">Low Stock Alerts</p>
                  <p className="text-xs text-gray-500">Notify when ingredients are low</p>
                </div>
              </div>
              <input 
                type="checkbox" 
                className="h-5 w-5 accent-pink-500" 
                checked={settings.auto_low_stock_alert} 
                onChange={e => setSettings({...settings, auto_low_stock_alert: e.target.checked})}
              />
            </div>

            <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-green-100 dark:bg-green-900/30 rounded-full text-green-500">
                  <TrendingUp size={18} />
                </div>
                <div>
                  <p className="font-medium">Weekly Profit Report</p>
                  <p className="text-xs text-gray-500">Get a summary of your weekly earnings</p>
                </div>
              </div>
              <input 
                type="checkbox" 
                className="h-5 w-5 accent-pink-500" 
                checked={settings.weekly_profit_report} 
                onChange={e => setSettings({...settings, weekly_profit_report: e.target.checked})}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;
