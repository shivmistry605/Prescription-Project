import boto3
from trp import Document
from collections import Counter
import json

try:
    from urllib.parse import unquote_plus
except ImportError:
    from urllib import unquote_plus

s3 = boto3.resource('s3')
s3client = boto3.client('s3')

textract = boto3.client(service_name='textract', region_name='us-east-1')

comprehend = boto3.client(service_name='comprehendmedical', region_name='us-east-1')

def lambda_handler(event, context):
    print("Received event: ", event)
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = unquote_plus(event['Records'][0]['s3']['object']['key'])
    print("key is " + key)
    print("bucket is " + bucket)
    
    try:
        s3.Bucket(bucket).download_file(Key=key,Filename='/tmp/{}')
        
        with open('/tmp/{}', 'rb') as document:
            imageBytes = bytearray(document.read())
        print("Object downloaded")
        
        response = textract.analyze_document(Document={'Bytes': imageBytes},FeatureTypes=["FORMS"])
        
        doc = Document(response)
        lines = ""

        for page in doc.pages:
            for field in page.form.fields:
                lines = lines + "\n" + str(field.key) + " : " + str(field.value)

        result = comprehend.detect_entities(Text= lines)
        entities = result['Entities']

        for entity in entities:
            print("-------------------------------------------")
            print("Text: {}, Category: {}, Type: {}, Score: {}".format(entity['Text'], entity['Category'], entity['Type'], entity['Score']))
        
        return 'Textract + Comprehend Successfully Completed!'
        
    except Exception as e:
        print(e)
        print("Error :")
        raise e
    