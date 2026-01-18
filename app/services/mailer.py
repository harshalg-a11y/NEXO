from typing import List, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

class MailerService:
    """Email service abstraction that can be swapped with different providers"""
    
    def __init__(self):
        self.from_email = settings.mail_from
        self.host = settings.mail_host
        self.port = settings.mail_port
        self.username = settings.mail_username
        self.password = settings.mail_password
        self.use_tls = settings.mail_use_tls
    
    def send_email(
        self, 
        to: List[str], 
        subject: str, 
        body: str, 
        html_body: Optional[str] = None,
        sender: Optional[str] = None
    ) -> bool:
        """
        Send an email using SMTP.
        
        Args:
            to: List of recipient email addresses
            subject: Email subject
            body: Plain text email body
            html_body: Optional HTML email body
            sender: Optional sender override (defaults to configured from_email)
            
        Returns:
            True if email was sent successfully, False otherwise
        """
        if not self.username or not self.password:
            # If credentials aren't configured, just log and return success
            # This allows the app to function without a mail server
            print(f"[MAILER] Would send email to {to}: {subject}")
            return True
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = sender or self.from_email
            msg['To'] = ', '.join(to)
            
            # Attach plain text
            text_part = MIMEText(body, 'plain')
            msg.attach(text_part)
            
            # Attach HTML if provided
            if html_body:
                html_part = MIMEText(html_body, 'html')
                msg.attach(html_part)
            
            # Connect to SMTP server
            with smtplib.SMTP(self.host, self.port) as server:
                if self.use_tls:
                    server.starttls()
                
                # Login if credentials provided
                if self.username and self.password:
                    server.login(self.username, self.password)
                
                # Send email
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"[MAILER] Error sending email: {str(e)}")
            return False

# Global instance
mailer = MailerService()

def send_email(to: List[str], subject: str, body: str, *, sender: Optional[str] = None, html_body: Optional[str] = None) -> bool:
    """
    Send an email using the global mailer instance.
    
    This is a convenience function that uses the global mailer service.
    """
    return mailer.send_email(to, subject, body, html_body=html_body, sender=sender)
