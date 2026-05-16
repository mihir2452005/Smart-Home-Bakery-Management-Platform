import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useStore } from '../services/store';
import { recipeAPI } from '../services/api';

const RecipeGeneratorPage = () => {
  const navigate = useNavigate();
  const { user } = useStore();
  const [flavor, setFlavor] = useState('Chocolate');
  const [cakeWeight, setCakeWeight] = useState('1kg');
  const [budget, setBudget] = useState('500');
  const [ovenType, setOvenType] = useState('gas_oven');
  const [servings, setServings] = useState('8');
  const [isEggless, setIsEggless] = useState(true);
  const [loading, setLoading] = useState(false);
  const [recipe, setRecipe] = useState(null);

  const handleGenerate = async (event) => {
    event.preventDefault();

    if (!user?.id) {
      toast.error('Please log in to generate recipes');
      navigate('/login');
      return;
    }

    if (!flavor || !budget) {
      toast.error('Please fill in the flavor and budget fields');
      return;
    }

    setLoading(true);
    try {
      const response = await recipeAPI.generateRecipe({
        user_id: user.id,
        cake_weight: cakeWeight,
        flavor,
        budget: Number(budget),
        oven_type: ovenType,
        servings: Number(servings),
        is_eggless: isEggless,
      });

      const generated = response?.data || response;
      setRecipe(generated);
      toast.success('Recipe generated successfully');
    } catch (error) {
      toast.error(error?.message || 'Failed to generate recipe');
    } finally {
      setLoading(false);
    }
  };

  const recipeName = recipe?.name || recipe?.recipe_name || `${flavor} Cake`;
  const ingredients = recipe?.ingredients || recipe?.data?.ingredients || [];
  const instructions = recipe?.instructions || recipe?.data?.instructions || [];
  const bakingTemp = recipe?.baking_temp || recipe?.data?.baking_temp;
  const bakingTime = recipe?.baking_time || recipe?.data?.baking_time;
  const estimatedCost = recipe?.estimated_cost || recipe?.data?.estimated_cost;

  return (
    <div className="space-y-6 animate-fadeIn">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">AI Recipe Generator</h1>
        <p className="text-gray-600 dark:text-gray-400">Generate eggless cake recipes optimized for cost, flavor, and serving size.</p>
      </div>

      <div className="card">
        <form className="grid grid-cols-1 md:grid-cols-2 gap-4" onSubmit={handleGenerate}>
          <div>
            <label className="form-label" htmlFor="flavor">
              Cake Flavor
            </label>
            <input
              id="flavor"
              type="text"
              value={flavor}
              onChange={(e) => setFlavor(e.target.value)}
              className="form-input"
              placeholder="Chocolate, Vanilla, Red Velvet"
            />
          </div>

          <div>
            <label className="form-label" htmlFor="cakeWeight">
              Cake Weight
            </label>
            <select
              id="cakeWeight"
              value={cakeWeight}
              onChange={(e) => setCakeWeight(e.target.value)}
              className="form-select"
            >
              <option value="500g">500g</option>
              <option value="1kg">1kg</option>
              <option value="2kg">2kg</option>
              <option value="3kg">3kg</option>
            </select>
          </div>

          <div>
            <label className="form-label" htmlFor="budget">
              Budget (INR)
            </label>
            <input
              id="budget"
              type="number"
              min="0"
              value={budget}
              onChange={(e) => setBudget(e.target.value)}
              className="form-input"
              placeholder="500"
            />
          </div>

          <div>
            <label className="form-label" htmlFor="ovenType">
              Oven Type
            </label>
            <select
              id="ovenType"
              value={ovenType}
              onChange={(e) => setOvenType(e.target.value)}
              className="form-select"
            >
              <option value="gas_oven">Gas Oven</option>
              <option value="electric_oven">Electric Oven</option>
              <option value="microwave">Microwave</option>
            </select>
          </div>

          <div>
            <label className="form-label" htmlFor="servings">
              Servings
            </label>
            <input
              id="servings"
              type="number"
              min="1"
              value={servings}
              onChange={(e) => setServings(e.target.value)}
              className="form-input"
              placeholder="8"
            />
          </div>

          <div className="flex items-center gap-3 mt-6">
            <input
              id="eggless"
              type="checkbox"
              checked={isEggless}
              onChange={(e) => setIsEggless(e.target.checked)}
              className="h-5 w-5 text-pink-500 rounded"
            />
            <label htmlFor="eggless" className="font-medium text-gray-700 dark:text-gray-200">
              Eggless recipe
            </label>
          </div>

          <div className="md:col-span-2">
            <button type="submit" className="btn btn-primary w-full" disabled={loading}>
              {loading ? 'Generating...' : 'Generate Recipe'}
            </button>
          </div>
        </form>
      </div>

      {recipe && (
        <div className="card space-y-4">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <h2 className="text-2xl font-bold">{recipeName}</h2>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {cakeWeight} · {servings} servings · {isEggless ? 'Eggless' : 'With eggs'}
              </p>
            </div>
            <div className="space-y-1 text-right">
              {estimatedCost && <p className="font-semibold">Estimated cost: ₹{estimatedCost}</p>}
              {bakingTemp && <p>Temp: {bakingTemp}°C</p>}
              {bakingTime && <p>Time: {bakingTime} mins</p>}
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-semibold mb-3">Ingredients</h3>
              {ingredients.length > 0 ? (
                <ul className="list-disc list-inside space-y-2 text-gray-700 dark:text-gray-300">
                  {ingredients.map((item, index) => (
                    <li key={`${item.name || index}-${index}`}>{item.name ? `${item.name} - ${item.quantity || item.qty || ''}` : item}</li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-600 dark:text-gray-400">Ingredients list will appear here.</p>
              )}
            </div>
            <div>
              <h3 className="font-semibold mb-3">Instructions</h3>
              {instructions.length > 0 ? (
                <ol className="list-decimal list-inside space-y-2 text-gray-700 dark:text-gray-300">
                  {instructions.map((step, index) => (
                    <li key={`${index}-${step}`}>{step}</li>
                  ))}
                </ol>
              ) : (
                <p className="text-gray-600 dark:text-gray-400">Step-by-step instructions will appear here.</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default RecipeGeneratorPage;
