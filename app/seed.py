"""
Seeds the database with realistic demo data on first startup.

Only runs if the tickets table is completely empty, so it never
overwrites real ticket data once the app has actual usage.
"""

from sqlalchemy.orm import Session
from . import models


def seed_if_empty(db: Session):
    existing = db.query(models.Ticket).first()
    if existing:
        return  # already has data, don't touch it

    sample_tickets = [
        {"ticket_id": "TKT-A1B2C3", "customer_name": "Rohan Mehta", "customer_email": "rohan.mehta@example.com",
         "subject": "Unable to reset password",
         "description": "I tried the forgot password link three times but the reset email never arrives. Checked spam folder too.",
         "status": "Open"},
        {"ticket_id": "TKT-D4E5F6", "customer_name": "Priya Sharma", "customer_email": "priya.sharma@example.com",
         "subject": "Invoice shows incorrect amount",
         "description": "My latest invoice charged me for the annual plan instead of monthly. Please correct and refund the difference.",
         "status": "In Progress"},
        {"ticket_id": "TKT-G7H8I9", "customer_name": "Arjun Nair", "customer_email": "arjun.nair@example.com",
         "subject": "App crashes on Android 14",
         "description": "The mobile app crashes immediately after login on my Pixel 8 running Android 14. Worked fine last week.",
         "status": "Open"},
        {"ticket_id": "TKT-J1K2L3", "customer_name": "Sneha Kulkarni", "customer_email": "sneha.k@example.com",
         "subject": "Feature request: dark mode",
         "description": "Would love a dark mode option for the dashboard, especially for late-night usage.",
         "status": "Closed"},
        {"ticket_id": "TKT-M4N5O6", "customer_name": "Vikram Rao", "customer_email": "vikram.rao@example.com",
         "subject": "API rate limit reached unexpectedly",
         "description": "Getting 429 errors well below our documented rate limit of 1000 req/min. Started around 3 PM yesterday.",
         "status": "In Progress"},
        {"ticket_id": "TKT-P7Q8R9", "customer_name": "Ayesha Khan", "customer_email": "ayesha.khan@example.com",
         "subject": "Cannot export data to CSV",
         "description": "The export button on the reports page spins forever and never downloads the file.",
         "status": "Open"},
        {"ticket_id": "TKT-S1T2U3", "customer_name": "Karan Malhotra", "customer_email": "karan.m@example.com",
         "subject": "Billing card declined repeatedly",
         "description": "My card keeps getting declined even though it has sufficient balance and works everywhere else.",
         "status": "Closed"},
        {"ticket_id": "TKT-V4W5X6", "customer_name": "Divya Iyer", "customer_email": "divya.iyer@example.com",
         "subject": "Integration with Slack not syncing",
         "description": "Notifications stopped coming through to our Slack channel two days ago. Reconnected the integration but no change.",
         "status": "Open"},
        {"ticket_id": "TKT-Y7Z8A9", "customer_name": "Farhan Ali", "customer_email": "farhan.ali@example.com",
         "subject": "Request for account deletion",
         "description": "Please permanently delete my account and all associated data per GDPR request.",
         "status": "In Progress"},
        {"ticket_id": "TKT-B1C2D3", "customer_name": "Neha Joshi", "customer_email": "neha.joshi@example.com",
         "subject": "Login page stuck loading",
         "description": "The login page just shows a spinner and never loads the form. Tried Chrome and Firefox, same issue.",
         "status": "Open"},
        {"ticket_id": "TKT-E4F5G6", "customer_name": "Aditya Verma", "customer_email": "aditya.verma@example.com",
         "subject": "Two-factor authentication not sending OTP",
         "description": "I enabled 2FA last week and now the OTP text message never arrives. Tried resending 5 times.",
         "status": "Open"},
        {"ticket_id": "TKT-H7I8J9", "customer_name": "Meera Pillai", "customer_email": "meera.pillai@example.com",
         "subject": "Duplicate charge on credit card",
         "description": "I was charged twice for the same subscription renewal on the 3rd. Please refund the duplicate.",
         "status": "Closed"},
        {"ticket_id": "TKT-K1L2M3", "customer_name": "Siddharth Rao", "customer_email": "siddharth.rao@example.com",
         "subject": "Unable to upload profile picture",
         "description": "Every image I try to upload as my avatar gives a file too large error even though it is under 2MB.",
         "status": "In Progress"},
        {"ticket_id": "TKT-N4O5P6", "customer_name": "Kavya Reddy", "customer_email": "kavya.reddy@example.com",
         "subject": "Report data does not match dashboard",
         "description": "The weekly report PDF shows different totals than what I see live on the dashboard. Which one is correct?",
         "status": "Open"},
        {"ticket_id": "TKT-Q7R8S9", "customer_name": "Imran Sheikh", "customer_email": "imran.sheikh@example.com",
         "subject": "Team member cannot be added",
         "description": "Trying to invite a new team member by email but the invite just fails silently with no error message.",
         "status": "Open"},
        {"ticket_id": "TKT-T1U2V3", "customer_name": "Ritu Bansal", "customer_email": "ritu.bansal@example.com",
         "subject": "Subscription downgrade not reflected",
         "description": "I downgraded from Pro to Basic plan 4 days ago but I am still being shown Pro features and limits.",
         "status": "In Progress"},
        {"ticket_id": "TKT-W4X5Y6", "customer_name": "Aman Gupta", "customer_email": "aman.gupta@example.com",
         "subject": "Webhook not firing on order completion",
         "description": "Our webhook endpoint used to get triggered on every order completion, but nothing has come through since Monday.",
         "status": "Open"},
        {"ticket_id": "TKT-Z7A8B9", "customer_name": "Pooja Desai", "customer_email": "pooja.desai@example.com",
         "subject": "Password reset link expired instantly",
         "description": "The reset link in the email says expired even when I click it within seconds of receiving it.",
         "status": "Closed"},
        {"ticket_id": "TKT-C1D2E3", "customer_name": "Naveen Kumar", "customer_email": "naveen.kumar@example.com",
         "subject": "Mobile app not syncing with desktop",
         "description": "Changes I make on the desktop app take over 24 hours to show up on mobile. Used to be instant.",
         "status": "Open"},
        {"ticket_id": "TKT-F4G5H6", "customer_name": "Tanya Chopra", "customer_email": "tanya.chopra@example.com",
         "subject": "Incorrect timezone on all timestamps",
         "description": "All ticket and order timestamps are showing in UTC instead of my account configured IST timezone.",
         "status": "In Progress"},
        {"ticket_id": "TKT-I7J8K9", "customer_name": "Rahul Saxena", "customer_email": "rahul.saxena@example.com",
         "subject": "Cannot cancel subscription from settings",
         "description": "The cancel subscription button in account settings does nothing when clicked, no confirmation or error.",
         "status": "Open"},
        {"ticket_id": "TKT-L1M2N3", "customer_name": "Anjali Bose", "customer_email": "anjali.bose@example.com",
         "subject": "Search results missing recent items",
         "description": "Search stopped showing anything created in the last 3 days, even though older items appear fine.",
         "status": "Open"},
        {"ticket_id": "TKT-O4P5Q6", "customer_name": "Yusuf Ansari", "customer_email": "yusuf.ansari@example.com",
         "subject": "Requesting bulk data export",
         "description": "Need to export our entire ticket history for the last year as a CSV for an internal audit.",
         "status": "Closed"},
        {"ticket_id": "TKT-R7S8T9", "customer_name": "Nikita Agarwal", "customer_email": "nikita.agarwal@example.com",
         "subject": "Email notifications arriving late",
         "description": "Notification emails are arriving 2-3 hours after the actual event instead of instantly.",
         "status": "In Progress"},
        {"ticket_id": "TKT-U1V2W3", "customer_name": "Deepak Menon", "customer_email": "deepak.menon@example.com",
         "subject": "Custom domain SSL not working",
         "description": "Set up our custom domain last week but it still shows not secure in the browser. DNS looks correctly configured.",
         "status": "Open"},
    ]

    for data in sample_tickets:
        db.add(models.Ticket(**data))

    db.commit()

    # Add one example note to demonstrate the notes feature
    db.commit()
    escalated_ticket = db.query(models.Ticket).filter(models.Ticket.ticket_id == "TKT-M4N5O6").first()
    if escalated_ticket:
        note = models.Note(
            ticket_id=escalated_ticket.id,
            note_text="Checked server logs - looks like a caching bug in the rate limiter, not actual overuse. Escalated to backend team.",
        )
        db.add(note)
        db.commit()