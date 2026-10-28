import os
import logging
import threading
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


def get_chief_editor_emails():
    """Returns email addresses of Chief Editors / Superusers."""
    chief_from_env = getattr(settings, 'CHIEF_EDITOR_EMAIL', '').strip()
    if chief_from_env:
        return [chief_from_env]
    emails = list(User.objects.filter(is_superuser=True).exclude(email='').values_list('email', flat=True))
    if not emails:
        emails = ['editor@ppai.org.in']
    return emails


def _send_email_thread(email_obj):
    """Background worker function executing the actual SMTP network transmission."""
    try:
        email_obj.send(fail_silently=False)
        logger.info(f"[ASYNC EMAIL SENT] '{email_obj.subject}' successfully dispatched to {email_obj.to}")
    except Exception as e:
        logger.error(f"[ASYNC EMAIL FAILED] '{email_obj.subject}' to {email_obj.to}. Error: {e}", exc_info=True)


def dispatch_email_message(email_obj):
    """
    High-Performance Non-blocking Email Dispatcher:
    - In Production: Dispatches email via a background daemon thread so HTTP requests return in <50ms without blocking.
    - In Testing (locmem backend): Dispatches synchronously so assertions on mail.outbox pass reliably.
    """
    backend_name = str(getattr(settings, 'EMAIL_BACKEND', ''))
    if 'locmem' in backend_name or getattr(settings, 'IS_TESTING', False):
        try:
            email_obj.send(fail_silently=False)
            logger.info(f"[TEST EMAIL SENT] '{email_obj.subject}' sent to {email_obj.to}")
        except Exception as e:
            logger.error(f"[TEST EMAIL FAILED] '{email_obj.subject}' to {email_obj.to}: {e}")
    else:
        thread = threading.Thread(target=_send_email_thread, args=(email_obj,), daemon=True)
        thread.start()


# ==============================================================================
# WORKFLOW TRIGGER 1 & 2: SUBMISSION (STAGE 1)
# ==============================================================================

def send_author_submission_acknowledgment(manuscript):
    """Trigger 1: Sends rich HTML acknowledgment email to Author upon manuscript & payment submission."""
    author_email = manuscript.author.email
    if not author_email:
        return

    subject = f"[PPAI] Submission Acknowledgment — {manuscript.tracking_id}"
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'PPAI Editorial Office <editor@ppai.org.in>')

    context = {
        'manuscript': manuscript,
        'author_name': manuscript.author.get_full_name() or manuscript.author.username,
        'subject_area_display': manuscript.get_subject_area_display(),
        'article_type_display': manuscript.get_article_type_display(),
        'payment_txn_id': manuscript.payment_transaction_id or 'Logged with submission',
        'payment_screenshot_status': 'Uploaded successfully' if manuscript.payment_screenshot else 'Pending',
        'abstract_snippet': manuscript.abstract[:500] + ('...' if len(manuscript.abstract) > 500 else ''),
    }

    html_content = render_to_string('emails/author_submission_ack.html', context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=[author_email]
    )
    email.attach_alternative(html_content, "text/html")
    dispatch_email_message(email)


def send_chief_editor_submission_alert(manuscript):
    """Trigger 2: Sends submission alert with attached manuscript file to Chief Editor."""
    chief_emails = get_chief_editor_emails()
    if not chief_emails:
        return

    subject = f"[PPAI New Submission] {manuscript.tracking_id} — {manuscript.author.get_full_name() or manuscript.author.username}"
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'PPAI Editorial Office <editor@ppai.org.in>')

    author_profile = getattr(manuscript.author, 'journal_profile', None)
    context = {
        'manuscript': manuscript,
        'author_name': manuscript.author.get_full_name() or manuscript.author.username,
        'author_email': manuscript.author.email,
        'author_affiliation': getattr(author_profile, 'affiliation', 'Affiliation Not Provided'),
        'subject_area_display': manuscript.get_subject_area_display(),
        'submitted_at': manuscript.created_at.strftime('%Y-%m-%d %H:%M UTC'),
        'payment_txn_id': manuscript.payment_transaction_id or 'Not specified',
        'payment_screenshot_url': manuscript.payment_screenshot.url if manuscript.payment_screenshot else None,
    }

    html_content = render_to_string('emails/chief_editor_submission_alert.html', context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=chief_emails
    )
    email.attach_alternative(html_content, "text/html")

    if manuscript.manuscript_file and os.path.exists(manuscript.manuscript_file.path):
        email.attach_file(manuscript.manuscript_file.path)

    dispatch_email_message(email)


