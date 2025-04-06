"""
Generate individual character color distribution plots
"""
import pandas as pd
import matplotlib.pyplot as plt

def plot_character_colors(data_path, archetype, character):
    df = pd.read_excel(data_path, engine="openpyxl")
    subset = df[(df["Archetypes"] == archetype) & 
                (df["File name"] == character)].sort_values("Percent", ascending=False)
    
    plt.figure(figsize=(10, 4))
    bars = plt.bar(subset["HEX color"], subset["Percent without background"], 
                  color=subset["HEX color"], edgecolor="black")
    
    plt.title(f"{archetype}: {character} Color Distribution")
    plt.xlabel("HEX Color")
    plt.ylabel("Percentage (%)")
    plt.xticks(rotation=45)
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(f"character_{archetype}_{character.replace(' ', '_')}.png", dpi=300)
    plt.close()
