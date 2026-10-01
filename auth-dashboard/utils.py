"""Email sending through Resend; one function the pages call."""
import os
import resend
 
resend.api_key = os.environ.get("RESEND_API_KEY")   # from .env
 
def send_email(title, body, to):
    """Send one HTML email. to is a list of addresses."""
    resend.Emails.send({
        # test sender; use your own verified domain in production
        "from": "YourApp <email@resend.dev>",
        "to": to,
        "subject": title,
        "html": body,
    })