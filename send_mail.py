

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Email parameters
# Replace with your sender email address


def send_email(recipient_email, file_path2):
    sender_email = 'sowmiyavasubalaji@gmail.com'
    # Replace with the recipient email address
    smtp_server = 'smtp.gmail.com'  # Use the SMTP server of your email provider
    smtp_port = 587  # SMTP port (587 for TLS)
    app_password = 'ldfftcawudnpawzq'

    # Compose the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = 'Document Attachmenst'

    # Email body (optional)
    body = 'Please find the attached document.'
    msg.attach(MIMEText(body, 'plain'))

    # Attach the document (replace 'file_path' with the actual path of your document file)
    # Replace with the path to your document file
    file_path = 'updated_word_file.docx'
    with open(file_path, "rb") as file:
        part = MIMEApplication(file.read(), Name=file_path)
        part['Content-Disposition'] = f'attachment; filename="{file_path}"'
        msg.attach(part)
        # Attach the first document

    # Attach the second document

    with open(file_path2, "rb") as file2:
        part2 = MIMEApplication(file2.read(), Name=file_path2)
        part2['Content-Disposition'] = f'attachment; filename="{file_path2}"'
        msg.attach(part2)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, [recipient_email], msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)
    finally:
        print("Bit2Bytes")
