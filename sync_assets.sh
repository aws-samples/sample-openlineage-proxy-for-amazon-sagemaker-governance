while getopts p:b: flag
do
    case "${flag}" in
        p) PROFILE_NAME=${OPTARG};;
        b) S3_BUCKET_NAME=${OPTARG};;
    esac
done

aws s3 sync ./code s3://${S3_BUCKET_NAME}/lineage-proxy/code --delete --profile $PROFILE_NAME
aws s3 sync ./stacks s3://${S3_BUCKET_NAME}/lineage-proxy/stacks --delete --profile $PROFILE_NAME