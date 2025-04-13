"""
Analyze and visualize color similarity between characters
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import to_rgb, LinearSegmentedColormap
from sklearn.metrics.pairwise import cosine_similarity

# Assuming you have a DataFrame 'df' loaded with the following columns:
# 'File name', 'Archetypes', 'HEX color', and potentially others

def generate_archetype_similarity_heatmaps(df):
    """
    Generate cosine similarity heatmaps for character color palettes within each archetype.
    
    Args:
        df (pd.DataFrame): DataFrame containing character color data with columns:
                          'File name', 'Archetypes', 'HEX color'
    """
    # 1. Create filtered DataFrame (remove first color per character)
    df_filtered = df.groupby('File name').apply(lambda x: x.iloc[1:]).reset_index(drop=True)

    # 2. Prepare color data for each character (no weights)
    def get_character_colors(file_name):
        char_data = df_filtered[df_filtered['File name'] == file_name]
        return [to_rgb(c) for c in char_data['HEX color']]

    # 3. Create figure with 12 subplots (3x4 grid)
    archetypes = df_filtered['Archetypes'].unique()
    fig, axes = plt.subplots(3, 4, figsize=(24, 18))
    fig.suptitle('Character Color Similarity (Unweighted)', y=1.02, fontsize=16)

    # Create colormap (dark green to dark red)
    colors = ['#006400', '#228B22', '#32CD32', '#90EE90', '#FFFFFF', 
              '#FFB6C1', '#FF6347', '#DC143C', '#8B0000']
    custom_cmap = LinearSegmentedColormap.from_list('dr_dg', colors, N=10)

    # 4. Generate one heatmap per archetype
    for idx, archetype in enumerate(archetypes):
        ax = axes.flatten()[idx]
        
        # Get all characters for this archetype
        archetype_chars = df_filtered[df_filtered['Archetypes'] == archetype]['File name'].unique()
        n_chars = len(archetype_chars)
        
        # Create color vectors (flattened RGB values)
        color_vectors = []
        for char in archetype_chars:
            rgb_colors = get_character_colors(char)
            # Flatten all RGB values into one vector
            flat_vector = np.array(rgb_colors).flatten()
            # Pad with zeros if needed for equal length
            max_length = max(len(v) for v in color_vectors) if color_vectors else len(flat_vector)
            if len(flat_vector) < max_length:
                flat_vector = np.pad(flat_vector, (0, max_length - len(flat_vector))
            color_vectors.append(flat_vector)
        
        # Calculate pairwise cosine similarity
        similarity_matrix = cosine_similarity(color_vectors)
        
        # Plot heatmap
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
            xticklabels=archetype_chars,
            yticklabels=archetype_chars,
            linewidths=0.5,
            linecolor='white'
        )
        
        # Formatting
        ax.set_title(archetype, pad=12)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

    plt.tight_layout()
    plt.savefig('archetype_similarities_unweighted.png', dpi=300, bbox_inches='tight')
    plt.show()

# Example usage:
# df = pd.read_csv('your_color_data.csv')  # Load your data first
# generate_archetype_similarity_heatmaps(df)
