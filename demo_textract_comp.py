import boto3
from trp import Document
from collections import Counter
import json
import csv

client = boto3.client('textract')

response = client.analyze_document(
    Document={
        'S3Object':{
            'Bucket':'test-bujet',
            'Name':'prescription_1.jpeg'
        }
    },      
    FeatureTypes=[
        'FORMS'
    ],
)

doc = Document(response)
lines = ""

for page in doc.pages:
    for field in page.form.fields:
        lines = lines + "\n" + str(field.key) + " : " + str(field.value)

client_two = boto3.client(service_name='comprehendmedical', region_name='us-east-1')
result = client_two.detect_entities(Text= lines)
entities = result['Entities']

for entity in entities:
    print("-------------------------------------------")
    print("Text: {}, Category: {}, Type: {}, Score: {}".format(entity['Text'], entity['Category'], entity['Type'], entity['Score']))
