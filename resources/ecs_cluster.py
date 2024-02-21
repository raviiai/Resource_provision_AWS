# import boto3
# from datetime import datetime, timedelta, timezone

# def extract_creation_date(cluster_info):
#     # Extract creation date from the 'clusters' list in the response
#     for cluster in cluster_info.get('clusters', []):
#         creation_date_str = cluster.get('createdAt')
#         if creation_date_str:
#             # Convert creation date string to datetime object
#             creation_date = datetime.strptime(creation_date_str, "%Y-%m-%dT%H:%M:%S.%f%z")
#             return creation_date

# def list_ecs_clusters_created_last_60_days():
#     # Get all available regions
#     ec2_client = boto3.client('ec2')
#     regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

#     # List to store ECS clusters created in the last 60 days
#     ecs_clusters_last_60_days = []

#     # Get the current time
#     current_time = datetime.now(timezone.utc)

#     # Calculate the time 60 days ago
#     start_time = current_time - timedelta(days=60)

#     # Iterate through each region
#     for region in regions:
#         ecs_client = boto3.client('ecs', region_name=region)

#         # List ECS clusters in the region
#         response = ecs_client.list_clusters()

#         # Iterate through each cluster
#         for cluster_arn in response['clusterArns']:
#             # Describe the cluster to get its creation time
#             cluster_info = ecs_client.describe_clusters(clusters=[cluster_arn])

#             # Extract creation date from the cluster information
#             creation_date = extract_creation_date(cluster_info)

#             # Check if the creation date is within the last 60 days
#             if creation_date and creation_date >= start_time:
#                 ecs_clusters_last_60_days.append((cluster_arn, region))

#     return ecs_clusters_last_60_days

# def main():
#     print("**********************************************************")
#     print("ECS Clusters created in the last 60 days in all regions:")
#     print("**********************************************************")

#     ecs_clusters_last_60_days = list_ecs_clusters_created_last_60_days()

#     if not ecs_clusters_last_60_days:
#         print("No ECS Clusters created in the last 60 days.")
#     else:
#         for cluster_arn, region in ecs_clusters_last_60_days:
#             print(f"Cluster ARN: {cluster_arn}\nRegion: {region}")
#             print("-------------------------------------------")

# if __name__ == "__main__":
#     main()


import boto3

def list_ecs_clusters_in_all_regions():
    # Create a Boto3 EC2 client
    ec2_client = boto3.client('ec2')

    # Get a list of all available AWS regions
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

    # Iterate over each region
    for region in regions:
        # Create a Boto3 ECS client for the current region
        ecs_client = boto3.client('ecs', region_name=region)

        # Retrieve a list of ECS clusters in the current region
        response = ecs_client.list_clusters()

        # Extract cluster ARNs from the response
        cluster_arns = response['clusterArns']

        # If there are no ECS clusters in the region, print a message
        if not cluster_arns:
            continue

        else:
            # Iterate over each cluster ARN and print the cluster name
            for cluster_arn in cluster_arns:
                # Extract the cluster name from the ARN
                cluster_name = cluster_arn.split('/')[-1]
                print(f"Cluster Name: {cluster_name}\nRegion      : {region}")
                print("--------------------------------")

def main():
    print("********************************************")
    print("Listing ECS Clusters in every region in AWS:")
    print("********************************************")
    list_ecs_clusters_in_all_regions()

if __name__ == "__main__":
    main()
