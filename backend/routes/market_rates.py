"""
Market Rates Routes
Bakery pricing and market analysis
"""

from flask import Blueprint, request
from datetime import date
from models.database import db, BakeryMarketRate, DecorationReference
from services.scraping_service import ScrapingService
from utils.helpers import api_response, require_json, validate_inputs, Helpers

market_rates_bp = Blueprint('market_rates', __name__)


@market_rates_bp.route('/scrape', methods=['POST'])
@require_json
@validate_inputs(['user_id', 'location'])
def scrape_market_rates():
    """
    Scrape nearby bakery rates
    
    Required fields:
    - user_id: User ID
    - location: Location to scrape
    """
    data = request.get_json()
    user_id = data['user_id']
    location = data['location']
    
    try:
        scraping_service = ScrapingService()
        cake_types = data.get('cake_types', ['Chocolate', 'Truffle', 'Designer', 'Fondant', 'Eggless'])
        
        # Scrape rates
        scraped_rates = scraping_service.scrape_nearby_bakery_rates(location, cake_types)
        
        # Store in database
        for rate in scraped_rates:
            market_rate = BakeryMarketRate(
                user_id=user_id,
                location=rate['location'],
                bakery_name=rate['bakery_name'],
                bakery_url=rate.get('bakery_url'),
                cake_type=rate['cake_type'],
                weight=rate.get('weight'),
                price=rate['price'],
                currency=rate.get('currency', 'INR'),
                last_updated=date.today()
            )
            db.session.add(market_rate)
        
        db.session.commit()
        
        return api_response(
            status="success",
            message=f"Scraped {len(scraped_rates)} market rates!",
            data={
                "rates_scraped": len(scraped_rates),
                "location": location,
                "rates": scraped_rates
            },
            code=201
        )
    
    except Exception as e:
        db.session.rollback()
        return api_response(
            status="error",
            message=f"Scraping failed: {str(e)}",
            code=500
        )


@market_rates_bp.route('/<int:user_id>', methods=['GET'])
def get_market_rates(user_id):
    """Get market rates for user"""
    page = request.args.get('page', 1, type=int)
    location = request.args.get('location', '')
    cake_type = request.args.get('cake_type', '')
    
    query = BakeryMarketRate.query.filter_by(user_id=user_id)
    
    if location:
        query = query.filter_by(location=location)
    
    if cake_type:
        query = query.filter_by(cake_type=cake_type)
    
    query = query.order_by(BakeryMarketRate.last_updated.desc())
    items, total_count, total_pages = Helpers.paginate_query(query, page)
    
    rates_data = [{
        "id": rate.id,
        "bakery_name": rate.bakery_name,
        "location": rate.location,
        "cake_type": rate.cake_type,
        "weight": rate.weight,
        "price": rate.price,
        "currency": rate.currency,
        "last_updated": rate.last_updated.isoformat() if rate.last_updated else None
    } for rate in items]
    
    pagination_data = Helpers.generate_pagination_data(
        rates_data, total_count, total_pages, page
    )
    
    return api_response(
        status="success",
        data=pagination_data
    )


@market_rates_bp.route('/analyze/<int:user_id>', methods=['POST'])
@require_json
@validate_inputs(['cake_type', 'weight', 'user_cake_cost'])
def analyze_market_rates(user_id):
    """
    Analyze market rates and provide competitive insights
    
    Required fields:
    - cake_type: Type of cake
    - weight: Weight of cake
    - user_cake_cost: User's cake cost
    """
    data = request.get_json()
    location = data.get('location', 'default')
    
    # Get market rates
    rates = BakeryMarketRate.query.filter(
        BakeryMarketRate.user_id == user_id,
        BakeryMarketRate.cake_type == data['cake_type'],
        BakeryMarketRate.weight == data['weight']
    ).all()
    
    if not rates:
        return api_response(
            status="error",
            message="No market data found. Try scraping first.",
            code=404
        )
    
    # Convert to list for analysis
    rates_list = [{
        'cake_type': rate.cake_type,
        'weight': rate.weight,
        'price': rate.price,
        'bakery_name': rate.bakery_name
    } for rate in rates]
    
    scraping_service = ScrapingService()
    analysis = scraping_service.calculate_market_analysis(
        bakery_rates=rates_list,
        user_cake_cost=data['user_cake_cost'],
        cake_type=data['cake_type'],
        weight=data['weight']
    )
    
    return api_response(
        status="success",
        data=analysis
    )


@market_rates_bp.route('/locations/<int:user_id>', methods=['GET'])
def get_unique_locations(user_id):
    """Get unique locations with market data"""
    locations = db.session.query(BakeryMarketRate.location).filter_by(
        user_id=user_id
    ).distinct().all()
    
    locations_data = [loc[0] for loc in locations]
    
    return api_response(
        status="success",
        data={"locations": locations_data}
    )


@market_rates_bp.route('/decoration-refs/<int:user_id>', methods=['GET'])
def get_decoration_references(user_id):
    """Get decoration references"""
    page = request.args.get('page', 1, type=int)
    cake_weight = request.args.get('cake_weight', '')
    style = request.args.get('style', '')
    
    query = DecorationReference.query.filter_by(user_id=user_id)
    
    if cake_weight:
        query = query.filter_by(cake_weight=cake_weight)
    
    if style:
        query = query.filter(DecorationReference.style.ilike(f'%{style}%'))
    
    items, total_count, total_pages = Helpers.paginate_query(query, page)
    
    refs_data = [{
        "id": ref.id,
        "cake_weight": ref.cake_weight,
        "style": ref.style,
        "image_url": ref.image_url,
        "source": ref.source,
        "cream_quantity": ref.cream_quantity_grams,
        "piping_style": ref.piping_style,
        "difficulty_level": ref.difficulty_level,
        "estimated_time_hours": ref.estimated_time_hours
    } for ref in items]
    
    pagination_data = Helpers.generate_pagination_data(
        refs_data, total_count, total_pages, page
    )
    
    return api_response(
        status="success",
        data=pagination_data
    )


@market_rates_bp.route('/decoration-refs', methods=['POST'])
@require_json
@validate_inputs(['user_id', 'cake_weight', 'style'])
def add_decoration_reference():
    """Add custom decoration reference"""
    data = request.get_json()
    
    try:
        reference = DecorationReference(
            user_id=data['user_id'],
            cake_weight=data['cake_weight'],
            style=data['style'],
            image_url=data.get('image_url'),
            source=data.get('source', 'custom'),
            cream_quantity_grams=data.get('cream_quantity_grams'),
            piping_style=data.get('piping_style'),
            drip_design=data.get('drip_design'),
            flower_quantity=data.get('flower_quantity'),
            fondant_usage=data.get('fondant_usage'),
            difficulty_level=data.get('difficulty_level'),
            estimated_time_hours=data.get('estimated_time_hours'),
            description=data.get('description')
        )
        
        db.session.add(reference)
        db.session.commit()
        
        return api_response(
            status="success",
            message="Reference added!",
            data={"reference_id": reference.id},
            code=201
        )
    
    except Exception as e:
        db.session.rollback()
        return api_response(
            status="error",
            message=f"Failed to add reference: {str(e)}",
            code=500
        )
