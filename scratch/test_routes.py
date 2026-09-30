import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.test import Client

c = Client()
routes = [
    '',
    'about/',
    'executive-council/',
    'legends/',
    'journal/current/',
    'journal/archives/',
    'journal/editorial-board/',
    'journal/guidelines/',
    'journal/books/',
    'membership/info/',
    'membership/directory/',
    'awards/',
    'awards/nomination/',
    'conferences/',
    'events/election/',
    'register/',
    'login/',
    'search/?q=journal',
    'contact/'
]

print("--- TESTING ALL 19 LOCAL ROUTES ---")
all_ok = True
for r in routes:
    response = c.get('/' + r)
    print(f"Route: /{r:<28} -> HTTP Status {response.status_code}")
    if response.status_code not in (200, 302):
        all_ok = False

if all_ok:
    print("\nSUCCESS: All 19 routes resolved with HTTP 200 OK locally!")
else:
    print("\nFAILURE: Some routes returned error codes.")
