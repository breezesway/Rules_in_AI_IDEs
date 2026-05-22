"""
Batch send English emails via QQ/Foxmail
"""

import smtplib
import csv
import ssl
import os
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# ========== Configuration (fill in your email credentials) ==========
QQ_EMAIL = "<your-email@qq.com>"  # Your QQ or Foxmail email address
QQ_PASSWORD = "<your-password>"  # QQ email authorization code (not your QQ password)
# How to get QQ email authorization code: https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256
# Foxmail uses the same SMTP settings

# ========== File paths ==========
TEMPLATE_FILE = os.path.join(os.path.dirname(__file__), "invite_email.txt")
CSV_FILE = os.path.join(os.path.dirname(__file__), "..", "send_records", "send_2026_02_11.csv")

def load_template(template_path):
    """Load email template"""
    with open(template_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # First line is the subject
    subject = lines[0].strip()
    # Body starts from the third line (index 2)
    body_lines = lines[2:]
    body = ''.join(body_lines)
    
    return subject, body

def get_column_value(row, column_name):
    """Safely get column value, handling whitespace in column names"""
    # Try direct match
    if column_name in row:
        return row[column_name]
    # Try matching after stripping whitespace
    for key in row.keys():
        if key.strip() == column_name:
            return row[key]
    # Return empty string if not found
    return ''

def create_email_html(subject, body, name, project_name):
    """Create HTML email content"""
    # Replace [Name] with bold name
    body_html = body.replace('[Name]', f'<strong>{name}</strong>')
    # Replace [Project Name] with project name
    body_html = body_html.replace('[Project Name]', project_name)
    # Convert newlines to HTML line breaks
    body_html = body_html.replace('\n', '<br>')
    
    return subject, body_html

def send_email_qq(sender_email, sender_password, recipient_email, subject, html_body, max_retries=2):
    """Send email via QQ SMTP"""
    for attempt in range(max_retries):
        server = None
        try:
            # Create message object
            msg = MIMEMultipart('alternative')
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = Header(subject, 'utf-8')
            
            # Attach HTML content
            html_part = MIMEText(html_body, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Create SSL context
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            # Connect to QQ SMTP server via SSL on port 465
            server = smtplib.SMTP_SSL('smtp.qq.com', 465, timeout=30, context=context)
            
            server.login(sender_email, sender_password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)
            server.quit()
            
            return True

        except smtplib.SMTPException as e:
            if server:
                try: server.quit()
                except: pass
            
            # Print more detailed error
            print(f"  SMTP error ({attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
                
        except Exception as e:
            if server:
                try: server.quit()
                except: pass
            
            print(f"  Connection error ({attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(5)

    return False

def check_and_add_sent_column(csv_file):
    """Check if CSV has email_sent column; add it if missing"""
    # Read all rows
    rows = []
    fieldnames = None
    has_sent_column = False
    sent_column_name = None
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        
        # Check for email_sent column (handle possible whitespace)
        for col in fieldnames:
            if col.strip() == 'email_sent':
                has_sent_column = True
                sent_column_name = col
                break
        
        # Add column if missing
        if not has_sent_column:
            # Add new column name
            fieldnames = list(fieldnames) + ['email_sent']
            sent_column_name = 'email_sent'
            print("email_sent column not found in CSV; adding it...")
        
        # Read all rows
        for row in reader:
            # Set default FALSE for each row if column was missing
            if not has_sent_column:
                row[sent_column_name] = 'FALSE'
            rows.append(row)
    
    # Write back to file if modified
    if not has_sent_column:
        with open(csv_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print("Added email_sent column with default value FALSE")
    
    return sent_column_name, rows, fieldnames

def update_sent_status(csv_file, row_index, sent_column_name, fieldnames, all_rows):
    """Update send status to TRUE for the given CSV row"""
    all_rows[row_index][sent_column_name] = 'TRUE'
    
    # Write back to CSV file
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

def main():
    """Main entry point"""
    # Validate configuration
    if QQ_EMAIL == "your_email@qq.com" or QQ_PASSWORD == "your_auth_code":
        print("Error: Please configure QQ email address and authorization code first!")
        return
    
    # Load template
    print("Loading email template...")
    subject_template, body_template = load_template(TEMPLATE_FILE)
    
    # Check and handle email_sent column in CSV
    print(f"Reading CSV file: {CSV_FILE}")
    sent_column_name, all_rows, fieldnames = check_and_add_sent_column(CSV_FILE)
    
    sent_count = 0
    failed_count = 0
    skipped_count = 0
    
    # Process each row
    for row_index, row in enumerate(all_rows):
        # Skip if already sent
        sent_status = get_column_value(row, 'email_sent').strip().upper()
        if sent_status == 'TRUE':
            skipped_count += 1
            continue
        
        # Only process non-Chinese users (is_chinese_user is FALSE)
        is_chinese_user = get_column_value(row, 'is_chinese_user').strip().upper()
        if is_chinese_user != 'FALSE':
            continue
        
        contributor_name = get_column_value(row, 'contributor_name').strip()
        contributor_email = get_column_value(row, 'contributor_email').strip()
        repo_url = get_column_value(row, 'repo_url').strip()
        
        # Skip empty email
        if not contributor_email:
            print(f"Skipping: {contributor_name} (no email address)")
            continue
        
        # Build email content
        subject, html_body = create_email_html(
            subject_template, 
            body_template, 
            contributor_name, 
            repo_url
        )
        
        # Send email
        print(f"Sending email to: {contributor_name} ({contributor_email})...")
        if send_email_qq(QQ_EMAIL, QQ_PASSWORD, contributor_email, subject, html_body):
            print(f"✓ Successfully sent to: {contributor_name}")
            sent_count += 1
            # Update send status in CSV
            update_sent_status(CSV_FILE, row_index, sent_column_name, fieldnames, all_rows)
            # Pause 15-25 seconds between sends to avoid spam detection
            delay = random.randint(15, 25)
            print(f"Waiting {delay} seconds before sending next email...")
            time.sleep(delay)
        else:
            failed_count += 1
    
    print(f"\nSending complete!")
    print(f"Succeeded: {sent_count}")
    print(f"Failed: {failed_count}")
    if skipped_count > 0:
        print(f"Skipped (already sent): {skipped_count}")

if __name__ == "__main__":
    main()

