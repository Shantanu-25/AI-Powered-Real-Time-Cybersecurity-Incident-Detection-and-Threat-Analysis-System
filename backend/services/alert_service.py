import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiohttp
import logging
from core.config import settings

logger = logging.getLogger(__name__)

async def send_telegram_alert(message: str):
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        return
        
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    logger.error(f"Failed to send Telegram alert: {await response.text()}")
        except Exception as e:
            logger.error(f"Telegram alert error: {e}")

def send_email_alert(subject: str, body: str):
    if not settings.SMTP_SERVER or not settings.SMTP_USER or not settings.ALERT_EMAIL_TO:
        return
        
    msg = MIMEMultipart()
    msg['From'] = settings.SMTP_USER
    msg['To'] = settings.ALERT_EMAIL_TO
    msg['Subject'] = f"[URGENT] SOC Alert: {subject}"
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        logger.error(f"Email alert error: {e}")
