# CapstonePixelPioneers
# Archetype Color Analyzer

Capstone project for University of Michigan's Master of Applied Data Science program by Miranda Kuns and Heather Whittaker analyzing character color palettes and their psychological archetype associations using computer vision and clustering techniques.

## Getting Started

### Clone the repo
Clone this repository to get started.

```bash
git clone https://github.com/wachmr/archetype-color-analyzer.git
cd archetype-color-analyzer

##Prerequisites
Get all of the dependencies needed.

pip install -r requirements.txt



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


# Archetype Color Visualizer

Visualization tools for character color analysis.

## Features
- Square grid palette visualizations
- Archetype similarity heatmaps
- Individual character color distributions

## Usage
```python
# Generate all visualizations
from src.color_palette_visualizer import visualize_archetype_palettes
from src.similarity_analyzer import analyze_similarity

visualize_archetype_palettes("data/color_analysis.xlsx", "output/")
analyze_similarity("data/color_analysis.xlsx", "output/")

# Plot individual character
from src.character_color_plot import plot_character_colors
plot_character_colors("data/color_analysis.xlsx", "Sage", "Master Splinter")
```
