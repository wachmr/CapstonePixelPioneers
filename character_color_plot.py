"""
Generate individual character color distribution plots
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_character_colors(data_path: str, archetype: str, character: str, output_dir: str = "."):
    """Plot color distribution bar chart for a specific character."""
    df = pd.read_excel(data_path, engine="openpyxl") if data_path.endswith(".xlsx") else pd.read_csv(data_path)
    subset = df[(df["Archetypes"] == archetype) & 
                (df["File name"] == character)].sort_values("Percent", ascending=False)

    plt.figure(figsize=(10, 4))
    bars = plt.bar(
        subset["HEX color"],
        subset["Percent without background"],
        color=subset["HEX color"],
        edgecolor="black"
    )

    plt.title(f"{archetype}: {character} Color Distribution")
    plt.xlabel("HEX Color")
    plt.ylabel("Percentage (%)")
    plt.xticks(rotation=45)

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height,
                 f'{height:.1f}%', ha='center', va='bottom')

    plt.tight_layout()
    filename = f"character_{archetype}_{character.replace(' ', '_')}.png"
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, filename), dpi=300)
    plt.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Plot individual character color distribution.")
    parser.add_argument("--data_path", required=True, help="Path to CSV/XLSX color analysis file")
    parser.add_argument("--archetype", required=True, help="Archetype of the character")
    parser.add_argument("--character", required=True, help="Character name")
    parser.add_argument("--output_dir", default=".", help="Directory to save the plot")
    args = parser.parse_args()

    plot_character_colors(args.data_path, args.archetype, args.character, args.output_dir)
