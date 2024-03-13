#!/bin/bash

# Define the output CSV file
output_file="instances.csv"

# Get a list of regions
regions=$(aws ec2 describe-regions --query 'Regions[*].RegionName' --output text)

# Create the CSV file with header
echo "InstanceId,Region,Owner,PrivateIP, PublicIP, State, Tags" > "$output_file"

# Iterate over each region
for region in $regions; do
    echo "Instances in region: $region"
    # Run the command and append output to the CSV file
    #aws ec2 describe-instances --region "$region" --query 'Reservations[*].Instances[*].[InstanceId, PublicIpAddress, PrivateIpAddress]' --output text | awk -v region="$region" -F'\t' '{OFS=","} {print region, $1, $2, $3}' >> "$output_file"
    #echo "InstanceId,Region,Owner,PrivateIP,PublicIP,State,Tags" > "$output_file"
    aws ec2 describe-instances --region "$region" --query 'Reservations[*].Instances[*].[InstanceId,Placement.AvailabilityZone,OwnerId,PrivateIpAddress,PublicIpAddress,State.Name,Tags]' --output text | awk -v region="$region" -F'\t' '{OFS=","} {print $1, region, $3, $4, $5, $6, $7}' >> "$output_file"

    echo "----------------------------------------"
done

echo "Output written to $output_file"
