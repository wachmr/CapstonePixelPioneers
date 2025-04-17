"""
Analyze and visualize color similarity between characters
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import to_rgb, LinearSegmentedColormap
from sklearn.metrics.pairwise import cosine_similarity


def load_and_filter_data(file_path: str) -> pd.DataFrame:
    """Load data and remove the first color per character."""
    df = pd.read_excel(file_path) if file_path.endswith(".xlsx") else pd.read_csv(file_path)
    return df.groupby('File name').apply(lambda x: x.iloc[1:]).reset_index(drop=True)


def perceptual_similarity(palette1, palette2):
    """
    Calculate perceptual similarity between two color palettes using weighted RGB distance.
    Returns similarity score between 0 (dissimilar) and 1 (identical).
    """
    arr1 = np.array(palette1)
    arr2 = np.array(palette2)
    distances = np.sqrt(np.sum((arr1[:, np.newaxis] - arr2)**2, axis=2))
    min_distances1 = np.min(distances, axis=1)
    min_distances2 = np.min(distances, axis=0)
    avg_distance = (np.mean(min_distances1) + np.mean(min_distances2)) / 2
    return 1 / (1 + avg_distance)


def get_character_colors(df: pd.DataFrame, file_name: str):
    """Get list of RGB tuples for a character."""
    char_data = df[df['File name'] == file_name]
    return [to_rgb(c) for c in char_data['HEX color']]


def get_archetype_similarity_matrix(df: pd.DataFrame, archetype: str):
    """Generate similarity matrix for all characters of an archetype."""
    characters = sorted(df[df['Archetypes'] == archetype]['File name'].unique())
    palettes = [get_character_colors(df, char) for char in characters]
    n = len(characters)
    similarity = np.eye(n)
    for i in range(n):
        for j in range(i + 1, n):
            score = perceptual_similarity(palettes[i], palettes[j])
            similarity[i, j] = similarity[j, i] = score
    return characters, similarity


def plot_archetype_similarities(df: pd.DataFrame, output_file: str):
    """Plot similarity heatmaps for each archetype."""
    archetypes = df['Archetypes'].unique()
    n_archetypes = len(archetypes)
    n_cols = 4
    n_rows = int(np.ceil(n_archetypes / n_cols))

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(24, 6 * n_rows))
    fig.suptitle('Archetype Color Similarity Across Characters (Perceptual Metric)', y=1.02, fontsize=16)

    colors = ['#006400', '#228B22', '#32CD32', '#90EE90', '#FFFFFF',
              '#FFB6C1', '#FF6347', '#DC143C', '#8B0000']
    custom_cmap = LinearSegmentedColormap.from_list('dr_dg', colors, N=10)

    for idx, archetype in enumerate(archetypes):
        ax = axes.flatten()[idx]
        characters, similarity_matrix = get_archetype_similarity_matrix(df, archetype)

        sns.heatmap(
            similarity_matrix,
            ax=ax,
            cmap=custom_cmap,
            vmin=0,
            vmax=1,
            square=True,
            annot=True,
            fmt=".2f",
            cbar=False,
            xticklabels=characters,
            yticklabels=characters,
            linewidths=0.5,
            linecolor='white'
        )

        ax.set_title(archetype, pad=12, fontsize=16)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

    for j in range(n_archetypes, n_rows * n_cols):
        axes.flatten()[j].axis('off')

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate perceptual similarity heatmaps by archetype.")
    parser.add_argument("--input_file", required=True, help="Path to CSV/XLSX color analysis file")
    parser.add_argument("--output_file", default="archetype_character_similarities_perceptual.png", help="Path to output image file")
    args = parser.parse_args()

    df = load_and_filter_data(args.input_file)
    plot_archetype_similarities(df, args.output_file)
