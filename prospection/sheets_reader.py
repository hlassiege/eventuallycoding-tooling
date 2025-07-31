import gspread
from google.oauth2.service_account import Credentials
from typing import List, Dict
import logging

class SheetsReader:
    def __init__(self, credentials_path: str):
        self.credentials_path = credentials_path
        self.client = None

    def authenticate(self):
        """Authenticate with Google Sheets API"""
        try:
            scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
            creds = Credentials.from_service_account_file(
                self.credentials_path, scopes=scopes
            )
            self.client = gspread.authorize(creds)
            logging.info("Successfully authenticated with Google Sheets")
        except Exception as e:
            logging.error(f"Authentication failed: {e}")
            raise

    def read_contacts(self, spreadsheet_id: str, range_name: str = "Sheet1!A:D") -> List[Dict]:
        """Read contacts from Google Sheets"""
        if not self.client:
            self.authenticate()

        try:
            sheet = self.client.open_by_key(spreadsheet_id)

            # Parse sheet name from range_name (e.g., "Sheet2!B:E" -> "Sheet2")
            if '!' in range_name:
                sheet_name = range_name.split('!')[0]
                worksheet = sheet.worksheet(sheet_name)
            else:
                worksheet = sheet.get_worksheet(0)  # Default to first sheet

            # Get all records as list of dicts
            records = worksheet.get_all_records()

            contacts = []
            seen_emails = set()
            duplicates = []

            for i, record in enumerate(records, start=2):  # Start at 2 (row 1 = headers)
                contact = {
                    'email': record.get('email', '').strip(),
                    'blog_url': record.get('blog', '').strip(),
                    'language': record.get('langue', 'en').strip(),
                    'sent': record.get('envoyé', '').strip().lower() == 'yes',
                    'row': i  # Track row number for debugging
                }

                # Skip empty emails
                if not contact['email']:
                    continue

                # Check for duplicates
                if contact['email'].lower() in seen_emails:
                    duplicates.append(f"Row {i}: {contact['email']}")
                    logging.warning(f"Duplicate email found at row {i}: {contact['email']}")
                    continue

                seen_emails.add(contact['email'].lower())

                # Debug: log all valid contacts found
                logging.info(f"Row {i}: {contact['email']} - sent: {contact['sent']}")

                # Skip if already sent
                if contact['sent']:
                    logging.info(f"Skipping {contact['email']} - already sent")
                    continue

                contacts.append(contact)

            # Report duplicates summary
            if duplicates:
                logging.warning(f"Found {len(duplicates)} duplicate emails:")
                for dup in duplicates:
                    logging.warning(f"  - {dup}")
                logging.warning("Please clean up duplicates in your spreadsheet")

            logging.info(f"Found {len(contacts)} unique contacts to process (out of {len(records)} total rows)")
            return contacts

        except Exception as e:
            logging.error(f"Error reading contacts: {e}")
            raise