import logging
import os
from prospection.config import EmailConfig
from prospection.templates import TEMPLATES
from prospection.sheets_reader import SheetsReader
from prospection.email_sender import EmailSender

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('email_campaign.log'),
            logging.StreamHandler()
        ]
    )

def main():
    setup_logging()

    # Configuration
    config = EmailConfig()

    # Use existing service account file
    home_dir = os.path.expanduser("~")
    service_account_file = os.path.join(home_dir, 'perso', 'gdrive.json')

    # Initialize components
    sheets_reader = SheetsReader(service_account_file)
    email_sender = EmailSender(config)

    try:
        # Read contacts from Google Sheets
        logging.info("Reading contacts from Google Sheets...")
        contacts = sheets_reader.read_contacts(config.spreadsheet_id, config.range_name)

        if not contacts:
            logging.info("No contacts to process. Exiting.")
            return

        # Preview contacts
        logging.info(f"Found {len(contacts)} contacts:")
        for contact in contacts[:5]:  # Show first 5
            logging.info(f"  - {contact['email']} ({contact['language']}) - {contact['blog_url']}")

        # Confirm before sending
        if len(contacts) > 5:
            logging.info(f"  ... and {len(contacts) - 5} more")

        # Ask for confirmation
        response = input(f"\nSend emails to {len(contacts)} contacts? (y/N/dry): ").lower()

        if response == 'y':
            # Send emails
            logging.info("Starting email campaign...")
            results = email_sender.send_batch(contacts, TEMPLATES, dry_run=False)

        elif response == 'dry':
            # Dry run
            logging.info("Starting dry run...")
            results = email_sender.send_batch(contacts, TEMPLATES, dry_run=True)

        else:
            logging.info("Campaign cancelled.")
            return

        # Report results
        logging.info(f"\nCampaign completed!")
        logging.info(f"Sent: {results['sent']}")
        logging.info(f"Failed: {results['failed']}")
        logging.info(f"Skipped: {results['skipped']}")

    except Exception as e:
        logging.error(f"Campaign failed: {e}")
        raise

if __name__ == "__main__":
    main()
