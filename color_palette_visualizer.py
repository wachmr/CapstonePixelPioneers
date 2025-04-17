"""
Visualize archetype color palettes in square grid format
"""
import pandas as pd
import matplotlib.pyplot as plt
import math
import os
from matplotlib.patches import Rectangle

def visualize_archetype_palettes(data_path: str, output_dir: str):
    """Generate square grid palette visualization for each archetype."""
    df = pd.read_excel(data_path, engine="openpyxl") if data_path.endswith(".xlsx") else pd.read_csv(data_path)
    df = df.dropna(subset=["Archetypes"])

    archetypes = df['Archetypes'].unique()
    n_archetypes = len(archetypes)
    n_cols = 4
    n_rows = math.ceil(n_archetypes / n_cols)

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, 5 * n_rows))
    fig.suptitle('Archetype Color Palettes (Original Order)', fontsize=16, y=1.02)

    for idx, archetype in enumerate(archetypes):
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

        ax.set_title(f"{archetype}", fontsize=12)
        ax.set_xlim(0, grid_size)
        ax.set_ylim(0, grid_size)
        ax.set_aspect('equal')
        ax.axis('off')

    for j in range(n_archetypes, n_rows * n_cols):
        axes.flatten()[j].axis('off')

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'archetype_palettes.png')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Visualize archetype color palettes as square grids.")
    parser.add_argument("--data_path", required=True, help="Path to CSV/XLSX color analysis file")
    parser.add_argument("--output_dir", required=True, help="Directory to save the palette image")
    args = parser.parse_args()

    visualize_archetype_palettes(args.data_path, args.output_dir)
