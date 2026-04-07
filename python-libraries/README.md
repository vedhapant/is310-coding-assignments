# Command Line Data Curation - The Art Vault 

A CLI tool for manually entering and saving artwork data to a CSV file, built with Python and the [Rich](https://rich.readthedocs.io/) library.

## What It Does

- Displays a pre-loaded table of famous artworks as example data
- Prompts you to enter as many new artworks as you'd like
- Asks you to confirm each entry before saving it
- Writes all entries (existing + new) to a timestamped `.csv` file in your current directory
- Prints the full file path so you can find it immediately

## Fields Collected

| Field | Example |
|-------|---------|
| Title | The Starry Night |
| Artist | Vincent van Gogh |
| Year | 1889 |
| Medium | Oil on canvas |
| Location | MoMA, New York |

## How to Run

**1. Install dependencies:**
```bash
pip install rich
```

**2. Run the script**


**3. Follow the prompts** — enter how many artworks you want to add, fill in each field, confirm your entries, and your CSV will be saved automatically.

## Output

A file named `my_artworks_YYYYMMDD_HHMMSS.csv` will be created in the directory where you ran the script.
