# count_red.py
"""
Counts red pixels in an image using a tolerant color detection method.
This works for real images (photos, logos, paintings, etc.)
"""

import sys
from PIL import Image

def count_red_pixels(img, min_red=150, red_ratio=1.2):
    """
    Count red pixels by thresholding.
    A pixel is red if:
    - R >= min_red
    - R is greater than G and B by a ratio
    """
    pixels = img.getdata()
    count = 0
    for r, g, b in pixels:
        if r >= min_red and r >= red_ratio * max(g, b):
            count += 1
    return count

def highlight_red_pixels(img, min_red=150, red_ratio=1.2, save_to="highlighted.png"):
    """
    Creates an image showing detected red pixels in bright red.
    """
    img = img.convert("RGB")
    width, height = img.size
    out = Image.new("RGB", (width, height))
    in_pixels = img.load()
    out_pixels = out.load()

    for y in range(height):
        for x in range(width):
            r, g, b = in_pixels[x, y]
            if r >= min_red and r >= red_ratio * max(g, b):
                out_pixels[x, y] = (255, 0, 0)
            else:
                out_pixels[x, y] = (int(r*0.25), int(g*0.25), int(b*0.25))

    out.save(save_to)
    return save_to

def main():
    if len(sys.argv) < 2:
        print("Usage: python count_red.py <image_path>")
        return

    path = sys.argv[1]
    img = Image.open(path).convert("RGB")
    total_pixels = img.size[0] * img.size[1]

    red_count = count_red_pixels(img, min_red=150, red_ratio=1.2)

    percent = (red_count * 100.0) / total_pixels

    print(f"Image: {path}")
    print(f"Total pixels: {total_pixels:,}")
    print()
    print("Red Pixels Detected:")
    print(f"  Count: {red_count:,}")
    print(f"  Percentage: {percent:.3f}%")

    out_path = highlight_red_pixels(img)
    print()
    print(f"Saved visualization to: {out_path}")

if __name__ == "__main__":
    main()
