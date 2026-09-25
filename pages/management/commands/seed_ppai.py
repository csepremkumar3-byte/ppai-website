import os
from django.core.management.base import BaseCommand
from django.conf import settings
from pages.models import (
    SiteSetting, CarouselSlide, ExecutiveMember, PastBearer,
    EditorialBoardMember, PublicationBook, ConferenceEvent,
    SocietyAward, JournalVolume, JournalArticle
)

class Command(BaseCommand):
    help = 'Seeds all PPAI Society data into the active database'

    def handle(self, *args, **options):
        db_engine = settings.DATABASES['default']['ENGINE'].split('.')[-1]
        db_name = settings.DATABASES['default']['NAME']
        self.stdout.write(f"Connected to Database Engine: [{db_engine}], Database: [{db_name}]")
        self.stdout.write("Seeding full dataset from official document...")

        # 1. SiteSetting
        site, _ = SiteSetting.objects.get_or_create(
            id=1,
            defaults={
                'site_title': 'Plant Protection Association of India',
                'registration_info': '(Regn. No. S399 of 1949-50 under the Societies Registration Act XXI of 1860)',
                'logo': 'logo/ppai_logo.png',
                'hero_badge': 'Since 1972',
                'hero_title': 'Indian Journal of Plant Protection',
                'hero_description': 'The Indian Journal of Plant Protection (IJPP) is a peer-reviewed quarterly journal published by the Plant Protection Association of India (PPAI), Hyderabad. It publishes original research, reviews, and short communications in agricultural entomology, plant pathology, nematology, weed science, and integrated pest management (IPM).',
                'members_count': '1,900+',
                'society_years': '54',
                'published_volumes': '54',
            }
        )
        site.logo = 'logo/ppai_logo.png'
        site.save()

        # 2. Carousel Slides
        CarouselSlide.objects.all().delete()
        slides_data = [
            (0, 'carousel/journal_cover.png', 'Indian Journal of Plant Protection Vol 54 No 1 Cover'),
            (1, 'carousel/golden_jubilee_banner.png', 'PPAI Golden Jubilee (1972–2022) 50 Years Celebration'),
            (2, 'carousel/slide1.jpg', 'Agricultural Research and Entomology'),
            (3, 'carousel/slide2.jpg', 'Biological Pest Control & Ladybird Beetle'),
            (4, 'carousel/slide3.jpg', 'Plant Disease Management and Phytopathology'),
            (5, 'carousel/slide4.jpg', 'Sustainable Agriculture and Plant Health'),
        ]
        for order, img, title in slides_data:
            CarouselSlide.objects.create(order=order, image=img, title=title, is_active=True)

        # 3. Executive Council (Page 2 of document - Dr. B. Sarath Babu is PRESIDENT)
        ExecutiveMember.objects.all().delete()
        executive_members_data = [
            ('Dr. B Sarath Babu', 'President', 'Principal Scientist & Former Head, ICAR-National Bureau of Plant Genetic Resources, Regional Station, Hyderabad', 'male', 'President of PPAI.', 1),
            ('Dr. Jagadeeshwar', 'Vice-President', 'Professor, Jayashankar Telangana State Agricultural University, Hyderabad', 'male', 'Vice-President.', 2),
            ('Dr. Celia Challam', 'Vice-President', 'ICAR-National Bureau of Plant Genetic Resources, Pusa Campus, New Delhi', 'female', 'Vice-President.', 3),
            ('Dr. M Srinivas Prasad', 'Vice-President', 'ICAR-Indian Institute of Rice Research, Hyderabad', 'male', 'Vice-President.', 4),
            ('Dr. B Parameshwari', 'General Secretary', 'ICAR-National Bureau of Plant Genetic Resources, Regional Station, Hyderabad', 'female', 'General Secretary.', 5),
            ('Dr. V Prakasam', 'Assistant Secretary', 'ICAR-Indian Institute of Rice Research, Hyderabad', 'male', 'Assistant Secretary.', 6),
            ('Dr. B Bhaskar', 'Treasurer', 'ICAR-National Bureau of Plant Genetic Resources, Regional Station, Hyderabad', 'male', 'Treasurer.', 7),
            ('Prof. T V K Singh', 'Chief Editor', 'Dean of ANGRAU and PJTSAU Retd. & Ex. ICAR-Emeritus Scientist, Hyderabad.', 'male', 'Chief Editor.', 8),
            ('Dr. Kavita Gupta', 'Associate Editor', 'ICAR-National Bureau of Plant Genetic Resources, New Delhi', 'female', 'Associate Editor.', 9),
            ('Dr. Prasanna Holajjer', 'Associate Editor', 'ICAR-National Bureau of Plant Genetic Resources, Regional Station, Hyderabad', 'male', 'Associate Editor.', 10),
            ('Dr. B S Gotyal', 'Councillor', 'ICAR- National Bureau of Agricultural Insect Resources, Bengaluru', 'male', 'Councillor.', 11),
            ('Dr. Alpesh Kumar Valjibhai Khanpara', 'Councillor', 'Department of Entomology, Junagadh Agricultural University, Junagadh, Gujarat', 'male', 'Councillor.', 12),
            ('Dr. D Sagar', 'Councillor', 'ICAR- National Bureau of Agricultural Insect Resources, Bengaluru', 'male', 'Councillor.', 13),
            ('Dr. K Rameash', 'Councillor', 'ICAR-Central Institute of Cotton Research, Regional Station, Coimbatore', 'male', 'Councillor.', 14),
            ('Dr. J Stanley', 'Councillor', 'ICAR-Indian Institute of Millet Research, Hyderabad, Telangana', 'male', 'Councillor.', 15),
        ]
        for name, desig, aff, gender, bio, order in executive_members_data:
            ExecutiveMember.objects.create(name=name, designation=desig, affiliation=aff, gender=gender, bio=bio, order=order)

        # 4. Past Office Bearers (Pages 3 & 4 of document)
        PastBearer.objects.all().delete()
        presidents = [
            ('Dr. K. K. Nirula', 'Founder President (1972 – 1978)', 'CPPTI, Hyderabad', 'male', 1),
            ('Dr. N. C. Joshi', '1979 – 1980', 'CPPTI, Hyderabad', 'male', 2),
            ('Dr. K. D. Paharia', '1981 – 1984', 'CPPTI, Hyderabad', 'male', 3),
            ('Dr. N. C. Joshi', '1985 – 1986', 'CPPTI, Hyderabad', 'male', 4),
            ('Dr. D. Bap Reddy', '1987 – 1988', 'FAO Representative', 'male', 5),
            ('Dr. S. Jayaraj', '1989 – 1990', 'TNAU, Coimbatore', 'male', 6),
            ('Dr. D. V. R. Reddy', '1991 – 1997', 'ICRISAT, Patancheru', 'male', 7),
            ('Dr. K. Krishnaiah', '1997 – 1999', 'DRR (ICAR-IIRR), Hyderabad', 'male', 8),
            ('Dr. P. S. Chandukar', '2000 – 2002', 'PPA to Govt. of India', 'male', 9),
            ('Dr. Y. L. Nene', '2003 – 2006', 'ICRISAT / Asian Agri-History Foundation', 'male', 10),
            ('Dr. K. S. R. K. Murthy', '2007 – 2009', 'ANGRAU, Hyderabad', 'male', 11),
            ('Dr. K. S. Varaprasad', '2010 – 2012', 'ICAR-NBPGR RS / IIOR', 'male', 12),
            ('Dr. B. Sarath Babu', '2018 – 2022', 'ICAR-NBPGR RS, Hyderabad', 'male', 13),
        ]
        for name, tenure, aff, gender, order in presidents:
            PastBearer.objects.create(role='president', name=name, tenure=tenure, affiliation=aff, gender=gender, order=order)

        secretaries = [
            ('Dr. S. S. Hussaine', '1972 – 1974', 'CPPTI, Hyderabad', 'male', 1),
            ('Dr. V. Lakshminarayana', '1975 – 1976, 1979 – 1980', 'CPPTI, Hyderabad', 'male', 2),
            ('Dr. Basu Chaudhary', '1977 – 1978', 'CPPTI, Hyderabad', 'male', 3),
            ('Dr. V. Raghunathan', '1981 – 1984', 'Central Plant Protection Station', 'male', 4),
            ('Shri B. Govinda Naik', '1985 – 1986', 'CPPTI, Hyderabad', 'male', 5),
            ('Dr. B. J. Divakar', '1987 – 1997', 'Directorate of Plant Protection', 'male', 6),
            ('Dr. Renu Sharma', '1997 – 1999', 'ICAR-NBPGR RS, Hyderabad', 'female', 7),
            ('Dr. R. D. V. J. Prasada Rao', '2000 – 2006', 'ICAR-NBPGR RS, Hyderabad', 'male', 8),
            ('Dr. S. K. Chakrabarty', '2007 – 2009', 'ICAR-NBPGR RS, Hyderabad', 'male', 9),
            ('Dr. B. Sarath Babu', '2010 – 2012', 'ICAR-NBPGR RS, Hyderabad', 'male', 10),
            ('Dr. R. Jagadeeshwar', '2018 – 2020', 'PJTSAU, Hyderabad', 'male', 11),
            ('Dr. B. Parameswari', '2020 – 2022', 'ICAR-NBPGR RS, Hyderabad', 'female', 12),
        ]
        for name, tenure, aff, gender, order in secretaries:
            PastBearer.objects.create(role='secretary', name=name, tenure=tenure, affiliation=aff, gender=gender, order=order)

        treasurers = [
            ('Shri P. K. Menon', '1972 – 1974', 'CPPTI, Hyderabad', 'male', 1),
            ('Shri S. S. Lal', '1975 – 1976', 'CPPTI, Hyderabad', 'male', 2),
            ('Shri T. Rengarajan', '1977 – 1980, 1987 – 1990', 'CPPTI, Hyderabad', 'male', 3),
            ('Dr. A. Jayaprakash', '1981 – 1984', 'CPPTI, Hyderabad', 'male', 4),
            ('Dr. B. J. Divakar', '1985 – 1986', 'CPPTI, Hyderabad', 'male', 5),
            ('Mr. D. Chatterjee', '1991 – 1993', 'CPPTI, Hyderabad', 'male', 6),
            ('Mr. C. V. Rama Rao', '1993 – 1999', 'ANGRAU, Hyderabad', 'male', 7),
            ('Dr. K. Anitha', '2000 – 2004', 'ICAR-NBPGR RS, Hyderabad', 'female', 8),
            ('Dr. S. K. Chakrabarty', '2005 – 2006, 2010 – 2012', 'ICAR-NBPGR RS, Hyderabad', 'male', 9),
            ('Dr. Kamala Venkateswaran', '2007 – 2009', 'ICAR-NBPGR RS, Hyderabad', 'female', 10),
            ('Dr. Prasanna Holajjer', '2018 – 2020', 'ICAR-NBPGR RS, Hyderabad', 'male', 11),
            ('Dr. Bhasker Bajaru', '2020 – 2022', 'ICAR-NBPGR RS, Hyderabad', 'male', 12),
        ]
        for name, tenure, aff, gender, order in treasurers:
            PastBearer.objects.create(role='treasurer', name=name, tenure=tenure, affiliation=aff, gender=gender, order=order)

        editors = [
            ('Shri B. K. Verma', '1972 – 1976', 'CPPTI, Hyderabad', 'male', 1),
            ('Dr. V. Lakshminarayana', '1977 – 1978', 'CPPTI, Hyderabad', 'male', 2),
            ('Dr. K. K. Nirula', '1979 – 1982', 'CPPTI, Hyderabad', 'male', 3),
            ('Dr. M. Veerabhadra Rao', '1983 – 1993', 'CPPTI / ANGRAU', 'male', 4),
            ('Dr. H. C. Sharma', '1993 – 1995', 'ICRISAT, Patancheru', 'male', 5),
            ('Dr. T. B. Gour', '1995 – 1999', 'ANGRAU, Hyderabad', 'male', 6),
            ('Dr. K. S. Varaprasad', '2000 – 2004', 'ICAR-NBPGR RS, Hyderabad', 'male', 7),
            ('Dr. B. Sarath Babu', '2005 – 2009', 'ICAR-NBPGR RS, Hyderabad', 'male', 8),
            ('Dr. Gururaj Katti', '2010 – 2012', 'DRR (ICAR-IIRR), Hyderabad', 'male', 9),
            ('Dr. G. Sridevi', '2018 – 2020', 'PJTSAU, Hyderabad', 'female', 10),
            ('Dr. L. Saravanan', '2020 – 2022', 'ICAR-NBPGR RS, Hyderabad', 'male', 11),
        ]
        for name, tenure, aff, gender, order in editors:
            PastBearer.objects.create(role='editor', name=name, tenure=tenure, affiliation=aff, gender=gender, order=order)

        # 5. Editorial Board Members & Honorary Patrons
        EditorialBoardMember.objects.all().delete()
        editorial_board_data = [
            ('Prof. T V K Singh', 'chief_editor', 'Dean of ANGRAU and PJTSAU Retd. & Ex. ICAR-Emeritus Scientist, Hyderabad.', 1),
            ('Dr. Kavita Gupta', 'assoc_editor', 'ICAR-National Bureau of Plant Genetic Resources, New Delhi', 2),
            ('Dr. Prasanna Holajjer', 'assoc_editor', 'ICAR-National Bureau of Plant Genetic Resources, Regional Station, Hyderabad', 3),
            ('Dr. J Alice R P Sujeetha', 'member', 'National Institute of Plant Health Management (NIPHM), Hyderabad', 4),
            ('Dr. Jameel Aktar', 'member', 'ICAR-National Bureau of Plant Genetic Resources, Pusa Campus, New Delhi', 5),
            ('Dr. Kuldeep Singh Jadon', 'member', 'ICAR-Central Arid Zone Research Institute, Jodhpur, Rajasthan', 6),
            ('Dr. Jose Remeno Faleiro', 'member', 'FAO Expert (Red Palm Weevil), Goa', 7),
            ('Dr. Hamadttu Abdel Farag Elshafie', 'member', 'Senior Research Entomologist and Head IPM Program in Date Palm, King Faisal University Hofuf, Kingdom of Saudi Arabia', 8),
            ('Dr. P Anandhi', 'member', 'Tamil Nadu Rice Research Institute, TNAU, Aduthurai, Tamil Nadu', 9),
            ('Dr. P Raja', 'member', 'College of Horticultural and Forestry, CAU, Pasighat, Arunachal Pradesh', 10),
            ('Dr. A K Sinha', 'patron', 'Plant Protection Advisor, Directorate of Plant Protection, Quarantine & Storage, Faridabad, Haryana', 11),
            ('Dr. K S R K Murthy', 'patron', 'Telecom Colony, Ved Vihar, Secunderabad, Telangana', 12),
            ('Mr. N Sukumar', 'patron', 'Managing Director, Hyderabad Chemical Products Ltd., Hyderabad, Telangana', 13),
        ]
        for name, role, inst, order in editorial_board_data:
            EditorialBoardMember.objects.create(name=name, role=role, institution=inst, order=order)

        # 6. Special Publications & Monographs (Page 6 of document)
        PublicationBook.objects.all().delete()
        books_data = [
            (1986, 'Plant Protection in the Year 2000 AD (Eds. S. Jayaraj, B.K. Verma, D. Bap Reddy)'),
            (1993, 'Integrated Pest Management in Crops (Eds. M. Veerabhadra Rao, H.C. Sharma, T.B. Gour)'),
            (2012, 'Plant Protection in Agriculture: Challenges & Opportunities (Eds. K.S. Varaprasad, B. Sarath Babu)'),
            (2016, 'Plant Health Management in Organic Agriculture (Eds. B. Sarath Babu, B. Parameswari, G. Sridevi)'),
        ]
        for year, title in books_data:
            PublicationBook.objects.create(year=year, title=title)

        # 7. Conferences, Seminars & Symposia (Page 8 / Section 8.0)
        ConferenceEvent.objects.all().delete()
        conferences_data = [
            (2023, 'International Conference on Plant Protection in Agriculture: Horizon 2047, Hyderabad (Nov 27-29, 2023)'),
            (2021, 'National Symposium on Emerging Pests and Diseases in Climate Resilient Agriculture, Virtual Mode (Dec 15-17, 2021)'),
            (2018, 'National Symposium on Plant Health Management: Embracing Eco-Friendly Technologies, Hyderabad (Nov 15-17, 2018)'),
            (2016, 'National Symposium on Plant Health Management in Organic Agriculture, Hyderabad (Dec 11-13, 2016)'),
            (2012, 'National Symposium on Plant Protection in Agriculture: Challenges and Opportunities, Hyderabad (Nov 26-28, 2012)'),
            (2009, 'National Symposium on Plant Protection: Technology Transition & Innovations, Hyderabad (Nov 27-28, 2009)'),
            (2006, 'National Symposium on Plant Health Management: Proactive Approaches, Hyderabad (Nov 29-Dec 1, 2006)'),
            (2003, 'National Symposium on Plant Protection: Challenges for the Next Decade, Hyderabad (Nov 24-25, 2003)'),
            (2000, 'National Symposium on Crop Protection in Sustainable Agriculture, Hyderabad (Nov 23-25, 2000)'),
            (1997, 'Silver Jubilee National Symposium on Plant Protection: Retrospect & Prospects, Hyderabad (Dec 22-24, 1997)'),
            (1993, 'National Symposium on IPM: Principles and Practice, Hyderabad (Nov 24-26, 1993)'),
            (1990, 'National Symposium on Biological Control of Pests and Diseases, Coimbatore (Oct 18-20, 1990)'),
            (1988, 'National Symposium on Plant Protection Technology: Gaps and Strategies, Hyderabad (Nov 24-26, 1988)'),
            (1986, 'National Seminar on Plant Protection in the Year 2000 AD, Hyderabad (Nov 20-22, 1986)'),
        ]
        for year, title in conferences_data:
            ConferenceEvent.objects.create(year=year, event_title=title)

        # 8. PPAI Society Awards & Fellowship (Page 7 of document)
        SocietyAward.objects.all().delete()
        awards_data = [
            ('Dr. D. Bap Reddy Memorial Award', 'Conferred on an eminent scientist for outstanding research and contributions in the field of Plant Protection / Agricultural Entomology.'),
            ('Dr. S.B. Chattopadhyay Memorial Award', 'Conferred on a distinguished scientist for outstanding contributions in Plant Pathology and crop disease management.'),
            ('Dr. S.N. Banerjee Memorial Award', 'Conferred for exceptional research accomplishments in Integrated Pest Management (IPM) and ecological crop protection.'),
            ('Dr. K. Ramakrishnan Memorial Award', 'Conferred for exemplary contributions in basic and applied Plant Pathology and quarantine science.'),
            ('Fellow of Plant Protection Association of India (FPPAI)', 'Conferred on distinguished members in recognition of significant contributions to plant protection research, education, and the Association.'),
        ]
        for name, desc in awards_data:
            SocietyAward.objects.create(name=name, conferred_for=desc)

        # 9. Journal Volumes
        for vol in range(1, 55):
            year = 1972 + vol - 1
            JournalVolume.objects.get_or_create(
                volume_number=vol,
                defaults={
                    'year': year,
                    'issues_available': 'No. 1, No. 2, No. 3, No. 4',
                    'epubs_url': f'https://epubs.icar.org.in/index.php/IJPP'
                }
            )

        self.stdout.write(self.style.SUCCESS("SUCCESS: 100% of PPAI Society Data (Site Settings, Slides, Executive Council with Dr. B. Sarath Babu as President, Legends, Editorial Board, Books, Conferences, Awards, Journal Volumes) seeded cleanly into the database!"))
