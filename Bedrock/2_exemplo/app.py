
import boto3
import json

boto3.setup_default_session(aws_access_key_id='',
                            aws_secret_access_key='',
                            region_name='')
bedrock = boto3.client(service_name="bedrock-runtime")

prompt = "Camberra is capital of Australia"

body = json.dumps({
    "inputText": prompt
})

model_id = 'amazon.titan-embed-text-v1'
accept = 'application/json'
content_type = 'application/json'

response = bedrock.invoke_model(
    body = body,
    modelId = model_id,
    accept = accept,
    contentType = content_type
)

response_body = json.loads(response['body'].read())
embedding = response_body.get('embedding')
print(embedding)