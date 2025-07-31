import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
from typing import Dict, List
import logging
import time
import random

class EmailSender:
    def __init__(self, config):
        self.config = config

    def create_email(self, contact: Dict, template_data: Dict) -> MIMEMultipart:
        """Create email from template and contact data"""
        template = Template(template_data['template'])

        # Render template with contact data
        body = template.render(
            blog_url=contact['blog_url'],
            my_blog_url=template_data['my_blog_url']
        )

        # Create email
        msg = MIMEMultipart()
        msg['From'] = self.config.from_email
        msg['To'] = contact['email']
        msg['Subject'] = template_data['subject']

        msg.attach(MIMEText(body, 'plain'))

        return msg

    def send_email(self, msg: MIMEMultipart, contact: Dict) -> bool:
        """Send single email"""
        try:
            with smtplib.SMTP(self.config.smtp_server, self.config.smtp_port) as server:
                server.starttls()
                server.login(self.config.email, self.config.password)

                text = msg.as_string()
                server.sendmail(self.config.email, contact['email'], text)

                logging.info(f"Email sent successfully to {contact['email']}")
                return True

        except Exception as e:
            logging.error(f"Failed to send email to {contact['email']}: {e}")
            return False

    def send_batch(self, contacts: List[Dict], templates: Dict,
                   delay_range: tuple = (10, 20), dry_run: bool = False) -> Dict:
        """Send emails to multiple contacts with delays"""
        results = {'sent': 0, 'failed': 0, 'skipped': 0}

        for i, contact in enumerate(contacts):
            language = contact['language']

            if language not in templates:
                logging.warning(f"No template for language '{language}', skipping {contact['email']}")
                results['skipped'] += 1
                continue

            # Create email
            template_data = templates[language]
            msg = self.create_email(contact, template_data)

            if dry_run:
                logging.info(f"[DRY RUN] Would send to {contact['email']} in {language}")
                results['sent'] += 1
            else:
                # Send email
                if self.send_email(msg, contact):
                    results['sent'] += 1
                else:
                    results['failed'] += 1

            # Add delay between emails (except for last one)
            if i < len(contacts) - 1:
                delay = random.randint(*delay_range)
                logging.info(f"Waiting {delay} seconds before next email...")
                time.sleep(delay)

        return results