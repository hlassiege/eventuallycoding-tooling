import argparse
import os
from datetime import datetime
import requests

parser = argparse.ArgumentParser(description="Translate file in english")
parser.add_argument('slug', help='slug of the blog post')
args = parser.parse_args()

blog_dir='../eventuallycoding-nuxt3'
now = datetime.now()
year = now.year
month = now.month

dir_of_french_blog_post = os.path.join(blog_dir, 'content', 'articles', str(year), f"{month:02d}")
dir_of_english_blog_post = os.path.join(blog_dir, 'content', 'articles','en', str(year), f"{month:02d}")
blog_post_in_french = os.path.join(dir_of_french_blog_post, f'{args.slug}.md')
blog_post_in_english = os.path.join(dir_of_english_blog_post, f'{args.slug}.md')

if not os.path.exists(blog_post_in_french):
    print(f"Le fichier {blog_post_in_french} n'existe pas.")
    exit(1)
if not os.path.exists(dir_of_english_blog_post):
    os.makedirs(dir_of_english_blog_post, exist_ok=True)
    print(f"Le répertoire {dir_of_english_blog_post} a été créé.")

deepl_api_key = os.environ['DEEPL_API']

with open(blog_post_in_french, 'r', encoding='utf-8') as file:
    french_content = file.read()

data = {
    'auth_key': deepl_api_key,
    'text': french_content,
    'target_lang': 'EN'
}

response = requests.post('https://api-free.deepl.com/v2/translate', data=data)

if response.status_code == 200:
    translated_text = response.json()['translations'][0]['text']
    with open(blog_post_in_english, 'w', encoding='utf-8') as file:
        file.write(translated_text)
    print(f"Blog post translated and saved to {blog_post_in_english}")
else:
    print(f"Error during translation: {response.text}")
