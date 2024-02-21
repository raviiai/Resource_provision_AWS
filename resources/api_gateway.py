import boto3
from datetime import datetime, timedelta, timezone

# Get a list of all available AWS regions
ec2_client = boto3.client('ec2')
regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
print("**********************************************")
print("List of API Gateways Created in last 60days...")
print("**********************************************")
# Iterate through each region
for region in regions:
 
    # Initialize the Boto3 client for API Gateway in the current region
    client = boto3.client('apigateway', region_name=region)

    # Get the current date
    current_date = datetime.now(timezone.utc)

    # Calculate the date 60 days ago
    start_date = current_date - timedelta(days=60)

    # Convert the dates to strings in ISO 8601 format
    start_date_str = start_date.strftime('%Y-%m-%dT%H:%M:%S')
    current_date_str = current_date.strftime('%Y-%m-%dT%H:%M:%S')

    # Call the API Gateway's get_rest_apis method to retrieve the list of APIs
    response = client.get_rest_apis()

    # Iterate through each API Gateway
    for api in response['items']:
        # Check if the API was created between the specified date range
        if str(api['createdDate']) >= start_date_str and str(api['createdDate']) <= current_date_str:
            print("API Name:", api['name'])
            print("API ID:", api['id'])
            print("Created Date:", api['createdDate'])
            print(f"Region: {region}")
            print("---------------------------------")
