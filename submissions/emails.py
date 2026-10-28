import os
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.contrib.auth.models import User


def get_chief_editor_emails():
    """Returns email addresses of Chief Editors / Superusers."""
    emails = list(User.objects.filter(is_superuser=True).exclude(email='').values_list('email', flat=True))
    if not emails:
        emails = ['ijpp1972@yahoo.co.in', 'admin@ppai.org.in']
    return emails


def send_author_submission_acknowledgment(manuscript):
    """Trigger 1: Sends acknowledgment email to Author upon manuscript & payment submission."""
    author_email = manuscript.author.email
    if not author_email:
        return

    subject = f"[IJPP] Submission Acknowledgment — {manuscript.tracking_id}"
    message = f"""Dear {manuscript.author.get_full_name() or manuscript.author.username},

Thank you for submitting your manuscript to the Indian Journal of Plant Protection (IJPP), published by the Plant Protection Association of India (PPAI).

Your submission has been logged into the editorial pipeline with the following details:

============================================================
MANUSCRIPT SUBMISSION DETAILS
============================================================
Tracking ID: {manuscript.tracking_id}
Title: {manuscript.title}
Subject Area: {manuscript.get_subject_area_display()}
Article Category: {manuscript.get_article_type_display()}

PAYMENT VERIFICATION:
Transaction / Reference ID: {manuscript.payment_transaction_id or 'Logged with submission'}
Payment Screenshot: {'Uploaded successfully' if manuscript.payment_screenshot else 'Pending'}

============================================================
ABSTRACT:
{manuscript.abstract[:500]}...

Your manuscript will now undergo initial technical screening by the Chief Editor. You may track the live evaluation status at any time by logging into the portal:
https://ppai.org.in/login/

Sincerely,
Editorial Office
Indian Journal of Plant Protection (IJPP)
Plant Protection Association of India (PPAI)
https://ppai.org.in
"""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'ijpp@ppai.org.in'),
            recipient_list=[author_email],
            fail_silently=True
        )
    except Exception:
        pass


def send_chief_editor_submission_alert(manuscript):
    """Trigger 2: Sends submission alert with attached manuscript file to Chief Editor."""
    chief_emails = get_chief_editor_emails()
    subject = f"[IJPP New Submission] {manuscript.tracking_id} — {manuscript.author.get_full_name() or manuscript.author.username}"
    message = f"""Chief Editor,

A new manuscript and payment proof have been lodged in the IJPP portal.

============================================================
SUBMISSION SUMMARY
============================================================
Tracking ID: {manuscript.tracking_id}
Author: {manuscript.author.get_full_name() or manuscript.author.username} ({manuscript.author.email})
Affiliation: {getattr(getattr(manuscript.author, 'journal_profile', None), 'affiliation', 'N/A')}
Title: {manuscript.title}
Subject Area: {manuscript.get_subject_area_display()}
Submitted On: {manuscript.created_at.strftime('%Y-%m-%d %H:%M UTC')}

PAYMENT PROOF:
Transaction ID: {manuscript.payment_transaction_id or 'Not specified'}
Payment Proof File: {manuscript.payment_screenshot.url if manuscript.payment_screenshot else 'None'}

============================================================
Direct Action in Chief Editor Console:
https://ppai.org.in/portal/admin/
"""
    try:
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'ijpp@ppai.org.in'),
            to=chief_emails
        )
        if manuscript.manuscript_file and os.path.exists(manuscript.manuscript_file.path):
            email.attach_file(manuscript.manuscript_file.path)
        email.send(fail_silently=True)
    except Exception:
        pass


def send_reviewer_invitation(assignment):
    """Trigger 3: Sends peer review invitation with window time to Reviewer."""
    reviewer_email = assignment.reviewer.email
    if not reviewer_email:
        return

    due_str = assignment.due_date.strftime('%d %B %Y') if assignment.due_date else '14 days from receipt'
    subject = f"[IJPP Review Invitation] Peer Review for {assignment.manuscript.tracking_id}"
    message = f"""Dear {assignment.reviewer.get_full_name() or assignment.reviewer.username},

You have been invited by the Chief Editor of the Indian Journal of Plant Protection (IJPP) to evaluate the following manuscript:

Title: {assignment.manuscript.title}
Discipline: {assignment.manuscript.get_subject_area_display()}
Review Window Due Date: {due_str}

ABSTRACT:
{assignment.manuscript.abstract}

Please log into your Reviewer Console to access the full manuscript files and submit your evaluation:
https://ppai.org.in/login/

Thank you for contributing your scientific expertise to peer review.

Chief Editor
Indian Journal of Plant Protection (IJPP)
Plant Protection Association of India (PPAI)
"""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'ijpp@ppai.org.in'),
            recipient_list=[reviewer_email],
            fail_silently=True
        )
    except Exception:
        pass


