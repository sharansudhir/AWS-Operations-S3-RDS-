import boto3
import json

def upload_file(s,bucket_name):
    client = boto3.client('s3')
    client.upload_file(s, bucket_name ,Key = s)
    print(s+" File Uploaded")


def create_bucket(bucket_name):
    client = boto3.client('s3')
    client.create_bucket(Bucket=bucket_name)
    print("Bucket Created Successfully")
    response = client.put_public_access_block(
    Bucket=bucket_name,
    PublicAccessBlockConfiguration={
        'BlockPublicAcls': True,
        'IgnorePublicAcls': True,
        'BlockPublicPolicy': True,
        'RestrictPublicBuckets': True})

    print("Public Access Disabled")

    response = client.put_bucket_acl(Bucket = bucket_name, GrantRead = 'id=d7f21188371ef451c3f59fe953f743ce04e1541592d2c92fb4d560a1a2927a98', GrantWrite = 'id=d7f21188371ef451c3f59fe953f743ce04e1541592d2c92fb4d560a1a2927a98', GrantReadACP = 'id=d7f21188371ef451c3f59fe953f743ce04e1541592d2c92fb4d560a1a2927a98')

    print("ACL Write Option Disabled for Bucket Owner")
    
def move(dest_bucket_name,source_bucket_name,filename):

    source = source_bucket_name+'/'+filename

    client = boto3.client('s3')
    response = client.copy_object(Bucket = dest_bucket_name, CopySource = source ,Key = filename)

    resource = boto3.resource('s3')
    obj = resource.Object(source_bucket_name,filename).delete()
    print('File Transfered Successfully')
       

# upload_file('Sharan.txt',"bucket01-sharan")

# create_bucket('bucket02-sharan')

# move('bucket02-sharan','bucket01-sharan','Sharan.txt')
