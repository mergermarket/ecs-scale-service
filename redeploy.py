import argparse
import sys
import re
import boto3

parser = argparse.ArgumentParser(description='Redeploy an ECS service')
parser.add_argument(
    '--account', required=True, help='The account to assume the role in'
)
parser.add_argument(
    '--role', default='admin', help='The account to assume the role in'
)
parser.add_argument(
    '--role-session-name', default=None,
    help='An identifier for you, to make it easy to see who did this'
)
parser.add_argument('--region', help='The region the service is in')
parser.add_argument(
    '--cluster', default='default', help='The ECS cluster for the service'
)
parser.add_argument('--service', required=True, help='The ECS service')
args = parser.parse_args()

session = boto3.Session()

orgs = session.client('organizations')

try:
    accounts = {
        account['Name']: account['Id']
        for page in orgs.get_paginator('list_accounts').paginate()
        for account in page['Accounts']
    }
except Exception as e:
    print(str(e), file=sys.stderr)
    sys.exit(1)
account_id = accounts.get(args.account)
if account_id is None:
    print(f'unknown account {args.account}', file=sys.stderr)
    sys.exit(1)
role_arn = f'arn:aws:iam::{account_id}:role/{args.role}'

sts = boto3.client('sts')

if args.role_session_name is not None:
    role_session_name = re.sub(r'[^\w=,.@-]', '-', args.role_session_name)[:64]
else:
    caller_identity = sts.get_caller_identity()
    match = re.search(r':assumed-role/[^/]+/([^/]+)$', caller_identity['Arn'])
    if match is None:
        print(
            f'--role-session-name is required for IAM user credentials',
            file=sys.stderr
        )
        sys.exit(1)
    role_session_name = match.group(1)

try:
    credentials = sts.assume_role(
        RoleArn=role_arn,
        RoleSessionName=role_session_name
    )['Credentials']
except Exception as e:
    print(f'could not assume role {role_arn}:\n\n{e}', file=sys.stderr)
    sys.exit(1)

print(f'assumed role {role_arn}', file=sys.stderr)

ecs = boto3.client(
    'ecs',
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey'],
    aws_session_token=credentials['SessionToken'],
    region_name=args.region
)

print('updating service...', file=sys.stderr)

ecs.update_service(
    cluster=args.cluster,
    service=args.service,
    forceNewDeployment=True,
)

print(
    'waiting for service to stabilise (15 second interval, 40 attempts)...',
    file=sys.stderr
)

ecs.get_waiter('services_stable').wait(
    cluster=args.cluster,
    services=[args.service],
)

print('done.', file=sys.stderr)
