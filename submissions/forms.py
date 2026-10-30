import os
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Manuscript, ReviewAssignment, ManuscriptRevision


ALLOWED_MANUSCRIPT_EXTENSIONS = ['.pdf', '.doc', '.docx']


def validate_file_extension(file_obj, max_mb=5):
    if file_obj:
        ext = os.path.splitext(file_obj.name)[1].lower()
        if ext not in ALLOWED_MANUSCRIPT_EXTENSIONS:
            raise forms.ValidationError(f"Unsupported file format ({ext}). Please upload a Microsoft Word (.doc, .docx) or PDF (.pdf) file.")
        # 5 MB limit
        if file_obj.size > max_mb * 1024 * 1024:
            raise forms.ValidationError(f"File size exceeds {max_mb}MB limit. Please upload a compressed document up to {max_mb}MB.")


class RoleRegistrationForm(forms.Form):
    ROLE_CHOICES = [
        ('author', 'Author (Submit manuscripts and track reviews)'),
        ('reviewer', 'Reviewer (Join review panel for peer review)'),
        ('editor', 'Editor (Editorial Board Member)'),
    ]

    full_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'portal-input', 'placeholder': 'e.g. Dr. Rajesh Kumar Sharma'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'portal-input', 'placeholder': 'official.email@institution.edu.in'
    }))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={
        'class': 'portal-input', 'placeholder': '+91 98765 43210'
    }))
    role = forms.ChoiceField(choices=ROLE_CHOICES, initial='author', widget=forms.Select(attrs={
        'class': 'portal-select'
    }))
    affiliation = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class': 'portal-input', 'placeholder': 'e.g. ICAR-IARI, Division of Entomology, New Delhi'
    }))
    designation = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={
        'class': 'portal-input', 'placeholder': 'e.g. Principal Scientist / Associate Professor'
    }))
    specialization = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={
        'class': 'portal-input', 'placeholder': 'e.g. Insect Toxicology, Plant Virology, Biocontrol'
    }))
    orcid_id = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={
        'class': 'portal-input', 'placeholder': '0000-0002-1825-0097'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'portal-input', 'placeholder': 'Create secure password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'portal-input', 'placeholder': 'Confirm password'
    }))

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        import re
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise forms.ValidationError("Please enter a valid email address (e.g. user@institution.edu.in).")
        if User.objects.filter(email__iexact=email).exists() or User.objects.filter(username__iexact=email).exists():
            raise forms.ValidationError("An account with this email address already exists. Please log in.")
        return email

    def clean_password(self):
        p1 = self.cleaned_data.get('password')
        if p1:
            if len(p1) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long.")
            if not any(c.isupper() for c in p1):
                raise forms.ValidationError("Password must contain at least one uppercase letter.")
            if not (any(c.isalpha() for c in p1) and any(c.isdigit() for c in p1)):
                raise forms.ValidationError("Password must contain both letters and numbers for security.")
        return p1

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned_data


