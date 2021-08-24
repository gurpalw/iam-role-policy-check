# This script finds all instance profiles that do not have a specific policy attached.

import boto3
import time
from botocore.exceptions import ClientError

iam = boto3.resource('iam')
instance_profiles = iam.instance_profiles.all()

client = boto3.client('iam')

allRoles = []
ssmEnabled = []
ssmDisabled = []

for instance_profile in instance_profiles:
    response = client.get_instance_profile(InstanceProfileName=instance_profile.name)
    roleName = response['InstanceProfile']['Roles'][0]['RoleName']
    allRoles.append(roleName)
    role = iam.Role(roleName)
    attached = client.list_attached_role_policies(
        RoleName=role.name
    )

    for policy in (attached['AttachedPolicies']):
        if policy['PolicyName'] == "AmazonSSMManagedInstanceCore":
           ssmEnabled.append(role.name)



for iamRole in allRoles:
    if iamRole not in ssmEnabled:
       ssmDisabled.append(iamRole)

#Print the roles without the policy we named.
print(ssmDisabled)
