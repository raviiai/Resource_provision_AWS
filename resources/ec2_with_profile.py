import boto3
import csv
import argparse


def list_aws_profiles():
    session = boto3.Session()
    profiles = session.available_profiles
    return profiles


def main():
    # listing available profiles
    print("List of Available Profiles: ")
    print("-----------------------------")
    profiles = list_aws_profiles()
    for i in range(0, len(profiles)):
        print(f"{i + 1}. {profiles[i]}")
    print("-----------------------------")
    choice = int(input("Enter Number to select that profile: "))
    profile_name = profiles[choice - 1]
    print(f"Selected Profile: {profile_name}")
    print("------------------------------")

    # Initialize Boto3 session with the selected profile
    session = boto3.Session(profile_name=profile_name)

    # Get EC2 resource using the session
    ec2_resource = session.resource('ec2')

    regions = [region['RegionName'] for region in session.client('ec2').describe_regions()['Regions']]
    csv_file = 'ec2_instances.csv'
    field_names = ['InstanceId', 'Owner', 'PrivateIpAddress', 'PublicIpAddress', 'Region', 'State', 'Tags']

    # reading command line arguments
    args = parse_arguments()
    desired_tags = [tag.strip() for tag in args.tags.split(',')] if args.tags else None
    get_ec2(ec2_resource, regions, desired_tags, csv_file, field_names)
    print(f"CSV file '{csv_file}' has been created successfully.")


def parse_arguments():
    parser = argparse.ArgumentParser(description='Export EC2 instances information to a CSV file')
    parser.add_argument('-t', '--tags', type=str, help='Comma-separated list of tags to include in the CSV file')
    return parser.parse_args()


def get_ec2(ec2_resource, regions, desired_tags, csv_file, field_names):
    # Set to keep track of processed instance IDs
    processed_instances = set()

    # Open CSV file for writing
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()

        # Iterate over each region
        for region in regions:
            # Get all instances in the region
            instances = ec2_resource.instances.filter()
            # Iterate over each instance
            for instance in instances:
                # Ensure each instance is processed only once
                if instance.id not in processed_instances:
                    instance_tags = {tag['Key']: tag['Value'] for tag in instance.tags or []}
                    # If specific tags are provided, use them; otherwise, use default
                    if desired_tags:
                        specific_tags = {tag: instance_tags.get(tag, None) for tag in desired_tags}
                    else:
                        specific_tags = instance_tags
                    # Write instance details to CSV
                    writer.writerow({
                        'InstanceId': instance.id,
                        'Owner': instance_tags.get('AppOwner', None),
                        'PrivateIpAddress': instance.private_ip_address,
                        'PublicIpAddress': instance.public_ip_address,
                        'Region': region,
                        'State': instance.state['Name'],
                        'Tags': str(specific_tags)  # Convert dictionary to string
                    })
                    # Add instance ID to processed set
                    processed_instances.add(instance.id)


if __name__ == "__main__":
    main()
