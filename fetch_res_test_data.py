from google.cloud import storage
import os
import re
from pathlib import Path

# Load Google Cloud Storage client
path_to_private_key = 'fifth-compass-415612-76f634511b19.json'  # Path to your service account key file
client = storage.Client.from_service_account_json(json_credentials_path=path_to_private_key)


def extract_bucket_from_path(path):
    # Extract bucket name using regular expression
    match = re.match(r"https://console\.cloud\.google\.com/storage/browser/([^/]+)/?", path)
    if match:
        bucket_name = match.group(1)
        return bucket_name
    else:
        return None

def download_files(bucket_name, source_blob_prefix, destination_directory):
    bucket_name = extract_bucket_from_path(bucket_name)
    if bucket_name is not None:
        # Create the directory locally
        Path(destination_directory).mkdir(parents=True, exist_ok=True)        
        try:
            bucket = storage.Bucket(client, bucket_name)
            bucket = client.bucket(bucket_name)
            
            blobs = bucket.list_blobs(prefix=source_blob_prefix)
            
            for blob in blobs:
                if not blob.name.endswith('/') and blob.content_type in ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                    # Construct destination blob path
                    destination_blob_path = os.path.join(destination_directory, os.path.basename(blob.name))
                    blob.download_to_filename(destination_blob_path)
        
        except Exception as e:
            print(f"Error downloading files: {e}")

# if __name__ == "__main__":
#    download_files('https://console.cloud.google.com/storage/browser/hackathon1415', 'JD/', 'jobstrainingdata')
