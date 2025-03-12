from PIL import Image
import sys


def convert_to_ico(png_path, ico_path):
    # Open the PNG file
    img = Image.open(png_path)
    # Save as .ico with multiple sizes
    img.save(ico_path, format='ICO', sizes=[
        (16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)
    ])
    print(f"Converted {png_path} to {ico_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python convert_to_ico.py input.png output.ico")
        sys.exit(1)
    input_png = sys.argv[1]
    output_ico = sys.argv[2]
    convert_to_ico(input_png, output_ico)