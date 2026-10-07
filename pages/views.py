import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from .models import (
    SiteSetting, CarouselSlide, ExecutiveMember, PastBearer,
    EditorialBoardMember, PublicationBook, ConferenceEvent,
    SocietyAward, JournalVolume, JournalArticle
)

RECENT_EVENTS = [
    {
        'day': '16',
        'month': 'OCT',
        'year': '2026',
        'category': 'PPAI Guest Lecture',
        'title': 'From a Remote Village to Global Science: Plant Virus Discovery and Innovation',
        'doc_file': 'documents/events/guest_lecture_poster.jpg',
        'doc_name': 'PPAI Guest Lecture - Dr. Satyanarayana Tatineni.jpg',
    },
    {
        'day': '19',
        'month': 'SEP',
        'year': '2026',
        'category': 'PPAI Collaborations',
        'title': 'Joint Representation by leading plant protection Societies of India',
        'doc_file': 'documents/events/joint_representation.pdf',
        'doc_name': 'JOINT REPRESENTATION BY LEADING PLANT PROTECTION SOCIETIES OF INDIA.pdf',
    },
    {
        'day': '04',
        'month': 'AUG',
        'year': '2026',
        'category': 'PPAI Proposal',
        'title': 'Prohibition of Paraquat Dichloride',
        'doc_file': 'documents/events/paraquat_dichloride_submission.pdf',
        'doc_name': 'Comprehensive Submission on the Proposed Prohibition of Paraquat Dichloride 24_ SL.pdf',
    },
    {
        'day': '06',
        'month': 'JUN',
        'year': '2026',
        'category': 'PPAI Proceedings',
        'title': 'Enhancing Agricultural Contribution And GDP Growth',
        'doc_file': 'documents/events/agricultural_contribution_gdp_growth.pdf',
        'doc_name': 'Enhancing Agricultural Contribution and GDP Growth.pdf',
    },
    {
        'day': '03',
        'month': 'FEB',
        'year': '2026',
        'category': 'PPAI Comments',
        'title': 'Pesticide Management Bill',
        'doc_file': 'documents/events/pesticide_management_bill_comments.pdf',
        'doc_name': 'Comments on the pesticide management bill.pdf',
    },
    {
        'day': '23',
        'month': 'DEC',
        'year': '2025',
        'category': 'PPAI Farmer Training',
        'title': 'Problems and solutions on Mango farming',
        'doc_file': 'documents/events/mango_training_programme.pdf',
        'doc_name': 'Mango training programme PDF.pdf',
    },
    {
        'day': '10',
        'month': 'DEC',
        'year': '2025',
        'category': 'PPAI Comments',
        'title': 'SGD Suggestions on the Seed Bill',
        'doc_file': 'documents/events/sgd_suggestions_seed_bill.pdf',
        'doc_name': 'SGD Suggestions on the Seed Bill.pdf',
    },
    {
        'day': '25',
        'month': 'JUL',
        'year': '2025',
        'category': 'PPAI Petition',
        'title': 'Curbing the usage of counterfeit pesticides',
        'doc_file': 'documents/events/spurious_pesticides_petition.pdf',
        'doc_name': 'Petition to the Director of Agriculture Telangana on Spurious Pesticides.pdf',
    },
    {
        'day': '17',
        'month': 'APR',
        'year': '2025',
        'category': 'PPAI Seminars',
        'title': 'A one-day seminar with Stakeholders on Seed Sovereignty',
        'doc_file': 'documents/events/seminar_seed_sovereignty.pdf',
        'doc_name': 'Proceedings and Recommendations of one day seminar on seed sovereignty.pdf',
    },
    {
        'day': '23',
        'month': 'MAY',
        'year': '2023',
        'category': 'PPAI Meeting',
        'title': 'Seed Research Companies attended ICPHM',
        'doc_file': 'documents/events/seed_industry_icphm_meeting.pdf',
        'doc_name': 'Seed Industry participants on 23rd May Interactive session.pdf',
    },
]

def get_common_context():
    return {
        'site_settings': SiteSetting.objects.first(),
    }

def home(request):
    context = get_common_context()
    context['slides'] = CarouselSlide.objects.filter(is_active=True)
    context['events'] = RECENT_EVENTS
    return render(request, 'pages/home.html', context)

def about(request):
    context = get_common_context()
    return render(request, 'pages/about.html', context)

def agbm(request):
    return redirect('/about/#annual-general-body-meeting')

def executive_council(request):
    context = get_common_context()
    all_members = ExecutiveMember.objects.all().order_by('order', 'id')
    context['presidents_group'] = all_members.filter(order__in=[1, 2, 3, 4])
    context['secretaries_group'] = all_members.filter(order__in=[5, 6, 7])
    context['editors_group'] = all_members.filter(order__in=[8, 9, 10])
    context['councillors_group'] = all_members.filter(order__in=[11, 12, 13, 14, 15])
    
    members_data = {}
    for m in all_members:
        members_data[str(m.id)] = {
            'id': m.id,
            'name': m.name,
            'designation': m.designation,
            'affiliation': m.affiliation,
            'image': m.image.url if m.image else '',
            'gender': m.gender,
            'email': m.email or '',
            'phone': m.phone or '',
            'qualification': m.qualification or '',
            'date_of_birth': m.date_of_birth or '',
            'official_address': m.official_address or '',
            'bio': m.bio or '',
            'achievements': m.achievements or '',
            'projects': m.projects or '',
            'publications': m.publications or '',
        }
    context['members_json'] = json.dumps(members_data)
    return render(request, 'pages/executive_council.html', context)

def legends(request):
    return redirect('/executive-council/#past-executive-council')

def journal_about(request):
    context = get_common_context()
    return render(request, 'pages/journal_about.html', context)

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
    context['chief_editors'] = EditorialBoardMember.objects.filter(role__in=['chief_editor', 'assoc_editor']).order_by('order', 'id')
    context['board_members'] = EditorialBoardMember.objects.filter(role__in=['member', 'intl_member']).order_by('order', 'id')
    context['patrons'] = EditorialBoardMember.objects.filter(role='patron').order_by('order', 'id')
    return render(request, 'pages/editorial_board.html', context)

def author_guidelines(request):
    context = get_common_context()
    return render(request, 'pages/author_guidelines.html', context)

def books(request):
    return redirect('other_publications')

def other_publications(request):
    context = get_common_context()
    return render(request, 'pages/other_publications.html', context)

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
        return JsonResponse({'status': 'error', 'message': 'Email is required.'}, status=400)

    if len(email) > 100:
        return JsonResponse({'status': 'error', 'message': 'Email is too long.'}, status=400)

    # Strict regex check
    if not EMAIL_REGEX.match(email):
        return JsonResponse({'status': 'error', 'message': 'Enter a valid email address.'}, status=400)

    # Standard Django email validator check
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'status': 'error', 'message': 'Enter a valid email address.'}, status=400)

    # Check if already subscribed (do not allow duplicate registration)
    if NewsletterSubscriber.objects.filter(email=email).exists():
        return JsonResponse({'status': 'exists', 'message': 'Email is already subscribed.'})

    # Register new subscriber
    NewsletterSubscriber.objects.create(email=email)
    return JsonResponse({'status': 'success', 'message': 'Subscribed successfully!'})



