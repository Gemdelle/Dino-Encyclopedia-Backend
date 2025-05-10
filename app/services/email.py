from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from app.core.config import settings
from fastapi import HTTPException
import logging
import json

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        if not settings.SENDGRID_API_KEY:
            logger.error("SendGrid API key is not configured")
            raise ValueError("SendGrid API key is not configured. Please add SENDGRID_API_KEY to your .env file")
        
        if not settings.EMAIL_SENDER:
            logger.error("Email sender is not configured")
            raise ValueError("Email sender is not configured. Please add EMAIL_SENDER to your .env file")
        
        api_key = settings.SENDGRID_API_KEY
        masked_key = f"{api_key[:4]}...{api_key[-4:]}" if len(api_key) > 8 else "***"
        logger.info(f"Initializing SendGrid with API key: {masked_key}")
        logger.info(f"Using sender email: {settings.EMAIL_SENDER}")
        
        try:
            self.sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            self.test_api_key()
            self.from_email = Email(settings.EMAIL_SENDER)
        except Exception as e:
            logger.error(f"Failed to initialize SendGrid client: {str(e)}")
            raise ValueError(f"Failed to initialize SendGrid client: {str(e)}")

    def test_api_key(self):
        """Test if the API key is valid by making a simple API call"""
        try:
            response = self.sg.client.api_keys._(settings.SENDGRID_API_KEY).get()
            logger.info("SendGrid API key validation successful")
        except Exception as e:
            logger.error(f"SendGrid API key validation failed: {str(e)}")
            if "403" in str(e):
                raise ValueError(
                    "SendGrid API key is invalid or doesn't have proper permissions. "
                    "Please check that:\n"
                    "1. The API key is correct\n"
                    "2. The API key has 'Mail Send' permissions\n"
                    "3. The API key is active"
                )
            raise

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
            
            to_email = To(to_email)
            subject = "Reset Your Password - Dino Encyclopedia"
            content = Content(
                "text/html",
                f"""
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
            )
            
            mail = Mail(self.from_email, to_email, subject, content)
            logger.debug(f"Sending email with from_email={settings.EMAIL_SENDER}, to_email={to_email}")
            
            try:
                response = self.sg.client.mail.send.post(request_body=mail.get())
                logger.info(f"SendGrid API response: {response.status_code}")
            except Exception as e:
                error_msg = str(e)
                if hasattr(e, 'body'):
                    try:
                        error_body = json.loads(e.body)
                        error_msg = f"SendGrid Error: {error_body.get('errors', [{'message': 'Unknown error'}])[0].get('message')}"
                    except:
                        error_msg = f"SendGrid Error: {e.body if hasattr(e, 'body') else str(e)}"
                logger.error(f"Failed to send email: {error_msg}")
                raise HTTPException(status_code=500, detail=error_msg)
            
            if response.status_code not in [200, 201, 202]:
                error_body = response.body.decode() if hasattr(response.body, 'decode') else response.body
                logger.error(f"SendGrid API error: Status={response.status_code}, Body={error_body}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to send reset email. SendGrid Status: {response.status_code}"
                )
            
            logger.info(f"Successfully sent password reset email to {to_email}")
            return True
            
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