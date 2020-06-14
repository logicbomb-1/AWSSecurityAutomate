import boto3
from botocore.exceptions import ClientError
import json
import os

ACL_RD_WARNING = "The S3 bucket ACL allows public read access."
PLCY_RD_WARNING = "The S3 bucket policy allows public read access."
ACL_WRT_WARNING = "The S3 bucket ACL allows public write access."
PLCY_WRT_WARNING = "The S3 bucket policy allows public write access."
COMPLIANT_FAIL = "NON_COMPLIANT"
RD_COMBO_WARNING = ACL_RD_WARNING + PLCY_RD_WARNING
WRT_COMBO_WARNING = ACL_WRT_WARNING + PLCY_WRT_WARNING

def policyNotifier(bucketName, s3client):
    try:
        bucketPolicy = s3client.get_bucket_policy(Bucket = bucketName)
        # notify that the bucket policy may need to be reviewed due to security concerns
        sns = boto3.client('sns')
        subject = "Potential compliance violation in " + bucketName + " bucket policy"
        message = "Potential bucket policy compliance violation. Please review: " + json.dumps(bucketPolicy['Policy'])
        # send SNS message with warning and bucket policy
        response = sns.publish(
            TopicArn = os.environ['TOPIC_ARN'],
            Subject = subject,
            Message = message
        )
    except ClientError as e:
        # error caught due to no bucket policy
        print("No bucket policy found; no alert sent.")

def lambda_handler(event, context):
    # instantiate Amazon S3 client
    s3 = boto3.client('s3')
    #resource = list(event['detail']['requestParameters']['evaluations'])[0]
    #bucketName = resource['complianceResourceId']
    #complianceFailure = event['detail']['requestParameters']['evaluations'][0]['complianceType']
    for i in range(len(event['detail']['requestParameters']['evaluations'])):
        bucketName = event['detail']['requestParameters']['evaluations'][i]['complianceResourceId']
        if(event['detail']['requestParameters']['evaluations'][i]['complianceType'] == COMPLIANT_FAIL):
            policyNotifier(bucketName, s3)
        
