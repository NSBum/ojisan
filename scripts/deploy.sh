set -e

BUCKET_NAME=www.ojisanseiuchi.com

hugo -v --noTimes=false

aws s3 sync --acl "public-read" --sse "AES256" public/ s3://$BUCKET_NAME --dryrun
