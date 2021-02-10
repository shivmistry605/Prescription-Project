import boto3
client = boto3.client(service_name='comprehendmedical', region_name='us-east-1')
result = client.detect_entities(Text= 'cerealx 84 mg daily')
entities = result['Entities']

for entity in entities:
    print('\n Entity:', entity)