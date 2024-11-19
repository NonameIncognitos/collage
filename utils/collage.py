from PIL import Image
import math
import os

def create_collage(image_paths, output_path, margin=10, collage_width=800):
    images = [Image.open(path) for path in image_paths]
    n = len(images)

    if n <= 2:
        rows, cols = 1, n
    else:
        cols = math.ceil(math.sqrt(n))
        rows = math.ceil(n / cols)

    max_height = 800
    processed_images = []

    for img in images:
        aspect_ratio = img.width / img.height
        new_height = int(collage_width / aspect_ratio)

        if new_height > max_height:
            new_width = int(max_height * aspect_ratio)
            new_height = max_height
        else:
            new_width = collage_width

        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        processed_images.append(img_resized)

    collage_width = (collage_width * cols) + (margin * (cols + 1))
    max_height_per_row = []

    for i in range(rows):
        row_images = processed_images[i * cols:min((i + 1) * cols, n)]
        max_height_per_row.append(max(img.height for img in row_images))

    collage_height = sum(max_height_per_row) + (margin * (rows + 1))

    collage = Image.new('RGB', (collage_width, collage_height), (255, 255, 255))

    current_y = margin
    for row in range(rows):
        current_x = margin
        row_images = processed_images[row * cols:min((row + 1) * cols, n)]

        for img in row_images:
            collage.paste(img, (current_x, current_y))
            current_x += img.width + margin

        current_y += max_height_per_row[row] + margin

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    collage.save(output_path, quality=95)
