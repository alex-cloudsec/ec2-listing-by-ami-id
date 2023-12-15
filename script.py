import boto3

def list_instances_using_ami(ami_id):
    ec2 = boto3.client('ec2', region_name='us-east-1')  # Change the region

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

    return instances_using_ami

# Request AMI id
ami_id = input("Enter AMI ID (e.g., ami-0351343259d321a34): ")

# Output
instances = list_instances_using_ami(ami_id)
for instance_id, instance_name in instances:
    print(f"{instance_id}, ({instance_name})")
  
