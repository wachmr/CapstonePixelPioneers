import os
import csv
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

def get_dominant_colors(image_path, num_colors=5, resize_size=(100, 100)):
    image = Image.open(image_path)
    image = image.resize(resize_size).convert('RGB')
    pixels = np.array(image).reshape(-1, 3)
    
    kmeans = KMeans(n_clusters=num_colors, random_state=0)
    kmeans.fit(pixels)
    
    counts = np.bincount(kmeans.labels_)
    colors = kmeans.cluster_centers_.astype(int)
    
    sorted_indices = np.argsort(-counts)
    hex_colors = [rgb_to_hex(colors[i]) for i in sorted_indices]
    percentages = (counts[sorted_indices] / len(pixels)) * 100
    
    return hex_colors, percentages

def process_images(input_dir, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['File name', 'HEX color', 'Percent', 'Percent without background'])
        
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(input_dir, filename)
                try:
                    hex_colors, percentages = get_dominant_colors(image_path)
                    base_name = os.path.splitext(filename)[0]
                    total_non_bg = 100 - percentages[0]
                    
                    # Write results for each color
                    for i in range(len(hex_colors)):
                        hex_code = hex_colors[i]
                        percent = f"{percentages[i]:.2f}%"
                        
                        if i == 0:
                            adjusted = ''
                        else:
                            adjusted_pct = (percentages[i] / total_non_bg) * 100
                            adjusted = f"{adjusted_pct:.2f}%"
                        
                        writer.writerow([base_name, hex_code, percent, adjusted])
                        
                    # Add empty row between images
                    writer.writerow([])
                    
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    input_directory = "character "
    output_file = "color_analysis.csv"
    process_images(input_directory, output_file)
    print(f"Analysis complete. Results saved to {output_file}")
