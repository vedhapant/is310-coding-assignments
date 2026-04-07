# API Getting Data — IS310 Assignment

## Overview
This folder contains scripts for the IS310 "Getting Culture Across APIs" assignment. 
The goal is to demonstrate how to use APIs to retrieve data from the web, 
cross-reference data between two different APIs, and save the results in a structured format.

APIs (Application Programming Interfaces) are a way to request data from a server 
programmatically — similar to how a web browser loads a webpage, but instead of getting 
back HTML, we get back structured data (usually JSON) that we can work with in Python.

## APIs Used

### 1. NASA APOD API (Astronomy Picture of the Day)
- **URL:** https://api.nasa.gov/
- **Why I chose it:** NASA's APOD API is a free, well-documented public API that provides 
daily astronomy images and explanations written by professional astronomers. I chose it 
because astronomy has a rich cultural history — humans have been observing and documenting 
the night sky for thousands of years — which makes it a natural fit for cross-referencing 
with European heritage collections.
- **What it returns:** Each entry includes a title, date, description, and image URL

### 2. Europeana API
- **URL:** https://pro.europeana.eu/pages/get-api
- **Why I used it:** Europeana provides access to millions of digitized items from European 
museums, libraries, and archives. It bridges modern scientific imagery with historical 
cultural artifacts.
- **What it returns:** Metadata about cultural heritage items including titles, institution 
sources, and links to the original items

## How the Script Works

### `getculture.py`
1. Connects to the NASA APOD API and retrieves 10 random Astronomy Picture of the Day entries
2. Takes the title of the first NASA result and searches Europeana for related cultural items
3. Prints both sets of results to the terminal
4. Saves everything to `nasa_europeana_data.csv` (API keys are excluded from saved data)

## Output
- `nasa_europeana_data.csv` — combined data from NASA and Europeana (20 rows total)

