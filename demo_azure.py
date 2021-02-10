from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential
import csv

client = FormRecognizerClient(
    "",
    AzureKeyCredential("")
)

output = []

with open('prescription_1.jpg', 'rb') as f:
    form_rec = client.begin_recognize_content(form=f)

result = form_rec.result()

for idx, content in enumerate(result):
    for line_idx, line in enumerate(content.lines):
        for word in line.words:
            output.append((word.text,word.confidence))

with open("azure_presc_1.csv","a",newline="") as f:
    writer = csv.writer(f)
    writer.writerows(output)

print("done")




    