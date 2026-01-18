import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from app.config import get_settings

settings = get_settings()


class MailerService:
    """Email service for sending emails"""
    
    def __init__(self):
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_user = settings.smtp_user
        self.smtp_password = settings.smtp_password
        self.smtp_from = settings.smtp_from
    
    async def send_email(
        self,
        to: List[str],
        subject: str,
        body: str,
        html: Optional[str] = None
    ) -> bool:
        """Send email via SMTP"""
        if not self.smtp_user or not self.smtp_password:
            print("Email service not configured")
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.smtp_from
            msg['To'] = ', '.join(to)
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            if html:
                msg.attach(MIMEText(html, 'html'))
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False
    
    async def send_welcome_email(self, to: str, name: str) -> bool:
        """Send welcome email to new user"""
        subject = "Welcome to NEXO!"
        body = f"Hello {name},\n\nWelcome to NEXO platform. We're glad to have you here!"
        return await self.send_email([to], subject, body)
    
    async def send_booking_confirmation(self, to: str, booking_details: dict) -> bool:
        """Send booking confirmation email"""
        subject = "Booking Confirmation - NEXO"
        body = f"Your booking has been confirmed.\n\nDetails: {booking_details}"
        return await self.send_email([to], subject, body)


mailer_service = MailerService()
