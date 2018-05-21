Replace an ECS service's containers without changing anything else.

This container makes it easy to perform `aws ecs update-service --force-new-deployment ...`
for an ecs service running in another AWS account.

Note: there shouldn't be an occassion where you need to do this as tasks should be
made to recover by themselves without needing to be killed. This is mainly useful
as a temporary workaround for things like memory leaks while you fix the underlying
cause.

## Usage

    docker pull mergermarket/ecs-redeploy-service
    docker run -i \
        -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_SESSION_TOKEN \
        mergermarket/ecs-redeploy-service \
            --account myaccount \
            --role admin \
            --region eu-west-1 \
            --role-session-name "$JOB_NAME" \
            --service aslive-dispatcher-service

## Options

* `--account` - name of the account in organisations for role to assume (required).
* `--role` - name of the role to assume (required).
* `--role-session-name` - session name for the role, so it's easy to identify who did this (required, unless called from an assumed role already).
* `--region` - region where the service is running (required unless `AWS_DEFAULT_REGION` is passed).
* `--cluster` - cluster where the service is running (optional, default: `default`).
* `--service` - name of the service to redeploy (required).
