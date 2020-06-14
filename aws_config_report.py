import boto3

client = boto3.client('config')
region_name = {'us-west-2','ap-south-1','ap-southeast-1'}

for region in region_name:
    response = client.get_aggregate_config_rule_compliance_summary(
        ConfigurationAggregatorName='aws_config_alert',
        Filters={
            'AccountId': '4******5',
            'AwsRegion': region
        },
        Limit=123,
    )
    print "Total Non-compliant rule in region ", region,": ",response['AggregateComplianceCounts'][0]['ComplianceSummary']['NonCompliantResourceCount']['CappedCount']

config_rules = {'s3-bucket-public-read-prohibited','s3-account-level-public-access-blocks','rds-snapshots-public-prohibited','redshift-cluster-public-access-check','root-account-mfa-enabled','multi-region-cloudtrail-enabled','db-instance-backup-enabled','s3-bucket-public-read-prohibited','s3-bucket-public-write-prohibited','rds-instance-public-access-check','multi-region-cloudtrail-enabled','s3-bucket-public-read-prohibited','db-instance-backup-enabled','rds-instance-public-access-check'}

for region in region_name:
    client = boto3.client('config',region_name=region)
    print "Region: ", region
    for id in  config_rules:
        response = client.get_compliance_details_by_config_rule(
            ConfigRuleName=id,
            ComplianceTypes=[
                'NON_COMPLIANT',
            ],
            Limit=99,
        )
        l = len(response['EvaluationResults'])
        for i in range(l):
            print id, ": ",response['EvaluationResults'][i]['EvaluationResultIdentifier']['EvaluationResultQualifier']['ResourceId']
