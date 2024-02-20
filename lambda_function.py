import boto3
from datetime import datetime, timedelta, timezone

def list_lambda_functions_created_last_60_days():
    # Create a boto3 client for Lambda
    lambda_client = boto3.client('lambda')

    # Get the current timestamp
    current_time = datetime.now(timezone.utc)

    # Calculate the timestamp 60 days ago
    sixty_days_ago = current_time - timedelta(days=60)

    # List to store lambda function names and their respective regions
    functions_last_60_days = []

    # Get a list of all AWS regions
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

    # Iterate over each region
    for region in regions:
        try:
            # Create a boto3 client for Lambda in the current region
            lambda_client = boto3.client('lambda', region_name=region)

            # List all Lambda functions in the region
            response = lambda_client.list_functions()

            # Check if there are any functions
            if 'Functions' in response:
                for function_data in response['Functions']:
                    function_name = function_data['FunctionName']
                    # Get detailed information about the Lambda function
                    function = lambda_client.get_function(FunctionName=function_name)
                    creation_time_str = str(function['Configuration']['LastModified'])
                    # Parse creation time string into a datetime object
                    creation_time = datetime.strptime(creation_time_str, "%Y-%m-%dT%H:%M:%S.%f%z")
                    # Check if the Lambda function was created within the last 60 days
                    if creation_time > sixty_days_ago:
                        functions_last_60_days.append((function_name, region))
        except Exception as e:
            print(f"Error processing region {region}: {e}")

    return functions_last_60_days

def main():
    lambda_functions_last_60_days = list_lambda_functions_created_last_60_days()
    print("**************************************************")
    print("Lambda functions created in the last 60 days:")
    print("**************************************************")
    if lambda_functions_last_60_days:
        for function_name, region in lambda_functions_last_60_days:
            print("--------------------------------------")
            print(f"Function Name: {function_name}\nRegion: {region}")
    else:
        print("No Lambda functions were created in the last 60 days.")
        print("--------------------------------------")

if __name__ == "__main__":
    main()
