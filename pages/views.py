from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from .models import (
    SiteSetting, CarouselSlide, ExecutiveMember, PastBearer,
    EditorialBoardMember, PublicationBook, ConferenceEvent,
    SocietyAward, JournalVolume, JournalArticle
)

def get_common_context():
    return {
        'site_settings': SiteSetting.objects.first(),
    }

def home(request):
    context = get_common_context()
    context['slides'] = CarouselSlide.objects.filter(is_active=True)
    return render(request, 'pages/home.html', context)

def about(request):
    context = get_common_context()
    return render(request, 'pages/about.html', context)

def executive_council(request):
    context = get_common_context()
    context['council_members'] = ExecutiveMember.objects.all()
    return render(request, 'pages/executive_council.html', context)

def legends(request):
    context = get_common_context()
    context['past_presidents'] = PastBearer.objects.filter(role='president')
    context['past_secretaries'] = PastBearer.objects.filter(role='secretary')
    context['past_treasurers'] = PastBearer.objects.filter(role='treasurer')
    context['past_editors'] = PastBearer.objects.filter(role='editor')
    return render(request, 'pages/legends.html', context)

def journal_current(request):
    context = get_common_context()
    # Vol 54 (2026) Issues 1 & 2
    context['issue_1_articles'] = JournalArticle.objects.filter(volume=54, issue=1)
    context['issue_2_articles'] = JournalArticle.objects.filter(volume=54, issue=2)
    return render(request, 'pages/journal_current.html', context)

def journal_archives(request):
    context = get_common_context()
    # Back archives Vol 42 (2014) to Vol 53 (2025)
    context['back_volumes'] = JournalVolume.objects.filter(volume_number__lt=54)
    return render(request, 'pages/journal_archives.html', context)

def editorial_board(request):
    context = get_common_context()
    context['board_members'] = EditorialBoardMember.objects.all()
    return render(request, 'pages/editorial_board.html', context)

def author_guidelines(request):
    context = get_common_context()
    return render(request, 'pages/author_guidelines.html', context)

def books(request):
    context = get_common_context()
    context['books_list'] = PublicationBook.objects.all()
    return render(request, 'pages/books.html', context)

def membership_info(request):
    context = get_common_context()
    return render(request, 'pages/membership_info.html', context)

def membership_directory(request):
    context = get_common_context()
    return render(request, 'pages/membership_directory.html', context)

def awards(request):
    context = get_common_context()
    context['awards_list'] = SocietyAward.objects.all()
    return render(request, 'pages/awards.html', context)

def awards_nomination(request):
    context = get_common_context()
    return render(request, 'pages/awards_nomination.html', context)

def conferences(request):
    context = get_common_context()
    context['events_list'] = ConferenceEvent.objects.all()
    return render(request, 'pages/conferences.html', context)

def election(request):
    context = get_common_context()
    return render(request, 'pages/election.html', context)

def register(request):
    context = get_common_context()
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        contact_num = request.POST.get('contact', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        member_type = request.POST.get('member_type', 'inland')

        if not email or not password:
            context['error'] = 'Please fill in all required fields.'
            return render(request, 'pages/register.html', context)

        if password != confirm_password:
            context['error'] = 'Passwords do not match.'
            return render(request, 'pages/register.html', context)

        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            context['error'] = 'An account with this email address already exists.'
            return render(request, 'pages/register.html', context)

        # Securely create user with PBKDF2/SHA256 password encryption
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=full_name
        )
        user.save()
        context['success'] = 'Registration successful! You can now log in.'
        return render(request, 'pages/login.html', context)

    return render(request, 'pages/register.html', context)

def login_view(request):
    context = get_common_context()
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            context['error'] = 'Invalid email address or password. Please try again.'
            return render(request, 'pages/login.html', context)
    return render(request, 'pages/login.html', context)

def search_view(request):
    query = request.GET.get('q', '').strip().lower()
    if not query:
        return redirect('home')
    
    if any(w in query for w in ['journal', 'volume', 'issue', 'article', 'paper', 'current', 'ijpp']):
        return redirect('journal_current')
    elif any(w in query for w in ['archive', 'past issue', 'back volume', 'archives', 'past']):
        return redirect('journal_archives')
    elif any(w in query for w in ['editorial', 'board', 'editor', 'reviewer', 'chief editor']):
        return redirect('editorial_board')
    elif any(w in query for w in ['guideline', 'author', 'manuscript', 'submission', 'format']):
        return redirect('author_guidelines')
    elif any(w in query for w in ['book', 'monograph', 'special publication', 'books']):
        return redirect('books')
    elif any(w in query for w in ['fee', 'membership info', 'subscription', 'student fee', 'life member', 'membership', 'member']):
        return redirect('membership_info')
    elif any(w in query for w in ['directory', 'member list', 'fellow list', 'roster']):
        return redirect('membership_directory')
    elif any(w in query for w in ['register', 'registration', 'join', 'signup']):
        return redirect('register')
    elif any(w in query for w in ['login', 'signin', 'portal', 'auth']):
        return redirect('login')
    elif any(w in query for w in ['award', 'honor', 'medal', 'prasada', 'dodla', 'sarada', 'fppai', 'awards']):
        return redirect('awards')
    elif any(w in query for w in ['nomination', 'nominate']):
        return redirect('awards_nomination')
    elif any(w in query for w in ['conference', 'seminar', 'symposi', 'workshop', 'event', 'conferences', 'seminars']):
        return redirect('conferences')
    elif any(w in query for w in ['election', 'council election', 'vote', 'elections']):
        return redirect('election')
    elif any(w in query for w in ['council', 'executive', 'president', 'secretary', 'treasurer']):
        return redirect('executive_council')
    elif any(w in query for w in ['legend', 'past president', 'past secretary', 'founder', 'nirula', 'legends']):
        return redirect('legends')
    elif any(w in query for w in ['about', 'aim', 'objective', 'society', 'history']):
        return redirect('about')
    else:
        return redirect('journal_current')

def contact(request):
    context = get_common_context()
    return render(request, 'pages/contact.html', context)

import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import NewsletterSubscriber

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

@require_POST
def subscribe_newsletter(request):
    email = request.POST.get('email', '').strip().lower()

    if not email:
        return JsonResponse({'status': 'error', 'message': 'Email address is required.'}, status=400)

    if len(email) > 100:
        return JsonResponse({'status': 'error', 'message': 'Email address cannot exceed 100 characters.'}, status=400)

    # Strict regex check (valid user, valid domain, valid TLD of 2+ letters)
    if not EMAIL_REGEX.match(email):
        return JsonResponse({'status': 'error', 'message': 'Please provide a valid email address (e.g. name@institution.org).'}, status=400)

    # Standard Django email validator check
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'status': 'error', 'message': 'The email address entered is not valid.'}, status=400)

    # Check for disposable/malformed domains with no dot
    parts = email.split('@')
    if len(parts) != 2 or '.' not in parts[1] or len(parts[1].split('.')[-1]) < 2:
        return JsonResponse({'status': 'error', 'message': 'Please enter a complete email domain (e.g. .com, .in, .org).'}, status=400)

    subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
    if not created:
        if not subscriber.is_active:
            subscriber.is_active = True
            subscriber.save()
            return JsonResponse({'status': 'success', 'message': 'Welcome back! Your newsletter subscription has been reactivated.'})
        return JsonResponse({'status': 'info', 'message': 'This email address is already subscribed to PPAI updates.'})

    return JsonResponse({'status': 'success', 'message': 'Thank you! You have successfully subscribed to PPAI updates.'})