class ManuscriptSubmissionForm(forms.ModelForm):
    class Meta:
        model = Manuscript
        fields = [
            'article_type', 'subject_area', 'title', 'abstract',
            'keywords', 'co_authors', 'manuscript_file', 'supplementary_file',
            'payment_transaction_id', 'payment_screenshot',
            'cover_letter', 'conflict_of_interest'
        ]
        widgets = {
            'article_type': forms.Select(attrs={'class': 'portal-select'}),
            'subject_area': forms.Select(attrs={'class': 'portal-select'}),
            'title': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'Enter full title of the manuscript'}),
            'abstract': forms.Textarea(attrs={'class': 'portal-textarea', 'rows': 6, 'placeholder': 'Paste structured or unstructured abstract (up to 350 words)...'}),
            'keywords': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'e.g. Spodoptera frugiperda, biopesticides, neem oil, toxicity'}),
            'co_authors': forms.Textarea(attrs={'class': 'portal-textarea', 'rows': 3, 'placeholder': 'Co-authors with email & institution (e.g. Dr. A. Rao, University; Dr. P. Singh, College)'}),
            'payment_transaction_id': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'e.g. UPI/123456789012 or IMPS Reference No.'}),
            'cover_letter': forms.Textarea(attrs={'class': 'portal-textarea', 'rows': 4, 'placeholder': 'Brief statement explaining the novel scientific findings and why it fits PPAI scope...'}),
            'conflict_of_interest': forms.CheckboxInput(attrs={'class': 'portal-checkbox'}),
        }

    def clean_manuscript_file(self):
        f = self.cleaned_data.get('manuscript_file')
        validate_file_extension(f)
        if f and f.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Manuscript file size must not exceed 5MB. Please compress your document.")
        return f

    def clean_payment_screenshot(self):
        f = self.cleaned_data.get('payment_screenshot')
        if f:
            ext = os.path.splitext(f.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.webp', '.pdf']:
                raise forms.ValidationError("Payment screenshot must be an image (.jpg, .jpeg, .png, .webp) or PDF (.pdf).")
            if f.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Payment screenshot file size must not exceed 5MB.")
        return f

    def clean_supplementary_file(self):
        f = self.cleaned_data.get('supplementary_file')
        if f:
            validate_file_extension(f)
        return f


class ReviewEvaluationForm(forms.ModelForm):
    class Meta:
        model = ReviewAssignment
        fields = [
            'originality_score', 'technical_quality_score', 'clarity_score', 'significance_score',
            'recommendation', 'comments_for_author', 'confidential_comments_to_editor', 'annotated_file'
        ]
        widgets = {
            'originality_score': forms.Select(choices=[(i, f"{i} - " + ["Poor", "Fair", "Good", "Very Good", "Outstanding"][i-1]) for i in range(1, 6)], attrs={'class': 'portal-select'}),
            'technical_quality_score': forms.Select(choices=[(i, f"{i} - " + ["Poor", "Fair", "Good", "Very Good", "Outstanding"][i-1]) for i in range(1, 6)], attrs={'class': 'portal-select'}),
            'clarity_score': forms.Select(choices=[(i, f"{i} - " + ["Poor", "Fair", "Good", "Very Good", "Outstanding"][i-1]) for i in range(1, 6)], attrs={'class': 'portal-select'}),
            'significance_score': forms.Select(choices=[(i, f"{i} - " + ["Poor", "Fair", "Good", "Very Good", "Outstanding"][i-1]) for i in range(1, 6)], attrs={'class': 'portal-select'}),
            'recommendation': forms.Select(attrs={'class': 'portal-select'}),
            'comments_for_author': forms.Textarea(attrs={'class': 'portal-textarea', 'rows': 7, 'placeholder': 'Detailed constructive comments to be shared with authors (strengths, major comments, minor points, recommendations)...'}),
            'confidential_comments_to_editor': forms.Textarea(attrs={'class': 'portal-textarea', 'rows': 4, 'placeholder': 'Confidential remarks for the Editor (ethical concerns, suspected plagiarism, overall assessment)...'}),
        }

    def clean_annotated_file(self):
        f = self.cleaned_data.get('annotated_file')
        if f:
            validate_file_extension(f)
        return f


class ManuscriptRevisionForm(forms.ModelForm):
    class Meta:
        model = ManuscriptRevision
        fields = ['revised_file', 'response_to_reviewers']
        widgets = {
            'response_to_reviewers': forms.Textarea(attrs={
                'class': 'portal-textarea',
                'rows': 8,
                'placeholder': 'Provide a point-by-point response detailing how every reviewer and editor comment was addressed...'
            })
        }

    def clean_revised_file(self):
        f = self.cleaned_data.get('revised_file')
        validate_file_extension(f)
        return f


class EditorDecisionForm(forms.Form):
    DECISION_CHOICES = [
        ('accept', 'Accept for Publication'),
        ('minor_revision', 'Request Minor Revisions'),
        ('major_revision', 'Request Major Revisions'),
        ('reject', 'Reject Manuscript'),
    ]

    decision = forms.ChoiceField(choices=DECISION_CHOICES, widget=forms.Select(attrs={'class': 'portal-select'}))
    comments_to_author = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'portal-textarea',
        'rows': 7,
        'placeholder': 'Editorial decision letter and consolidated comments returned to the author...'
    }))
    internal_notes = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'portal-textarea',
        'rows': 3,
        'placeholder': 'Confidential internal notes for editorial record...'
    }))
