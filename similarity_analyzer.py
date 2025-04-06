"""
Analyze and visualize color similarity between characters
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import to_rgb, LinearSegmentedColormap

def analyze_similarity(data_path, output_dir):
    df = pd.read_excel(data_path, engine="openpyxl")
    df_filtered = df.groupby('File name').apply(lambda x: x.iloc[1:]).reset_index(drop=True)
    
    def get_palette(file_name):
        char_data = df_filtered[df_filtered['File name'] == file_name]
        return (
            char_data['HEX color'].tolist(),
            char_data['Percent without background'].fillna(0).tolist()
        )

    archetypes = df_filtered['Archetypes'].unique()
    fig, axes = plt.subplots(3, 4, figsize=(24, 18))
    fig.suptitle('Character Color Similarity (Green=High)', y=1.02, fontsize=16)

    colors = ['#006400', '#228B22', '#32CD32', '#90EE90', '#FFFFFF', 
              '#FFB6C1', '#FF6347', '#DC143C', '#8B0000']
    cmap = LinearSegmentedColormap.from_list('dr_dg', colors, N=10)

    for idx, archetype in enumerate(archetypes):
        ax = axes.flatten()[idx]
        chars = df_filtered[df_filtered['Archetypes'] == archetype]['File name'].unique()
        n_chars = len(chars)
        sim_matrix = np.zeros((n_chars, n_chars))
        
        for i in range(n_chars):
            for j in range(i, n_chars):
                cols1, wts1 = get_palette(chars[i])
                cols2, wts2 = get_palette(chars[j])
                vec1 = sum(np.array(to_rgb(c)) * w for c, w in zip(cols1, wts1))
                vec2 = sum(np.array(to_rgb(c)) * w for c, w in zip(cols2, wts2))
                norm = np.linalg.norm(vec1) * np.linalg.norm(vec2)
                sim_matrix[i,j] = sim_matrix[j,i] = np.dot(vec1, vec2)/norm if norm > 0 else 0

        sns.heatmap(
            sim_matrix,
            ax=ax,
            cmap=cmap,
            vmin=0,
            vmax=1,
            square=True,
            annot=True,
            fmt=".2f",
            cbar=False,
            xticklabels=chars,
            yticklabels=chars,
            linewidths=0.5,
            linecolor='white'
        )
        ax.set_title(archetype, pad=12)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/archetype_similarities.png', dpi=300, bbox_inches='tight')
    plt.close()
