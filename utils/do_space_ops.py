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


def dospace_upload(args, dosClient=None, req_id=None, insideReqFolder=True):
    try:
        if dosClient == None:
            dosClient = create_dospaces_session()

        file_content, file_name = args
        if not isinstance(file_content, bytes):
            file_content = file_content.encode()  # Convert to bytes if necessary

        file_path = f'{req_id}/{file_name}.txt' if insideReqFolder else file_name
        dosClient.put_object(
            Bucket=DIGITAL_OCEAN_SPACE_CONF.BUCKET_NAME,
            Key= file_path,
            Body=file_content,
            ACL='private',
        )

        return True

    except Exception as e:
        print(f"Exception in digitalocean file upload {e}")
        return False, str(e)



# File upload test

# doclient = create_dospaces_session()
# text = "Hi, This is my text"
# res = upload_file_to_do_spaces(doclient, text, 'priv', 'hambaa')
# print(res)

