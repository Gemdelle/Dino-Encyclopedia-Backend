from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, HtmlContent
from app.core.config import settings
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        if not settings.SENDGRID_API_KEY:
            logger.error("SendGrid API key is not configured")
            raise ValueError("SendGrid API key is not configured. Please add SENDGRID_API_KEY to your .env file")
        
        if not settings.EMAIL_SENDER:
            logger.error("Email sender is not configured")
            raise ValueError("Email sender is not configured. Please add EMAIL_SENDER to your .env file")
        
        self.sendgrid_client = SendGridAPIClient(settings.SENDGRID_API_KEY)
        self.sender_email = settings.EMAIL_SENDER
        
        logger.info(f"Initializing SendGrid email service")
        logger.info(f"Using sender email: {self.sender_email}")

    async def send_password_reset_email(self, to_email: str, reset_link: str):
        """
        Send password reset email using SendGrid
        """
        try:
            logger.info(f"Attempting to send password reset email to {to_email}")
            
            if not to_email:
                raise ValueError("Recipient email is required")
            
            if not reset_link:
                raise ValueError("Reset link is required")
            
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
            
            # Create SendGrid message
            message = Mail(
                from_email=self.sender_email,
                to_emails=to_email,
                subject="Reset Your Password - Dino Encyclopedia",
                html_content=html_content
            )
            
            try:
                response = self.sendgrid_client.send(message)
                if response.status_code in [200, 201, 202]:
                    logger.info(f"Successfully sent password reset email to {to_email}")
                    return True
                else:
                    error_msg = f"Failed to send email. Status code: {response.status_code}"
                    logger.error(error_msg)
                    raise HTTPException(status_code=500, detail=error_msg)
                    
            except Exception as e:
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