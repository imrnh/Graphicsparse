import os, shutil
from PIL import Image
from pdf2image import convert_from_path

from utils.config import DIGITAL_OCEAN_SPACE_CONF, D_CONF


def create_necessary_dir():
    # Step-1: Make a dir with same name as unq id of this pdf to save all images in later steps.
    directories = {
        "raw_images_dir" : D_CONF.PROCESS_DIR + "raw_images/",
        "pages__notfgc" : D_CONF.PROCESS_DIR + "pages__no-tfgc/",
        "tfgc_blocks" : D_CONF.PROCESS_DIR + "tfgc/",
        "pages__nomecr":  D_CONF.PROCESS_DIR + "pages__no-mecr/",
        "mecr_blocks": D_CONF.PROCESS_DIR + "mecr/"
    }

    os.makedirs(D_CONF.PROCESS_DIR, exist_ok=True)        
    for folder_path in directories.values(): #iteratievly create other directories
        os.makedirs(folder_path, exist_ok=True)

    return directories



"""
@ Download file from digitalocean space.

"""

def download_pdf(do_client, req_id, local_save_path):
    do_client.download_file(DIGITAL_OCEAN_SPACE_CONF.BUCKET_NAME, f"{req_id}.pdf", local_save_path)


"""
    @ Extract all pages and save them into lib/tmp/raw_images directory.
"""

def extract_pages(local_path, directories):
    images = convert_from_path(local_path) #convert into image

    for idx in range(len(images)):  #save images into directory
        images[idx].save(f"{directories['raw_images_dir']}{idx+1}.jpg", 'JPEG')