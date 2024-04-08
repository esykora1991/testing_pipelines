import yfinance as yf

# Download SPY data from the last year
data = yf.download('SPY', start='2020-01-01', end='2023-01-01')

# Save data to a CSV file
data.to_csv('SPY_data.csv')


from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.core.exceptions import ResourceExistsError
from azure.identity import DefaultAzureCredential

account_url = "https://blobstorageems001.blob.core.windows.net"
default_credential = DefaultAzureCredential()  # Logged into Azure account with VS Code extension. Added RABC to storage account.
blob_service_client = BlobServiceClient(account_url, credential=default_credential)

#connection_string = 'DefaultEndpointsProtocol=https;AccountName=blobstorageems001;AccountKey=;EndpointSuffix=core.windows.net'
#blob_service_client = BlobServiceClient.from_connection_string(conn_str=connection_string)

container_name = "data"
local_file_name = "SPY_data.csv"
upload_file_path = "SPY_data.csv"

# Create a blob client using the local file name as the name for the blob
try:
    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
    
    # Check if the blob already exists
    if blob_client.exists():
        # Handle the case when the blob already exists
        # You can either skip the upload or delete the existing blob before uploading the new one
        # For example, you can delete the existing blob before uploading the new one
        blob_client.delete_blob()
    
    # Upload the created file
    with open(file=upload_file_path, mode="rb") as data:
        blob_client.upload_blob(data)
    
    print("File uploaded to Azure Blob Storage")
    
except ResourceExistsError as e:
    print("Error: The specified blob already exists.")
    print(e)
