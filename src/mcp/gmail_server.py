import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from mcp.server.fastmcp import FastMCP

# Initialize the Server
mcp = FastMCP("gmail")

@mcp.tool()
def send_email(to_email: str, subject: str, body: str) -> str:
    """
    Sends a single email via Gmail.
    Args:
        to_email: The recipient's email address.
        subject: The subject line.
        body: The plain text body of the email.
    """
    sender_email = os.getenv("GMAIL_USER")
    password = os.getenv("GMAIL_APP_PASSWORD")

    if not sender_email or not password:
        return "❌ Error: GMAIL_USER or GMAIL_APP_PASSWORD missing in .env"

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Connect to Gmail SMTP Server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()

        return f"✅ Email sent successfully to {to_email}"
    except Exception as e:
        return f"❌ Failed to send email: {str(e)}"

@mcp.tool()