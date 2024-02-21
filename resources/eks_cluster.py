import boto3
from datetime import datetime, timedelta, timezone

def get_eks_clusters_created_last_60_days(region):
    # Get the current time
    eks_client = boto3.client("eks", region_name=region)

    current_time = datetime.now()

    # Calculate the time 60 days ago in UTC
    sixty_days_ago = current_time - timedelta(days=60)

    # Make sixty_days_ago offset-aware by adding timezone information
    sixty_days_ago = sixty_days_ago.replace(tzinfo=timezone.utc)

    # Get all Amazon EKS clusters
    response = eks_client.list_clusters()

    # List to store clusters created in the last 60 days
    clusters_last_60_days = []

    # Iterate through each cluster
    for cluster_name in response['clusters']:
        # Get cluster details
        cluster_info = eks_client.describe_cluster(name=cluster_name)
        creation_time = cluster_info['cluster']['createdAt']
        
        # Check if the cluster was created within the last 60 days
        if creation_time > sixty_days_ago:
            clusters_last_60_days.append(cluster_info['cluster'])

    return clusters_last_60_days

def print_cluster_details(clusters, region):
    for cluster in clusters:
        # Print cluster details
        print("-------------------------")
        print("Cluster Name: ", cluster['name'])
        print("Created At: ", cluster['createdAt'])
        print("Status: ", cluster['status'])
        print("Region: ", region)
        print("-------------------------")


def main():
    print("*******************************************************")
    print("   List of Amazon EKS Clusters Created in Last 60 Days")
    print("*******************************************************")
    eks_regions = [region['RegionName'] for region in boto3.client('ec2').describe_regions()['Regions']]
    
    clusters_last_60_days = []
    for region in eks_regions:
        clusters_last_60_days.extend(get_eks_clusters_created_last_60_days(region))
    
    if len(clusters_last_60_days) == 0:
        print("No Amazon EKS Clusters Created in the Last 60 Days")
        print("-------------------------")
    else:
        print_cluster_details(clusters_last_60_days, region)

if __name__ == "__main__":
    main()
    