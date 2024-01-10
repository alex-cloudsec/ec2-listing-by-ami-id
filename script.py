import boto3

def list_instances_using_ami(ami_id):
    ec2 = boto3.client('ec2', region_name='us-east-1')  # Change the region

    # Function to get AMI name from AMI ID
    def get_ami_name(ami_id):
        ami_info = ec2.describe_images(ImageIds=[ami_id])
        return ami_info['Images'][0]['Name'] if ami_info['Images'] else 'Unknown AMI'

    # Collecting the list ec2 instances
    response = ec2.describe_instances()

    # Filter EC2 by AMI
    instances_using_ami = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            if instance['ImageId'] == ami_id:
                instance_id = instance['InstanceId']
                instance_name = ''
                # Getting EC2 names from Tags
                for tag in instance.get('Tags', []):
                    if tag['Key'] == 'Name':
                        instance_name = tag['Value']
                instances_using_ami.append((instance_id, instance_name))

    return instances_using_ami, get_ami_name(ami_id)

# Request AMI id
ami_id = input("Enter AMI ID (e.g., ami-123456789d321a34): ")

# Output
instances, ami_name = list_instances_using_ami(ami_id)
print(f"AMI Name: {ami_name}")
for instance_id, instance_name in instances:
    print(f"{instance_id}, ({instance_name})")
