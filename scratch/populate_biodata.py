import os
import sys
import django

sys.path.insert(0, os.path.abspath('.'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from pages.models import ExecutiveMember

# 1. Update Dr. Bajaru Bhaskar (Treasurer)
bhaskar = ExecutiveMember.objects.filter(designation__icontains='Treasurer').first()
if not bhaskar:
    bhaskar = ExecutiveMember.objects.filter(name__icontains='Bhaskar').first()

if bhaskar:
    bhaskar.name = "Dr. Bajaru Bhaskar"
    bhaskar.designation = "Treasurer"
    bhaskar.affiliation = "Scientist (Plant Pathology), ICAR-National Bureau of Plant Genetic Resources (NBPGR), Regional Station, Rajendranagar, Hyderabad – 500030, Telangana"
    bhaskar.email = "bhaskar.bajaru@icar.org.in, bhaskar2008agrico@gmail.com"
    bhaskar.phone = "+91 8297968097, +91 8074484504"
    bhaskar.date_of_birth = "July 3, 1990"
    bhaskar.qualification = "Ph.D. in Plant Pathology"
    bhaskar.official_address = "ICAR-National Bureau of Plant Genetic Resources (NBPGR), Regional Station, Rajendranagar, Hyderabad – 500030, Telangana"
    bhaskar.bio = "Dr. Bajaru Bhaskar is a Scientist (Plant Pathology) at ICAR-NBPGR Regional Station, Hyderabad, serving as the Treasurer of the Plant Protection Association of India. His research focuses on plant quarantine, biosecurity clearance, and pathogen interception across agricultural germplasm imports and exports."
    bhaskar.achievements = """• Germplasm Quarantine Processing: Associated with processing over 3,07,696 crop germplasm samples (1,09,113 imports and 1,98,583 exports) for biosecurity and phytosanitary clearance.
• Quarantine Pathogen Interceptions: Successfully intercepted high-risk pathogens including Pyricularia grisea (finger millet from Kenya), Peronospora manshurica (soybean from USA/Taiwan), Plasmopara halstedii (sunflower from USA), and Bean common mosaic virus (Bambara groundnut from Ghana), preventing their entry into India."""
    bhaskar.projects = """1. Evaluation of Stress Tolerant Orphan Legumes for Dryland Farming Systems across Sub-Saharan Africa and India (Co-PI, Ongoing)
2. CRP-Agrobiodiversity Component-II Maize Programme (Co-PI, 2022–2024)
3. Quarantine of PGR under Exchange, Health Testing, Supportive Research & Related Biosecurity Policy Issues (Co-PI, Ongoing)
4. Characterization, Evaluation, Pre-breeding and Documentation of Agri-Horticultural Crops Germplasm (Co-PI, Ongoing)"""
    bhaskar.publications = """1. Parameswari, B., Bhaskar, B., et al. (2022). First Report of the Association of Zygocactus virus X with Dragon Fruit (Hylocereus spp.) plants from Telangana, India. Plant Disease, 107(4): 1249. (NAAS: 10.50)
2. Parameswari, B., Bhaskar, B., et al. (2022). First record of Cactus virus X in Dragon Fruit (Hylocereus spp.) in India. Indian Phytopathology, 75(1): 297–299. (NAAS: 5.99)
3. Bhaskar, B., et al. (2021). Elucidation of Tissue Specific Variability in Pyricularia oryzae Population Causing Rice Leaf Blast and Neck Blast. Journal of Mycology and Plant Pathology, 50(3): 299–310. (NAAS: 5.08)
4. Bhaskar, B., et al. (2016). Fungicidal action of mycogenic silver nanoparticles against Aspergillus niger inciting collar rot disease in groundnut. Indian Phytopathology, 69(4S): 605–608. (NAAS: 5.99)
5. Bhaskar, B., et al. (2016). Role of organic acids production in Pathogenicity of Aspergillus niger inciting collar rot disease in groundnut. Indian Phytopathology, 69(4S): 172–174. (NAAS: 5.99)"""
    bhaskar.save()
    print("Updated Dr. Bajaru Bhaskar successfully!")
else:
    print("Dr. Bajaru Bhaskar not found!")

# 2. Update Dr. Johnson Stanley (Councillor)
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

He completed his postgraduate and doctoral studies at Tamil Nadu Agricultural University (TNAU) and began his career as a Scientist at ICAR–Vivekananda Parvatiya Krishi Anusandhan Sansthan, Almora, Uttarakhand, where he served for 12 years before joining ICAR–IIMR, Hyderabad.

Dr. Stanley has published 50+ national and international research articles and 4 books and has received several awards and recognitions. He is a Fellow of the Royal Entomological Society (FRES), London, Entomological Society of India (FESI), and Plant Protection Association of India (FPPAI), and an Associate of the National Academy of Agricultural Sciences (NAAS).

At ICAR–IIMR, he is the Officer-in-Charge for Intellectual Property and Technology Management, overseeing intellectual property protection, commercialization and technology transfer. He also serves as the Nodal Officer for institutional collaborations with academia and public and private organizations."""
    stanley.achievements = """• CEO & Director, Nutrihub (Technology Business Incubator for Millets)
• Fellow of the Royal Entomological Society (FRES), London
• Fellow of the Entomological Society of India (FESI)
• Fellow of the Plant Protection Association of India (FPPAI)
• Associate of the National Academy of Agricultural Sciences (NAAS)
• Officer-in-Charge, Intellectual Property & Technology Management (ITM-BPD Unit), ICAR-IIMR
• Nodal Officer for institutional collaborations with academia and public/private organizations
• Author of 50+ research articles and 4 books in Agricultural Entomology and Crop Protection"""
    stanley.save()
    print("Updated Dr. Johnson Stanley successfully!")
else:
    print("Dr. Johnson Stanley not found!")
