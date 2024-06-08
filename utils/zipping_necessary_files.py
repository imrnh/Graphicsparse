import os
import shutil

from .do_space_ops import dospace_file_upload
from .config import D_CONF

"""
    This function zip all the images of the following directory. Each directory have seperate zip.

        1. no-mecr (i.e. pages without MECR and TFGC)
        2. mecr (i.e. all math eqn blocks)
        3. tfgc (i.e. all tfgc images)



    Return:
        a list naming all the zip files
"""


def zip_necessary(directories):
    no_mecr_path = directories['pages__nomecr']
    mecr_path = directories['mecr_blocks']
    tfgc_path = directories['tfgc_blocks']
    mecr_idx_map_path = directories['mecr_eqn_idx_maps']

    no_mecr_zip = D_CONF.PROCESS_DIR + "zip/no_mecr"
    mecr_zip = D_CONF.PROCESS_DIR + "zip/mecr"
    tfgc_zip = D_CONF.PROCESS_DIR + "zip/tfgc"
    mecr_idx_map_zip = D_CONF.PROCESS_DIR + "zip/mecr_idx_map"

    os.makedirs(D_CONF.PROCESS_DIR + "zip", exist_ok=True)

    shutil.make_archive(base_name=no_mecr_zip, format = "zip", root_dir=no_mecr_path)
    shutil.make_archive(base_name=mecr_zip, format = "zip", root_dir=mecr_path)
    shutil.make_archive(base_name=tfgc_zip, format = "zip", root_dir=tfgc_path)
    shutil.make_archive(base_name=mecr_idx_map_zip, format = "zip", root_dir=mecr_idx_map_path)

    return [no_mecr_zip, mecr_zip, tfgc_zip, mecr_idx_map_zip]



"""

    Upload all the zip file into do-space one by one

"""
def upload_necessary_zip(digital_ocean_client, zip_path, req_id):
    for file_path in zip_path:
        file_name = file_path.split("/")[-1].split(".")[0] # as I know zip file name are no_mecr.zip, mecr.zip and tfgc.zip and therefore after splitting through ".", first item is actual name of the file
        with open(file_path + ".zip", "rb") as z_file:
            file_content = z_file.read()
            dospace_file_upload(digital_ocean_client, file_content, req_id, file_name, "zip")