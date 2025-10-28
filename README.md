# MicroBurbs Property Dashboard

A modern, responsive web application that integrates with the MicroBurbs API to display property listings across Australian suburbs. Built with Python Flask backend and vanilla JavaScript frontend.

## Features

✨ **Modern UI/UX Design**
- Clean, responsive interface with gradient backgrounds
- Smooth animations and transitions
- Mobile-friendly responsive design

📊 **Real-time Data Integration**
- Fetches live property data from MicroBurbs API
- Displays comprehensive property statistics
- Dynamic data visualization

🔍 **Advanced Filtering & Sorting**
- Filter properties by type (Houses, Apartments, Units)
- Sort by price, bedrooms, and more
- Quick search for popular suburbs

📱 **Interactive Features**
- Detailed property modal views
- Property cards with key information
- Quick suburb search chips
- Error handling and loading states

## Technology Stack

- **Backend**: Python 3.x with Flask
- **Frontend**: Vanilla JavaScript (ES6+)
- **Styling**: CSS3 with modern features
- **API**: MicroBurbs Property API
- **Icons**: Font Awesome 6

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd "c:\Users\user\OneDrive\Desktop\MicroBurb"
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Open your browser and navigate to**
   ```
   http://localhost:5000
   ```

The application should now be running! You'll see the MicroBurbs Property Dashboard.

## Usage Guide

### Searching for Properties

1. **Enter a suburb name** in the search field (e.g., "Belmont North")
2. **Optional**: Select a property type from the dropdown
3. Click the **"Search Properties"** button or press Enter
4. Use the **quick search chips** for instant searches

### Viewing Results

- **Statistics Cards**: View total properties, average price, average bedrooms, and price range
- **Filter Buttons**: Click to filter by property type (All, Houses, Apartments, Units)
- **Sort Dropdown**: Sort properties by price or bedrooms (ascending/descending)
- **Property Cards**: Click "View Details" to see complete property information

### Property Details Modal

Click "View Details" on any property card to open a modal with:
- Complete property information
- All available features (bedrooms, bathrooms, parking, land size)
- Raw JSON data for developers

## Project Structure

```
MicroBurb/
├── app.py                  # Flask backend server
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html         # Main HTML template
├── static/
│   ├── app.js             # Frontend JavaScript
│   └── styles.css         # CSS styling
└── README.md              # This file
```

## API Integration

The application integrates with the MicroBurbs API:

- **Endpoint**: `https://www.microburbs.com.au/report_generator/api/suburb/properties`
- **Method**: GET
- **Authentication**: Bearer token (configured in `app.py`)
- **Parameters**: 
  - `suburb` (required): Suburb name to search
  - `property_type` (optional): Filter by property type

### Backend Routes

- `GET /` - Main application page
- `GET /api/properties` - Proxy endpoint for MicroBurbs API
  - Query params: `suburb`, `property_type`
  - Returns: Property data with calculated statistics

## Features Breakdown

### Backend (Flask)

- **RESTful API endpoint** for property data
- **Error handling** for API failures and timeouts
- **Statistics calculation** (average price, bedrooms, price range)
- **CORS support** for development
- **Data extraction** from various API response formats

### Frontend (JavaScript)

- **Asynchronous data fetching** with Fetch API
- **Dynamic DOM manipulation** for property cards
- **Real-time filtering and sorting**
- **Modal system** for property details
- **Responsive state management**
- **Error and loading states**

### Design (CSS)

- **Modern gradient backgrounds**
- **Card-based layouts**
- **Smooth animations** (fade-in, slide-up)
- **Hover effects and transitions**
- **Responsive grid system**
- **Custom scrollbar styling**
- **Mobile-first approach**

## Browser Compatibility

- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## Customization

### Changing Colors

Edit the CSS variables in `static/styles.css`:

```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #ec4899;
    /* ... more variables */
}
```

### API Configuration

Update the API settings in `app.py`:

```python
API_BASE_URL = "https://www.microburbs.com.au/report_generator/api"
API_TOKEN = "test"
```

### Default Suburb

Uncomment lines in `static/app.js` to auto-load a suburb on page load:

```javascript
window.addEventListener('DOMContentLoaded', () => {
    suburbInput.value = 'Belmont North';
    handleSearch();
});
```

## Troubleshooting

### Server won't start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check if port 5000 is available
- Try running with a different port: `flask run --port 5001`

### No properties showing
- Check browser console for errors (F12)
- Verify internet connection
- Check API status at https://www.microburbs.com.au
- Ensure correct suburb name spelling

### Styling issues
- Clear browser cache (Ctrl+F5)
- Check that `static/styles.css` exists
- Verify browser compatibility

## Development

### Adding New Features

1. **Backend**: Add new routes in `app.py`
2. **Frontend**: Add functions in `static/app.js`
3. **Styling**: Add CSS in `static/styles.css`

### Testing

Test the application with various suburbs:
- Belmont North
- Sydney
- Melbourne
- Brisbane
- Your local suburb

## Performance Optimization

- Properties are loaded once per search
- Filtering and sorting happen client-side
- Images are lazy-loaded (placeholders used)
- CSS animations use GPU acceleration
- Minimal dependencies for faster load times

## Security Notes

- API token is stored server-side
- CORS is configured for development
- Input validation on suburb names
- Error messages don't expose sensitive data

## Future Enhancements

Possible improvements:
- Property image integration
- Map view with property locations
- Save favorite properties
- Property comparison feature
- Price history charts
- Email alerts for new properties
- Dark mode toggle
- Export data to CSV/PDF

## Credits

- **API Provider**: [MicroBurbs](https://www.microburbs.com.au)
- **Icons**: [Font Awesome](https://fontawesome.com)
- **Fonts**: [Google Fonts - Inter](https://fonts.google.com)

## License

This project is for demonstration purposes. Please check MicroBurbs API terms of service for production use.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the [MicroBurbs API Documentation](https://www.microburbs.com.au/report_generator/api/docs)
3. Check browser console for error messages

## Version

**Version 1.0.0** - October 2025

---

Built with ❤️ for property data visualization
