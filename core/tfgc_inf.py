import os
from PIL import Image
from core.yolo_inference import YOLOInferenceManager
from utils.image_ops import place_rectangle_over_image
from utils.config import DL_MODEL_CONF



"""
    # Works with the RAW images.
    
    # Api returns a list. This list contains list of boxes and their labels in for each image. 
    # As the req is authorized, currently data is not encrypted.

    Gives output as 2 types of images:

        1. tfgc blocks
        2. images without tfgc blocks
"""

def tfgc_extraction(directories):
    try:
        tfgc_infr_obj  = YOLOInferenceManager(DL_MODEL_CONF.TFGC_PATH)

        tfgc_box_with_path = []

        for image_path in os.listdir(directories['raw_images_dir'])[:5]:
            tfgc_out = tfgc_infr_obj.inference( directories['raw_images_dir'] + image_path)
            tfgc_box_with_path.append(tfgc_out)

        return tfgc_box_with_path
    
    except Exception as e:
        print(f"Exception in tfgc-call, {e}")
        return None



"""
        TODO:
        The list returned by TFGC api is a list of tuple. The tuple conatain (list of boxes in the image, image_index)
        Each element of request list is a tuple of boxes for an image and image id.
            
            1. Pick an element from the main list.
            2. Pick the image by using the image_index.
            3. Iterate over the list of boxes.
            4. Make a temporary copy of the image and crop the box.
            5. Calculate cropped box size.
            6. Pick a random number. This will be unique id for this tfgc block.
            7. Rename the tfgc block as "picked_random_number.jpg"
"""

async def process_tfgc_output(tfgc_boxes_n_path, directories):
    for each_img_boxes in tfgc_boxes_n_path:
        image_path = each_img_boxes[1]
        boxes = each_img_boxes[0]

        page_image = Image.open(image_path)

        for idx, box in enumerate(boxes):                
            cropped_image = page_image.crop(box.tolist())

            cropped_version_name = str(idx) + "__" + image_path.split("/")[-1]  #keeping file extension for simplicity. Taking -1 with / split will give full name with extension.
            cropped_version_save_path = directories['tfgc_blocks'] + cropped_version_name
            cropped_image.save(cropped_version_save_path)

            # Place a white rectangle on that part of the page.
            page_image = place_rectangle_over_image(page_image, box=box, color="white", single_box=True)

        image_save_path =  directories['pages__notfgc'] + image_path.split("/")[-1]
        page_image.save(image_save_path)

