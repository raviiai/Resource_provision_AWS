#!/bin/bash

# Define the output CSV file
output_file="instances.csv"

# Get a list of regions
regions=$(aws ec2 describe-regions --query 'Regions[*].RegionName' --output text)

# Create the CSV file with header
echo "InstanceId,Region,Owner,PrivateIP, PublicIP, State" > "$output_file"

# Define the tags you want to filter for
tags="Name,Environment,Project"  # Example tags: Name, Environment, Project

# Iterate over each region
for region in $regions; do
    echo "Instances in region: $region"
    aws ec2 describe-instances --region "$region" --query "Reservations[*].Instances[*].[InstanceId,Placement.AvailabilityZone,OwnerId,PrivateIpAddress,PublicIpAddress,State.Name]" --output text | awk -v region="$region" -F'\t' '{OFS=","} {print $1, region, $3, $4, $5, $6, $7}' >> "$output_file"

    echo "----------------------------------------"
done

echo "Output written to $output_file"
