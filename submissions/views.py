from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
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


def get_user_profile(user):
    """Safely retrieves or creates a UserProfile for the given user."""
    profile, created = UserProfile.objects.get_or_create(user=user)
    # If user is staff/superuser, make sure they have editor permissions
    if user.is_staff or user.is_superuser:
        if not profile.is_editor:
            profile.is_editor = True
            profile.role = 'editor'
            profile.save()
    return profile


def portal_login(request):
    """Redirects to role-based dashboard if authenticated, else login."""
    if request.user.is_authenticated:
        profile = get_user_profile(request.user)
        if profile.is_editor or request.user.is_staff or request.user.is_superuser:
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
    messages.info(request, "You have been logged out of the IJPP Editorial Portal.")
    return redirect('login')


# ==============================================================================
# AUTHOR PORTAL VIEWS
# ==============================================================================

@login_required(login_url='login')
def author_dashboard(request):
    """Author home: summary metrics and list of all submitted manuscripts."""
    profile = get_user_profile(request.user)
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
    if not (profile.is_editor or request.user.is_staff or request.user.is_superuser):
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

    manuscript = get_object_or_404(Manuscript, tracking_id=tracking_id)
    reviews = manuscript.review_assignments.all().select_related('reviewer')
    revisions = manuscript.revisions.all()
    activity_logs = manuscript.activity_logs.all()

    # Available reviewers in the system (excluding the author)
    assigned_reviewer_ids = reviews.values_list('reviewer_id', flat=True)
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
            ReviewAssignment.objects.create(
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
    if not (profile.is_reviewer or profile.role == 'reviewer' or profile.is_editor or request.user.is_staff):
        messages.error(request, "Reviewer panel access required.")
        return redirect('author_dashboard')

    assignments = ReviewAssignment.objects.filter(reviewer=request.user).select_related('manuscript', 'assigned_by')

    stats = {
        'total': assignments.count(),
        'pending': assignments.filter(status='pending').count(),
        'in_progress': assignments.filter(status='accepted').count(),
        'completed': assignments.filter(status='completed').count(),
    }

    return render(request, 'submissions/reviewer_dashboard.html', {
        'profile': profile,
        'assignments': assignments,
        'stats': stats,
    })


@login_required(login_url='login')
def reviewer_respond_invitation(request, assignment_id, response_action):
    """Allows reviewer to Accept or Decline a review request."""
    assignment = get_object_or_404(ReviewAssignment, id=assignment_id, reviewer=request.user)

    if response_action == 'accept':
        assignment.status = 'accepted'
        assignment.save()
        SubmissionActivityLog.objects.create(
            manuscript=assignment.manuscript,
            user=request.user,
            action="Review Invitation Accepted",
            details=f"Reviewer {request.user.get_full_name() or request.user.username} accepted the evaluation."
        )
        messages.success(request, f"You have accepted the review for {assignment.manuscript.tracking_id}. Please submit your review before {assignment.due_date}.")
        return redirect('reviewer_evaluate_manuscript', assignment_id=assignment.id)
    elif response_action == 'decline':
        assignment.status = 'declined'
        assignment.save()
        SubmissionActivityLog.objects.create(
            manuscript=assignment.manuscript,
            user=request.user,
            action="Review Invitation Declined",
            details=f"Reviewer {request.user.get_full_name() or request.user.username} declined the evaluation."
        )
        messages.info(request, "Review invitation declined.")

    return redirect('reviewer_dashboard')


@login_required(login_url='login')
def reviewer_evaluate_manuscript(request, assignment_id):
    """Reviewer evaluation form: scores, author comments, confidential editor notes."""
    assignment = get_object_or_404(ReviewAssignment, id=assignment_id, reviewer=request.user)

    if assignment.status == 'declined':
        messages.error(request, "You previously declined this review request.")
        return redirect('reviewer_dashboard')

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
