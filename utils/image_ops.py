from PIL import Image, ImageDraw
import os



def place_rectangle_over_image(image, box, color, single_box=False):
    draw = ImageDraw.Draw(image)

    if not single_box:
        for bx in box:
            rectangle_coordinates = (int(bx[0]), int(bx[1]), int(bx[2]), int(bx[3]))
            draw.rectangle(rectangle_coordinates, fill=color)
    else:
        rectangle_coordinates = (int(box[0]), int(box[1]), int(box[2]), int(box[3]))
        draw.rectangle(rectangle_coordinates, fill=color)
        
    return image

def resize_image(image, max_width=500, max_height=600):
    width, height = image.size
    if width > max_width or height > max_height:
        aspect_ratio = width / height
        if aspect_ratio > 1:
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(max_height * aspect_ratio)
        return image.resize((new_width, new_height))
    else:
        return image

def combine_images_vertically(images, save_path, save=True, spacer_height=20):
    resized_images = [resize_image(image) for image in images]
    spacer = Image.new('RGB', (resized_images[0].width, spacer_height), color='white')
    combined_height = sum(image.size[1] for image in resized_images) + spacer_height * (len(resized_images) - 1)
    max_width = max(image.size[0] for image in resized_images)

    new_image = Image.new('RGB', (max_width, combined_height), color='white')

    y_offset = 0
    for image in resized_images:
        new_image.paste(image, (0, y_offset))
        y_offset += image.size[1]
        if y_offset < combined_height:
            new_image.paste(spacer, (0, y_offset))
            y_offset += spacer_height

    if save:
        new_image.save(save_path)

    return new_image




# image_paths = os.listdir("/home/sugarcat/Pictures/Wallpapers/swiss")
# output_path = 'combined_image.jpg'  # Path to save the combined image

# combine_images_vertically(image_paths, output_path)