import boto3
import csv
import argparse

# Initialize Boto3 EC2 client
ec2_client = boto3.client('ec2')

# Get all regions
regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

csv_file = 'ec2_instances.csv'
field_names = ['InstanceId', 'Owner', 'PrivateIpAddress', 'PublicIpAddress', 'Region', 'State', 'Tags']

def parse_arguments():
    parser = argparse.ArgumentParser(description='Export EC2 instances information to a CSV file')
    parser.add_argument('-t', '--tags', type=str, help='Comma-separated list of tags to include in the CSV file')
    return parser.parse_args()

# Open CSV file for writing
def get_ec2(desired_tags):
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
                instance_tags = {tag['Key']: tag['Value'] for tag in instance.tags or []}
                
                # If specific tags are provided, use them; otherwise, use default
                if desired_tags:
                    specific_tags = {tag: instance_tags.get(tag, None) for tag in desired_tags}
                else:
                    specific_tags = instance_tags
                
                # Check if the desired tag value is None, if so, skip writing this instance to the CSV
                if desired_tags and None in specific_tags.values():
                    specific_tags = {}
                
                # Write instance details to CSV
                writer.writerow({
                    'InstanceId': instance.id,
                    'Owner': specific_tags.get('Owner', None),
                    'PrivateIpAddress': instance.private_ip_address,
                    'PublicIpAddress': instance.public_ip_address,
                    'Region': region,
                    'State': instance.state['Name'],
                    'Tags': specific_tags
                })


def main():
    args = parse_arguments()
    desired_tags = [tag.strip() for tag in args.tags.split(',')] if args.tags else None
    get_ec2(desired_tags)
    print(f"CSV file '{csv_file}' has been created successfully.")

if __name__ == "__main__":
    main()
