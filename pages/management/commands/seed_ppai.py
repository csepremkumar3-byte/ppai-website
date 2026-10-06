import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from pages.models import (
    SiteSetting, CarouselSlide, ExecutiveMember, PastBearer,
    EditorialBoardMember, PublicationBook, ConferenceEvent,
    SocietyAward, JournalVolume, JournalArticle
)

EXECUTIVE_MEMBERS_FULL_DATA = [   {   'achievements': '• PGR & Quarantine Policy: Registered several germplasm genotypes resistant to biotic '
                        'stresses; formulated national plant quarantine policies as FAO Consultant for Saudi Arabia '
                        'and World Bank SOPs for Kyrgyzstan (2022).\n'
                        '• Community Conservation: Played a pivotal role in raising awareness for landrace '
                        'conservation in Eastern Ghats; enabled Sanjeevini Rural Development Society to win the Plant '
                        'Genome Saviour Community Award (2011).\n'
                        '• Visiting Fellowships: Natural History Museum, London (2006–2007); Rutgers University, USA '
                        '(2003); University of Hawaii (1995).\n'
                        '• Chief Editor & Author: Served as Editor and Chief Editor of the Indian Journal of Plant '
                        'Protection; authored 100+ research papers and regular policy columns in The Hindu, Sakshi, '
                        'and Down To Earth.\n'
                        '• Scientific Leadership: Chair for ICPHM 2023; Co-Chair for IPPC 2019 (with ICRISAT); '
                        'Organizing Secretary for ICPGM 2012; Organized National Seminars on Seed Sovereignty & Gene '
                        'Banks (2025) and Agriculture & GDP Growth (2026).',
        'affiliation': 'Former Principal Scientist & Head, ICAR-NBPGR Regional Station, Hyderabad',
        'bio': 'Dr Sarath Babu Balijepalli is a distinguished scientist and policy expert in Plant Genetic Resources '
               '(PGR) and Plant Quarantine. Throughout a career spanning over three decades, he has been a tireless '
               "advocate for farmers' welfare and the conservation of biodiversity. He superannuated on May 31, 2020, "
               'as Principal Scientist and Head of the NBPGR Regional Station, Hyderabad, and currently serves as the '
               'President of the Plant Protection Association of India (PPAI), an organization dedicated to supporting '
               'researchers, academicians, and the farming community.',
        'date_of_birth': None,
        'designation': 'President',
        'email': None,
        'gender': 'male',
        'image': 'council/dr_b_sarath_babu.png',
        'name': 'Dr. Sarath Babu',
        'official_address': 'ICAR-NBPGR Regional Station, Rajendranagar, Hyderabad – 500030, Telangana',
        'order': 1,
        'phone': None,
        'projects': None,
        'publications': None,
        'qualification': 'Ph.D. & M.Sc. (Agricultural Entomology), IARI, New Delhi (1980–1986); B.Sc. (Ag.), ANGRAU'},
    {   'achievements': None,
        'affiliation': 'Professor, Jayashankar Telangana State Agricultural University, Hyderabad',
        'bio': 'Vice-President.',
        'date_of_birth': None,
        'designation': 'Vice-President',
        'email': None,
        'gender': 'male',
        'image': 'council/dr_jagadeeshwar.png',
        'name': 'Dr. Jagadeeshwar',
        'official_address': None,
        'order': 2,
        'phone': None,
        'projects': None,
        'publications': None,
        'qualification': None},
    {   'achievements': None,
        'affiliation': 'ICAR-National Bureau of Plant Genetic Resources, Pusa Campus, New Delhi',
        'bio': 'Vice-President.',
        'date_of_birth': None,
        'designation': 'Vice-President',
        'email': None,
        'gender': 'female',
        'image': 'council/dr_celia_chalam.png',
        'name': 'Dr. Celia Chalam',
        'official_address': None,
        'order': 3,
        'phone': None,
        'projects': None,
        'publications': None,
        'qualification': None},
    {   'achievements': None,
        'affiliation': 'ICAR-Indian Institute of Rice Research, Hyderabad',
        'bio': 'Vice-President.',
        'date_of_birth': None,
        'designation': 'Vice-President',
        'email': None,
        'gender': 'male',
        'image': 'council/dr_m_srinivas_prasad.jpg',
        'name': 'Dr. M Srinivas Prasad',
        'official_address': None,
        'order': 4,
        'phone': None,
        'projects': None,
        'publications': None,
        'qualification': None},
    {   'achievements': '• Prestigious Awards: CSIR-ASPIRE Award (2024), Best Women Scientist Award from Deccan '
                        'Society of Plant Pathologists (2024), SERB POWER Fellowship (2023), DST (SERB)-Women '
                        'Excellence Research Award (2020), DST (SERB)-Early Career Research Award (2017), '
                        'ICAR-Jawaharlal Nehru Award (2010), IARI Gold Medal in Ph.D (2010).\n'
                        '• Fellowships & Memberships: Membership of NASI (2026), Fellow PPAI (2026), Fellow Society '
                        'for Plant Research (2023), Associate Fellow NAAS (2019), Indo-US Post-Doctoral Research '
                        'Fellowship of IUSSTF (2013), Fellow Society for Applied Biotechnology (2011), Distinguished '
                        'Member World Society of Virology (2018).\n'
                        '• Research Output: 74 Research Papers, 10 Review Papers, 8 Books, and 55 Other Scientific '
                        'Publications.',
        'affiliation': 'Principal Scientist, ICAR-NBPGR Regional Station, Rajendranagar, Hyderabad – 500030',
        'bio': 'Dr. B. Parameswari is a Principal Scientist at ICAR-NBPGR Regional Station, Hyderabad, and General '
               'Secretary of PPAI. She has served across prestigious institutions including DFRL (DRDO) Mysore, '
               'ICAR-SBI Karnal, and as Visiting Scientist at the University of California, Davis, USA (2014-15). Her '
               'core research spans Diagnostics, Genomics of plant viruses and their management, RNAi, VIGS, '
               'Genome-wide association studies for Host resistance, and Plant Quarantine.',
        'date_of_birth': 'June 20, 1980',
        'designation': 'General Secretary',
        'email': 'parameswari.b@icar.gov.in, parampathnem1@gmail.com',
        'gender': 'female',
        'image': 'council/dr_b_parameshwari.png',
        'name': 'Dr. B Parameshwari',
        'official_address': 'ICAR-NBPGR Regional Station, Rajendranagar, Hyderabad – 500030, Telangana',
        'order': 5,
        'phone': '+91 9468178283',
        'projects': None,
        'publications': None,
        'qualification': 'B.Sc. (Ag.) TNAU Coimbatore (1997-2001); M.Sc. UAS Dharwad (2001-2003); Ph.D. IARI New Delhi '
                         '(2004-2009)'},
    {   'achievements': None,
        'affiliation': 'ICAR-Indian Institute of Rice Research, Hyderabad',
        'bio': 'Assistant Secretary.',
        'date_of_birth': None,
        'designation': 'Assistant Secretary',
        'email': None,
        'gender': 'male',
        'image': 'council/dr_v_prakasam.png',
        'name': 'Dr. V Prakasam',
        'official_address': None,
        'order': 6,
        'phone': None,
        'projects': None,
        'publications': None,
        'qualification': None},
    {   'achievements': '• Germplasm Quarantine Processing: Associated with processing over 3,07,696 crop germplasm '
                        'samples (1,09,113 imports and 1,98,583 exports) for biosecurity and phytosanitary clearance.\n'
                        '• Quarantine Pathogen Interceptions: Successfully intercepted high-risk pathogens including '
                        'Pyricularia grisea (finger millet from Kenya), Peronospora manshurica (soybean from '
                        'USA/Taiwan), Plasmopara halstedii (sunflower from USA), and Bean common mosaic virus (Bambara '
                        'groundnut from Ghana), preventing their entry into India.\n'
                        '• Key Projects: Co-PI in 4 major projects including Orphan Legumes for Dryland Farming, '
                        'CRP-Agrobiodiversity Maize Programme, and Quarantine Health Testing & Biosecurity Policy.',
        'affiliation': 'Scientist (Plant Pathology), ICAR-National Bureau of Plant Genetic Resources (NBPGR), Regional '
                       'Station, Rajendranagar, Hyderabad – 500030',
        'bio': 'Dr. Bajaru Bhaskar is a Scientist (Plant Pathology) at ICAR-NBPGR Regional Station, Hyderabad, serving '
               'as the Treasurer of the Plant Protection Association of India. His research focuses on plant '
               'quarantine, biosecurity clearance, and pathogen interception across agricultural germplasm imports and '
               'exports.',
        'date_of_birth': 'July 3, 1990',
        'designation': 'Treasurer',
        'email': 'bhaskar.bajaru@icar.org.in, bhaskar2008agrico@gmail.com',
        'gender': 'male',
        'image': 'council/dr_b_bhaskar.png',
        'name': 'Dr. Bajaru Bhaskar',
        'official_address': 'ICAR-National Bureau of Plant Genetic Resources (NBPGR), Regional Station, Rajendranagar, '
                            'Hyderabad – 500030, Telangana',
        'order': 7,
        'phone': '+91 8297968097, +91 8074484504',
        'projects': '1. Evaluation of Stress Tolerant Orphan Legumes for Dryland Farming Systems across Sub-Saharan '
                    'Africa and India (Co-PI, Ongoing)\n'
                    '2. CRP-Agrobiodiversity Component-II Maize Programme (Co-PI, 2022–2024)\n'
                    '3. Quarantine of PGR under Exchange, Health Testing, Supportive Research & Related Biosecurity '
                    'Policy Issues (Co-PI, Ongoing)\n'
                    '4. Characterization, Evaluation, Pre-breeding and Documentation of Agri-Horticultural Crops '
                    'Germplasm (Co-PI, Ongoing)',
        'publications': '1. Parameswari, B., Bhaskar, B., et al. (2022). First Report of the Association of Zygocactus '
                        'virus X with Dragon Fruit (Hylocereus spp.) plants from Telangana, India. Plant Disease, '
                        '107(4): 1249. (NAAS: 10.50)\n'
                        '2. Parameswari, B., Bhaskar, B., et al. (2022). First record of Cactus virus X in Dragon '
                        'Fruit (Hylocereus spp.) in India. Indian Phytopathology, 75(1): 297–299. (NAAS: 5.99)\n'
                        '3. Bhaskar, B., et al. (2021). Elucidation of Tissue Specific Variability in Pyricularia '
                        'oryzae Population Causing Rice Leaf Blast and Neck Blast. Journal of Mycology and Plant '
                        'Pathology, 50(3): 299–310. (NAAS: 5.08)\n'
                        '4. Bhaskar, B., et al. (2016). Fungicidal action of mycogenic silver nanoparticles against '
                        'Aspergillus niger inciting collar rot disease in groundnut. Indian Phytopathology, 69(4S): '
                        '605–608. (NAAS: 5.99)\n'
                        '5. Bhaskar, B., et al. (2016). Role of organic acids production in Pathogenicity of '
                        'Aspergillus niger inciting collar rot disease in groundnut. Indian Phytopathology, 69(4S): '
                        '172–174. (NAAS: 5.99)',
        'qualification': 'Ph.D. in Plant Pathology'},
    {   'achievements': None,
        'affiliation': 'Dean of ANGRAU and PJTSAU Retd. & Ex. ICAR-Emeritus Scientist, Hyderabad.',
        'bio': 'Chief Editor.',
        'date_of_birth': None,
        'designation': 'Chief Editor',
        'email': None,
        'gender': 'male',
        'image': 'council/prof_t_v_k_singh.png',
        'name': 'Prof. T V K Singh',
        'official_address': None,
        'order': 8,
        'phone': None,
        'projects': None,
        'publications': None,
        'qualification': None},
    {   'achievements': None,
        'affiliation': 'ICAR-National Bureau of Plant Genetic Resources, New Delhi',
        'bio': 'Associate Editor.',
        'date_of_birth': None,
        'designation': 'Associate Editor',
        'email': None,
        'gender': 'female',
        'image': 'council/dr_kavita_gupta.png',
        'name': 'Dr. Kavita Gupta',
        'official_address': None,
        'order': 9,
        'phone': None,
        'projects': None,
        'publications': None,
        'qualification': None},
    {   'achievements': None,
        'affiliation': 'ICAR-National Bureau of Plant Genetic Resources, Regional Station, Hyderabad',
        'bio': 'Associate Editor.',
        'date_of_birth': None,
        'designation': 'Associate Editor',
        'email': None,
        'gender': 'male',
        'image': 'council/dr_prasanna_holajjer.png',
        'name': 'Dr. Prasanna Holajjer',
        'official_address': None,
        'order': 10,
        'phone': None,
        'projects': None,
        'publications': None,
        'qualification': None},
    {   'achievements': None,
        'affiliation': 'ICAR-Central Institute of Cotton Research, Regional Station, Coimbatore',
        'bio': 'Councillor.',
        'date_of_birth': None,
        'designation': 'Councillor',
        'email': None,
        'gender': 'male',
        'image': 'council/dr_k_rameash.jpg',
        'name': 'Dr. K Rameash',
        'official_address': None,
        'order': 11,
        'phone': None,
        'projects': None,
        'publications': None,
        'qualification': None},
    {   'achievements': '• CEO & Director, Nutrihub (Technology Business Incubator for Millets)\n'
                        '• Fellow of the Royal Entomological Society (FRES), London\n'
                        '• Fellow of the Entomological Society of India (FESI)\n'
                        '• Fellow of the Plant Protection Association of India (FPPAI)\n'
                        '• Associate of the National Academy of Agricultural Sciences (NAAS)\n'
                        '• Officer-in-Charge, Intellectual Property & Technology Management (ITM-BPD Unit), ICAR-IIMR\n'
                        '• Author of 50+ research articles and 4 books in Agricultural Entomology and Crop Protection',
        'affiliation': 'CEO & Director (Nutrihub) & Principal Scientist (Agricultural Entomology), ICAR–Indian '
                       'Institute of Millets Research (ICAR–IIMR), Hyderabad',
        'bio': 'Dr. Johnson Stanley is the CEO & Director of Nutrihub, a technology business incubator exclusively '
               'focused on millets and hosted at ICAR–Indian Institute of Millets Research (ICAR–IIMR), Hyderabad. He '
               'is also a Principal Scientist in Agricultural Entomology at ICAR–IIMR.\n'
               '\n'
               'He completed his postgraduate and doctoral studies at Tamil Nadu Agricultural University (TNAU) and '
               'began his career as a Scientist at ICAR–Vivekananda Parvatiya Krishi Anusandhan Sansthan, Almora, '
               'Uttarakhand, where he served for 12 years before joining ICAR–IIMR, Hyderabad.',
        'date_of_birth': None,
        'designation': 'Councillor',
        'email': None,
        'gender': 'male',
        'image': 'council/dr_j_stanley.png',
        'name': 'Dr. Johnson Stanley',
        'official_address': 'ICAR–Indian Institute of Millets Research (ICAR–IIMR), Rajendranagar, Hyderabad – 500030, '
                            'Telangana',
        'order': 12,
        'phone': None,
        'projects': None,
        'publications': None,
        'qualification': 'Postgraduate & Ph.D. in Agricultural Entomology (TNAU); PG Diploma in Intellectual Property '
                         'Rights'},
    {   'achievements': '• 14 international and 18 national research articles\n'
                        '• Principal Investigator of 30+ research and extension projects\n'
                        '• Appreciation certificates from the Ministry of Finance and the Ministry of Earth Sciences',
        'affiliation': 'Department of Entomology, Junagadh Agricultural University, Morbi, Gujarat',
        'bio': 'Professor (Entomology) and Senior Scientist & Head at Junagadh Agricultural University, Morbi. Ph.D. '
               'in Agricultural Entomology from JAU; his research focuses on eco-friendly pest management that reduces '
               'pesticide load and residues.',
        'date_of_birth': None,
        'designation': 'Councillor',
        'email': None,
        'gender': 'male',
        'image': 'council/dr_alpesh_kumar.png',
        'name': 'Dr. Alpeshkumar V. Khanpara',
        'official_address': 'Junagadh Agricultural University, Morbi, Gujarat',
        'order': 13,
        'phone': None,
        'projects': None,
        'publications': None,
        'qualification': 'Ph.D. in Agricultural Entomology (JAU)'},
    {   'achievements': None,
        'affiliation': 'ICAR- National Bureau of Agricultural Insect Resources, Bengaluru',
        'bio': 'Councillor.',
        'date_of_birth': None,
        'designation': 'Councillor',
        'email': None,
        'gender': 'male',
        'image': 'council/dr_b_s_gotyal.png',
        'name': 'Dr. B S Gotyal',
        'official_address': None,
        'order': 14,
        'phone': None,
        'projects': None,
        'publications': None,
        'qualification': None},
    {   'achievements': None,
        'affiliation': 'ICAR- National Bureau of Agricultural Insect Resources, Bengaluru',
        'bio': 'Councillor.',
        'date_of_birth': None,
        'designation': 'Councillor',
        'email': None,
        'gender': 'male',
        'image': 'council/dr_d_sagar.png',
        'name': 'Dr. D Sagar',
        'official_address': None,
        'order': 15,
        'phone': None,
        'projects': None,
        'publications': None,
        'qualification': None}]


