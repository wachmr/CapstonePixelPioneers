"""
Visualize archetype color palettes in square grid format
"""
import pandas as pd
import matplotlib.pyplot as plt
import math
from matplotlib.patches import Rectangle

def visualize_archetype_palettes(data_path, output_dir):
    df = pd.read_excel(data_path, engine="openpyxl")
    df = df.dropna(subset=["Archetypes"])
    
    fig, axes = plt.subplots(3, 4, figsize=(20, 15))
    fig.suptitle('Archetype Color Palettes (Original Order)', fontsize=16, y=1.02)

    for idx, archetype in enumerate(df['Archetypes'].unique()):
        ax = axes.flatten()[idx]
        archetype_data = df[df['Archetypes'] == archetype].copy()
        
        n_colors = len(archetype_data)
        grid_size = math.ceil(math.sqrt(n_colors))
        
        for i, (_, row) in enumerate(archetype_data.iterrows()):
            x_pos = i % grid_size
            y_pos = grid_size - 1 - (i // grid_size)
            
            ax.add_patch(Rectangle(
                (x_pos, y_pos), 1, 1,
                facecolor=row['HEX color'],
                edgecolor='white',
                linewidth=2
            ))

        ax.set_title(f"{archetype}\n{archetype_data['File name'].iloc[0]}", fontsize=10)
        ax.set_xlim(0, grid_size)
        ax.set_ylim(0, grid_size)
        ax.set_aspect('equal')
        ax.axis('off')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/archetype_palettes.png', dpi=300, bbox_inches='tight')
    plt.close()
