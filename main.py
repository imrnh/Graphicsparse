import asyncio, os
from manager.pdf_to_images import create_necessary_dir, download_pdf, extract_pages
from manager.tfgc_inf import tfgc_extraction, process_tfgc_output
from manager.mecr_inf import mecr_extraction, process_mecr_output

from utils.do_space_ops import create_dospaces_session
from utils.zipping_necessary_files import zip_necessary, upload_necessary_zip
from utils.config import D_CONF

async def main(args):
    req_id = args['req_id']
    secret_token = args['secret_token']

    if secret_token != os.getenv("REQUEST_SECRET_TOKEN"):
        return "Unauthorized"

    digital_ocean_client = create_dospaces_session()
    local_save_path = D_CONF.PROCESS_DIR + "file.pdf" #as this function is unique for each request, no need for unifying inside the function's processing..

    directories = create_necessary_dir()
    download_pdf(digital_ocean_client, req_id, local_save_path)
    extract_pages(local_save_path, directories)

    box_n_path = tfgc_extraction(directories)
    await process_tfgc_output(box_n_path, directories)

    box_n_path = mecr_extraction(directories)
    process_mecr_output(box_n_path, directories)

    zip_path = zip_necessary(directories)
    upload_necessary_zip(digital_ocean_client, zip_path, req_id)


    #Trigger digitalocean function, do-fn send ACK, if not, retry 3 times. ACK found = this instance die.


if __name__ == "__main__":
    dummy_args = {'req_id' : "1234", "secret_token" : os.getenv("REQUEST_SECRET_TOKEN")}
    asyncio.run(main(dummy_args))