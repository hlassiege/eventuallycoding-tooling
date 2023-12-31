from googleapiclient.discovery import build
from google.oauth2 import service_account
import os
import pypandoc
import argparse
import re

parser = argparse.ArgumentParser(description='Export Google Doc as DOCX.')
parser.add_argument('document_id', help='ID of the Google Docs document to export')
parser.add_argument('slug', help='slug of the blog post')

args = parser.parse_args()

home_dir = os.path.expanduser('~')
service_account_file = os.path.join(home_dir, 'perso', 'gdrive.json')
document_id = args.document_id

SCOPES = ['https://www.googleapis.com/auth/drive']

creds = service_account.Credentials.from_service_account_file(service_account_file, scopes=SCOPES)

service = build('drive', 'v3', credentials=creds)
request = service.files().export_media(fileId=document_id,
                                       mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
response = request.execute()

with open('output.docx', 'wb') as file:
    file.write(response)

print('Document exported and saved as output.docx')

input_file = 'output.docx'
output_file = f'{args.slug}.md'
output = pypandoc.convert_file(input_file, 'markdown', outputfile=output_file, extra_args=['--extract-media', '.', '--wrap=none'])


def update_image_format(md_file_path):
    with open(md_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    pattern = r'!\[\]\(\./media/(.*?)\)\{.*?\}'
    replacement = r'::nuxt-image{src="/images/' + args.slug + r'/\1" alt=""}\n::'
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(md_file_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

    print(f"Le format des images a été mis à jour dans {md_file_path}")


update_image_format(output_file)
