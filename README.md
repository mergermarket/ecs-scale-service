Set the desired count for an ECS service within an account

This container makes it easy to perform `aws ecs update-service --desired-count x ...`
for an ecs service running in another AWS account.

## Usage

    docker pull mergermarket/ecs-scale-service
    docker run -i \
        -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_SESSION_TOKEN \
        mergermarket/ecs-scale-service \
            --account myaccount \
            --role admin \
            --region eu-west-1 \
            --role-session-name "$JOB_NAME" \
            --desired-count 2 \
            --service aslive-dispatcher-service

## Options

* `--account` - name of the account in organisations for role to assume (required).
* `--role` - name of the role to assume (required).
* `--role-session-name` - session name for the role, so it's easy to identify who did this (required, unless called from an assumed role already).
* `--region` - region where the service is running (required unless `AWS_DEFAULT_REGION` is passed).
* `--service` - name of the service to redeploy (required).
* `--desired-count` - number of tasks to run (required).
* `--cluster` - cluster where the service is running (optional, default: `default`).
