from datetime import timedelta
import secrets
import string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q
from django.http import HttpResponseForbidden, Http404

from .models import UserProfile, Manuscript, ReviewAssignment, ManuscriptRevision, SubmissionActivityLog
from .forms import (
    RoleRegistrationForm, ManuscriptSubmissionForm, ReviewEvaluationForm,
    ManuscriptRevisionForm, EditorDecisionForm
)
from .emails import (
    send_author_submission_acknowledgment,
    send_chief_editor_submission_alert,
    send_reviewer_invitation,
    send_reviewer_reminder,
    send_chief_editor_invitation_expired,
    send_chief_editor_reviewer_response,
    send_reviewer_acceptance_confirmation,
    send_user_credentials_email,
    send_chief_editor_review_completed,
    send_author_editorial_decision,
)


def generate_secure_password(length=10):
    """Generates a secure temporary password containing uppercase, lowercase, and digits."""
    chars = string.ascii_letters + string.digits + '!@%'
    pwd = [secrets.choice(string.ascii_uppercase), secrets.choice(string.digits)]
    pwd += [secrets.choice(chars) for _ in range(max(0, length - 2))]
    secrets.SystemRandom().shuffle(pwd)
    return ''.join(pwd)


def get_user_profile(user):
    """Safely retrieves or creates a UserProfile for the given user."""
    try:
        profile, created = UserProfile.objects.get_or_create(user=user)
    except Exception as e:
        err_str = str(e).lower()
        if 'relation' in err_str or 'does not exist' in err_str or 'no such table' in err_str:
            from django.core.management import call_command
            call_command('migrate', interactive=False)
            profile, created = UserProfile.objects.get_or_create(user=user)
        else:
            raise e
    # If user is superuser/admin, mark admin role (Admin is NOT an editor)
    if user.is_superuser:
        if profile.role != 'admin' or profile.is_editor or profile.is_reviewer or profile.is_author:
            profile.role = 'admin'
            profile.is_editor = False
            profile.is_reviewer = False
            profile.is_author = False
            profile.save()
    elif user.is_staff:
        if not profile.is_editor:
            profile.is_editor = True
            profile.role = 'editor'
            profile.save()
    return profile


def check_and_update_invitation_deadlines():
    """
    Self-healing review deadline tracker:
    1. Past 14 days without acceptance: mark expired and alert Chief Editor to reassign.
    2. Past 7 days without acceptance: send automated follow-up reminder.
    """
    try:
        now = timezone.now()
        seven_days_ago = now - timedelta(days=7)
        fourteen_days_ago = now - timedelta(days=14)

        # 1. 14-Day Expiration
        expired_assignments = ReviewAssignment.objects.filter(
            status='pending',
            invitation_date__lte=fourteen_days_ago
        ).select_related('manuscript', 'reviewer')

        for assignment in expired_assignments:
            assignment.status = 'expired'
            assignment.save()
            SubmissionActivityLog.objects.create(
                manuscript=assignment.manuscript,
                user=assignment.reviewer,
                action="Invitation Expired",
                details=f"Reviewer invitation to {assignment.reviewer.get_full_name() or assignment.reviewer.username} expired after 14 days. Alternate reviewer assignment required."
            )
            send_chief_editor_invitation_expired(assignment)

        # 2. 7-Day Reminder
        reminder_assignments = ReviewAssignment.objects.filter(
            status='pending',
            invitation_date__lte=seven_days_ago,
            invitation_date__gt=fourteen_days_ago,
            reminder_sent=False
        ).select_related('manuscript', 'reviewer')

        for assignment in reminder_assignments:
            send_reviewer_reminder(assignment)
            assignment.reminder_sent = True
            assignment.reminder_date = now
            assignment.save()
            SubmissionActivityLog.objects.create(
                manuscript=assignment.manuscript,
                user=assignment.reviewer,
                action="Review Reminder Sent",
                details=f"Automated 7-day reminder sent to reviewer {assignment.reviewer.get_full_name() or assignment.reviewer.username}."
            )
    except Exception:
        pass