class Command(BaseCommand):
    help = 'Seeds all PPAI Society data into the active database'

    def handle(self, *args, **options):
        db_engine = settings.DATABASES['default']['ENGINE'].split('.')[-1]
        db_name = settings.DATABASES['default']['NAME']
        self.stdout.write(f"Connected to Database Engine: [{db_engine}], Database: [{db_name}]")
        self.stdout.write("Seeding full dataset from official document...")

        # Copy static council & editorial images to media directory
        for folder in ['council', 'editorial']:
            src_dir = os.path.join(settings.BASE_DIR, 'static', 'images', folder)
            dst_dir = os.path.join(settings.MEDIA_ROOT, folder)
            if os.path.exists(src_dir):
                os.makedirs(dst_dir, exist_ok=True)
                for fname in os.listdir(src_dir):
                    shutil.copy2(os.path.join(src_dir, fname), os.path.join(dst_dir, fname))

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

        # 3. Executive Council (With Full Biodata)
        ExecutiveMember.objects.all().delete()
        for m_data in EXECUTIVE_MEMBERS_FULL_DATA:
            ExecutiveMember.objects.create(**m_data)

        # 4. Past Office Bearers (Pages 3 & 4 of document)
        PastBearer.objects.all().delete()
        presidents = [
            ('Dr. K K Nirula', 'Founder President (1972 – 1978)', 'CPPTI, Hyderabad', 'male', 1),
            ('Dr. N C Joshi', '1979 – 1980', 'CPPTI, Hyderabad', 'male', 2),
            ('Dr. K D Paharia', '1981 – 1984', 'CPPTI, Hyderabad', 'male', 3),
            ('Dr. N C Joshi', '1985 – 1986', 'CPPTI, Hyderabad', 'male', 4),
            ('Dr. D Bap Reddy', '1987 – 1988', 'FAO Representative', 'male', 5),
            ('Dr. S Jayaraj', '1989 – 1990', 'TNAU, Coimbatore', 'male', 6),
            ('Dr. D V R Reddy', '1991 – 1997', 'ICRISAT, Patancheru', 'male', 7),
            ('Dr. K Krishnaiah', '1997 – 1999', 'DRR (ICAR-IIRR), Hyderabad', 'male', 8),
            ('Dr. P S Chandukar', '2000 – 2002', 'PPA to Govt. of India', 'male', 9),
            ('Dr. Y L Nene', '2003 – 2006', 'ICRISAT / Asian Agri-History Foundation', 'male', 10),
            ('Dr. K S R K Murthy', '2007 – 2009', 'ANGRAU, Hyderabad', 'male', 11),
            ('Dr. K S Varaprasad', '2010 – 2012', 'ICAR-NBPGR RS / IIOR', 'male', 12),
            ('Dr. B Sarath Babu', '2018 – 2022', 'ICAR-NBPGR RS, Hyderabad', 'male', 13),
        ]
        for name, tenure, aff, gender, order in presidents:
            PastBearer.objects.create(role='president', name=name, tenure=tenure, affiliation=aff, gender=gender, order=order)

        secretaries = [
            ('Dr. S S Hussaine', '1972 – 1974', 'CPPTI, Hyderabad', 'male', 1),
            ('Dr. V Lakshminarayana', '1975 – 1976, 1979 – 1980', 'CPPTI, Hyderabad', 'male', 2),
            ('Dr. Basu Chaudhary', '1977 – 1978', 'CPPTI, Hyderabad', 'male', 3),
            ('Dr. V Raghunathan', '1981 – 1984', 'Central Plant Protection Station', 'male', 4),
            ('Shri. B Govinda Naik', '1985 – 1986', 'CPPTI, Hyderabad', 'male', 5),
            ('Dr. B J Divakar', '1987 – 1997', 'Directorate of Plant Protection', 'male', 6),
            ('Dr. Renu Sharma', '1997 – 1999', 'ICAR-NBPGR RS, Hyderabad', 'female', 7),
            ('Dr. R D V J Prasada Rao', '2000 – 2006', 'ICAR-NBPGR RS, Hyderabad', 'male', 8),
            ('Dr. S K Chakrabarty', '2007 – 2009', 'ICAR-NBPGR RS, Hyderabad', 'male', 9),
            ('Dr. B Sarath Babu', '2010 – 2012', 'ICAR-NBPGR RS, Hyderabad', 'male', 10),
            ('Dr. R Jagadeeshwar', '2018 – 2020', 'PJTSAU, Hyderabad', 'male', 11),
            ('Dr. B Parameswari', '2020 – 2022', 'ICAR-NBPGR RS, Hyderabad', 'female', 12),
        ]
        for name, tenure, aff, gender, order in secretaries:
            PastBearer.objects.create(role='secretary', name=name, tenure=tenure, affiliation=aff, gender=gender, order=order)

        treasurers = [
            ('Shri. P K Menon', '1972 – 1974', 'CPPTI, Hyderabad', 'male', 1),
            ('Shri. S S Lal', '1975 – 1976', 'CPPTI, Hyderabad', 'male', 2),
            ('Shri. T Rengarajan', '1977 – 1980, 1987 – 1990', 'CPPTI, Hyderabad', 'male', 3),
            ('Dr. A Jayaprakash', '1981 – 1984', 'CPPTI, Hyderabad', 'male', 4),
            ('Dr. B J Divakar', '1985 – 1986', 'CPPTI, Hyderabad', 'male', 5),
            ('Mr. D Chatterjee', '1991 – 1993', 'CPPTI, Hyderabad', 'male', 6),
            ('Mr. C V Rama Rao', '1993 – 1999', 'ANGRAU, Hyderabad', 'male', 7),
            ('Dr. K Anitha', '2000 – 2004', 'ICAR-NBPGR RS, Hyderabad', 'female', 8),
            ('Dr. S K Chakrabarty', '2005 – 2006, 2010 – 2012', 'ICAR-NBPGR RS, Hyderabad', 'male', 9),
            ('Dr. Kamala Venkateswaran', '2007 – 2009', 'ICAR-NBPGR RS, Hyderabad', 'female', 10),
            ('Dr. Prasanna Holajjer', '2018 – 2020', 'ICAR-NBPGR RS, Hyderabad', 'male', 11),
            ('Dr. Bhasker Bajaru', '2020 – 2022', 'ICAR-NBPGR RS, Hyderabad', 'male', 12),
        ]
        for name, tenure, aff, gender, order in treasurers:
            PastBearer.objects.create(role='treasurer', name=name, tenure=tenure, affiliation=aff, gender=gender, order=order)

        editors = [
            ('Shri. B K Verma', '1972 – 1976', 'CPPTI, Hyderabad', 'male', 1),
            ('Dr. V Lakshminarayana', '1977 – 1978', 'CPPTI, Hyderabad', 'male', 2),
            ('Dr. K K Nirula', '1979 – 1982', 'CPPTI, Hyderabad', 'male', 3),
            ('Dr. M Veerabhadra Rao', '1983 – 1993', 'CPPTI / ANGRAU', 'male', 4),
            ('Dr. H C Sharma', '1993 – 1995', 'ICRISAT, Patancheru', 'male', 5),
            ('Dr. T B Gour', '1995 – 1999', 'ANGRAU, Hyderabad', 'male', 6),
            ('Dr. K S Varaprasad', '2000 – 2004', 'ICAR-NBPGR RS, Hyderabad', 'male', 7),
            ('Dr. B Sarath Babu', '2005 – 2009', 'ICAR-NBPGR RS, Hyderabad', 'male', 8),
            ('Dr. Gururaj Katti', '2010 – 2012', 'DRR (ICAR-IIRR), Hyderabad', 'male', 9),
            ('Dr. G Sridevi', '2018 – 2020', 'PJTSAU, Hyderabad', 'female', 10),
            ('Dr. L Saravanan', '2020 – 2022', 'ICAR-NBPGR RS, Hyderabad', 'male', 11),
        ]
        for name, tenure, aff, gender, order in editors:
            PastBearer.objects.create(role='editor', name=name, tenure=tenure, affiliation=aff, gender=gender, order=order)

        # 5. Editorial Board Members & Honorary Patrons
        EditorialBoardMember.objects.all().delete()
        editorial_board_data = [
            ('Prof. T V K Singh', 'chief_editor', 'Dean of ANGRAU and PJTSAU Retd. & Ex. ICAR-Emeritus Scientist, Hyderabad.', 'male', 'editorial/prof_t_v_k_singh.png', 1),
            ('Dr. Kavita Gupta', 'assoc_editor', 'ICAR-National Bureau of Plant Genetic Resources, New Delhi', 'female', 'editorial/dr_kavita_gupta.png', 2),
            ('Dr. Prasanna Holajjer', 'assoc_editor', 'ICAR-National Bureau of Plant Genetic Resources, Regional Station, Hyderabad', 'male', 'editorial/dr_prasanna_holajjer.png', 3),
            ('Dr. J Alice R P Sujeetha', 'member', 'National Institute of Plant Health Management (NIPHM), Hyderabad', 'female', None, 4),
            ('Dr. Jameel Akhtar', 'member', 'ICAR-National Bureau of Plant Genetic Resources, Pusa Campus, New Delhi', 'male', 'editorial/dr_jameel_akhtar.png', 5),
            ('Dr. Kuldeep Singh Jadon', 'member', 'ICAR-Central Arid Zone Research Institute, Jodhpur, Rajasthan', 'male', 'editorial/dr_kuldeep_singh_jadon.png', 6),
            ('Dr. Jose Romeno Faleiro', 'member', 'FAO Expert (Red Palm Weevil), Goa', 'male', 'editorial/dr_jose_romeno_faleiro.png', 7),
            ('Dr. Hamadttu Abdel Farag Elshafie', 'member', 'Senior Research Entomologist and Head IPM Program in Date Palm, King Faisal University Hofuf, Kingdom of Saudi Arabia', 'male', 'editorial/dr_hamadttu_abdel_farag_elshafie.png', 8),
            ('Dr. P Anandhi', 'member', 'Tamil Nadu Rice Research Institute, TNAU, Aduthurai, Tamil Nadu', 'female', 'editorial/dr_p_anandhi.png', 9),
            ('Dr. P Raja', 'member', 'College of Horticultural and Forestry, CAU, Pasighat, Arunachal Pradesh', 'male', 'editorial/dr_p_raja.png', 10),
            ('Dr. A K Sinha', 'patron', 'Plant Protection Advisor, Directorate of Plant Protection, Quarantine & Storage, Faridabad, Haryana', 'male', None, 11),
            ('Dr. K S R K Murthy', 'patron', 'Telecom Colony, Ved Vihar, Secunderabad, Telangana', 'male', None, 12),
            ('Mr. N Sukumar', 'patron', 'Managing Director, Hyderabad Chemical Products Ltd., Hyderabad, Telangana', 'male', None, 13),
        ]
        for name, role, inst, gender, img, order in editorial_board_data:
            kwargs = {'name': name, 'role': role, 'institution': inst, 'gender': gender, 'order': order}
            if img:
                kwargs['image'] = img
            EditorialBoardMember.objects.create(**kwargs)

        # 6. Special Publications & Monographs (Page 6 of document)
        PublicationBook.objects.all().delete()
        books_data = [
            (1986, 'Plant Protection in the Year 2000 AD (Eds. S Jayaraj, B K Verma, D Bap Reddy)'),
            (1993, 'Integrated Pest Management in Crops (Eds. M Veerabhadra Rao, H C Sharma, T B Gour)'),
            (2012, 'Plant Protection in Agriculture: Challenges & Opportunities (Eds. K S Varaprasad, B Sarath Babu)'),
            (2016, 'Plant Health Management in Organic Agriculture (Eds. B Sarath Babu, B Parameswari, G Sridevi)'),
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
            ('Dr. D Bap Reddy Memorial Award', 'Conferred on an eminent scientist for outstanding research and contributions in the field of Plant Protection / Agricultural Entomology.'),
            ('Dr. S B Chattopadhyay Memorial Award', 'Conferred on a distinguished scientist for outstanding contributions in Plant Pathology and crop disease management.'),
            ('Dr. S N Banerjee Memorial Award', 'Conferred for exceptional research accomplishments in Integrated Pest Management (IPM) and ecological crop protection.'),
            ('Dr. K Ramakrishnan Memorial Award', 'Conferred for exemplary contributions in basic and applied Plant Pathology and quarantine science.'),
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

        self.stdout.write(self.style.SUCCESS("SUCCESS: 100% of PPAI Society Data (Site Settings, Slides, Executive Council with Full Biodata, Legends, Editorial Board, Books, Conferences, Awards, Journal Volumes) seeded cleanly into the database!"))
