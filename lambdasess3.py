import boto3

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    s3_client = boto3.client('s3')
    file_obj = s3_client.get_object(Bucket=bucket_name, Key=key)
    file_content = file_obj['Body'].read().decode('utf-8')
    
    email_ids = file_content.split('\n')  
    
    ses_client = boto3.client('ses', region_name='us-east-1')  
    
    for email_id in email_ids:
        email_id = email_id.strip()  
        
        if email_id:
            message = f"Hello {email_id}, Successfully integrate S3, Lambda with SES."
            subject = "Successfully Email from Lambda"
            
            response = ses_client.send_email(
                Source='sender@xxxx.com',  
                Destination={
                    'ToAddresses': [email_id]
                },
                Message={
                    'Subject': {
                        'Data': subject
                    },
                    'Body': {
                        'Text': {
                            'Data': message
                        }
                    }
                }
            )
            print(f"Email sent to {email_id}. Message ID: {response['MessageId']}")