def portal_login(request):
    """Redirects to role-based dashboard if authenticated, else login."""
    if request.user.is_authenticated:
        profile = get_user_profile(request.user)
        if request.user.is_superuser or getattr(profile, 'role', '') == 'admin':
            return redirect('admin_dashboard')
        elif profile.is_editor or (request.user.is_staff and not request.user.is_superuser):
            return redirect('editor_dashboard')
        elif profile.is_reviewer:
            return redirect('reviewer_dashboard')
        return redirect('author_dashboard')
    return redirect('login')


def portal_register(request):
    """Redirects to unified registration."""
    return redirect('register')


def portal_logout(request):
    """Logs out and redirects back to portal login."""
    auth_logout(request)
    messages.info(request, "You have been logged out of the PPAI Editorial Portal.")
    return redirect('login')


# ==============================================================================
# AUTHOR PORTAL VIEWS
# ==============================================================================

@login_required(login_url='login')
def author_dashboard(request):
    """Author home: summary metrics and list of all submitted manuscripts."""
    profile = get_user_profile(request.user)
    if request.user.is_superuser or getattr(profile, 'role', '') == 'admin':
        return redirect('admin_dashboard')

    manuscripts = Manuscript.objects.filter(author=request.user).prefetch_related('revisions', 'review_assignments')

    stats = {
        'total': manuscripts.count(),
        'under_review': manuscripts.filter(status__in=['submitted', 'under_review', 'revised_submitted']).count(),
        'needs_revision': manuscripts.filter(status='revisions_requested').count(),
        'accepted': manuscripts.filter(status='accepted').count(),
    }

    return render(request, 'submissions/author_dashboard.html', {
        'profile': profile,
        'manuscripts': manuscripts,
        'stats': stats,
    })


@login_required(login_url='login')
def submit_manuscript(request):
    """Author submission form: file uploads and metadata entry."""
    profile = get_user_profile(request.user)

    if request.method == 'POST':
        form = ManuscriptSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            manuscript = form.save(commit=False)
            manuscript.author = request.user
            manuscript.save()

            # Record audit log
            SubmissionActivityLog.objects.create(
                manuscript=manuscript,
                user=request.user,
                action="Manuscript Submitted",
                details=f"Initial submission with tracking ID {manuscript.tracking_id}."
            )

            # Automated Triggers (via Brevo / Email): Author Acknowledgment & Chief Editor Alert
            send_author_submission_acknowledgment(manuscript)
            send_chief_editor_submission_alert(manuscript)

            messages.success(request, f"Your manuscript has been successfully submitted! Reference ID: {manuscript.tracking_id}")
            return redirect('author_manuscript_detail', tracking_id=manuscript.tracking_id)
    else:
        form = ManuscriptSubmissionForm()

    return render(request, 'submissions/submit_manuscript.html', {
        'form': form,
        'profile': profile,
    })


