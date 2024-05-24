import boto3, os, botocore
from concurrent.futures import ProcessPoolExecutor
from .config import DIGITAL_OCEAN_SPACE_CONF


"""
    Create a session for digitalocean spaces
"""
def create_dospaces_session():
    session = boto3.session.Session()
    client = session.client('s3',
        endpoint_url=DIGITAL_OCEAN_SPACE_CONF.ENDPOINT_URL, # Find your endpoint in the control panel, under Settings. Prepend "https://".
        config=botocore.config.Config(s3={'addressing_style': 'virtual'}), # Configures to use subdomain/virtual calling format.
        region_name='nyc3', # Use the region in your endpoint.
        aws_access_key_id=DIGITAL_OCEAN_SPACE_CONF.DO_SPACE_ACCESS_KEY, # Access key pair. You can create access key pairs using the control panel or API.
        aws_secret_access_key=DIGITAL_OCEAN_SPACE_CONF.DO_SPACE_SECRET_KEY)
    
    return client



def dospace_file_upload(do_space_client, file_content, folder_name, file_name, file_ext="txt"):
    """
        Take text content and upload a text file into a folder.

        params:

            do_space_client: File upload client.
            file_content: Any file content. Can be image, video, text whatever.
            folder_name: Valid folder name. Set to none if a single file outside folders.
            file_name: Valid file name.
            file_ext: Valid file extension.

    """
    if do_space_client == None:
        do_space_client = create_dospaces_session()

    if not isinstance(file_content, bytes):
        file_content = file_content.encode() # convert to bytes if necessary

    if folder_name == None:
        file_path = f"{file_name}.{file_ext}"
    else:
        file_path = f'{folder_name}/{file_name}.{file_ext}'

    do_space_client.put_object(Bucket=DIGITAL_OCEAN_SPACE_CONF.BUCKET_NAME,
            Key= file_path, Body=file_content, ACL='private', )
