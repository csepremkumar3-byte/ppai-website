from django.db import models
from django.core.validators import FileExtensionValidator

class SiteSetting(models.Model):
    site_title = models.CharField(max_length=255, default='Plant Protection Association of India')
    registration_info = models.CharField(
        max_length=255, 
        default='(Regn. No. S399 of 1949-50 under the Societies Registration Act XXI of 1860)'
    )
    logo = models.ImageField(upload_to='logo/', blank=True, null=True)
    hero_badge = models.CharField(max_length=50, default='Since 1972')
    hero_title = models.CharField(max_length=255, default='Indian Journal of Plant Protection')
    hero_description = models.TextField(
        default='The Indian Journal of Plant Protection (IJPP) is a peer-reviewed quarterly journal published by the Plant Protection Association of India (PPAI), Hyderabad. It publishes original research, reviews, and short communications in agricultural entomology, plant pathology, nematology, weed science, and integrated pest management (IPM).'
    )
    members_count = models.CharField(max_length=50, default='1,900+')
    society_years = models.CharField(max_length=50, default='54')
    published_volumes = models.CharField(max_length=50, default='54')

    class Meta:
        verbose_name = 'Site Setting'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_title


class CarouselSlide(models.Model):
    title = models.CharField(max_length=200, blank=True, help_text="Title or alt text")
    image = models.ImageField(upload_to='carousel/')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title or f"Slide {self.id}"


class ExecutiveMember(models.Model):
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=150)
    affiliation = models.CharField(max_length=255)
    image = models.ImageField(upload_to='council/', blank=True, null=True, help_text="Upload member photo. Defaults to gender avatar if blank.")
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], default='male')
    bio = models.TextField(blank=True, help_text="Short bio / description")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Executive Council Member'

    def __str__(self):
        return f"{self.name} - {self.designation}"


class PastBearer(models.Model):
    ROLE_CHOICES = [
        ('president', 'Past President'),
        ('secretary', 'Past General Secretary'),
        ('treasurer', 'Past Treasurer'),
        ('editor', 'Past Chief Editor'),
    ]
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    tenure = models.CharField(max_length=100)
    affiliation = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='legends/', blank=True, null=True, help_text="Upload past bearer photo. Defaults to gender avatar if blank.")
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], default='male')
    bio = models.TextField(blank=True, help_text="Short bio / contribution details")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['role', 'order', 'id']

    def __str__(self):
        return f"{self.get_role_display()}: {self.name} ({self.tenure})"



class EditorialBoardMember(models.Model):
    ROLE_CHOICES = [
        ('chief_editor', 'Editor-in-Chief'),
        ('assoc_editor', 'Associate Editor'),
        ('member', 'Editorial Member'),
        ('intl_member', 'Editorial Member (International)'),
        ('patron', 'Honorary Patron'),
    ]
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    institution = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.get_role_display()}: {self.name}"


class PublicationBook(models.Model):
    year = models.IntegerField()
    title = models.CharField(max_length=255)

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f"{self.year} - {self.title}"


class ConferenceEvent(models.Model):
    year = models.IntegerField()
    event_title = models.TextField()

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f"{self.year}: {self.event_title[:50]}"


class SocietyAward(models.Model):
    name = models.CharField(max_length=255)
    conferred_for = models.TextField()

    def __str__(self):
        return self.name


class JournalVolume(models.Model):
    volume_number = models.IntegerField()
    year = models.IntegerField()
    issues_available = models.CharField(max_length=255, default='No. 1, No. 2')
    epubs_url = models.URLField(default='https://epubs.icar.org.in/index.php/IJPP')

    class Meta:
        ordering = ['-volume_number']

    def __str__(self):
        return f"Vol. {self.volume_number} ({self.year})"


class JournalArticle(models.Model):
    volume = models.IntegerField(default=54)
    issue = models.IntegerField(default=1)
    year = models.IntegerField(default=2026)
    title = models.CharField(max_length=300)
    authors = models.CharField(max_length=300)
    abstract = models.TextField(blank=True)
    pdf_file = models.FileField(
        upload_to='journals/pdf/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-volume', '-issue', 'id']

    def __str__(self):
        return f"Vol {self.volume} No {self.issue}: {self.title[:50]}"
