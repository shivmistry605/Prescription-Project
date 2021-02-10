import boto3
from trp import Document
from collections import Counter
import json
import csv
print(boto3.__version__)

client = boto3.client('textract')

response = client.analyze_document(
    Document={
        'S3Object':{
            'Bucket':'test-bujet',
            'Name':'prescription_1.jpg'
        }
    },      
    FeatureTypes=[
        'FORMS'
    ],
)

columns = []
lines = []

for item in response["Blocks"]:
    if item["BlockType"] == "WORD":
        column_found = False
        for index, column in enumerate(columns):
            bbox_left = item["Geometry"]["BoundingBox"]["Left"]
            bbox_right = item["Geometry"]["BoundingBox"]["Left"] + \
                item["Geometry"]["BoundingBox"]["Width"]
            bbox_centre = item["Geometry"]["BoundingBox"]["Left"] + \
                item["Geometry"]["BoundingBox"]["Width"] / 2
            column_centre = column['left'] + column['right'] / 2

            if (bbox_centre > column['left'] and bbox_centre < column['right']) or (column_centre > bbox_left and column_centre < bbox_right):
                # Bbox appears inside the column
                lines.append((item["Text"], item['Confidence']))
                column_found = True
                break
        if not column_found:
            columns.append({'left': item["Geometry"]["BoundingBox"]["Left"], 'right': item["Geometry"]
                                ["BoundingBox"]["Left"] + item["Geometry"]["BoundingBox"]["Width"]})
            lines.append((item["Text"], item['Confidence']))

with open("aws_presc_1.csv", "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(lines)

print("done")
