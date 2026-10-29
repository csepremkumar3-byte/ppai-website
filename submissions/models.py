import os
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


def manuscript_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    clean_id = instance.tracking_id or uuid.uuid4().hex[:8]
    return f'manuscripts/{clean_id}/{uuid.uuid4().hex[:6]}_{filename}'


def revision_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    clean_id = instance.manuscript.tracking_id or 'rev'
    return f'manuscripts/{clean_id}/revisions/rev_{instance.revision_number}_{uuid.uuid4().hex[:6]}_{filename}'


def reviewer_annotated_path(instance, filename):
    clean_id = instance.manuscript.tracking_id or 'review'
    return f'manuscripts/{clean_id}/reviews/{uuid.uuid4().hex[:6]}_{filename}'


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('author', 'Author (Submit & Track Manuscripts)'),
        ('reviewer', 'Reviewer (Peer Review Assigned Papers)'),
        ('editor', 'Editor (Editorial Decision & Reviewer Assignment)'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='journal_profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='author')
    is_author = models.BooleanField(default=True)
    is_reviewer = models.BooleanField(default=False)
    is_editor = models.BooleanField(default=False)

    phone = models.CharField(max_length=25, blank=True)
    affiliation = models.CharField(max_length=255, blank=True, help_text="Institution / University / Department")
    designation = models.CharField(max_length=150, blank=True, help_text="e.g. Principal Scientist, Professor, Research Scholar")
    specialization = models.CharField(max_length=255, blank=True, help_text="e.g. Agricultural Entomology, Biocontrol, Plant Virology")
    orcid_id = models.CharField(max_length=50, blank=True, help_text="0000-0000-0000-0000")
    bio = models.TextField(blank=True)

    is_approved_reviewer = models.BooleanField(default=True, help_text="Allows user to be assigned papers as a reviewer")
    is_approved_editor = models.BooleanField(default=False, help_text="Admin approval required for editorial access")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Journal Profile"
        verbose_name_plural = "User Journal Profiles"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"

    def save(self, *args, **kwargs):
        if self.role == 'editor':
            self.is_editor = True
            self.is_author = True
        elif self.role == 'reviewer':
            self.is_reviewer = True
            self.is_author = True
        elif self.role == 'author':
            self.is_author = True
        super().save(*args, **kwargs)


class Manuscript(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted / Initial Screening'),
        ('under_review', 'Under Peer Review'),
        ('review_completed', 'Review Completed - Pending Decision'),
        ('revisions_requested', 'Revisions Requested'),
        ('revised_submitted', 'Revised Manuscript Submitted'),
        ('accepted', 'Accepted for Publication'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn by Author'),
    ]

    ARTICLE_TYPES = [
        ('research_article', 'Original Research Article'),
        ('review_article', 'Review Article'),
        ('short_communication', 'Short Communication'),
        ('scientific_note', 'Scientific Note / First Report'),
    ]

    SUBJECT_AREAS = [
        ('entomology', 'Agricultural Entomology'),
        ('pathology', 'Plant Pathology & Mycology'),
        ('nematology', 'Nematology'),
        ('weed_science', 'Weed Science & Management'),
        ('biosecurity', 'Plant Biosecurity & Quarantine'),
        ('pesticide_chemistry', 'Pesticide Chemistry, Formulations & Residues'),
        ('biocontrol', 'Biological Control & IPM'),
        ('other', 'Other Allied Plant Protection Sciences'),
    ]

    tracking_id = models.CharField(max_length=32, unique=True, editable=False, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manuscripts')
    co_authors = models.TextField(blank=True, help_text="List co-authors (Name, Email, Affiliation) separated by lines or commas")

    title = models.CharField(max_length=500)
    abstract = models.TextField()
    keywords = models.CharField(max_length=300, help_text="5 to 8 comma-separated keywords")
    article_type = models.CharField(max_length=40, choices=ARTICLE_TYPES, default='research_article')
    subject_area = models.CharField(max_length=40, choices=SUBJECT_AREAS, default='entomology')

    # Primary manuscript files
    manuscript_file = models.FileField(upload_to=manuscript_upload_path, help_text="Full manuscript file (DOC, DOCX, or PDF)")
    supplementary_file = models.FileField(upload_to=manuscript_upload_path, blank=True, null=True, help_text="Optional figures, tables, or raw datasets")
    cover_letter = models.TextField(blank=True, help_text="Cover letter to the Editor-in-Chief")
    conflict_of_interest = models.BooleanField(default=False, help_text="Authors declare no conflict of interest")

    # Payment Verification
    payment_transaction_id = models.CharField(max_length=100, blank=True, null=True, help_text="Payment / UPI / Bank Transaction ID")
    payment_screenshot = models.FileField(upload_to='submissions/payments/%Y/%m/', blank=True, null=True, help_text="Screenshot proof of payment")

    # Workflow & Editorial management
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='submitted', db_index=True)
    assigned_editor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_editor_manuscripts')

    editor_decision = models.CharField(
        max_length=25,
        choices=[
            ('pending', 'Pending Decision'),
            ('accept', 'Accept Manuscript'),
            ('minor_revision', 'Request Minor Revisions'),
            ('major_revision', 'Request Major Revisions'),
            ('reject', 'Reject Manuscript'),
        ],
        default='pending'
    )
    editor_comments_to_author = models.TextField(blank=True, help_text="Decision remarks and feedback returned to the author")
    editor_internal_notes = models.TextField(blank=True, help_text="Confidential notes for editorial board only")
    decision_date = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Manuscript"
        verbose_name_plural = "Manuscripts"

    def __str__(self):
        return f"[{self.tracking_id}] {self.title[:60]}"

    def save(self, *args, **kwargs):
        if not self.tracking_id:
            # Generate collision-safe PPAI-YYYY-XXXX tracking ID
            year = timezone.now().year
            count = Manuscript.objects.filter(created_at__year=year).count() + 1
            candidate_id = f"PPAI-{year}-{count:04d}"
            while Manuscript.objects.filter(tracking_id=candidate_id).exists():
                count += 1
                candidate_id = f"PPAI-{year}-{count:04d}"
            self.tracking_id = candidate_id
        super().save(*args, **kwargs)


class ReviewAssignment(models.Model):
    RECOMMENDATION_CHOICES = [
        ('accept', 'Accept Without Revision'),
        ('minor_revision', 'Minor Revision Required'),
        ('major_revision', 'Major Revision Required'),
        ('reject', 'Reject Manuscript'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Invitation Pending'),
        ('accepted', 'Review Accepted / In Progress'),
        ('declined', 'Review Invitation Declined'),
        ('expired', 'Invitation Expired'),
        ('completed', 'Review Completed & Submitted'),
    ]

    manuscript = models.ForeignKey(Manuscript, on_delete=models.CASCADE, related_name='review_assignments')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_reviews')
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='delegated_reviews')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    due_date = models.DateField(null=True, blank=True)
    reminder_sent = models.BooleanField(default=False)
    reminder_date = models.DateTimeField(null=True, blank=True)

    # Review Rubric Scores (1=Poor to 5=Excellent)
    originality_score = models.PositiveSmallIntegerField(default=3, help_text="1 (Poor) to 5 (Outstanding)")
    technical_quality_score = models.PositiveSmallIntegerField(default=3, help_text="1 (Poor) to 5 (Outstanding)")
    clarity_score = models.PositiveSmallIntegerField(default=3, help_text="1 (Poor) to 5 (Outstanding)")
    significance_score = models.PositiveSmallIntegerField(default=3, help_text="1 (Poor) to 5 (Outstanding)")

    recommendation = models.CharField(max_length=25, choices=RECOMMENDATION_CHOICES, blank=True)
    comments_for_author = models.TextField(blank=True, help_text="Detailed constructive feedback shared with the author (blinded)")
    confidential_comments_to_editor = models.TextField(blank=True, help_text="Confidential remarks seen only by the editor")
    annotated_file = models.FileField(upload_to=reviewer_annotated_path, blank=True, null=True, help_text="Optional manuscript copy with reviewer comments/track changes")

    is_approved_by_editor = models.BooleanField(default=False, help_text="Editor approves releasing comments to author")
    invitation_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('manuscript', 'reviewer')
        ordering = ['-invitation_date']

    def __str__(self):
        return f"Review of {self.manuscript.tracking_id} by {self.reviewer.get_full_name() or self.reviewer.username}"


class ManuscriptRevision(models.Model):
    manuscript = models.ForeignKey(Manuscript, on_delete=models.CASCADE, related_name='revisions')
    revision_number = models.PositiveIntegerField(default=1)
    revised_file = models.FileField(upload_to=revision_upload_path, help_text="Clean or tracked revised manuscript file")
    response_to_reviewers = models.TextField(help_text="Point-by-point response to reviewer and editor comments")
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['revision_number']

    def __str__(self):
        return f"{self.manuscript.tracking_id} - Revision {self.revision_number}"


class SubmissionActivityLog(models.Model):
    manuscript = models.ForeignKey(Manuscript, on_delete=models.CASCADE, related_name='activity_logs')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"[{self.manuscript.tracking_id}] {self.action} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