def send_user_credentials_email(user, raw_password, role_name):
    """Trigger 4: Sends generated portal login credentials for Associate Editor or Reviewer."""
    user_email = user.email
    if not user_email:
        return

    subject = f"[IJPP Portal] Your {role_name} Login Credentials"
    message = f"""Dear {user.get_full_name() or user.username},

Your {role_name} account for the Indian Journal of Plant Protection (IJPP) editorial management portal has been provisioned by the Chief Editor.

============================================================
YOUR LOGIN CREDENTIALS
============================================================
Portal URL: https://ppai.org.in/login/
Role: {role_name}
Username / Email: {user.email or user.username}
Initial Password: {raw_password}
============================================================

Instructions:
1. Visit https://ppai.org.in/login/
2. Select the '{role_name}' role chip located below the credentials fields.
3. Enter your email and password to access your dedicated console.

Editorial Office
Indian Journal of Plant Protection (IJPP)
Plant Protection Association of India (PPAI)
"""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'ijpp@ppai.org.in'),
            recipient_list=[user_email],
            fail_silently=True
        )
    except Exception:
        pass


def send_chief_editor_review_completed(assignment):
    """Trigger 5: Alerts Chief Editor that peer review has been submitted for a manuscript."""
    chief_emails = get_chief_editor_emails()
    subject = f"[IJPP Review Complete] Reviewer Feedback Lodged for {assignment.manuscript.tracking_id}"
    message = f"""Chief Editor,

Peer reviewer {assignment.reviewer.get_full_name() or assignment.reviewer.username} has completed and submitted evaluation for:

Tracking ID: {assignment.manuscript.tracking_id}
Title: {assignment.manuscript.title}
Reviewer Recommendation: {assignment.get_recommendation_display()}

The rubric scores, author feedback, and confidential editor notes are ready for your inspection and moderation:
https://ppai.org.in/portal/editor/manuscript/{assignment.manuscript.tracking_id}/

Editorial Management System
Indian Journal of Plant Protection (IJPP)
"""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'ijpp@ppai.org.in'),
            recipient_list=chief_emails,
            fail_silently=True
        )
    except Exception:
        pass


def send_author_editorial_decision(manuscript):
    """Trigger 6: Sends formal decision letter and moderated peer comments to Author."""
    author_email = manuscript.author.email
    if not author_email:
        return

    subject = f"[IJPP Decision] Editorial Decision on Manuscript {manuscript.tracking_id}"
    decision_name = manuscript.get_editor_decision_display()

    comments_block = ""
    # Fetch approved reviews
    approved_reviews = manuscript.review_assignments.filter(status='completed', is_approved_by_editor=True)
    if approved_reviews.exists():
        comments_block += "\n--- PEER REVIEW COMMENTS ---\n"
        for idx, rev in enumerate(approved_reviews, start=1):
            comments_block += f"\nReviewer #{idx}:\n{rev.comments_for_author}\n"

    if manuscript.editor_comments_to_author:
        comments_block += f"\n--- CHIEF EDITOR REMARKS ---\n{manuscript.editor_comments_to_author}\n"

    message = f"""Dear {manuscript.author.get_full_name() or manuscript.author.username},

Regarding your manuscript submitted to the Indian Journal of Plant Protection (IJPP):

Tracking ID: {manuscript.tracking_id}
Title: {manuscript.title}

EDITORIAL DECISION: {decision_name}
{comments_block}
============================================================
You can view full feedback or submit revisions by visiting your Author Dashboard:
https://ppai.org.in/portal/author/

Sincerely,
Chief Editor
Indian Journal of Plant Protection (IJPP)
Plant Protection Association of India (PPAI)
"""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'ijpp@ppai.org.in'),
            recipient_list=[author_email],
            fail_silently=True
        )
    except Exception:
        pass
