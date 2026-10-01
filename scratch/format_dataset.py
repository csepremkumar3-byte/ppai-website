# Script to generate clean JS dataset for templates/pages/awards.html
import json

fellows_raw = [
    ("Before 2003", [
        "Dr D Bap Reddy", "Dr N C Joshi", "Dr B V David", "Dr K Krishnaiah", "Dr V C S Sastry",
        "Dr B J Divakar", "Dr H C Sharma", "Dr L V Gangwane", "Dr Viswanath", "Dr S M A Rizvi",
        "Dr S S Lateef", "Dr O P Singh", "Dr A D Pawar", "Dr K P Srivastava", "Dr D J Patel",
        "Dr S S Misra", "Dr A R Solayappan", "Dr K Natarajan", "Dr A K Garg", "Dr Allahnoor",
        "Dr S K Gangwar", "Dr S K Srivastava", "Dr G Arjanan", "Dr M Balasubramanian", "Dr D Kumaresan",
        "Dr M Veerabhadra Rao", "Dr G Maruthi Ram", "Dr K C Bhagat", "Dr V K Kalra", "Dr K S R K Murthy",
        "Dr Shashi Verma", "Dr K C D Urs", "Dr R C Joshi", "Dr S R Das", "Dr G Balasubramanian",
        "Dr H P Patnaik", "Dr S Kumarasamy", "Dr Rambabu Gaur", "Dr P V Sarma", "Dr G T Gujar",
        "Dr T V K Singh", "Dr V Raghunathan", "Dr S P Singh", "Dr T B Gour", "Dr K C S Rao",
        "Dr H R Patel", "Dr Raghunatha Rao", "Dr Sanjay Kumar", "Dr I V Dhruj", "Dr R T Gahukar",
        "Dr B Senapthi", "Dr G Ramaprasad", "Dr S V Damdhere", "Dr N C Misra", "Dr R P Thakur",
        "Dr S B Sharma", "Dr Renu Sharma", "Dr Meera Gupta", "Dr Amrit Phokela", "Dr S Jayaraj",
        "Dr K Abbaiah", "Dr B K Sontakke", "Dr P S Chandukar", "Dr N Venugopal Rao", "Dr G V Subbarathnam",
        "Dr Suresh Pande", "Dr S K Pal", "Dr Mangal Sain", "Dr S P Sharma", "Dr S S Bhardwaj",
        "Dr C P C Kumar", "Dr S Uthamasamy", "Dr B Padmanabhan", "Dr M P Singh", "Dr P R M Rao",
        "Dr T M Manjunath", "Dr R D V J Prasada Rao", "Dr T Ramesh Babu", "Dr P R Misra", "Dr Ravi Prakash Maurya",
        "Dr A J Tamhankar", "Dr V R Bhagwat", "Dr M K Naik", "Dr Prakash P Shastry", "Mr Satish Parsai",
        "Dr Madhuban Gopal", "Mr J Kannaiyan", "Dr M Mani", "Dr Chirantan Chattopadhyay", "Dr P V Krishnayya",
        "Dr D Jagadishwar Reddy", "Dr K K Pandey", "Prof S V Sarode", "Prof A Regupathy", "Dr B K Mishra",
        "Dr Ashok Krishna", "Dr H P Mishra", "Dr (Mrs) Saxena", "Mr V Ambethgar"
    ]),
    ("2003", ["Dr U Sreedhar", "Dr Prem Raj Gupta", "Dr Kanchan Baral", "Dr B K Sahoo", "Dr Rajgopal"]),
    ("2005", ["Dr M A Raoof", "Dr V B Nargund", "Dr Gururaj Katti", "Dr Asif Tanweer", "Dr P Nagaraja Rao"]),
    ("2006", ["Dr S Desai", "Dr Subrata Satpathy", "Dr P Sreerama Kumar", "Dr Ladu Kishore Rath", "Dr Anitha Kodaru"]),
    ("2010", [
        "Dr A Rajareddy", "Dr Satya Vir", "Dr V Ramesh Babu", "Dr RW Alexander Jesudasan", "Dr S Manickavasagam",
        "Dr V Jayalakshmi", "Dr Yashoda R Hegde", "Dr Pankaj Sharma", "Prof Ram Singh", "Dr V Selvanarayanan",
        "Dr Rajesh Pratap Singh", "Dr S Jeyarani", "Dr R Velazhahan", "Dr PS Vimaladevi", "Dr Mukesh K Dhillon",
        "Dr J Jayakumar", "Dr Abhishek Shukla", "Dr T V K Singh"
    ]),
    ("2012", [
        "Dr T S K Patro", "Dr P C Rath", "Dr P D Meena", "Dr Kavita Gupta", "Dr S R Pandravada",
        "Dr B Sree laxmi", "Dr T Saravanan", "Dr G Shyam Prasad", "Dr P G Padmaja", "Dr Chandish R Ballal",
        "Dr G M V Prasad", "Dr Dewa Ram Bajya", "Dr S Ramakrishnan", "Dr N Somasekhar", "Dr Arjun Lal",
        "Dr A P Padma Kumari", "Dr M Prabhakar", "Dr P K Behera", "Dr Sashi Bhalla", "Dr V Kamala"
    ]),
    ("2016", [
        "Dr V Lakshminarayanamma", "Dr Ch Padmavathi", "Dr Bharati N Bhat", "Dr K Shankarganesh", "Dr M Rajasri",
        "Dr R Jagadeeshwar", "Dr G Sridevi", "Dr K Karthikeyal", "Dr M Visalakshmi", "Dr B Bhavani",
        "Ashish Kumar Tripathi", "Dr Aravindnath Singh", "Dr D Karthikeyan", "Dr T V Prasad", "Dr K Rameash"
    ]),
    ("2017 – 2023", [
        "Dr Srinivas Parimi", "Dr C Alice Retna Packia Sujeetha", "Dr M Srinivas Prasad", "Dr Suresh Kumar Khinchi",
        "Dr A Muthu Kumar", "Dr Jameel Akhtar", "Dr M Alagar", "Dr K P Manju", "Dr V Prakasam",
        "Dr R Maruthadurai", "Dr Pardeep Kumar", "Dr D Ladhalakshmi", "Dr Prasanna Holajjer",
        "Dr Veghra Durga Prasad Rao Nimmakayala", "Dr L Saravanan", "Dr M Punithavalli", "Dr B S Gotyal",
        "Dr K Selvaraj", "Dr Kuldeep Singh Jadon", "Dr P Duraimurugan", "Dr Issai Aruna Sri", "Dr V Jhansi Lakshmi",
        "Dr Kiran Babu Talluri", "Dr Satish Kumar Sain", "Dr SVS Gopala Swamy", "Dr Girish Anantrao Gunjotikar",
        "Dr K Vemana", "Dr MH Kodandaram", "Dr Bonthagorla Subbarayudu", "Dr J Gulsar Banu", "Dr M Visalakshi",
        "Dr D Krishnaveni", "Dr S Subramanian", "Dr MK Jyosthna", "Dr D Anitha Kumari"
    ])
]

fellows_list = []
for year, names in fellows_raw:
    for name in names:
        fellows_list.append({"year": year, "name": name})

print(f"Total fellows: {len(fellows_list)}")
