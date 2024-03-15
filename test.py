import os

def list_aws_profiles():
    # Get the path to the AWS configuration directory
    aws_config_dir = os.path.expanduser("~/.aws")
    
    # Path to the config and credentials files
    config_file = os.path.join(aws_config_dir, "config")
    credentials_file = os.path.join(aws_config_dir, "credentials")
    
    # List to store profile names
    profiles = []
    
    # Read profile names from the config file
    with open(config_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith("[profile"):
                profile_name = line.split("[profile ")[1].split("]")[0]
                profiles.append(profile_name)
    
    # Read profile names from the credentials file
    with open(credentials_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith("["):
                profile_name = line.split("[")[1].split("]")[0]
                profiles.append(profile_name)
    
    # Remove duplicates
    profiles = list(set(profiles))
    
    return profiles

# List all AWS profiles
profiles = list_aws_profiles()
print("AWS Profiles:")
for profile in profiles:
    print("-", profile)
