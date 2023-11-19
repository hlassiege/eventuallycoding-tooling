import argparse
import shutil
import os
from datetime import datetime

parser = argparse.ArgumentParser(description="Copy files from one directory to another.")
parser.add_argument('slug', help='slug of the blog post')
args = parser.parse_args()

# ----------------------
# Copy media files
# ----------------------
blog_dir='../eventuallycoding-nuxt3'
source_dir='./media'
dest_dir=f'{blog_dir}/public/images/{args.slug}'

if not os.path.exists(source_dir):
    print(f"Le répertoire source {source_dir} n'existe pas.")
    exit(1)

os.makedirs(dest_dir, exist_ok=True)

for filename in os.listdir(source_dir):
    file_path = os.path.join(source_dir, filename)
    if os.path.isfile(file_path):
        shutil.copy(file_path, dest_dir)

print(f'Les fichiers ont été copiés de {source_dir} à {dest_dir}')

# ----------------------
# Copy markdown file
# ----------------------
now = datetime.now()
year = now.year
month = now.month

source_file = f'{args.slug}.md'

dest_dir = os.path.join(blog_dir, 'content', 'articles', str(year), f"{month:02d}")

os.makedirs(dest_dir, exist_ok=True)
blog_post_in_french = os.path.join(dest_dir, f'{args.slug}.md')
shutil.copy(source_file, blog_post_in_french)

print(f'Le fichier a été copié et renommé en {blog_post_in_french}')

# ----------------------
# Create english version
# ----------------------
dest_dir = os.path.join(blog_dir, 'content', 'articles', 'en', str(year), f"{month:02d}")

os.makedirs(dest_dir, exist_ok=True)
blog_post_in_english = os.path.join(dest_dir, f'{args.slug}.md')
shutil.copy(source_file, blog_post_in_english)

print(f'Le fichier a été copié et renommé pour sa version anglaise {blog_post_in_english}')

# ----------------------
# Add yaml front matter
# ----------------------
current_date = datetime.now().strftime("%Y-%m-%d")


def add_yaml_front_matter(blog_post, language='fr'):
    if language == 'fr':
        alternate_language = 'en'
        alternate_url = f"https://eventuallycoding.com/en/{year}/{month:02d}/{args.slug}"
    else:
        alternate_language = 'fr'
        alternate_url = f"https://eventuallycoding.com/{year}/{month:02d}/{args.slug}"


    with open(blog_post, 'r', encoding='utf-8') as file:
        content = file.read()
    yaml_header = f"""---
id: ""
title: ""
description: ""
tags: []
date: "{current_date}"
cover: ""

language: "{language}"
alternates:
    - {alternate_language}: "{alternate_url}"
---
"""
    # Écrire l'en-tête YAML et le contenu dans le fichier
    with open(blog_post, 'w', encoding='utf-8') as file:
        file.write(yaml_header + content)
    print(f"L'en-tête YAML a été ajouté au fichier {blog_post}")


add_yaml_front_matter(blog_post_in_french, language='fr')
add_yaml_front_matter(blog_post_in_english, language='en')

