from jinja2 import Template

TEMPLATES = {
    "en": {
        "subject": "Quick question about your blog",
        "blog_url": "{{ blog_url }}",
        "my_blog_url": "https://eventuallymaking.io",
        "template": """Hello,

I came across your blog {{ blog_url }}.

I am a blogger myself ({{ my_blog_url }}) and I am trying to build tools for bloggers, especially for people using static blogs.

I wanted to ask you some questions about this. I would be delighted if you could take a moment to answer me :)

• What bothers you the most about managing your blog right now? What would you change?
• Do you send newsletters, and if so, how?
• Do you pay special attention to your traffic numbers, and if so, what tool do you use?

No worries if you don't want to answer. I understand :) 

Thanks !

Hugo
hakanai.io
"""
    },
    "fr": {
        "subject": "Question rapide sur votre blog",
        "blog_url": "{{ blog_url }}",
        "my_blog_url": "https://eventuallycoding.com",
        "template": """Bonjour,

Je suis tombé sur votre blog {{ blog_url }}.

Je suis moi-même blogueur ({{ my_blog_url }}) et j'essaie de créer des outils pour les blogueurs, en particulier pour les personnes utilisant des blogs statiques.

Je voulais vous poser quelques questions à ce sujet. Je serais ravi si vous pouviez prendre un moment pour me répondre :)

• Qu'est-ce qui vous dérange le plus dans la gestion de votre blog en ce moment ? Qu'est-ce que vous changeriez ?
• Envoyez-vous des newsletters, et si oui, comment ?
• Portez-vous une attention particulière à vos chiffres de trafic, et si oui, quel outil utilisez-vous ?

Pas de souci si vous ne voulez pas répondre. Je comprends :) 

Merci !

Hugo
hakanai.io
"""
    }
}