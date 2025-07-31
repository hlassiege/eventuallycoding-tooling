import os
import re
import yaml

class CustomDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, *args, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)

def get_relative_path(url):
    """Extrait le chemin relatif correct selon le format de l'URL"""
    # Retire le domaine s'il existe
    path = url.split('eventuallycoding.com/')[-1]

    # Si le chemin contient des segments de date (YYYY/MM/...)
    if re.match(r'\d{4}/\d{2}/', path):
        return '/' + path
    else:
        # Pour les chemins simples, on ne garde que le dernier segment
        return '/' + path.split('/')[-1]

def transform_frontmatter(content):
    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not frontmatter_match:
        return content

    original_frontmatter = frontmatter_match.group(1)

    try:
        frontmatter = yaml.safe_load(original_frontmatter)
        if not isinstance(frontmatter, dict):
            return content

        original_lang = frontmatter.pop('language', None)
        old_alternates = frontmatter.pop('alternates', [])

        # Extraction de l'URL en anglais
        en_url = None
        for alt in old_alternates:
            if isinstance(alt, dict) and 'fr' in alt:
                en_url = alt['fr']

        if not en_url or not original_lang:
            return content

        # Construction du nouveau alternates avec le chemin relatif correct
        new_alternates = [
            {'hreflang': 'fr', 'href': en_url},
            {'hreflang': original_lang, 'href': get_relative_path(en_url)}
        ]

        frontmatter['alternates'] = new_alternates

        # Configuration du style de dump YAML
        yaml.add_representer(str, lambda dumper, value: dumper.represent_scalar(
            'tag:yaml.org,2002:str', value, style='"' if ' ' in value or ':' in value else None
        ), Dumper=CustomDumper)

        new_frontmatter = yaml.dump(frontmatter,
                                    Dumper=CustomDumper,
                                    allow_unicode=True,
                                    sort_keys=False,
                                    width=float("inf"))

        return f"---\n{new_frontmatter}---\n" + content[frontmatter_match.end():]

    except yaml.YAMLError:
        return content

def process_directory(directory, dry_run=True):
    modified_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)

                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                new_content = transform_frontmatter(content)

                if new_content != content:
                    if dry_run:
                        print(f"Modification prévue pour : {file_path}")
                        print("Ancien frontmatter :")
                        print(content.split('---\n')[1])
                        print("Nouveau frontmatter :")
                        print(new_content.split('---\n')[1])
                        print("-" * 50)
                    else:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Fichier modifié : {file_path}")
                    modified_files.append(file_path)

    return modified_files


if __name__ == "__main__":
    blog_dir='../eventuallymaking.io/content'

    # Premier passage en dry_run pour voir les modifications
    print("Mode test - aucune modification ne sera effectuée")
    modified_files = process_directory(blog_dir, dry_run=True)

    if modified_files:
        print("\nApplication des modifications...")
        process_directory(blog_dir, dry_run=False)
        print("Modifications terminées.")
    else:
        print("Aucune modification nécessaire.")