# ==============================================================================
# WORKFLOW TRIGGER 3: REVIEWER INVITATION (STAGE 3)
# ==============================================================================

def send_reviewer_invitation(assignment):
    """Trigger 3: Sends peer review invitation with window time and Accept/Decline action buttons to Reviewer."""
    reviewer_email = assignment.reviewer.email
    if not reviewer_email:
        return

    due_str = assignment.due_date.strftime('%d %B %Y') if assignment.due_date else '14 days from receipt'
    accept_url = f"https://ppai.org.in/portal/reviewer/invitation/{assignment.id}/accept/"
    decline_url = f"https://ppai.org.in/portal/reviewer/invitation/{assignment.id}/decline/"

    subject = f"[PPAI Review Invitation] Peer Review for {assignment.manuscript.tracking_id}"
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'PPAI Editorial Office <editor@ppai.org.in>')

    context = {
        'manuscript': assignment.manuscript,
        'reviewer_name': assignment.reviewer.get_full_name() or assignment.reviewer.username,
        'subject_area_display': assignment.manuscript.get_subject_area_display(),
        'due_date_str': due_str,
        'accept_url': accept_url,
        'decline_url': decline_url,
    }

    html_content = render_to_string('emails/reviewer_invitation.html', context)
    text_content = strip_tags(html_content) + f"\n\nAccept URL: {accept_url}\nDecline URL: {decline_url}\nDue Date: {due_str}"

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=[reviewer_email]
    )
    email.attach_alternative(html_content, "text/html")
    dispatch_email_message(email)


# ==============================================================================
# WORKFLOW TRIGGER 4: CREDENTIALS DISPATCH (STAGE 4)
# ==============================================================================

def send_user_credentials_email(user, raw_password, role_name):
    """Trigger 4: Sends generated portal login credentials for Associate Editor or Reviewer."""
    user_email = user.email
    if not user_email:
        return

    subject = f"[PPAI Portal] Your {role_name} Login Credentials"
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'PPAI Editorial Office <editor@ppai.org.in>')

    context = {
        'full_name': user.get_full_name() or user.username,
        'role_name': role_name,
        'username': user.email or user.username,
        'initial_password': raw_password,
    }

    html_content = render_to_string('emails/user_credentials.html', context)
    text_content = strip_tags(html_content) + f"\n\nUsername: {user.email or user.username}\nPassword: {raw_password}\nPortal URL: https://ppai.org.in/login/"

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=[user_email]
    )
    email.attach_alternative(html_content, "text/html")
    dispatch_email_message(email)


# ==============================================================================
# WORKFLOW TRIGGER 5: REVIEW COMPLETE (STAGE 5)
# ==============================================================================

def send_chief_editor_review_completed(assignment):
    """Trigger 5: Alerts Chief Editor that peer review has been submitted for a manuscript."""
    chief_emails = get_chief_editor_emails()
    if not chief_emails:
        return

    subject = f"[PPAI Review Complete] Reviewer Feedback Lodged for {assignment.manuscript.tracking_id}"
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'PPAI Editorial Office <editor@ppai.org.in>')

    context = {
        'manuscript': assignment.manuscript,
        'reviewer_name': assignment.reviewer.get_full_name() or assignment.reviewer.username,
        'recommendation_display': assignment.get_recommendation_display(),
    }

    html_content = render_to_string('emails/chief_editor_review_completed.html', context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=chief_emails
    )
    email.attach_alternative(html_content, "text/html")
    dispatch_email_message(email)


# ==============================================================================
# WORKFLOW TRIGGER 6: EDITORIAL DECISION (STAGE 6)
# ==============================================================================

def send_author_editorial_decision(manuscript):
    """Trigger 6: Sends formal decision letter and moderated peer comments to Author."""
    author_email = manuscript.author.email
    if not author_email:
        return

    subject = f"[PPAI Decision] Editorial Decision on Manuscript {manuscript.tracking_id}"
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'PPAI Editorial Office <editor@ppai.org.in>')

    approved_reviews = manuscript.review_assignments.filter(status='completed', is_approved_by_editor=True)
    context = {
        'manuscript': manuscript,
        'author_name': manuscript.author.get_full_name() or manuscript.author.username,
        'decision_display': manuscript.get_editor_decision_display(),
        'approved_reviews': approved_reviews,
    }

    html_content = render_to_string('emails/author_editorial_decision.html', context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=[author_email]
    )
    email.attach_alternative(html_content, "text/html")
    dispatch_email_message(email)
