import boto3
from datetime import datetime, timedelta, timezone

def list_dynamodb_tables_created_last_60_days():
    # Create a boto3 client for CloudTrail
    cloudtrail_client = boto3.client('cloudtrail')

    # Get the current timestamp
    current_time = datetime.now(timezone.utc)

    # Calculate the timestamp 60 days ago
    sixty_days_ago = current_time - timedelta(days=60)

    # List to store table names and their respective regions
    tables_last_60_days = []

    # Get a list of all AWS regions
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
    #regions = ["ap-south-1"]

    # Iterate over each region
    for region in regions:
        # Create a boto3 client for CloudTrail in the current region
        cloudtrail_client = boto3.client('cloudtrail', region_name=region)

        # Query CloudTrail logs for DynamoDB table creation events
        response = cloudtrail_client.lookup_events(
            LookupAttributes=[{'AttributeKey': 'EventName', 'AttributeValue': 'CreateTable'}],
            StartTime=sixty_days_ago,
            EndTime=current_time
        )

        # Extract table names and regions from the CloudTrail events
        for event in response['Events']:
            table_arn = event['Resources'][0]['ResourceName']
            table_name = table_arn.split('/')[-1]  # Extract table name from ARN
            tables_last_60_days.append((table_name, region))

    return tables_last_60_days

def main():
    tables_last_60_days = list_dynamodb_tables_created_last_60_days()
    print("***********************************************")
    print("DynamoDB tables created in the last 60 days:")
    print("***********************************************")
    if tables_last_60_days:
        for table_name, region_name in tables_last_60_days:
            print("------------------------------")
            print(f"Table Name: {table_name},\nRegion: {region_name}")
    else:
        print("No DynamoDB tables were created in the last 60 days.")

if __name__ == "__main__":
    main()