@login_required(login_url='login')
def author_manuscript_detail(request, tracking_id):
    """Author view: track timeline, status, and view editor comments/feedback."""
    profile = get_user_profile(request.user)
    manuscript = get_object_or_404(Manuscript, tracking_id=tracking_id)

    # Security check: only the author or editor/staff can view
    if manuscript.author != request.user and not (profile.is_editor or request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("You do not have permission to view this manuscript.")

    revisions = manuscript.revisions.all()
    activity_logs = manuscript.activity_logs.all()

    # Comments done by reviewer go to editor first. ONLY after editor approves and issues decision, it goes to authors!
    if manuscript.status in ['revisions_requested', 'accepted', 'rejected'] and manuscript.editor_decision != 'pending':
        completed_reviews = manuscript.review_assignments.filter(status='completed', is_approved_by_editor=True)
    else:
        completed_reviews = ReviewAssignment.objects.none()

    return render(request, 'submissions/author_manuscript_detail.html', {
        'manuscript': manuscript,
        'profile': profile,
        'revisions': revisions,
        'activity_logs': activity_logs,
        'completed_reviews': completed_reviews,
    })


@login_required(login_url='login')
def author_submit_revision(request, tracking_id):
    """Allows author to submit a revised manuscript and response letter."""
    manuscript = get_object_or_404(Manuscript, tracking_id=tracking_id, author=request.user)

    if manuscript.status != 'revisions_requested':
        messages.warning(request, "This manuscript is not currently awaiting revision.")
        return redirect('author_manuscript_detail', tracking_id=tracking_id)

    if request.method == 'POST':
        form = ManuscriptRevisionForm(request.POST, request.FILES)
        if form.is_valid():
            next_rev_num = manuscript.revisions.count() + 1
            revision = form.save(commit=False)
            revision.manuscript = manuscript
            revision.revision_number = next_rev_num
            revision.save()

            # Update manuscript status
            manuscript.status = 'revised_submitted'
            manuscript.editor_decision = 'pending'
            manuscript.save()

            SubmissionActivityLog.objects.create(
                manuscript=manuscript,
                user=request.user,
                action=f"Revision {next_rev_num} Submitted",
                details="Author uploaded revised manuscript and point-by-point response."
            )

            messages.success(request, f"Revision {next_rev_num} successfully submitted to the editorial board!")
            return redirect('author_manuscript_detail', tracking_id=tracking_id)
    else:
        form = ManuscriptRevisionForm()

    return render(request, 'submissions/submit_revision.html', {
        'manuscript': manuscript,
        'form': form,
    })


# ==============================================================================
# EDITOR PORTAL VIEWS
# ==============================================================================

@login_required(login_url='login')
def editor_dashboard(request):
    """Editor command center: triage, reviewer assignment, and decision management."""
    profile = get_user_profile(request.user)
    if request.user.is_superuser or getattr(profile, 'role', '') == 'admin':
        return redirect('admin_dashboard')

    if not (profile.is_editor or (request.user.is_staff and not request.user.is_superuser)):
        messages.error(request, "Access restricted to Editorial Board members.")
        return redirect('author_dashboard')

    status_filter = request.GET.get('status', 'all')
    manuscripts = Manuscript.objects.all().select_related('author').prefetch_related('review_assignments__reviewer')

    if status_filter != 'all':
        manuscripts = manuscripts.filter(status=status_filter)

    counts = {
        'all': Manuscript.objects.count(),
        'submitted': Manuscript.objects.filter(status='submitted').count(),
        'under_review': Manuscript.objects.filter(status='under_review').count(),
        'review_completed': Manuscript.objects.filter(status='review_completed').count(),
        'revisions_requested': Manuscript.objects.filter(status='revisions_requested').count(),
        'revised_submitted': Manuscript.objects.filter(status='revised_submitted').count(),
        'accepted': Manuscript.objects.filter(status='accepted').count(),
        'rejected': Manuscript.objects.filter(status='rejected').count(),
    }

    return render(request, 'submissions/editor_dashboard.html', {
        'profile': profile,
        'manuscripts': manuscripts,
        'status_filter': status_filter,
        'counts': counts,
    })


@login_required(login_url='login')
def editor_manuscript_review(request, tracking_id):
    """Full editorial view: inspect manuscript, assign reviewers, and return decision/comments."""
    profile = get_user_profile(request.user)
    if not (profile.is_editor or request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("Editorial access required.")

    # Check and process pending reviewer deadlines (7-day reminder, 14-day expiration)
    check_and_update_invitation_deadlines()

    manuscript = get_object_or_404(Manuscript, tracking_id=tracking_id)
    reviews = manuscript.review_assignments.all().select_related('reviewer')
    revisions = manuscript.revisions.all()
    activity_logs = manuscript.activity_logs.all()

    # Available reviewers in the system (excluding author and currently active reviewers)
    assigned_reviewer_ids = reviews.exclude(status__in=['expired', 'declined']).values_list('reviewer_id', flat=True)
    available_reviewers = UserProfile.objects.filter(
        Q(is_reviewer=True) | Q(role='reviewer')
    ).exclude(user=manuscript.author).exclude(user_id__in=assigned_reviewer_ids).select_related('user')

    # Handle Editor Editing Manuscript Details (view and edit access)
    if request.method == 'POST' and 'edit_manuscript' in request.POST:
        title = request.POST.get('title', '').strip()
        abstract = request.POST.get('abstract', '').strip()
        keywords = request.POST.get('keywords', '').strip()
        subject_area = request.POST.get('subject_area', '').strip()
        article_type = request.POST.get('article_type', '').strip()
        co_authors = request.POST.get('co_authors', '').strip()

        if title:
            manuscript.title = title
        if abstract:
            manuscript.abstract = abstract
        if keywords:
            manuscript.keywords = keywords
        if subject_area:
            manuscript.subject_area = subject_area
        if article_type:
            manuscript.article_type = article_type
        if co_authors is not None:
            manuscript.co_authors = co_authors
        manuscript.save()

        SubmissionActivityLog.objects.create(
            manuscript=manuscript,
            user=request.user,
            action="Manuscript Updated by Editor",
            details=f"Editor {request.user.get_full_name() or request.user.username} updated manuscript details."
        )
        messages.success(request, "Manuscript details have been successfully updated.")
        return redirect('editor_manuscript_review', tracking_id=tracking_id)

    # Handle Reviewer Assignment Form submission
    if request.method == 'POST' and 'assign_reviewer' in request.POST:
        reviewer_id = request.POST.get('reviewer_id')
        due_days = int(request.POST.get('due_days', 21))
        due_date = timezone.now().date() + timedelta(days=due_days)

        if reviewer_id:
            reviewer_user = get_object_or_404(User, id=reviewer_id)
            assignment = ReviewAssignment.objects.create(
                manuscript=manuscript,
                reviewer=reviewer_user,
                assigned_by=request.user,
                due_date=due_date,
                status='pending'
            )

            # Update status to under review
            if manuscript.status in ['submitted', 'revised_submitted']:
                manuscript.status = 'under_review'
                manuscript.save()

            # Automated Trigger 3: Send Reviewer Invitation Email (via Brevo)
            send_reviewer_invitation(assignment)

            SubmissionActivityLog.objects.create(
                manuscript=manuscript,
                user=request.user,
                action="Reviewer Assigned",
                details=f"Assigned reviewer {reviewer_user.get_full_name() or reviewer_user.username} with due date {due_date}."
            )

            messages.success(request, f"Review invitation assigned to {reviewer_user.get_full_name() or reviewer_user.username}.")
            return redirect('editor_manuscript_review', tracking_id=tracking_id)

    # Handle explicit Reviewer Comment Approval by Editor
    if request.method == 'POST' and 'toggle_review_approval' in request.POST:
        assignment_id = request.POST.get('assignment_id')
        rev = get_object_or_404(ReviewAssignment, id=assignment_id, manuscript=manuscript)
        rev.is_approved_by_editor = not rev.is_approved_by_editor
        rev.save()
        st_label = "approved to be sent to author" if rev.is_approved_by_editor else "held for editor only"
        messages.success(request, f"Reviewer evaluation {st_label}.")
        return redirect('editor_manuscript_review', tracking_id=tracking_id)

    # Handle Editorial Decision Form submission (Accept / Revision / Reject)
    if request.method == 'POST' and 'submit_decision' in request.POST:
        decision = request.POST.get('decision')
        comments_to_author = request.POST.get('comments_to_author', '')
        internal_notes = request.POST.get('internal_notes', '')

        status_mapping = {
            'accept': 'accepted',
            'publish': 'published',
            'minor_revision': 'revisions_requested',
            'major_revision': 'revisions_requested',
            'reject': 'rejected',
        }

        if decision in status_mapping:
            manuscript.editor_decision = decision
            manuscript.status = status_mapping[decision]
            manuscript.editor_comments_to_author = comments_to_author
            manuscript.editor_internal_notes = internal_notes
            manuscript.assigned_editor = request.user
            manuscript.decision_date = timezone.now()
            manuscript.save()

            # Approve reviewer comments so they are released to author with this decision
            if request.POST.get('approve_reviewer_comments', '1') == '1':
                manuscript.review_assignments.filter(status='completed').update(is_approved_by_editor=True)

            # Automated Trigger 6: Send Formal Editorial Decision & Moderated Feedback Email to Author (via Brevo)
            send_author_editorial_decision(manuscript)

            decision_display = dict(EditorDecisionForm.DECISION_CHOICES).get(decision, decision)
            SubmissionActivityLog.objects.create(
                manuscript=manuscript,
                user=request.user,
                action=f"Editorial Decision: {decision_display}",
                details=f"Decision issued by Editor {request.user.get_full_name() or request.user.username}. Comments returned to author."
            )

            messages.success(request, f"Editorial decision '{decision_display}' has been recorded and comments returned to author!")
            return redirect('editor_manuscript_review', tracking_id=tracking_id)

    return render(request, 'submissions/editor_manuscript_review.html', {
        'manuscript': manuscript,
        'profile': profile,
        'reviews': reviews,
        'revisions': revisions,
        'activity_logs': activity_logs,
        'available_reviewers': available_reviewers,
        'article_types': Manuscript.ARTICLE_TYPES,
        'subject_areas': Manuscript.SUBJECT_AREAS,
    })


# ==============================================================================
# REVIEWER PORTAL VIEWS
# ==============================================================================

@login_required(login_url='login')
def reviewer_dashboard(request):
    """Reviewer home: assigned manuscripts awaiting evaluation or in progress."""
    profile = get_user_profile(request.user)
    if request.user.is_superuser or getattr(profile, 'role', '') == 'admin':
        return redirect('admin_dashboard')

    if not (profile.is_reviewer or profile.role == 'reviewer'):
        messages.error(request, "Reviewer panel access required.")
        return redirect('author_dashboard')

    assignments = ReviewAssignment.objects.filter(reviewer=request.user).select_related('manuscript', 'assigned_by').order_by('-id')

    stats = {
        'total': assignments.count(),
        'new_assignments': assignments.filter(status='pending').count(),
        'pending_assignments': assignments.filter(status='accepted').count(),
        'complete_assignments': assignments.filter(status='completed').count(),
        'pending': assignments.filter(status='pending').count(),
        'in_progress': assignments.filter(status='accepted').count(),
        'completed': assignments.filter(status='completed').count(),
    }

    return render(request, 'submissions/reviewer_dashboard.html', {
        'profile': profile,
        'assignments': assignments,
        'stats': stats,
    })


def reviewer_respond_invitation(request, assignment_id, response_action):
    """Allows reviewer to Accept or Decline a review request, directly via signed link or portal."""
    from django.core.signing import TimestampSigner
    from django.urls import reverse
    token = request.GET.get('token')
    signer = TimestampSigner()
    assignment = None

    if token:
        try:
            unsigned = signer.unsign(token, max_age=86400 * 30)
            parts = unsigned.split(':')
            if len(parts) == 2 and int(parts[0]) == assignment_id:
                assignment = get_object_or_404(ReviewAssignment, id=assignment_id, reviewer_id=int(parts[1]))
        except Exception:
            assignment = None

    if not assignment:
        if not request.user.is_authenticated:
            return redirect(f"{reverse('portal_login')}?next={request.get_full_path()}")
        assignment = get_object_or_404(ReviewAssignment, id=assignment_id)
        if assignment.reviewer != request.user and not request.user.is_superuser:
            return HttpResponseForbidden("You are not the assigned reviewer for this manuscript.")

    reviewer_user = assignment.reviewer

    if response_action == 'accept':
        assignment.status = 'accepted'
        assignment.save()
        SubmissionActivityLog.objects.create(
            manuscript=assignment.manuscript,
            user=reviewer_user,
            action="Review Invitation Accepted",
            details=f"Reviewer {reviewer_user.get_full_name() or reviewer_user.username} accepted the evaluation."
        )

        # Trigger 4: Provision/reset password & dispatch credentials to Reviewer so they can sign in
        temp_password = generate_secure_password(length=10)
        reviewer_user.set_password(temp_password)
        reviewer_user.save()
        if request.user.is_authenticated and request.user.id == reviewer_user.id:
            update_session_auth_hash(request, reviewer_user)

        # Automated Email Dispatches (via Brevo): Credentials (Email 4), alert to Chief Editor, confirmation to Reviewer
        send_user_credentials_email(reviewer_user, temp_password, 'Reviewer')
        send_chief_editor_reviewer_response(assignment, action='accepted')
        send_reviewer_acceptance_confirmation(assignment)

        return render(request, 'submissions/invitation_response.html', {
            'assignment': assignment,
            'action': 'accept',
        })
    elif response_action == 'decline':
        assignment.status = 'declined'
        assignment.save()
        SubmissionActivityLog.objects.create(
            manuscript=assignment.manuscript,
            user=reviewer_user,
            action="Review Invitation Declined",
            details=f"Reviewer {reviewer_user.get_full_name() or reviewer_user.username} declined the evaluation."
        )
        # Notify Chief Editor so they can reassign immediately
        send_chief_editor_reviewer_response(assignment, action='declined')
        return render(request, 'submissions/invitation_response.html', {
            'assignment': assignment,
            'action': 'decline',
        })

    return redirect('reviewer_dashboard')


@login_required(login_url='portal_login')
def reviewer_evaluate_manuscript(request, assignment_id):
    """Reviewer evaluation form: scores, author comments, confidential editor notes."""
    assignment = get_object_or_404(ReviewAssignment, id=assignment_id, reviewer=request.user)

    if assignment.status == 'declined':
        messages.error(request, "You previously declined this review request.")
        return redirect('reviewer_dashboard')

    # Automatically transition pending assignment to accepted upon opening workspace
    if assignment.status == 'pending':
        assignment.status = 'accepted'
        assignment.save()
        SubmissionActivityLog.objects.create(
            manuscript=assignment.manuscript,
            user=request.user,
            action="Review Workspace Opened",
            details=f"Reviewer {request.user.get_full_name() or request.user.username} opened review workspace."
        )
        # Notify Chief Editor & send confirmation to Reviewer
        send_chief_editor_reviewer_response(assignment, action='accepted')
        send_reviewer_acceptance_confirmation(assignment)

    if request.method == 'POST':
        form = ReviewEvaluationForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            review = form.save(commit=False)
            review.status = 'completed'
            review.completed_date = timezone.now()
            review.save()

            # Record activity log
            SubmissionActivityLog.objects.create(
                manuscript=assignment.manuscript,
                user=request.user,
                action="Peer Review Submitted",
                details=f"Reviewer submitted recommendation: {review.get_recommendation_display()}."
            )

            # Automated Trigger 5: Alert Chief Editor that Peer Review is complete (via Brevo)
            send_chief_editor_review_completed(review)

            # If all reviews are completed, update manuscript status
            remaining = assignment.manuscript.review_assignments.filter(status__in=['pending', 'accepted']).count()
            if remaining == 0:
                assignment.manuscript.status = 'review_completed'
                assignment.manuscript.save()

            messages.success(request, f"Thank you! Your peer review for {assignment.manuscript.tracking_id} has been submitted to the Editor.")
            return redirect('reviewer_dashboard')
    else:
        form = ReviewEvaluationForm(instance=assignment)

    return render(request, 'submissions/reviewer_evaluate.html', {
        'assignment': assignment,
        'manuscript': assignment.manuscript,
        'form': form,
    })


@login_required
def editor_add_user(request):
    """Allows Editor/Admin to register new Editors or Reviewers in a dedicated 1-step form."""
    profile = get_user_profile(request.user)
    if not (profile.is_editor or request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("Access restricted to Editors and Administrators.")

    context = {}
    if request.method == 'POST':
        role = request.POST.get('role', 'reviewer').strip().lower()
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        affiliation = request.POST.get('affiliation', '').strip()
        specialization = request.POST.get('specialization', '').strip()
        password = request.POST.get('password', '').strip()

        context.update({
            'role': role,
            'full_name': full_name,
            'email': email,
            'affiliation': affiliation,
            'specialization': specialization,
        })

        if not full_name:
            context['error'] = 'Please enter the full name.'
            return render(request, 'submissions/add_editorial_user.html', context)

        if not email:
            context['error'] = 'Please enter a valid email address.'
            return render(request, 'submissions/add_editorial_user.html', context)

        import re
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            context['error'] = 'Please enter a valid email address format.'
            return render(request, 'submissions/add_editorial_user.html', context)

        if User.objects.filter(username__iexact=email).exists() or User.objects.filter(email__iexact=email).exists():
            context['error'] = f'An account with email {email} already exists.'
            return render(request, 'submissions/add_editorial_user.html', context)

        if len(password) < 6:
            context['error'] = 'Password must be at least 6 characters long.'
            return render(request, 'submissions/add_editorial_user.html', context)

        if not any(c.isupper() for c in password):
            context['error'] = 'Password must contain at least one uppercase letter.'
            return render(request, 'submissions/add_editorial_user.html', context)

        # Create user
        name_parts = full_name.split(None, 1)
        first_name = name_parts[0] if name_parts else ''
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        is_editor = (role == 'editor')
        is_reviewer = (role == 'reviewer')

        if is_editor:
            user.is_staff = True
            user.save()

        user_prof, _ = UserProfile.objects.update_or_create(
            user=user,
            defaults={
                'role': 'editor' if is_editor else 'reviewer',
                'is_editor': is_editor,
                'is_reviewer': is_reviewer,
                'is_author': True,
                'is_approved_reviewer': is_reviewer,
                'is_approved_editor': is_editor,
                'affiliation': affiliation,
                'specialization': specialization,
            }
        )

        role_name = 'Editor' if is_editor else 'Reviewer'
        messages.success(
            request,
            f"Successfully registered {role_name}: {full_name} ({email})! They can now log in at /login/."
        )
        return redirect('editor_dashboard')

    return render(request, 'submissions/add_editorial_user.html', context)


# ==============================================================================
# ADMINISTRATOR COMMAND CENTER VIEWS
# ==============================================================================

@login_required(login_url='login')
def admin_dashboard(request):
    """Admin Command Center: view/filter users, register editors/reviewers, delete users."""
    profile = get_user_profile(request.user)
    if not (request.user.is_superuser or getattr(profile, 'role', '') == 'admin'):
        messages.error(request, "Access restricted to Administrators.")
        return redirect('portal_login')

    # Self-healing check for 7-day reminders and 14-day auto-expirations
    check_and_update_invitation_deadlines()

    if request.method == 'POST' and request.POST.get('action') == 'create_user':
        role = request.POST.get('role', 'reviewer').strip().lower()
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        affiliation = request.POST.get('affiliation', '').strip()
        specialization = request.POST.get('specialization', '').strip()
        password = request.POST.get('password', '').strip()

        import re
        if not full_name or not email or not password or not affiliation:
            messages.error(request, "Full name, email, affiliation, and password are required.")
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messages.error(request, "Please enter a valid email address format (e.g. user@institution.edu.in).")
        elif User.objects.filter(username__iexact=email).exists() or User.objects.filter(email__iexact=email).exists():
            messages.error(request, f"Registration Alert: An account with email {email} already exists. Two users cannot share the same login credentials.")
        elif len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
        elif not any(c.isupper() for c in password):
            messages.error(request, "Password must contain at least one uppercase letter.")
        else:
            name_parts = full_name.split(None, 1)
            first_name = name_parts[0] if name_parts else ''
            last_name = name_parts[1] if len(name_parts) > 1 else ''

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            is_editor = (role in ['editor', 'associate_editor', 'associate editor'])
            is_reviewer = (role == 'reviewer')

            if is_editor:
                user.is_staff = True
                user.save()

            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'role': 'editor' if is_editor else 'reviewer',
                    'is_editor': is_editor,
                    'is_reviewer': is_reviewer,
                    'is_author': True,
                    'is_approved_reviewer': is_reviewer,
                    'is_approved_editor': is_editor,
                    'affiliation': affiliation,
                    'specialization': specialization,
                }
            )

            role_name = 'Associate Editor' if is_editor else 'Reviewer'

            if is_editor:
                # Dispatch credentials only for Associate Editors upon account creation
                send_user_credentials_email(user, password, 'Associate Editor')
                messages.success(request, f"Successfully registered Associate Editor: {full_name} ({email})! Login credentials have been dispatched.")
            else:
                # Reviewers do NOT receive login credentials upon registration.
                # Reviewer credentials are ONLY dispatched after the reviewer accepts a peer review invitation.
                messages.success(request, f"Successfully registered Reviewer: {full_name} ({email}) in reviewer directory. Credentials will only be sent after they accept a review invitation.")
            return redirect('admin_dashboard')

    # Filtering users
    filter_role = request.GET.get('role', 'all').strip().lower()

    # Ensure all users have a journal_profile
    users_qs = User.objects.all().select_related('journal_profile').order_by('-date_joined')
    for u in users_qs:
        if not hasattr(u, 'journal_profile'):
            get_user_profile(u)

    users_qs = User.objects.all().select_related('journal_profile').order_by('-date_joined')

    counts = {
        'all': users_qs.count(),
        'editors': users_qs.filter(journal_profile__is_editor=True).exclude(is_superuser=True).distinct().count(),
        'reviewers': users_qs.filter(journal_profile__is_reviewer=True).exclude(is_superuser=True).count(),
        'authors': users_qs.filter(
            Q(journal_profile__is_editor=False, journal_profile__is_reviewer=False, is_superuser=False, is_staff=False)
        ).count(),
    }

    if filter_role == 'editor':
        filtered_users = [u for u in users_qs if not u.is_superuser and hasattr(u, 'journal_profile') and u.journal_profile.is_editor]
    elif filter_role == 'reviewer':
        filtered_users = [u for u in users_qs if not u.is_superuser and hasattr(u, 'journal_profile') and u.journal_profile.is_reviewer]
    elif filter_role == 'author':
        filtered_users = [
            u for u in users_qs
            if not u.is_superuser and not u.is_staff and hasattr(u, 'journal_profile') and not u.journal_profile.is_editor and not u.journal_profile.is_reviewer
        ]
    else:
        filter_role = 'all'
        filtered_users = list(users_qs)

    # Author-Centric Queue: All Authors who have submitted manuscripts
    author_users = User.objects.filter(
        manuscripts__isnull=False
    ).distinct().prefetch_related('manuscripts', 'journal_profile').order_by('-date_joined')

    author_cards = []
    for a in author_users:
        author_cards.append({
            'author': a,
            'profile': getattr(a, 'journal_profile', None),
            'manuscripts': a.manuscripts.all().order_by('-created_at'),
            'total_papers': a.manuscripts.count(),
        })

    # Manuscript Workflow Statistics & Filtering
    all_manuscripts = Manuscript.objects.all().select_related(
        'author', 'author__journal_profile', 'assigned_editor'
    ).order_by('-created_at')

    manuscript_stats = {
        'total': all_manuscripts.count(),
        'received': all_manuscripts.filter(status='submitted').count(),
        'under_review': all_manuscripts.filter(status__in=['under_review', 'review_completed']).count(),
        'under_2nd_review': all_manuscripts.filter(status='revised_submitted').count(),
        'sent_back_to_author': all_manuscripts.filter(status='revisions_requested').count(),
        'accepted': all_manuscripts.filter(status='accepted').count(),
        'rejected': all_manuscripts.filter(status='rejected').count(),
        'published': all_manuscripts.filter(status='published').count(),
    }

    filter_status = request.GET.get('status', 'all').strip().lower()
    search_q = request.GET.get('q', '').strip()

    filtered_manuscripts = all_manuscripts
    if filter_status == 'received':
        filtered_manuscripts = filtered_manuscripts.filter(status='submitted')
    elif filter_status == 'under_review':
        filtered_manuscripts = filtered_manuscripts.filter(status__in=['under_review', 'review_completed'])
    elif filter_status == 'under_2nd_review':
        filtered_manuscripts = filtered_manuscripts.filter(status='revised_submitted')
    elif filter_status in ['sent_back_to_author', 'sent_back']:
        filtered_manuscripts = filtered_manuscripts.filter(status='revisions_requested')
    elif filter_status == 'accepted':
        filtered_manuscripts = filtered_manuscripts.filter(status='accepted')
    elif filter_status == 'rejected':
        filtered_manuscripts = filtered_manuscripts.filter(status='rejected')
    elif filter_status == 'published':
        filtered_manuscripts = filtered_manuscripts.filter(status='published')
    else:
        filter_status = 'all'

    if search_q:
        filtered_manuscripts = filtered_manuscripts.filter(
            Q(tracking_id__icontains=search_q) |
            Q(title__icontains=search_q) |
            Q(author__first_name__icontains=search_q) |
            Q(author__last_name__icontains=search_q) |
            Q(author__email__icontains=search_q) |
            Q(keywords__icontains=search_q)
        )

    return render(request, 'submissions/admin_dashboard.html', {
        'profile': profile,
        'users': filtered_users,
        'filter_role': filter_role,
        'counts': counts,
        'author_cards': author_cards,
        'manuscripts': filtered_manuscripts,
        'manuscript_stats': manuscript_stats,
        'filter_status': filter_status,
        'search_q': search_q,
    })


@login_required(login_url='login')
def admin_delete_user(request, user_id):
    """Deletes a user account from the admin dashboard."""
    profile = get_user_profile(request.user)
    if not (request.user.is_superuser or getattr(profile, 'role', '') == 'admin'):
        messages.error(request, "Access restricted to Administrators.")
        return redirect('portal_login')

    if user_id == request.user.id:
        messages.error(request, "You cannot delete your own administrator account.")
        return redirect('admin_dashboard')

    target_user = get_object_or_404(User, id=user_id)
    username = target_user.username
    target_user.delete()
    messages.success(request, f"User '{username}' was successfully deleted.")
    return redirect('admin_dashboard')

