"""
AI Services
Handles all AI integrations with OpenAI and Google Gemini
"""

import os
import json
import re
from flask import current_app
import openai
import google.generativeai as genai


class AIService:
    """Main AI Service for all AI operations"""
    
    def __init__(self):
        """Initialize AI service with API keys"""
        self.openai_api_key = current_app.config.get('OPENAI_API_KEY')
        self.gemini_api_key = current_app.config.get('GEMINI_API_KEY')
        
        # Set API keys
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
    
    def generate_recipe(self, cake_weight, flavor, budget, oven_type, servings, is_eggless):
        """
        Generate AI-powered cake recipe based on parameters
        
        Args:
            cake_weight: '500g', '1kg', '2kg', '3kg'
            flavor: Cake flavor (e.g., 'Chocolate', 'Vanilla')
            budget: Budget in INR
            oven_type: 'microwave', 'gas_oven', 'electric_oven'
            servings: Number of servings
            is_eggless: Boolean - whether to use eggless recipe
        
        Returns:
            Dictionary with recipe details
        """
        try:
            eggless_note = " Make it completely eggless." if is_eggless else ""
            
            prompt = f"""Generate a perfect home cake recipe with these specifications:
            - Cake Type: {flavor} Cake
            - Weight: {cake_weight}
            - Number of Servings: {servings}
            - Oven Type: {oven_type}
            - Budget: ₹{budget}
            {eggless_note}
            
            Please provide in JSON format:
            {{
                "name": "Recipe name",
                "ingredients": [
                    {{"name": "ingredient", "quantity": 100, "unit": "grams", "notes": "optional notes"}}
                ],
                "instructions": [
                    {{"step": 1, "instruction": "Step description", "duration_minutes": 5}}
                ],
                "baking_temp": 180,
                "baking_time": 35,
                "tin_size": "8 inch round",
                "cream_quantity": 250,
                "difficulty_level": "easy|medium|hard",
                "tips": ["tip1", "tip2"],
                "estimated_cost": 250
            }}"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert home baker. Provide accurate, practical recipes."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            recipe_text = response.choices[0].message.content
            recipe_data = self._parse_json_response(recipe_text)
            
            return {
                "success": True,
                "data": recipe_data,
                "ai_provider": "openai"
            }
        
        except Exception as e:
            print(f"Error generating recipe with OpenAI: {str(e)}")
            return self._generate_recipe_gemini(cake_weight, flavor, budget, oven_type, servings, is_eggless)
    
    def _generate_recipe_gemini(self, cake_weight, flavor, budget, oven_type, servings, is_eggless):
        """Fallback recipe generation using Gemini API"""
        try:
            eggless_note = " Make it completely eggless." if is_eggless else ""
            
            prompt = f"""Generate a perfect home cake recipe with these specifications:
            - Cake Type: {flavor} Cake
            - Weight: {cake_weight}
            - Number of Servings: {servings}
            - Oven Type: {oven_type}
            - Budget: ₹{budget}
            {eggless_note}
            
            Please provide in JSON format:
            {{
                "name": "Recipe name",
                "ingredients": [
                    {{"name": "ingredient", "quantity": 100, "unit": "grams"}}
                ],
                "instructions": [
                    {{"step": 1, "instruction": "Step description"}}
                ],
                "baking_temp": 180,
                "baking_time": 35,
                "tin_size": "8 inch round",
                "cream_quantity": 250,
                "difficulty_level": "easy",
                "estimated_cost": 250
            }}"""
            
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            recipe_data = self._parse_json_response(response.text)
            
            return {
                "success": True,
                "data": recipe_data,
                "ai_provider": "gemini"
            }
        
        except Exception as e:
            print(f"Error with both AI providers: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def generate_decoration_recommendations(self, cake_weight, base_style):
        """
        Generate AI decoration recommendations based on cake weight
        
        Args:
            cake_weight: '500g', '1kg', '2kg', '3kg'
            base_style: Base decoration style preference
        
        Returns:
            Decoration recommendations with quantities
        """
        try:
            prompt = f"""Provide decoration recommendations for a {cake_weight} {base_style} cake.
            
            Consider:
            - Cream needed in grams
            - Piping styles that work well
            - Drip design suggestions
            - Number of flowers/garnishes
            - Fondant usage recommendations
            - Estimated time for decoration
            - Difficulty level for beginners
            
            Respond in JSON format:
            {{
                "style_name": "Style name",
                "cream_quantity_grams": 250,
                "piping_style": "French piping",
                "drip_design": "White chocolate drip",
                "flower_quantity": 3,
                "fondant_usage": "Light dusting",
                "estimated_time_hours": 1.5,
                "difficulty_level": "easy|medium|hard",
                "step_by_step": ["step1", "step2"]
            }}"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert cake decorator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            decoration_data = self._parse_json_response(response.choices[0].message.content)
            return {"success": True, "data": decoration_data}
        
        except Exception as e:
            print(f"Error generating decoration recommendations: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def diagnose_baking_mistake(self, problem_description, cake_type):
        """
        AI diagnosis of baking problems
        
        Args:
            problem_description: Description of the issue
            cake_type: Type of cake that failed
        
        Returns:
            Solutions and prevention tips
        """
        try:
            prompt = f"""A baker made a {cake_type} cake and encountered this problem: "{problem_description}"
            
            Please provide:
            1. Root cause analysis
            2. 3-4 potential solutions
            3. Prevention tips for next time
            4. Quick recovery methods if possible
            
            Respond in JSON:
            {{
                "problem": "Identified problem",
                "likely_cause": "Root cause explanation",
                "solutions": ["solution1", "solution2", "solution3"],
                "prevention_tips": ["tip1", "tip2"],
                "recovery_options": ["Can be saved by...", "Can be used for..."],
                "confidence_level": "high|medium|low"
            }}"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert cake baker and troubleshooter."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1200
            )
            
            diagnosis = self._parse_json_response(response.choices[0].message.content)
            return {"success": True, "data": diagnosis}
        
        except Exception as e:
            print(f"Error diagnosing baking mistake: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def optimize_profit_margin(self, ingredient_costs, selling_price, cake_type, market_rate):
        """
        AI profit optimization recommendations
        
        Args:
            ingredient_costs: Total ingredient cost
            selling_price: Current selling price
            cake_type: Type of cake
            market_rate: Average market rate
        
        Returns:
            Profit optimization strategies
        """
        try:
            current_profit_margin = ((selling_price - ingredient_costs) / selling_price * 100) if selling_price > 0 else 0
            
            prompt = f"""Analyze this cake business scenario and suggest profit optimization:
            
            - Cake Type: {cake_type}
            - Ingredient Cost: ₹{ingredient_costs}
            - Current Selling Price: ₹{selling_price}
            - Profit Margin: {current_profit_margin:.2f}%
            - Market Average Rate: ₹{market_rate}
            
            Provide suggestions in JSON:
            {{
                "current_margin": {current_profit_margin},
                "margin_status": "good|average|poor",
                "recommended_price": 350,
                "cost_reduction_strategies": ["Use bulk buying", "Substitute ingredients"],
                "premium_pricing_options": ["Add premium packaging", "Create special variants"],
                "estimated_monthly_profit": 5000,
                "bulk_buying_savings": 200,
                "alternative_ingredients": {{"ingredient": "substitute", "savings": "₹50"}}
            }}"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a bakery business consultant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            optimization = self._parse_json_response(response.choices[0].message.content)
            return {"success": True, "data": optimization}
        
        except Exception as e:
            print(f"Error optimizing profit: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def suggest_cakes_from_ingredients(self, available_ingredients, budget):
        """
        Suggest possible cakes based on available ingredients
        
        Args:
            available_ingredients: List of available ingredients
            budget: Budget in INR
        
        Returns:
            List of suggested cakes
        """
        try:
            ingredients_str = ", ".join(available_ingredients)
            
            prompt = f"""Based on these available ingredients: {ingredients_str}
            And budget of ₹{budget}
            
            Suggest 5 possible cakes that can be made:
            
            {{
                "suggestions": [
                    {{
                        "cake_name": "Name",
                        "flavor": "Flavor",
                        "difficulty": "easy|medium|hard",
                        "estimated_cost": 150,
                        "missing_ingredients": ["item1"],
                        "why_recommended": "Reason"
                    }}
                ]
            }}"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a creative baker."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=1500
            )
            
            suggestions = self._parse_json_response(response.choices[0].message.content)
            return {"success": True, "data": suggestions}
        
        except Exception as e:
            print(f"Error suggesting cakes: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def generate_cake_image(self, cake_description):
        """
        Generate AI cake design preview images
        
        Args:
            cake_description: Description of desired cake
        
        Returns:
            Image URL
        """
        try:
            # Enhance the prompt for better images
            enhanced_prompt = f"Professional bakery-quality photograph of: {cake_description}, beautiful lighting, studio setting, high resolution, 4k"
            
            response = openai.Image.create(
                prompt=enhanced_prompt,
                n=1,
                size="1024x1024",
                quality="hd"
            )
            
            image_url = response.data[0].url
            return {"success": True, "image_url": image_url, "ai_provider": "openai"}
        
        except Exception as e:
            print(f"Error generating image: {str(e)}")
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def _parse_json_response(response_text):
        """
        Parse JSON from AI response text
        Handles cases where JSON is wrapped in markdown code blocks
        """
        try:
            # Try direct JSON parsing first
            return json.loads(response_text)
        except json.JSONDecodeError:
            try:
                # Try to extract JSON from markdown code blocks
                json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group(1))
                
                # Try to find JSON object in response
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                if start_idx != -1 and end_idx > start_idx:
                    return json.loads(response_text[start_idx:end_idx])
            
            except (json.JSONDecodeError, AttributeError):
                pass
            
            # Return error response
            return {"error": "Failed to parse AI response", "raw_response": response_text}


class CalculationService:
    """Service for all cost calculations"""
    
    @staticmethod
    def calculate_ingredient_cost(used_quantity, total_quantity, total_price):
        """
        Calculate cost of used ingredient
        Formula: (Used Quantity / Total Quantity) × Total Price
        """
        if total_quantity == 0:
            return 0
        return (used_quantity / total_quantity) * total_price
    
    @staticmethod
    def calculate_total_cake_cost(ingredients_costs):
        """Calculate total cake cost from all ingredients"""
        return sum(ingredients_costs)
    
    @staticmethod
    def calculate_cost_per_slice(total_cost, servings):
        """Calculate cost per slice"""
        if servings == 0:
            return 0
        return total_cost / servings
    
    @staticmethod
    def calculate_profit_margin(total_cost, selling_price):
        """Calculate profit margin percentage"""
        if selling_price == 0:
            return 0
        return ((selling_price - total_cost) / selling_price) * 100
    
    @staticmethod
    def suggest_selling_price(total_cost, market_rate, desired_margin=40):
        """
        Suggest selling price based on cost and market rate
        
        Args:
            total_cost: Total ingredient cost
            market_rate: Average market rate
            desired_margin: Desired profit margin (default 40%)
        
        Returns:
            Suggested selling price
        """
        # Calculate price for desired margin
        price_for_margin = total_cost / (1 - desired_margin / 100)
        
        # Compare with market rate
        if price_for_margin > market_rate:
            # If our desired price is higher than market, use market rate
            # But ensure minimum margin
            if total_cost > 0:
                actual_margin = ((market_rate - total_cost) / market_rate) * 100
                if actual_margin < 20:  # Minimum 20% margin
                    return total_cost * 1.3  # 30% margin
            return market_rate
        
        return price_for_margin
