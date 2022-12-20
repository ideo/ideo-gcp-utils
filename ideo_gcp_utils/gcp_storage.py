import os
from pathlib import Path
from google.cloud import storage
from requests.exceptions import ConnectionError


class Bucket:

    def __init__(self, bucket_name, credentials=None):
        self.bucket_name = bucket_name
        self.credentials = credentials

        if self.credentials:
            self.client = storage.Client(credentials=self.credentials)
        else:
            self.client = storage.Client()
    

    def get_bucket_object_metadata(self):
        # storage_client = storage.Client()
        blobs = self.client.list_blobs(self.bucket_name)

        obj_metadata = [{
            "Name":     blob.name,
            "Size":     blob.size,
            "Last Updated":  blob.updated,
        } for blob in blobs]
        return obj_metadata


    def list_bucket_objects(self):
        """
        Pings the bucket to return the names of all the files
        """
        # storage_client = storage.Client()
        blobs = self.client.list_blobs(self.bucket_name)
        blob_names = [blob.name for blob in blobs]
        return blob_names


    def download_file(self, filename, data_dir):
        """
        Download bucket object using the default script
        """
        # FIXME: concatenation of data dir and filename depending on type
        if data_dir[-1]=='/':
            data_dir = data_dir[:-1]
        destination_filename = f"{data_dir}/{filename}"
        # Bucket.download_blob(self.bucket_name, filename, destination_filename)
        self.download_blob(self.bucket_name, filename, destination_filename)


    def upload_file(self, filename, data_dir):
        """
        Upload a file, first attempt is the default script, if that fails the 
        second attempt adjusts the chunk size and tries again. Curiously, it was
        increasing the chunk size that helped the call succeed with low upload 
        speeds
        """
        # FIXME: add scraped data folder to session state 
        # (are we missing a potential mkdir here if reddit_data doesn't exist)
        # FIXME: concatenation of data dir and filename depending on type
        if data_dir[-1]=='/':
            data_dir = data_dir[:-1]
        source_filename = f"{data_dir}/{filename}"
        try:
            # Bucket.upload_blob(self.bucket_name, source_filename, filename)
            self.upload_blob(self.bucket_name, source_filename, filename)

        except ConnectionError:
            warning_message = """
            Upload timed out. Trying again, adjusting for low internet speeds.
            """
            # TODO: return warnings as objects or logger
            # st.warning(warning_message)
            
            ## For slow upload speed
            chunk_size = 20 #mb
            chunk_size *= 1024 * 1024
            storage.blob._DEFAULT_CHUNKSIZE = chunk_size
            storage.blob._MAX_MULTIPART_SIZE = chunk_size
            # Bucket.upload_blob(self.bucket_name, source_filename, filename)
            self.upload_blob(self.bucket_name, source_filename, filename)
            


    ################### Google Cloud Storage Example Scripts ###################
    # The follow example scripts were taken from the following documentation:
    # https://cloud.google.com/storage/docs/reference/libraries#more_examples

    # @staticmethod
    def download_blob(self, bucket_name, source_blob_name, destination_file_name):
        """Downloads a blob from the bucket."""
        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"

        # The ID of your GCS object
        # source_blob_name = "storage-object-name"

        # The path to which the file should be downloaded
        # destination_file_name = "local/path/to/file"

        # storage_client = storage.Client()

        bucket = self.client.bucket(bucket_name)

        # Construct a client side representation of a blob.
        # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
        # any content from Google Cloud Storage. As we don't need additional data,
        # using `Bucket.blob` is preferred here.
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)

        print(
            "Downloaded storage object {} from bucket {} to local file {}.".format(
                source_blob_name, bucket_name, destination_file_name
            )
        )

    # @staticmethod
    def upload_blob(self, bucket_name, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"
        # The path to your file to upload
        # source_file_name = "local/path/to/file"
        # The ID of your GCS object
        # destination_blob_name = "storage-object-name"

        print("Uploading to cloud...")
        # storage_client = storage.Client()
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        print(storage.blob._MAX_MULTIPART_SIZE)
        blob.upload_from_filename(source_file_name)

        print(f"File {source_file_name} uploaded to {destination_blob_name}.")
