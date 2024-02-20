import boto3
from datetime import datetime, timedelta, timezone

def get_s3_buckets_created_last_60_days(region):
    # Create a boto3 client for CloudTrail in the specified region
    cloudtrail_client = boto3.client('cloudtrail', region_name=region)

    # Get the current timestamp in UTC
    current_time = datetime.now(timezone.utc)

    # Calculate the timestamp 60 days ago
    sixty_days_ago = current_time - timedelta(days=60)

    # Query CloudTrail logs for S3 bucket creation events
    response = cloudtrail_client.lookup_events(
        LookupAttributes=[{'AttributeKey': 'EventName', 'AttributeValue': 'CreateBucket'}],
        StartTime=sixty_days_ago,
        EndTime=current_time
    )

    # Extract bucket names from the CloudTrail events
    bucket_names = set()
    for event in response['Events']:
        resources = event['Resources']
        for resource in resources:
            if resource['ResourceType'] == 'AWS::S3::Bucket':
                bucket_names.add(resource['ResourceName'])

    return bucket_names

def print_buckets_in_all_regions():
    # Get a list of all AWS regions
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

    # Iterate over each region and print the S3 bucket creation events
    for region in regions:
        bucket_names = get_s3_buckets_created_last_60_days(region)
        if bucket_names:
            print("****************************")
            print(f"List of S3 Buckets in {region}")
            print("****************************")
            for bucket_name in bucket_names:
                print(f"==> {bucket_name}")
                print("------------------------")
        else:
            continue
        print("****************************************************")

def main():
    print_buckets_in_all_regions()

if __name__ == "__main__":
    main()
