from django.urls import path
from . import views

urlpatterns = [
    # Authentication & Role Entry
    path('portal/', views.portal_login, name='portal_home'),
    path('portal/login/', views.portal_login, name='portal_login'),
    path('portal/register/', views.portal_register, name='portal_register'),
    path('portal/logout/', views.portal_logout, name='portal_logout'),

    # Author Workflow
    path('portal/author/', views.author_dashboard, name='author_dashboard'),
    path('portal/author/submit/', views.submit_manuscript, name='submit_manuscript'),
    path('portal/author/manuscript/<str:tracking_id>/', views.author_manuscript_detail, name='author_manuscript_detail'),
    path('portal/author/manuscript/<str:tracking_id>/revision/', views.author_submit_revision, name='author_submit_revision'),

    # Editor Workflow
    path('portal/editor/', views.editor_dashboard, name='editor_dashboard'),
    path('portal/editor/manuscript/<str:tracking_id>/', views.editor_manuscript_review, name='editor_manuscript_review'),

    # Reviewer Workflow
    path('portal/reviewer/', views.reviewer_dashboard, name='reviewer_dashboard'),
    path('portal/reviewer/invitation/<int:assignment_id>/<str:response_action>/', views.reviewer_respond_invitation, name='reviewer_respond_invitation'),
    path('portal/reviewer/evaluate/<int:assignment_id>/', views.reviewer_evaluate_manuscript, name='reviewer_evaluate_manuscript'),
]
