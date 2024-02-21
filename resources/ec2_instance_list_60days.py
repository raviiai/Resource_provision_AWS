import boto3
from datetime import datetime, timedelta, timezone

################################################
## Function to list all EC2 in last 60 Days....
################################################

def get_ec2_instances_created_last_60_days(region):
    # Get the current time
    ec2_client = boto3.client("ec2", region_name=region)

    current_time = datetime.now()

    # Calculate the time 60 days ago in UTC
    sixty_days_ago = current_time - timedelta(days=60)

    # Make sixty_days_ago offset-aware by adding timezone information
    sixty_days_ago = sixty_days_ago.replace(tzinfo=timezone.utc)

    # Get all EC2 instances
    response = ec2_client.describe_instances()

    # List to store instances created in the last 60 days
    instances_last_60_days = []

    # Iterate through reservations
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            # Extract the creation timestamp of the instance
            launch_time_str = str(instance['LaunchTime'])

            # Attempt to parse the launch time string with flexible format
            try:
                launch_time = datetime.strptime(launch_time_str, "%Y-%m-%d %H:%M:%S%z")
            except ValueError:
                # Handle variations in datetime format returned by AWS
                launch_time = datetime.strptime(launch_time_str, "%Y-%m-%d %H:%M:%S.%f%z")

            # Check if the instance was launched within the last 60 days
            if launch_time > sixty_days_ago:
                instances_last_60_days.append(instance)

    return instances_last_60_days

def print_instance_details(instances,region):
    for instance in instances:
        # Print instance details
        print("-------------------------")
        print("Instance ID: ", instance['InstanceId'])
        print("Launch Time: ", instance['LaunchTime'])
        print("Instance State: ", instance['State']['Name'])
        print("Region : ", region)
        print("-------------------------")


##########################################################
## Main Function
##########################################################

def main():
    ## EC2 instances
    print("*******************************************************")
    print("   List of instances Created in last 60 Days....")
    print("*******************************************************")
    ec2_regions = [region['RegionName'] for region in boto3.client('ec2').describe_regions()['Regions']]
    
    instances_last_60_days = []
    for region in ec2_regions:
        instances_last_60_days.extend(get_ec2_instances_created_last_60_days(region))
    
    if len(instances_last_60_days) == 0:
        print("No Instance Created in last 60 Days....")
    else:
        print_instance_details(instances_last_60_days,region)

if __name__ == "__main__":
    main()
