import requests
import apikey
import os
import csv
import time

# -------------------------------------------------------
# FIRST TIME SETUP: Save your API keys (run once, then comment out)
apikey.save("NASA_API_KEY", "IgyVj07vTJyBhy4pDCgAhbrIYLC3bmg9f5WBUPmC")
apikey.save("EUROPEANA_API_KEY", "ricition")
# -------------------------------------------------------

# Load API keys
nasa_api_key = apikey.load("NASA_API_KEY")
europeana_api_key = apikey.load("EUROPEANA_API_KEY")

# Set Europeana key as environment variable (required by pyeuropeana)
os.environ['EUROPEANA_API_KEY'] = europeana_api_key

import pyeuropeana.apis as apis
import pyeuropeana.utils as utils

# ============================================================
# PART 1: NASA API — Astronomy Picture of the Day (APOD)
# ============================================================
print("=" * 60)
print("PART 1: NASA Astronomy Picture of the Day API")
print("=" * 60)

nasa_url = f'https://api.nasa.gov/planetary/apod?api_key={nasa_api_key}&count=10'
nasa_response = requests.get(nasa_url)

if nasa_response.status_code == 200:
    apod_data = nasa_response.json()
    print(f"\nSuccessfully retrieved {len(apod_data)} NASA APOD entries.\n")
    for item in apod_data:
        print(f"  Title: {item['title']}")
        print(f"  Date:  {item['date']}")
        print(f"  URL:   {item.get('url', 'N/A')}")
        print()
else:
    print(f"NASA API error: {nasa_response.status_code}")
    apod_data = []

time.sleep(2)

# Pick the first item to cross-reference with Europeana
if apod_data:
    selected = apod_data[0]
    search_term = selected['title']
    print(f"Selected NASA item for Europeana search: '{search_term}'")
else:
    search_term = "astronomy space"
    print(f"Using fallback search term: '{search_term}'")

# ============================================================
# PART 2: Europeana API — Search for related cultural items
# ============================================================
print("\n" + "=" * 60)
print("PART 2: Europeana API — Related Cultural Heritage Items")
print("=" * 60)

europeana_response = apis.search(
    query=search_term,
    rows=10,
    profile='rich'
)

print(f"\nTotal Europeana results for '{search_term}': {europeana_response.get('totalResults', 0)}\n")

# Convert to DataFrame for easy display
if europeana_response.get('items'):
    df = utils.search2df(europeana_response)
    print(df[['europeana_id', 'title_lang']].to_string())

    # Show first item's Europeana link
    first_item = europeana_response['items'][0]
    print(f"\nFirst Europeana item link: {first_item.get('guid', 'N/A')}")
else:
    print("No Europeana results found. Try a broader search term.")

time.sleep(2)

# ============================================================
# PART 3: Save data to CSV
# ============================================================
print("\n" + "=" * 60)
print("PART 3: Saving data to CSV")
print("=" * 60)

output_filename = 'nasa_europeana_data.csv'

rows_to_save = []

# Add NASA rows
for item in apod_data:
    rows_to_save.append({
        'source': 'NASA_APOD',
        'id': item.get('date', ''),
        'title': item.get('title', ''),
        'date': item.get('date', ''),
        'description': item.get('explanation', '')[:300],  # truncate long text
        'url': item.get('url', ''),
        'europeana_id': '',
        'europeana_title': ''
    })

# Add Europeana rows (filter out API key from response before saving!)
if europeana_response.get('items'):
    for item in europeana_response['items']:
        # Carefully avoid saving the API key
        title = ''
        if isinstance(item.get('title'), list):
            title = item['title'][0] if item['title'] else ''
        elif isinstance(item.get('title'), str):
            title = item['title']

        rows_to_save.append({
            'source': 'Europeana',
            'id': item.get('id', ''),
            'title': title,
            'date': '',
            'description': '',
            'url': item.get('edmIsShownAt', [''])[0] if item.get('edmIsShownAt') else '',
            'europeana_id': item.get('id', ''),
            'europeana_title': title
        })

# Write to CSV
fieldnames = ['source', 'id', 'title', 'date', 'description', 'url', 'europeana_id', 'europeana_title']
with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows_to_save)

print(f"\nData saved to '{output_filename}' ({len(rows_to_save)} rows)")
print("\nDone! Remember to NOT push your API keys to GitHub.")