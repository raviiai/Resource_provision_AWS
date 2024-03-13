#!/bin/bash

# Define the output CSV file
output_file="ec2_instances.csv"

# Write CSV header
echo "InstanceId,Owner,PrivateIpAddress,PublicIpAddress,Region,State,Tags" > "$output_file"

# Get list of all regions
regions=$(aws ec2 describe-regions --query "Regions[*].RegionName" --output text)

# Loop through each region
for region in $regions; do
    # Get EC2 instances information for the current region
    instances=$(aws ec2 describe-instances --region "$region" --output json)

    # Extract required details and append to CSV
    echo "$instances" | jq -r '.Reservations[] | .Instances[] | [.InstanceId, .OwnerId, .PrivateIpAddress, .PublicIpAddress, "'"$region"'", .State.Name, (.Tags | map(.Key + ":" + .Value) | join(", "))] | @csv' >> "$output_file"
done

echo "CSV file generated: $output_file"
