import os
from types import SimpleNamespace
from dotenv import load_dotenv

load_dotenv()


MINIMUM_NOPARALLEL_CORE = int(os.cpu_count() / 4) #miniumum number of cores to be out of parallel process on each process.

D_CONF = SimpleNamespace(
    PROCESS_DIR = "lib/tmp/",
)

os.makedirs(D_CONF.PROCESS_DIR, exist_ok=True)


DIGITAL_OCEAN_SPACE_CONF = SimpleNamespace(
    DO_SPACE_ACCESS_KEY = os.getenv('DIGITAL_OCEAN_SPACE_ACCESS_KEY'),
    DO_SPACE_SECRET_KEY = os.getenv('DIGITAL_OCEAN_SECRET_KEY'),
    ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com', 
    BUCKET_NAME = 'echoscript-pdf-n-text-space'
)

PROMPTS_LOC_CONF = SimpleNamespace(
    LLM_FORMATTING_PROMPT = "docs/gpt3_text_formatting_prompt.txt",
    TFGC_EXPLAINING_PROMPT = "docs/tfgc_prompt.txt",
)


DL_MODEL_CONF = SimpleNamespace(
    TFGC_PATH = "lib/models/tfgc_v2_yolov9c.pt",
    MECR_PATH = "lib/models/mecr_y8e_v1.pt"
)
