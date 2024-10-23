import imaplib
import email
from email.header import decode_header
import os
import datetime
from django.core.files.base import ContentFile
from .models import Email
import chardet

def decode_mime_words(s):
    decoded_words = []
    for word, charset in decode_header(s):
        if isinstance(word, bytes):
            if charset:
                try:
                    word = word.decode(charset, errors='replace')
                except LookupError:
                    word = word.decode('utf-8', errors='replace')
            else:
                # Detect encoding if not specified
                detected_encoding = chardet.detect(word)['encoding']
                word = word.decode(detected_encoding or 'utf-8', errors='replace')
        decoded_words.append(word)
    return ''.join(decoded_words)

def fetch_emails(email_config):
    # Connect to the server
    imap = imaplib.IMAP4_SSL(email_config.server, email_config.port)

    # Login to the account
    imap.login(email_config.username, email_config.password)

    # Select the mailbox (e.g., INBOX)
    imap.select("INBOX")

    # Search for all emails
    status, messages = imap.search(None, "ALL")

    # Convert messages to a list of email IDs
    email_ids = messages[0].split()

    for email_id in email_ids:
        # Fetch the email by ID
        status, msg_data = imap.fetch(email_id, "(RFC822)")

        # Get the email content
        msg_bytes = msg_data[0][1]

        # Parse the email
        msg = email.message_from_bytes(msg_bytes)

        # Decode the email subject using decode_mime_words()
        subject = decode_mime_words(msg["Subject"] or "")

        # Decode the sender using decode_mime_words()
        sender = decode_mime_words(msg.get("From", ""))

        # Get the date
        date_tuple = email.utils.parsedate_tz(msg.get("Date"))
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
        else:
            local_date = datetime.datetime.now()

        # Save the email content as a .eml file
        filename = f"{email_id.decode()}.eml"
        email_file = ContentFile(msg_bytes, name=filename)

        # Save the email record to the database
        Email.objects.create(
            subject=subject,
            sender=sender,
            date_received=local_date,
            eml_file=email_file
        )

    # Logout from the server
    imap.logout()
