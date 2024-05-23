import os
from PIL import Image, ImageDraw, ImageFont
from core.yolo_inference import YOLOInferenceManager

from utils.mecr_box_merger import make_mergeable_set, merge_from_set
from utils.config import DL_MODEL_CONF

def mecr_extraction(directories):
    image_path = os.listdir(directories['pages__notfgc'])
    image_path = [directories['pages__notfgc'] + img_name for img_name in image_path]
    mecr_infr_obj  = YOLOInferenceManager(DL_MODEL_CONF.MECR_PATH)

    box_n_path = []
    for image_path in image_path[:2]:
        box_n_path.append(mecr_infr_obj.inference(image_path))

    return box_n_path



"""

    MECR Processing:

        1. Merge all the overlapping boxes.
        2. Calulate each merged box and sort them. First element of the new list is area and 2nd is a list containing all the 4 coords.

"""
def process_mecr_output(box_n_path, directories):
    for image_index, image_info in enumerate(box_n_path):
        box_coords, image_path = image_info

        mergeable_set = make_mergeable_set(box_coords)
        merged_boxes = merge_from_set(mergeable_set, box_coords)

        merged_boxes_w_area = []
        for bx in merged_boxes:
            x1, y1, x2, y2 = bx
            area = (x2-x1) * (y2-y1)
            merged_boxes_w_area.append([area, [x1,y1,x2,y2]])
        merged_boxes_w_area.sort()

        # Load the image and perform cropping.
        page_image = Image.open(image_path)
        page_draw = ImageDraw.Draw(page_image)


        for box_index, box_info in enumerate(merged_boxes_w_area):
            _, box_coords_tensor = box_info
            
            #each box_coords is tensor. Convert it into integer. Otherwise, pillow throwing error in cropping in the next line.
            box_coords = []
            for pnt_tnsr in box_coords_tensor:
                box_coords.append(int(pnt_tnsr))

            cropped_image = page_image.crop(box_coords)

            cropped_version_name = str(box_index) + "__" + image_path.split("/")[-1]  #keeping file extension for simplicity. Taking -1 with / split will give full name with extension.
            cropped_version_save_path = directories['mecr_blocks'] + cropped_version_name
            cropped_image.save(cropped_version_save_path)

            #Place a white rectangle on original image and then write over it.
            page_draw.rectangle(box_coords, fill='white') 

            # Define the text and font
            text = f"ME-{box_index}"
            font = ImageFont.truetype("lib/Roboto-Regular.ttf", 28)

            # Calculate text size
            _, _, text_width, text_height = page_draw.textbbox((0, 0), text=text, font=font)

            # Calculate text position to center it within the rectangle
            text_x = box_coords[0] + (box_coords[2] - box_coords[0] - text_width) // 2
            text_y = box_coords[1] + (box_coords[3] - box_coords[1] - text_height) // 2

            # page_draw text on the image
            page_draw.text((text_x, text_y), text, fill='blue', font=font)
        
        #Save the no-mecr image.
        image_save_path =  directories['pages__nomecr'] + image_path.split("/")[-1]
        page_image.save(image_save_path)

