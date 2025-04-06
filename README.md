# CapstonePixelPioneers
# Color Archetype Analyzer

Analyzes character images to extract dominant colors and map to psychological archetypes.

## Features
- Extracts top 5 dominant colors from character images
- Calculates color percentages (with/without background)
- CSV output for further analysis

## Usage
1. Place character images in `/data/characters`
2. Run the analyzer:
```bash
python src/color_extractor.py --input_dir ./data/characters --output_file ./data/results.csv
```

## Sample Output
| Character    | HEX     | Pct    | Pct_Without_BG |
|--------------|---------|--------|----------------|
| hero_superman| #0000FF | 45.25% |                |
| hero_superman| #FF0000 | 30.10% | 55.02%         |
