import asyncio
from core.pdf_to_images import create_necessary_dir, download_pdf, extract_pages
from core.tfgc_inf import tfgc_extraction, process_tfgc_output
from core.mecr_inf import mecr_extraction, process_mecr_output

from utils.do_space_ops import create_dospaces_session
from utils.config import D_CONF

async def main(args):
    req_id = args['req_id']
    digital_ocean_client = create_dospaces_session()
    local_save_path = D_CONF.PROCESS_DIR + "file.pdf" #as this function is unique for each request, no need for unifying inside the function's processing..

    directories = create_necessary_dir()
    download_pdf(digital_ocean_client, req_id, local_save_path)
    extract_pages(local_save_path, directories)

    box_n_path = tfgc_extraction(directories)
    await process_tfgc_output(box_n_path, directories)

    box_n_path = mecr_extraction(directories)
    process_mecr_output(box_n_path, directories)


if __name__ == "__main__":
    dummy_args = {'req_id' : "1234"}
    asyncio.run(main(dummy_args))