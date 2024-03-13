import boto3
import csv

# Initialize Boto3 EC2 client
ec2_client = boto3.client('ec2')

# Get all regions
regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

csv_file = 'ec2_instances.csv'
field_names = ['InstanceId', 'Owner', 'PrivateIpAddress', 'PublicIpAddress', 'Region', 'State', 'Tags']

# Open CSV file for writing
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=field_names)
    writer.writeheader()

    # Iterate over each region
    for region in regions:
        # Initialize EC2 resource for the current region
        ec2_resource = boto3.resource('ec2', region_name=region)
        
        # Get all instances in the region
        instances = ec2_resource.instances.all()
        
        # Iterate over each instance
        for instance in instances:
            tags = {tag['Key']: tag['Value'] for tag in instance.tags or []}
            
            # Write instance details to CSV
            writer.writerow({
                'InstanceId': instance.id,
                'Owner': instance.tags[0]['Value'] if instance.tags and instance.tags[0]['Key'] == 'Owner' else '',
                'PrivateIpAddress': instance.private_ip_address,
                'PublicIpAddress': instance.public_ip_address,
                'Region': region,
                'State': instance.state['Name'],
                'Tags': tags
            })

print(f"CSV file '{csv_file}' has been created successfully.")
