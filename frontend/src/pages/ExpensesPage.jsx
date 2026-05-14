import { useState, useEffect } from 'react';
import { useStore } from '../services/store';
import { expenseAPI } from '../services/api';
import toast from 'react-hot-toast';
import { Plus, Trash2, Wallet, CreditCard } from 'lucide-react';

const ExpensesPage = () => {
  const { user } = useStore();
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [newExpense, setNewExpense] = useState({
    category: 'ingredients',
    amount: '',
    description: '',
    expense_date: new Date().toISOString().split('T')[0],
    payment_method: 'cash'
  });

  useEffect(() => {
    fetchExpenses();
  }, [user?.id]);

  const fetchExpenses = async () => {
    if (!user?.id) return;
    setLoading(true);
    try {
      const response = await expenseAPI.getExpenses(user.id);
      setExpenses(response?.items || []);
    } catch (error) {
      toast.error('Failed to load expenses');
    } finally {
      setLoading(false);
    }
  };

  const handleAddExpense = async (e) => {
    e.preventDefault();
    try {
      await expenseAPI.addExpense({
        ...newExpense,
        user_id: user.id,
        amount: Number(newExpense.amount)
      });
      toast.success('Expense added!');
      setShowAddModal(false);
      setNewExpense({
        category: 'ingredients',
        amount: '',
        description: '',
        expense_date: new Date().toISOString().split('T')[0],
        payment_method: 'cash'
      });
      fetchExpenses();
    } catch (error) {
      toast.error(error?.message || 'Failed to add expense');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this expense?')) return;
    try {
      await expenseAPI.deleteExpense(id);
      toast.success('Expense deleted');
      fetchExpenses();
    } catch (error) {
      toast.error('Failed to delete expense');
    }
  };

  if (loading) return <div className="text-center py-8">Loading expenses...</div>;

  return (
    <div className="space-y-6 animate-fadeIn">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Expense Tracking</h1>
          <p className="text-gray-600 dark:text-gray-400">Manage your bakery's operational costs</p>
        </div>
        <button 
          onClick={() => setShowAddModal(true)} 
          className="btn btn-primary flex items-center gap-2"
        >
          <Plus size={20} /> Add Expense
        </button>
      </div>

      <div className="grid grid-1 lg:grid-3 gap-6">
        <div className="lg:col-span-2 card overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400">
                <th className="p-4 font-semibold">Date</th>
                <th className="p-4 font-semibold">Category</th>
                <th className="p-4 font-semibold">Description</th>
                <th className="p-4 font-semibold">Amount</th>
                <th className="p-4 font-semibold">Action</th>
              </tr>
            </thead>
            <tbody>
              {expenses.length > 0 ? expenses.map((exp) => (
                <tr key={exp.id} className="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                  <td className="p-4 text-sm">{exp.expense_date}</td>
                  <td className="p-4">
                    <span className="badge badge-primary">{exp.category}</span>
                  </td}
                  <td className="p-4 text-gray-600 dark:text-gray-400">{exp.description}</td>
                  <td className="p-4 font-bold text-red-500">₹{exp.amount}</td>
                  <td className="p-4">
                    <button onClick={() => handleDelete(exp.id)} className="text-red-500 hover:text-red-700 p-1">
                      <Trash2 size={18} />
                    </button>
                  </td>
                </tr>
              )) : (
                <tr>
                  <td colSpan="5" className="p-8 text-center text-gray-500">No expenses recorded yet.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        <div className="card">
          <h3 className="font-bold text-lg mb-4 flex items-center gap-2">
            <Wallet size={20} className="text-pink-500" /> Summary
          </h3>
          <div className="space-y-4">
            <div className="p-4 bg-red-50 dark:bg-red-900/20 rounded-lg">
              <p className="text-sm text-red-500">Total Expenses</p>
              <p className="text-2xl font-bold text-red-600">
                ₹{expenses.reduce((acc, curr) => acc + curr.amount, 0).toFixed(2)}
              </p>
            </div>
            <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <p className="text-sm text-gray-500">Total Records</p>
              <p className="text-2xl font-bold">{expenses.length}</p>
            </div>
          </div>
        </div>
      </div>

      {showAddModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="card w-full max-w-md animate-fadeIn">
            <h2 className="text-2xl font-bold mb-6">Add New Expense</h2>
            <form onSubmit={handleAddExpense} className="space-y-4">
              <div>
                <label className="form-label">Category</label>
                <select 
                  className="form-select" 
                  value={newExpense.category} 
                  onChange={e => setNewExpense({...newExpense, category: e.target.value})}
                >
                  <option value="ingredients">Ingredients</option>
                  <option value="equipment">Equipment</option>
                  <option value="packaging">Packaging</option>
                  <option value="utilities">Utilities</option>
                  <option value="marketing">Marketing</option>
                  <option value="other">Other</option>
                </select>
              </div>
              <div>
                <label className="form-label">Amount (₹)</label>
                <input 
                  type="number" 
                  className="form-input" 
                  value={newExpense.amount} 
                  onChange={e => setNewExpense({...newExpense, amount: e.target.value})} 
                  required 
                />
              </div>
              <div>
                <label className="form-label">Description</label>
                <input 
                  type="text" 
                  className="form-input" 
                  value={newExpense.description} 
                  onChange={e => setNewExpense({...newExpense, description: e.target.value})} 
                />
              </div>
              <div>
                <label className="form-label">Date</label>
                <input 
                  type="date" 
                  className="form-input" 
                  value={newExpense.expense_date} 
                  onChange={e => setNewExpense({...newExpense, expense_date: e.target.value})} 
                  required 
                />
              </div>
              <div>
                <label className="form-label">Payment Method</label>
                <select 
                  className="form-select" 
                  value={newExpense.payment_method} 
                  onChange={e => setNewExpense({...newExpense, payment_method: e.target.value})}
                >
                  <option value="cash">Cash</option>
                  <option value="card">Card</option>
                  <option value="upi">UPI</option>
                </select>
              </div>
              <div className="flex gap-3 mt-6">
                <button type="submit" className="btn btn-primary flex-1">Save Expense</button>
                <button type="button" onClick={() => setShowAddModal(false)} className="btn btn-outline flex-1">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default ExpensesPage;
