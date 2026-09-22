from django.contrib import admin
import csv
from django.http import HttpResponse
from .models import (
    SiteSetting, CarouselSlide, ExecutiveMember, PastBearer,
    EditorialBoardMember, PublicationBook, ConferenceEvent,
    SocietyAward, JournalVolume, JournalArticle, NewsletterSubscriber
)

@admin.action(description="Export selected subscribers as CSV (for Zoho Campaigns / Email Broadcasts)")
def export_subscribers_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ppai_newsletter_subscribers.csv"'
    writer = csv.writer(response)
    writer.writerow(['Email', 'Subscribed Date', 'Status'])
    for sub in queryset:
        writer.writerow([sub.email, sub.subscribed_at.strftime('%Y-%m-%d %H:%M:%S'), 'Active' if sub.is_active else 'Inactive'])
    return response

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    actions = [export_subscribers_csv]

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_title', 'hero_title', 'members_count')

@admin.register(CarouselSlide)
class CarouselSlideAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'order', 'is_active', 'image')
    list_editable = ('order', 'is_active')

@admin.register(ExecutiveMember)
class ExecutiveMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'gender', 'affiliation', 'order')
    list_editable = ('order',)
    list_filter = ('gender', 'designation')
    search_fields = ('name', 'designation', 'affiliation')

@admin.register(PastBearer)
class PastBearerAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'gender', 'tenure', 'order')
    list_filter = ('role', 'gender')
    search_fields = ('name', 'tenure')


@admin.register(EditorialBoardMember)
class EditorialBoardMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'institution', 'order')
    list_filter = ('role',)

@admin.register(PublicationBook)
class PublicationBookAdmin(admin.ModelAdmin):
    list_display = ('year', 'title')

@admin.register(ConferenceEvent)
class ConferenceEventAdmin(admin.ModelAdmin):
    list_display = ('year', 'event_title')

@admin.register(SocietyAward)
class SocietyAwardAdmin(admin.ModelAdmin):
    list_display = ('name', 'conferred_for')

@admin.register(JournalVolume)
class JournalVolumeAdmin(admin.ModelAdmin):
    list_display = ('volume_number', 'year', 'issues_available')

@admin.register(JournalArticle)
class JournalArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'volume', 'issue', 'year', 'authors')
    list_filter = ('volume', 'issue', 'year')
    search_fields = ('title', 'authors')

