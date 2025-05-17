import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
from fastapi import HTTPException
import logging
import ssl

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        if not settings.SMTP_SERVER:
            logger.error("SMTP server is not configured")
            raise ValueError("SMTP server is not configured. Please add SMTP_SERVER to your .env file")
        
        if not settings.SMTP_PORT:
            logger.error("SMTP port is not configured")
            raise ValueError("SMTP port is not configured. Please add SMTP_PORT to your .env file")
        
        if not settings.SMTP_USERNAME:
            logger.error("SMTP username is not configured")
            raise ValueError("SMTP username is not configured. Please add SMTP_USERNAME to your .env file")
        
        if not settings.SMTP_PASSWORD:
            logger.error("SMTP password is not configured")
            raise ValueError("SMTP password is not configured. Please add SMTP_PASSWORD to your .env file")
        
        if not settings.EMAIL_SENDER:
            logger.error("Email sender is not configured")
            raise ValueError("Email sender is not configured. Please add EMAIL_SENDER to your .env file")
        
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.sender_email = settings.EMAIL_SENDER
        
        logger.info(f"Initializing SMTP email service with server: {self.smtp_server}:{self.smtp_port}")
        logger.info(f"Using sender email: {self.sender_email}")

    async def send_password_reset_email(self, to_email: str, reset_link: str):
        """
        Send password reset email using SMTP
        """
        try:
            logger.info(f"Attempting to send password reset email to {to_email}")
            
            if not to_email:
                raise ValueError("Recipient email is required")
            
            if not reset_link:
                raise ValueError("Reset link is required")
            
            # Create message
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = to_email
            message["Subject"] = "Reset Your Password - Dino Encyclopedia"
            
            # Create HTML content
            html_content = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #333;">Password Reset Request</h2>
                <p>You have requested to reset your password for your Dino Encyclopedia account.</p>
                <p>Click the button below to reset your password:</p>
                <div style="text-align: center; margin: 25px 0;">
                    <a href="{reset_link}" 
                       style="background-color: #4CAF50; 
                              color: white; 
                              padding: 14px 28px; 
                              text-align: center; 
                              text-decoration: none; 
                              display: inline-block; 
                              border-radius: 4px;
                              font-size: 16px;">
                        Reset Password
                    </a>
                </div>
                <p>If you didn't request this, you can safely ignore this email.</p>
                <p>This link will expire in 1 hour.</p>
                <hr style="border: 1px solid #eee; margin: 20px 0;">
                <p style="color: #666; font-size: 14px;">Best regards,<br>Dino Encyclopedia Team</p>
            </div>
            """
            
            # Attach HTML content
            message.attach(MIMEText(html_content, "html"))
            
            # Create secure SSL/TLS connection
            context = ssl.create_default_context()
            
            try:
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls(context=context)
                    server.login(self.smtp_username, self.smtp_password)
                    server.send_message(message)
                    logger.info(f"Successfully sent password reset email to {to_email}")
                    return True
                    
            except smtplib.SMTPAuthenticationError:
                error_msg = "SMTP authentication failed. Please check your credentials."
                logger.error(error_msg)
                raise HTTPException(status_code=500, detail=error_msg)
            except smtplib.SMTPException as e:
                error_msg = f"Failed to send email: {str(e)}"
                logger.error(error_msg)
                raise HTTPException(status_code=500, detail=error_msg)
            
        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Email sending error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to send reset email: {str(e)}"
            )

email_service = EmailService() 