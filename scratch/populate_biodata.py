import os
import sys
import django

sys.path.insert(0, os.path.abspath('.'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from pages.models import ExecutiveMember

# 1. Dr. Sarath Babu Balijepalli (President)
sarath = ExecutiveMember.objects.filter(designation__icontains='President').exclude(designation__icontains='Vice').first()
if not sarath:
    sarath = ExecutiveMember.objects.filter(name__icontains='Sarath').first()

if sarath:
    sarath.name = "Dr. Sarath Babu Balijepalli"
    sarath.designation = "President"
    sarath.affiliation = "Former Principal Scientist & Head, ICAR-NBPGR Regional Station, Hyderabad"
    sarath.qualification = "Ph.D. & M.Sc. (Agricultural Entomology), IARI, New Delhi (1980–1986); B.Sc. (Ag.), ANGRAU"
    sarath.official_address = "ICAR-NBPGR Regional Station, Rajendranagar, Hyderabad – 500030, Telangana"
    sarath.bio = """Dr Sarath Babu Balijepalli is a distinguished scientist and policy expert in Plant Genetic Resources (PGR) and Plant Quarantine. Throughout a career spanning over three decades, he has been a tireless advocate for farmers' welfare and the conservation of biodiversity. He superannuated on May 31, 2020, as Principal Scientist and Head of the NBPGR Regional Station, Hyderabad, and currently serves as the President of the Plant Protection Association of India (PPAI), an organization dedicated to supporting researchers, academicians, and the farming community."""
    sarath.achievements = """• PGR & Quarantine Policy: Registered several germplasm genotypes resistant to biotic stresses; formulated national plant quarantine policies as FAO Consultant for Saudi Arabia and World Bank SOPs for Kyrgyzstan (2022).
• Community Conservation: Played a pivotal role in raising awareness for landrace conservation in Eastern Ghats; enabled Sanjeevini Rural Development Society to win the Plant Genome Saviour Community Award (2011).
• Visiting Fellowships: Natural History Museum, London (2006–2007); Rutgers University, USA (2003); University of Hawaii (1995).
• Chief Editor & Author: Served as Editor and Chief Editor of the Indian Journal of Plant Protection; authored 100+ research papers and regular policy columns in The Hindu, Sakshi, and Down To Earth.
• Scientific Leadership: Chair for ICPHM 2023; Co-Chair for IPPC 2019 (with ICRISAT); Organizing Secretary for ICPGM 2012; Organized National Seminars on Seed Sovereignty & Gene Banks (2025) and Agriculture & GDP Growth (2026)."""
    sarath.save()
    print("Updated Dr. Sarath Babu Balijepalli successfully!")

# 2. Dr. B. Parameswari (General Secretary)
param = ExecutiveMember.objects.filter(designation__icontains='General Secretary').first()
if not param:
    param = ExecutiveMember.objects.filter(name__icontains='Parameswari').first()

if param:
    param.name = "Dr. B. Parameswari"
    param.designation = "General Secretary"
    param.affiliation = "Principal Scientist, ICAR-NBPGR Regional Station, Rajendranagar, Hyderabad – 500030"
    param.email = "parameswari.b@icar.gov.in, parampathnem1@gmail.com"
    param.phone = "+91 9468178283"
    param.date_of_birth = "June 20, 1980"
    param.qualification = "B.Sc. (Ag.) TNAU Coimbatore (1997-2001); M.Sc. UAS Dharwad (2001-2003); Ph.D. IARI New Delhi (2004-2009)"
    param.official_address = "ICAR-NBPGR Regional Station, Rajendranagar, Hyderabad – 500030, Telangana"
    param.bio = """Dr. B. Parameswari is a Principal Scientist at ICAR-NBPGR Regional Station, Hyderabad, and General Secretary of PPAI. She has served across prestigious institutions including DFRL (DRDO) Mysore, ICAR-SBI Karnal, and as Visiting Scientist at the University of California, Davis, USA (2014-15). Her core research spans Diagnostics, Genomics of plant viruses and their management, RNAi, VIGS, Genome-wide association studies for Host resistance, and Plant Quarantine."""
    param.achievements = """• Prestigious Awards: CSIR-ASPIRE Award (2024), Best Women Scientist Award from Deccan Society of Plant Pathologists (2024), SERB POWER Fellowship (2023), DST (SERB)-Women Excellence Research Award (2020), DST (SERB)-Early Career Research Award (2017), ICAR-Jawaharlal Nehru Award (2010), IARI Gold Medal in Ph.D (2010).
• Fellowships & Memberships: Membership of NASI (2026), Fellow PPAI (2026), Fellow Society for Plant Research (2023), Associate Fellow NAAS (2019), Indo-US Post-Doctoral Research Fellowship of IUSSTF (2013), Fellow Society for Applied Biotechnology (2011), Distinguished Member World Society of Virology (2018).
• Research Output: 74 Research Papers, 10 Review Papers, 8 Books, and 55 Other Scientific Publications."""
    param.save()
    print("Updated Dr. B. Parameswari successfully!")

# 3. Dr. Bajaru Bhaskar (Treasurer)
bhaskar = ExecutiveMember.objects.filter(designation__icontains='Treasurer').first()
if not bhaskar:
    bhaskar = ExecutiveMember.objects.filter(name__icontains='Bhaskar').first()

if bhaskar:
    bhaskar.name = "Dr. Bajaru Bhaskar"
    bhaskar.designation = "Treasurer"
    bhaskar.affiliation = "Scientist (Plant Pathology), ICAR-National Bureau of Plant Genetic Resources (NBPGR), Regional Station, Rajendranagar, Hyderabad – 500030"
    bhaskar.email = "bhaskar.bajaru@icar.org.in, bhaskar2008agrico@gmail.com"
    bhaskar.phone = "+91 8297968097, +91 8074484504"
    bhaskar.date_of_birth = "July 3, 1990"
    bhaskar.qualification = "Ph.D. in Plant Pathology"
    bhaskar.official_address = "ICAR-National Bureau of Plant Genetic Resources (NBPGR), Regional Station, Rajendranagar, Hyderabad – 500030, Telangana"
    bhaskar.bio = """Dr. Bajaru Bhaskar is a Scientist (Plant Pathology) at ICAR-NBPGR Regional Station, Hyderabad, serving as the Treasurer of the Plant Protection Association of India. His research focuses on plant quarantine, biosecurity clearance, and pathogen interception across agricultural germplasm imports and exports."""
    bhaskar.achievements = """• Germplasm Quarantine Processing: Associated with processing over 3,07,696 crop germplasm samples (1,09,113 imports and 1,98,583 exports) for biosecurity and phytosanitary clearance.
• Quarantine Pathogen Interceptions: Successfully intercepted high-risk pathogens including Pyricularia grisea (finger millet from Kenya), Peronospora manshurica (soybean from USA/Taiwan), Plasmopara halstedii (sunflower from USA), and Bean common mosaic virus (Bambara groundnut from Ghana), preventing their entry into India.
• Key Projects: Co-PI in 4 major projects including Orphan Legumes for Dryland Farming, CRP-Agrobiodiversity Maize Programme, and Quarantine Health Testing & Biosecurity Policy."""
    bhaskar.publications = """1. Parameswari, B., Bhaskar, B., et al. (2022). First Report of the Association of Zygocactus virus X with Dragon Fruit (Hylocereus spp.) plants from Telangana, India. Plant Disease, 107(4): 1249. (NAAS: 10.50)
2. Parameswari, B., Bhaskar, B., et al. (2022). First record of Cactus virus X in Dragon Fruit (Hylocereus spp.) in India. Indian Phytopathology, 75(1): 297–299. (NAAS: 5.99)
3. Bhaskar, B., et al. (2021). Elucidation of Tissue Specific Variability in Pyricularia oryzae Population Causing Rice Leaf Blast and Neck Blast. Journal of Mycology and Plant Pathology, 50(3): 299–310. (NAAS: 5.08)
4. Bhaskar, B., et al. (2016). Fungicidal action of mycogenic silver nanoparticles against Aspergillus niger inciting collar rot disease in groundnut. Indian Phytopathology, 69(4S): 605–608. (NAAS: 5.99)
5. Bhaskar, B., et al. (2016). Role of organic acids production in Pathogenicity of Aspergillus niger inciting collar rot disease in groundnut. Indian Phytopathology, 69(4S): 172–174. (NAAS: 5.99)"""
    bhaskar.save()
    print("Updated Dr. Bajaru Bhaskar successfully!")

# 4. Dr. Johnson Stanley (Councillor)
stanley = ExecutiveMember.objects.filter(name__icontains='Stanley').first()
if not stanley:
    stanley = ExecutiveMember.objects.filter(order=12).first()

if stanley:
    stanley.name = "Dr. Johnson Stanley"
    stanley.designation = "Councillor"
    stanley.affiliation = "CEO & Director (Nutrihub) & Principal Scientist (Agricultural Entomology), ICAR–Indian Institute of Millets Research (ICAR–IIMR), Hyderabad"
    stanley.qualification = "Postgraduate & Ph.D. in Agricultural Entomology (TNAU); PG Diploma in Intellectual Property Rights"
    stanley.official_address = "ICAR–Indian Institute of Millets Research (ICAR–IIMR), Rajendranagar, Hyderabad – 500030, Telangana"
    stanley.bio = """Dr. Johnson Stanley is the CEO & Director of Nutrihub, a technology business incubator exclusively focused on millets and hosted at ICAR–Indian Institute of Millets Research (ICAR–IIMR), Hyderabad. He is also a Principal Scientist in Agricultural Entomology at ICAR–IIMR.

He completed his postgraduate and doctoral studies at Tamil Nadu Agricultural University (TNAU) and began his career as a Scientist at ICAR–Vivekananda Parvatiya Krishi Anusandhan Sansthan, Almora, Uttarakhand, where he served for 12 years before joining ICAR–IIMR, Hyderabad."""
    stanley.achievements = """• CEO & Director, Nutrihub (Technology Business Incubator for Millets)
• Fellow of the Royal Entomological Society (FRES), London
• Fellow of the Entomological Society of India (FESI)
• Fellow of the Plant Protection Association of India (FPPAI)
• Associate of the National Academy of Agricultural Sciences (NAAS)
• Officer-in-Charge, Intellectual Property & Technology Management (ITM-BPD Unit), ICAR-IIMR
• Author of 50+ research articles and 4 books in Agricultural Entomology and Crop Protection"""
    stanley.save()
    print("Updated Dr. Johnson Stanley successfully!")

# 5. Dr. Alpeshkumar V. Khanpara (Councillor)
khanpara = ExecutiveMember.objects.filter(name__icontains='Khanpara').first()
if not khanpara:
    khanpara = ExecutiveMember.objects.filter(order=13).first()

if khanpara:
    khanpara.name = "Dr. Alpeshkumar V. Khanpara"
    khanpara.designation = "Councillor"
    khanpara.affiliation = "Department of Entomology, Junagadh Agricultural University, Morbi, Gujarat"
    khanpara.qualification = "Ph.D. in Agricultural Entomology (JAU)"
    khanpara.official_address = "Junagadh Agricultural University, Morbi, Gujarat"
    khanpara.bio = """Professor (Entomology) and Senior Scientist & Head at Junagadh Agricultural University, Morbi. Ph.D. in Agricultural Entomology from JAU; his research focuses on eco-friendly pest management that reduces pesticide load and residues."""
    khanpara.achievements = """• 14 international and 18 national research articles
• Principal Investigator of 30+ research and extension projects
• Appreciation certificates from the Ministry of Finance and the Ministry of Earth Sciences"""
    khanpara.save()
    print("Updated Dr. Alpeshkumar V. Khanpara successfully!")
