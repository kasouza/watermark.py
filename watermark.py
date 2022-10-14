import os

from PIL import Image
from pathlib import Path


# Watermark position in percentages (based on it's center)
WATERMARK_POS = (0.5, 0.5)

# Watermark size in percentages to the src image's width
WATERMARK_SIZE = 1/3

# Path to directories and the watermark image
WATERMARK_PATH = './watermark.png'
INPUT_PATH = './in'
OUTPUT_PATH = './out'


def add_watermark(src, watermark):
    watermark_width, watermark_height = watermark.size
    src_width, src_height = src.size

    result = Image.new(mode='RGBA', size=src.size, color=0)

    result.paste(src)

    scale_factor = WATERMARK_SIZE * src_width / watermark_width
    final_watermark_size = (int(watermark_width * scale_factor), int(watermark_height * scale_factor))
    resized = watermark.resize(final_watermark_size)

    x, y = WATERMARK_POS
    x = int(x * src_width - final_watermark_size[0] / 2)
    y = int(y * src_height - final_watermark_size[1] / 2)

    watermark_box = (x, y)
    result.paste(resized, watermark_box, resized)

    return result


def create_directories():
    output_path = Path('./out')
    if not output_path.is_dir():
        os.mkdir(output_path)

    input_path = Path('./in')
    if not input_path.is_dir():
        os.mkdir(input_path)

    return input_path, output_path


def main():
    watermark_path = Path(WATERMARK_PATH)
    if not watermark_path.exists():
        print('Could not find "' + watermark_path + '"!')
        return

    input_path, output_path = create_directories()
    
    watermark = Image.open(watermark_path)
    images = os.listdir(input_path)

    for image in images:
        image_path = Path(image)
        src_img = Image.open(Path(input_path, image_path))
        
        result = add_watermark( src_img, watermark)

        image_out = Path(output_path, 'watermarked_' + image_path.stem + '.png')
        result.save(image_out, 'png')


if __name__ == '__main__':
    main()