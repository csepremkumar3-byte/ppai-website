from django.contrib import admin
import csv
import io
from django.http import HttpResponse
from django.urls import path

from .models import (
    SiteSetting, CarouselSlide, ExecutiveMember, PastBearer,
    EditorialBoardMember, PublicationBook, ConferenceEvent,
    SocietyAward, JournalVolume, JournalArticle, NewsletterSubscriber, ElectionRegistration
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
    list_display = ('name', 'role', 'gender', 'institution', 'order')
    list_editable = ('order',)
    list_filter = ('role', 'gender')
    search_fields = ('name', 'institution')

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


def generate_election_registrations_excel(queryset):
    """
    Helper to generate an Excel (.xlsx or Excel CSV) response for election registrations.
    Uses openpyxl when installed, otherwise falls back gracefully to Excel-compatible CSV.
    """
    headers = [
        'ID', 'Member Category', 'Registration Type', 'Name', 
        'Phone Number', 'Email ID', 'Designation', 
        'Organization with Full Address', 'Residence with Full Address', 'Registration Date'
    ]

    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        from openpyxl.utils import get_column_letter

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Election 2026 Registrations"

        ws.append(headers)

        header_fill = PatternFill(start_color="00875A", end_color="00875A", fill_type="solid")
        header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        thin_border = Border(
            left=Side(style='thin', color='D0D7D3'),
            right=Side(style='thin', color='D0D7D3'),
            top=Side(style='thin', color='D0D7D3'),
            bottom=Side(style='thin', color='D0D7D3')
        )

        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

        ws.row_dimensions[1].height = 28

        for reg in queryset:
            ws.append([
                reg.id,
                reg.get_member_category_display(),
                reg.get_registration_type_display(),
                reg.name,
                reg.phone,
                reg.email,
                reg.designation,
                reg.organization_address,
                reg.residence_address,
                reg.created_at.strftime('%Y-%m-%d %H:%M:%S') if reg.created_at else '',
            ])

        for row in ws.iter_rows(min_row=2, max_col=10):
            for cell in row:
                cell.border = thin_border
                cell.alignment = Alignment(vertical="center", wrap_text=True)

        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val = str(cell.value or '')
                if '\n' in val:
                    val = max(val.split('\n'), key=len)
                max_len = max(max_len, len(val))
            ws.column_dimensions[col_letter].width = min(max(max_len + 3, 14), 45)

        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="PPAI_Election_2026_Registrations.xlsx"'
        return response

    except ImportError:
        # Fallback to UTF-8 BOM Excel CSV so Microsoft Excel opens cleanly without any installation
        response = HttpResponse(content_type='application/vnd.ms-excel; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="PPAI_Election_2026_Registrations.csv"'
        response.write('\ufeff')
        writer = csv.writer(response)
        writer.writerow(headers)
        for reg in queryset:
            writer.writerow([
                reg.id,
                reg.get_member_category_display(),
                reg.get_registration_type_display(),
                reg.name,
                reg.phone,
                reg.email,
                reg.designation,
                reg.organization_address,
                reg.residence_address,
                reg.created_at.strftime('%Y-%m-%d %H:%M:%S') if reg.created_at else '',
            ])
        return response


@admin.action(description="Download selected registrations in Excel (.xlsx)")
def export_election_registrations_excel(modeladmin, request, queryset):
    return generate_election_registrations_excel(queryset)


@admin.action(description="Download ALL registrations in Excel (.xlsx)")
def export_all_election_registrations_excel(modeladmin, request, queryset):
    all_qs = ElectionRegistration.objects.all().order_by('-created_at')
    return generate_election_registrations_excel(all_qs)


@admin.action(description="Export selected election registrations as CSV")
def export_election_registrations_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ppai_election_2026_registrations.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Member Category', 'Registration Type', 'Name', 
        'Phone Number', 'Email ID', 'Designation', 
        'Organization Address', 'Residence Address', 'Registered At'
    ])
    for reg in queryset:
        writer.writerow([
            reg.id,
            reg.get_member_category_display(),
            reg.get_registration_type_display(),
            reg.name,
            reg.phone,
            reg.email,
            reg.designation,
            reg.organization_address,
            reg.residence_address,
            reg.created_at.strftime('%Y-%m-%d %H:%M:%S') if reg.created_at else '',
        ])
    return response


@admin.register(ElectionRegistration)
class ElectionRegistrationAdmin(admin.ModelAdmin):
    change_list_template = "admin/pages/electionregistration/change_list.html"
    list_display = ('name', 'member_category', 'registration_type', 'designation', 'phone', 'email', 'created_at')
    list_filter = ('member_category', 'registration_type', 'created_at')
    search_fields = ('name', 'email', 'phone', 'designation', 'organization_address')
    actions = [export_election_registrations_excel, export_all_election_registrations_excel, export_election_registrations_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export-excel/', self.admin_site.admin_view(self.export_all_excel_view), name='election_registration_export_excel'),
        ]
        return custom_urls + urls

    def export_all_excel_view(self, request):
        qs = ElectionRegistration.objects.all().order_by('-created_at')
        return generate_election_registrations_excel(qs)
