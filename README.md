# Scrappy

A Python-based lead generation tool that scrapes business information from Google Maps and validates contacts through WhatsApp Web.

## Overview

Scrappy automates the process of collecting business leads by:
- Scraping business listings from Google Maps based on category and location
- Extracting contact information (phone, website, address)
- Filtering and validating phone numbers by country
- Checking WhatsApp availability for each contact
- Generating detailed statistics and reports

## Features

- **Google Maps Scraping**: Extract business data from multiple cities automatically
- **Phone Validation**: Filter valid phone numbers and verify country codes
- **WhatsApp Integration**: Verify which contacts have active WhatsApp accounts
- **Data Export**: Generate Excel files at each filtering stage
- **Statistics Generation**: Automatic reporting on lead conversion rates
- **Multi-City Support**: Process multiple cities from a text file

## Prerequisites

- Python 3.8+
- Google Chrome or Chromium browser
- Active WhatsApp account (for WhatsApp validation)

**Platform Support:**
- ✅ Linux
- ✅ macOS
- ❌ Windows (not currently supported)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/scrappy.git
cd scrappy
```

2. Create and activate a virtual environment:
```bash
python3 -m venv env
source env/bin/activate  # On Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Command

```bash
python scrappy/scraper.py -c <COUNTRY> -cat <CATEGORY> -l <CITIES_FILE>
```

### Parameters

- `-c, --country`: Country name to search in (e.g., "Bolivia", "Mexico", "Paraguay")
- `-cat, --category`: Business category to search for (e.g., "taxi", "restaurant", "hotel")
- `-l, --list`: Path to text file containing city names (one per line)

### Examples

Search for taxi services in Bolivian cities:
```bash
python scrappy/scraper.py -c Bolivia -cat taxi -l examples/cities_example.txt
```

Search for hotels in Paraguay:
```bash
python scrappy/scraper.py -c Paraguay -cat hotel -l cities.txt
```

### Cities File Format

Create a text file with one city name per line:
```
La Paz
Santa Cruz
Cochabamba
```

## Output Files

The tool generates multiple Excel files during the filtering process:

1. **`{CATEGORY}_{COUNTRY}_raw_data.xlsx`**
   - All businesses found on Google Maps
   - Contains duplicates and unfiltered data

2. **`{CATEGORY}_{COUNTRY}_contactos_con_telefono.xlsx`**
   - Businesses with valid phone numbers
   - Invalid formats and duplicates removed

3. **`{CATEGORY}_{COUNTRY}_contactos_nacionales_con_telefono.xlsx`**
   - Phone numbers verified to belong to the specified country

4. **`{CATEGORY}_{COUNTRY}_prospectos.xlsx`**
   - Final leads with verified WhatsApp accounts

5. **`{CATEGORY}_{COUNTRY}_estadisticas.txt`**
   - Statistics report showing conversion rates at each stage

All output files are saved in the `output/` directory.

## Project Structure

```
scrappy/
├── scrappy/              # Main package
│   ├── __init__.py
│   └── scraper.py        # Core scraping and filtering logic
├── assets/               # Static resources
│   └── alarm.mp3         # Notification sound
├── notebooks/            # Jupyter notebooks
│   └── comparador.ipynb  # Data analysis utilities
├── examples/             # Example files
├── output/               # Generated output files (gitignored)
├── tests/                # Unit tests
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## How It Works

### Pipeline Overview

1. **Scraping Phase**
   - Opens Google Maps in Chrome via Selenium
   - Searches for each city + country combination
   - Searches for businesses in the specified category
   - Scrolls through results to load more data
   - Extracts: name, phone, website, address, service type

2. **Phone Filtering Phase**
   - Removes entries with invalid phone formats
   - Removes duplicate phone numbers
   - Uses `phonenumbers` library to validate country codes

3. **WhatsApp Verification Phase** (Manual)
   - User scans QR code to authenticate WhatsApp Web
   - System tests each phone number (≈4.5 seconds per contact)
   - Filters out contacts without WhatsApp

4. **Statistics Generation**
   - Counts records at each stage
   - Calculates conversion percentages
   - Generates summary report

## Important Notes

### WhatsApp Verification

- You will need to scan a WhatsApp QR code when the alarm sounds
- The process takes approximately 4.5 seconds per phone number
- For 500 contacts, expect ~38 minutes of processing time

### Browser Configuration

The tool looks for Chrome/Chromium at these locations:
- **Linux**: `/usr/bin/google-chrome`
- **macOS**: `/Applications/Google Chrome 2.app/Contents/MacOS/Google Chrome`

If your Chrome installation is elsewhere, update the path in `scraper.py:129-132`.

### Rate Limiting

Google Maps may rate-limit or block automated scraping. Use responsibly and consider:
- Adding delays between requests
- Using residential proxies
- Limiting the number of cities per session

## Troubleshooting

**Error: "No funciona en windows..."**
- Windows is not currently supported. Use Linux or macOS.

**Error: Chrome driver not found**
- Ensure Chrome/Chromium is installed
- Update the `CHROME_DRIVER_PATH` in `create_driver()` function

**WhatsApp QR code not appearing**
- Increase the sleep timer in `open_whatsapp()` (default: 30 seconds)
- Ensure you're logged out of WhatsApp Web in other browser tabs

**No results found for a city**
- Verify the city name spelling
- Try adding the province/state (e.g., "Santa Cruz de la Sierra")
- Check Google Maps manually to confirm businesses exist

## Useful Resources

- [SimpleMaps](https://simplemaps.com) - Free database of world cities
- [Google Maps](https://maps.google.com) - Verify search results manually
- [WhatsApp Web](https://web.whatsapp.com) - Test contact validation

## License

MIT License - See LICENSE file for details

## Author

Created by @sleepydogo

## Version

Current version: 0.2.0

---

**Disclaimer**: This tool is for educational and legitimate business purposes only. Ensure compliance with Google's Terms of Service and local data protection regulations when scraping data. The author is not responsible for misuse of this tool.
