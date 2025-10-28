from flask import Flask, render_template, jsonify, request
import requests
from flask_cors import CORS
import os
import math
import json

app = Flask(__name__)
CORS(app)

# Custom JSON encoder to handle NaN values
class SafeJSONEncoder(json.JSONEncoder):
    def encode(self, o):
        if isinstance(o, float):
            if math.isnan(o) or math.isinf(o):
                return 'null'
        return super().encode(o)
    
    def iterencode(self, o, _one_shot=False):
        for chunk in super().iterencode(o, _one_shot):
            yield chunk

app.json_encoder = SafeJSONEncoder

# API Configuration
API_BASE_URL = "https://www.microburbs.com.au/report_generator/api"
API_TOKEN = "test"

# Demo suburbs that work with the sandbox token
# Note: The sandbox token is limited and only works with "Belmont North"
DEMO_SUBURBS = [
    "Belmont North"
]

@app.route('/')
def index():
    """Render the main dashboard page"""
    return render_template('index.html')

@app.route('/api/demo-suburbs', methods=['GET'])
def get_demo_suburbs():
    """Return list of demo suburbs that work with sandbox token"""
    return jsonify({
        'success': True,
        'suburbs': DEMO_SUBURBS
    })

@app.route('/api/properties', methods=['GET'])
def get_properties():
    """
    Fetch properties from MicroBurbs API
    Query params:
    - suburb: The suburb name to search (required)
    - property_type: Filter by property type (optional)
    """
    try:
        suburb = request.args.get('suburb')
        property_type = request.args.get('property_type', '')
        
        if not suburb:
            return jsonify({'error': 'Suburb parameter is required'}), 400
        
        # Build API request
        params = {'suburb': suburb}
        if property_type:
            params['property_type'] = property_type
        
        headers = {
            'Authorization': f'Bearer {API_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        # Make request to MicroBurbs API
        response = requests.get(
            f'{API_BASE_URL}/suburb/properties',
            params=params,
            headers=headers,
            timeout=30
        )
        
        # Handle response
        if response.status_code == 200:
            data = response.json()
            
            # Extract results array if data is wrapped
            properties = data
            if isinstance(data, dict) and 'results' in data:
                properties = data['results']
            
            # Clean NaN values from properties
            properties = clean_nan_values(properties)
            
            # Calculate statistics
            stats = calculate_statistics(properties)
            
            # Clean statistics as well
            stats = clean_nan_values(stats)
            
            return jsonify({
                'success': True,
                'data': properties,
                'statistics': stats,
                'suburb': suburb
            })
        elif response.status_code == 401:
            # Unauthorized - sandbox token issue
            error_message = "This demo uses a sandbox token that only works with specific suburbs."
            try:
                error_data = response.json()
                if 'error' in error_data:
                    error_message = error_data['error']
            except:
                pass
            
            return jsonify({
                'success': False,
                'error': 'Unauthorized',
                'message': error_message,
                'demo_suburbs': DEMO_SUBURBS,
                'hint': f'Try one of these demo suburbs: {", ".join(DEMO_SUBURBS)}'
            }), 401
        else:
            return jsonify({
                'success': False,
                'error': f'API returned status code {response.status_code}',
                'message': response.text
            }), response.status_code
            
    except requests.exceptions.Timeout:
        return jsonify({
            'success': False,
            'error': 'Request timeout',
            'message': 'The API request took too long to respond'
        }), 504
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'error': 'API request failed',
            'message': str(e)
        }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Server error',
            'message': str(e)
        }), 500

def clean_nan_values(obj):
    """Recursively clean NaN and Inf values from objects"""
    if isinstance(obj, dict):
        return {k: clean_nan_values(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nan_values(item) for item in obj]
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    return obj

def calculate_statistics(properties):
    """Calculate statistics from property data"""
    if not properties or not isinstance(properties, list):
        return {
            'total': 0,
            'average_price': 0,
            'average_bedrooms': 0,
            'min_price': 0,
            'max_price': 0,
            'property_types': {}
        }
    
    # Handle the case where properties is wrapped in a 'results' key
    if isinstance(properties, dict) and 'results' in properties:
        properties = properties['results']
    
    total = len(properties)
    prices = []
    bedrooms = []
    property_types = {}
    
    for prop in properties:
        # Extract price
        price = extract_price(prop)
        if price and price > 0:
            prices.append(price)
        
        # Extract bedrooms
        beds = extract_bedrooms(prop)
        if beds and beds > 0:
            bedrooms.append(beds)
        
        # Count property types
        prop_type = extract_property_type(prop)
        if prop_type:
            property_types[prop_type] = property_types.get(prop_type, 0) + 1
    
    # Calculate statistics with safety checks
    avg_price = 0
    if prices:
        avg_price = round(sum(prices) / len(prices))
    
    avg_bedrooms = 0.0
    if bedrooms:
        avg_bedrooms = round(sum(bedrooms) / len(bedrooms), 1)
    
    stats = {
        'total': total,
        'average_price': avg_price,
        'average_bedrooms': avg_bedrooms,
        'min_price': min(prices) if prices else 0,
        'max_price': max(prices) if prices else 0,
        'property_types': property_types
    }
    
    return stats

def extract_price(property_data):
    """Extract price from property data"""
    try:
        # Try different possible price fields
        price_fields = ['price', 'listing_price', 'sale_price', 'asking_price']
        for field in price_fields:
            if field in property_data and property_data[field] is not None:
                price = property_data[field]
                # Check for NaN or invalid values
                if isinstance(price, float):
                    if math.isnan(price) or math.isinf(price) or price <= 0:
                        continue
                    return int(price)
                elif isinstance(price, int) and price > 0:
                    return int(price)
                elif isinstance(price, str):
                    # Remove $ and commas, convert to number
                    clean_price = price.replace('$', '').replace(',', '').strip()
                    if clean_price.replace('.', '').isdigit():
                        return int(float(clean_price))
        return None
    except Exception as e:
        print(f"Error extracting price: {e}")
        return None

def extract_bedrooms(property_data):
    """Extract bedroom count from property data"""
    try:
        # Check attributes first (nested structure from API)
        if 'attributes' in property_data and isinstance(property_data['attributes'], dict):
            attrs = property_data['attributes']
            if 'bedrooms' in attrs and attrs['bedrooms'] is not None:
                beds = attrs['bedrooms']
                # Check for NaN using math.isnan
                if isinstance(beds, float):
                    if not math.isnan(beds) and not math.isinf(beds) and beds > 0:
                        return int(beds)
                elif isinstance(beds, int) and beds > 0:
                    return beds
        
        # Fallback to direct fields
        bedroom_fields = ['bedrooms', 'beds', 'bedroom_count', 'bed']
        for field in bedroom_fields:
            if field in property_data and property_data[field] is not None:
                beds = property_data[field]
                if isinstance(beds, float):
                    if not math.isnan(beds) and not math.isinf(beds) and beds > 0:
                        return int(beds)
                elif isinstance(beds, int) and beds > 0:
                    return beds
                elif isinstance(beds, str) and beds.isdigit():
                    return int(beds)
        return None
    except Exception as e:
        print(f"Error extracting bedrooms: {e}")
        return None

def extract_property_type(property_data):
    """Extract property type from property data"""
    try:
        type_fields = ['property_type', 'type', 'category', 'dwelling_type']
        for field in type_fields:
            if field in property_data and property_data[field]:
                return str(property_data[field]).lower()
        return 'unknown'
    except:
        return 'unknown'

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
