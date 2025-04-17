# CapstonePixelPioneers

Capstone project for University of Michigan's Master of Applied Data Science program by Miranda Kuns and Heather Whittaker analyzing character color palettes and their psychological archetype associations using computer vision and clustering techniques.

## Getting Started

### Clone the repo
Clone this repository to get started.

```bash
git clone https://github.com/wachmr/archetype-color-analyzer.git
cd archetype-color-analyzer
```
## Prerequisites

Get all of the dependencies needed.


```
pip install -r requirements.txt

```

# Color Archetype Analyzer

Analyzes character images to extract dominant colors and map to psychological archetypes.

## Features
- Extracts top 5 dominant colors from character images
- Calculates color percentages (with/without background)
- CSV output for further analysis

## Usage
1. Place character images in `/characters`
2. Run the analyzer:
```bash
python src/color_extractor.py --input_dir ./characters --output_file ./results.csv
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
## LLM prompting pipeline

![image](https://github.com/user-attachments/assets/13381e24-ce35-4d26-ad2b-5c3b0728f70f)


## Data Access Statement 

#### Goal: A data access statement indicating how to access the data or explaining who owns the data. Licenses for data use and redistribution are respected. 

We do not leverage any pre-created csv data files.     

Color definitions are extracted from open hex code RGB definitions. Images were pulled from openly available charachter images. Archetype descriptions were sourced from liturature, media, and industry desctiptions based on Jung's original publication. 

The resultant csvs levaged within the pipeline were created by our team: Miranda Kuns and Heather Whittaker
