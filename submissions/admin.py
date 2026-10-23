from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Manuscript, ReviewAssignment, ManuscriptRevision, SubmissionActivityLog


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Editorial & Journal Roles'
    fk_name = 'user'
    fields = ('role', 'affiliation', 'designation', 'specialization', 'phone', 'orcid_id', 'is_approved_reviewer', 'is_approved_editor')
    extra = 0


# Re-register UserAdmin with UserProfile inline so editors/reviewers can be configured directly
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff')

    def get_role(self, obj):
        try:
            return obj.journal_profile.get_role_display()
        except Exception:
            return "Author"
    get_role.short_description = "Journal Role"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'affiliation', 'specialization', 'is_approved_reviewer', 'is_approved_editor', 'created_at')
    list_filter = ('role', 'is_approved_reviewer', 'is_approved_editor')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email', 'affiliation', 'specialization')
    fields = ('user', 'role', 'affiliation', 'designation', 'specialization', 'phone', 'orcid_id', 'bio', 'is_approved_reviewer', 'is_approved_editor')

    def get_urls(self):
        from django.urls import path
        from . import views as sub_views
        urls = super().get_urls()
        custom_urls = [
            path('add-editorial-user/', self.admin_site.admin_view(sub_views.editor_add_user), name='admin_add_editorial_user'),
        ]
        return custom_urls + urls


class ReviewAssignmentInline(admin.TabularInline):
    model = ReviewAssignment
    extra = 0
    fields = ('reviewer', 'status', 'recommendation', 'due_date', 'completed_date')
    readonly_fields = ('completed_date',)


class ManuscriptRevisionInline(admin.TabularInline):
    model = ManuscriptRevision
    extra = 0
    readonly_fields = ('submitted_at',)


class SubmissionActivityLogInline(admin.TabularInline):
    model = SubmissionActivityLog
    extra = 0
    readonly_fields = ('user', 'action', 'details', 'timestamp')
    can_delete = False


@admin.register(Manuscript)
class ManuscriptAdmin(admin.ModelAdmin):
    list_display = ('tracking_id', 'title_short', 'author', 'article_type', 'subject_area', 'status', 'created_at')
    list_filter = ('status', 'article_type', 'subject_area', 'created_at')
    search_fields = ('tracking_id', 'title', 'author__username', 'author__email', 'keywords')
    readonly_fields = ('tracking_id', 'created_at', 'updated_at')
    inlines = [ReviewAssignmentInline, ManuscriptRevisionInline, SubmissionActivityLogInline]

    def title_short(self, obj):
        return obj.title[:50] + "..." if len(obj.title) > 50 else obj.title
    title_short.short_description = "Title"


@admin.register(ReviewAssignment)
class ReviewAssignmentAdmin(admin.ModelAdmin):
    list_display = ('manuscript', 'reviewer', 'status', 'recommendation', 'due_date', 'completed_date')
    list_filter = ('status', 'recommendation')
    search_fields = ('manuscript__tracking_id', 'reviewer__username', 'reviewer__email')


@admin.register(ManuscriptRevision)
class ManuscriptRevisionAdmin(admin.ModelAdmin):
    list_display = ('manuscript', 'revision_number', 'submitted_at')
    search_fields = ('manuscript__tracking_id',)


@admin.register(SubmissionActivityLog)
class SubmissionActivityLogAdmin(admin.ModelAdmin):
    list_display = ('manuscript', 'user', 'action', 'timestamp')
    search_fields = ('manuscript__tracking_id', 'action', 'details')
    readonly_fields = ('manuscript', 'user', 'action', 'details', 'timestamp')
