from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('executive-council/', views.executive_council, name='executive_council'),
    path('legends/', views.legends, name='legends'),
    path('journal/current/', views.journal_current, name='journal_current'),
    path('journal/archives/', views.journal_archives, name='journal_archives'),
    path('journal/editorial-board/', views.editorial_board, name='editorial_board'),
    path('journal/guidelines/', views.author_guidelines, name='author_guidelines'),
    path('journal/books/', views.books, name='books'),
    path('membership/info/', views.membership_info, name='membership_info'),
    path('membership/directory/', views.membership_directory, name='membership_directory'),
    path('awards/', views.awards, name='awards'),
    path('awards/nomination/', views.awards_nomination, name='awards_nomination'),
    path('conferences/', views.conferences, name='conferences'),
    path('events/election/', views.election, name='election'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('search/', views.search_view, name='search'),
    path('contact/', views.contact, name='contact'),
    path('subscribe-newsletter/', views.subscribe_newsletter, name='subscribe_newsletter'),
]


