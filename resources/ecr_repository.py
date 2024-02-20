import boto3
from datetime import datetime, timedelta, timezone

def get_ecr_repositories_created_last_60_days():
    # Create a boto3 client for CloudTrail
    cloudtrail_client = boto3.client('cloudtrail')

    # Get the current timestamp
    current_time = datetime.now(timezone.utc)

    # Calculate the timestamp 60 days ago
    sixty_days_ago = current_time - timedelta(days=60)

    # Dictionary to store repository names and their respective regions
    repository_regions = {}

    # Get a list of all AWS regions
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
    # Iterate over each region
    for region in regions:
        # Create a boto3 client for CloudTrail in the current region
        cloudtrail_client = boto3.client('cloudtrail', region_name=region)

        # Query CloudTrail logs for ECR repository creation events
        response = cloudtrail_client.lookup_events(
            LookupAttributes=[{'AttributeKey': 'EventName', 'AttributeValue': 'CreateRepository'}],
            StartTime=sixty_days_ago,
            EndTime=current_time
        )

        # Extract repository names from the CloudTrail events
        for event in response['Events']:
            resources = event['Resources']
            for resource in resources:
                if resource['ResourceType'] == 'AWS::ECR::Repository':
                    repository_name = resource['ResourceName']
                    repository_regions[repository_name] = region

    return repository_regions

def main():
    repository_regions = get_ecr_repositories_created_last_60_days()
    print("ECR repositories created in the last 60 days:")
    if repository_regions:
        for repository_name, region in repository_regions.items():
            print("--------------------------")
            print(f"Repository Name: {repository_name},\nRegion: {region}")
            print("--------------------------")

    else:
        print("No ECR repositories were created in the last 60 days.")

if __name__ == "__main__":
    main()
