import boto3

client = boto3.client('support', region_name='us-east-1')

count = {'error':0, 'warning':0, 'pass':0}
check_ids = {'7DAFEmoDos','zXCkfM1nI3','12Fnkpl8Y5','N430c450f2','N425c450f2','nNauJisYIT','rSs93HQwa1','ePs02jT06w','Yw2K9puPzl','xSqX82fQu','a2sEc6ILx','c9D319e7sG','DqdJqYeRm5','vjafUGJ9H0','1iG5NDGVre','HCP4007jGY','Pfx0RwqBli'}

for id in check_ids:
    response = client.describe_trusted_advisor_check_result(
        checkId=str(id),
        language='en'
    )

    if response['result']['status'] == 'error':
        flagged_resources =  response['result']['flaggedResources']
        for i in flagged_resources:
            if i['status'] == 'error' or i['status'] == 'warning':
                count['error'] = count['error'] + 1


    elif response['result']['status'] == 'warning':
        flagged_resources =  response['result']['flaggedResources']
        for i in flagged_resources:
            if i['status'] == 'error' or i['status'] == 'warning':
                count['warning'] = count['warning'] + 1


    elif response['result']['status'] == 'pass':
        flagged_resources =  response['result']['flaggedResources']
        for i in flagged_resources:
            if i['status'] == 'error' or i['status'] == 'warning':
                count['pass'] = count['pass'] + 1


print "Number of error check: ",count['error']
print "Numer of warning check: ",count['warning']
print "Number of pass check: ",count['pass']
