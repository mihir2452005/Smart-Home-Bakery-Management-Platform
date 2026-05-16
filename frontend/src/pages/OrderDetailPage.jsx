import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useStore } from '../services/store';
import { orderAPI } from '../services/api';
import toast from 'react-hot-toast';
import { ArrowLeft, CheckCircle, Calculator, Save, Trash2 } from 'lucide-react';

const OrderDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useStore();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [estimationItems, setEstimationItems] = useState([]);
  const [isEstimating, setIsEstimating] = useState(false);

  useEffect(() => {
    fetchOrder();
  }, [id]);

  const fetchOrder = async () => {
    try {
      setLoading(true);
      const data = await orderAPI.getOrder(id);
      setOrder(data);
      if (data.items) {
        setEstimationItems(data.items.map(item => ({
          ingredient_id: item.ingredient_id,
          quantity_used: item.quantity_used
        })));
      }
    } catch (error) {
      toast.error('Failed to load order details');
    } finally {
      setLoading(false);
    }
  };

  const handleEstimate = async () => {
    try {
      setIsEstimating(true);
      const result = await orderAPI.estimateCost(id, { ingredients: estimationItems });
      toast.success('Cost estimated successfully!');
      fetchOrder();
    } catch (error) {
      toast.error(error?.message || 'Estimation failed');
    } finally {
      setIsEstimating(false);
    }
  };

  const handleFinalize = async () => {
    try {
      await orderAPI.finalizeOrder(id, {
        selling_price: order.selling_price,
        actual_cost: order.actual_cost,
        notes: 'Order completed successfully'
      });
      toast.success('Order finalized!');
      fetchOrder();
    } catch (error) {
      toast.error('Finalization failed');
    }
  };

  const handleCancel = async () => {
    if (!window.confirm('Are you sure you want to cancel this order?')) return;
    try {
      await orderAPI.cancelOrder(id);
      toast.success('Order cancelled');
      navigate('/orders');
    } catch (error) {
      toast.error('Cancellation failed');
    }
  };

  if (loading) return <div className="text-center py-8">Loading order details...</div>;
  if (!order) return <div className="text-center py-8">Order not found</div>;

  return (
    <div className="space-y-6 animate-fadeIn">
      <div className="flex items-center justify-between">
        <button onClick={() => navigate('/orders')} className="btn btn-outline flex items-center gap-2">
          <ArrowLeft size={18} /> Back to Orders
        </button>
        <div className="flex gap-3">
          <button onClick={handleCancel} className="btn btn-danger">Cancel Order</button>
          <button onClick={handleFinalize} className="btn btn-success flex items-center gap-2">
            <CheckCircle size={18} /> Finalize Order
          </button>
        </div>
      </div>

      <div className="grid grid-1 lg:grid-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <div className="card">
            <h3 className="font-bold text-lg mb-4">Customer Info</h3>
            <div className="space-y-3 text-gray-700 dark:text-gray-300">
              <p><strong>Name:</strong> {order.customer_name}</p>
              <p><strong>Phone:</strong> {order.customer_phone}</p>
              <p><strong>Email:</strong> {order.customer_email}</p>
              <p><strong>Delivery:</strong> {order.delivery_date}</p>
              <p><strong>Status:</strong> <span className={`badge ${order.status === 'completed' ? 'badge-success' : 'badge-warning'}`}>{order.status}</span></p>
            </div>
          </div>

          <div className="card">
            <h3 className="font-bold text-lg mb-4">Cake Details</h3>
            <div className="space-y-3 text-gray-700 dark:text-gray-300">
              <p><strong>Type:</strong> {order.cake_type}</p>
              <p><strong>Weight:</strong> {order.cake_weight}</p>
              <p><strong>Flavor:</strong> {order.flavor}</p>
              <p><strong>Theme:</strong> {order.theme}</p>
              <p><strong>Requirements:</strong> {order.special_requirements || 'None'}</p>
            </div>
          </div>
        </div>

        <div className="lg:col-span-2 space-y-6">
          <div className="card">
            <div className="flex justify-between items-center mb-6">
              <h3 className="font-bold text-lg">Cost Estimation</h3>
              <button onClick={handleEstimate} className="btn btn-primary flex items-center gap-2" disabled={isEstimating}>
                <Calculator size={18} /> {isEstimating ? 'Calculating...' : 'Recalculate Cost'}
              </button>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead>
                  <tr className="border-b border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400">
                    <th className="p-3">Ingredient</th>
                    <th className="p-3">Quantity</th>
                    <th className="p-3">Cost</th>
                  </tr>
                </thead>
                <tbody>
                  {order.items?.map((item, idx) => (
                    <tr key={idx} className="border-b border-gray-100 dark:border-gray-800">
                      <td className="p-3">{item.ingredient_name}</td>
                      <td className="p-3">
                        <input 
                          type="number" 
                          className="form-input w-24 p-1" 
                          value={item.quantity_used} 
                          onChange={(e) => {
                            const newItems = [...estimationItems];
                            newItems[idx].quantity_used = Number(e.target.value);
                            setEstimationItems(newItems);
                          }}
                        />
                      </td>
                      <td className="p-3">₹{item.cost}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <div>
                <p className="text-sm text-gray-500">Total Cost</p>
                <p className="text-xl font-bold">₹{order.actual_cost || 0}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Suggested Price</p>
                <p className="text-xl font-bold text-pink-500">₹{order.selling_price || 0}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Estimated Profit</p>
                <p className="text-xl font-bold text-green-600">₹{order.actual_profit || 0}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OrderDetailPage;
