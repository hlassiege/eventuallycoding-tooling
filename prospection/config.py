import os
from dataclasses import dataclass

@dataclass
class EmailConfig:
    smtp_server: str = "in-v3.mailjet.com"
    smtp_port: int = 587
    email: str = os.getenv("EMAIL_ADDRESS", "")
    password: str = os.getenv("EMAIL_PASSWORD", "")
    from_email: str = os.getenv("FROM_EMAIL", "")

    # Google Sheets config
    spreadsheet_id: str = "1BRF6W8UuRUUf_kt03gIFjZpusmNC6b6jH83b426c9YE"
    range_name: str = "Feuille 1!B:E"
