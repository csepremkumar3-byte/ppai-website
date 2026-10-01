import json

html_template = """{% extends "base.html" %}

{% block title %}PPAI Society Awards — Plant Protection Association of India{% endblock %}

{% block extra_css %}
<style>
  /* ===================================================================
     PPAI SOCIETY AWARDS - SPLIT-PANEL AWARDS PORTAL
  =================================================================== */
  .awards-page-section {
    min-height: calc(100vh - 70px);
    box-sizing: border-box;
    max-width: 1280px;
    margin: 0 auto;
    padding: clamp(24px, 3vh, 36px) clamp(20px, 3.5vw, 48px) clamp(70px, 9vh, 110px) clamp(20px, 3.5vw, 48px);
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }

  .awards-page-titlebar {
    margin-bottom: clamp(16px, 2.2vh, 22px);
  }

  .awards-page-titlebar h1 {
    font-size: clamp(22px, 1.8vw, 28px);
    font-weight: 800;
    color: var(--deep-forest);
    margin: 0;
    letter-spacing: -0.02em;
  }

  /* Main Split-Panel Card */
  .awards-portal-container {
    background: #ffffff;
    border: 1px solid var(--border-color);
    border-radius: 14px;
    box-shadow: 0 4px 18px rgba(11, 36, 23, 0.05);
    display: grid;
    grid-template-columns: 340px 1fr;
    min-height: 480px;
    overflow: hidden;
  }

  /* Left Sidebar: Categories List */
  .awards-sidebar {
    background: #fbfdfc;
    border-right: 1px solid #e2ece5;
    display: flex;
    flex-direction: column;
  }

  .award-nav-item {
    padding: 16px 20px;
    border-bottom: 1px solid #eef4f0;
    cursor: pointer;
    position: relative;
    transition: all 0.18s ease;
    background: transparent;
    text-align: left;
    border-left: 4px solid transparent;
  }

  .award-nav-item:hover {
    background: #f2f8f4;
  }

  .award-nav-item.active {
    background: #eef7f1;
    border-left-color: #059669;
  }

  .award-nav-title {
    font-size: clamp(13.5px, 0.92vw, 15px);
    font-weight: 700;
    color: var(--deep-forest);
    margin: 0;
    line-height: 1.35;
  }

  /* Right Panel: Content Area */
  .awards-content-panel {
    padding: clamp(20px, 2.5vw, 28px);
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
    background: #ffffff;
    overflow-y: auto;
  }

  .panel-header-title {
    font-size: clamp(18px, 1.35vw, 22px);
    font-weight: 800;
    color: var(--deep-forest);
    margin: 0 0 12px 0;
    line-height: 1.3;
  }

  /* Award Description Box */
  .award-description-card {
    background: #f4f9f6;
    border: 1px solid #d2e6dc;
    border-left: 4px solid #059669;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 14px;
  }

  .award-description-card h3 {
    font-size: 13px;
    font-weight: 800;
    color: var(--deep-forest);
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin: 0 0 6px 0;
  }

  .award-description-card p {
    font-size: 13.5px;
    color: #2c4235;
    line-height: 1.55;
    margin: 0;
  }

  /* Era Filter Bar */
  .era-filter-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
    margin-bottom: 14px;
  }

  .era-filter-btn {
    appearance: none;
    background: #f4faf6;
    border: 1px solid #cce2d6;
    color: #1e3a29;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 12.5px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.15s ease;
    outline: none;
  }

  .era-filter-btn:hover {
    background: #e6f4ec;
    border-color: #059669;
    color: #059669;
  }

  .era-filter-btn.active {
    background: #059669;
    border-color: #059669;
    color: #ffffff;
    box-shadow: 0 2px 6px rgba(5, 150, 105, 0.25);
  }

  /* Recipients Section */
  .recipients-section-title {
    font-size: 15.5px;
    font-weight: 800;
    color: var(--deep-forest);
    margin: 0 0 10px 0;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .recipients-section-title .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #059669;
    display: inline-block;
  }

  /* Awardees List Container - Sized for 4-6 rows with clean internal scrolling */
  .awardees-list-container {
    border: 1px solid #d5e5dc;
    border-radius: 8px;
    overflow-y: auto;
    max-height: 295px;
    background: #ffffff;
    box-shadow: 0 1px 3px rgba(11, 36, 23, 0.04);
    scrollbar-width: thin;
    scrollbar-color: #8bbfa3 #f0f6f2;
  }

  .awardees-list-container::-webkit-scrollbar {
    width: 6px;
  }

  .awardees-list-container::-webkit-scrollbar-track {
    background: #f0f6f2;
    border-radius: 4px;
  }

  .awardees-list-container::-webkit-scrollbar-thumb {
    background: #8bbfa3;
    border-radius: 4px;
  }

  .awardees-list-container::-webkit-scrollbar-thumb:hover {
    background: #059669;
  }

  .awardee-row-item {
    display: grid;
    grid-template-columns: 145px 1fr;
    padding: 12px 18px;
    border-bottom: 1px solid #edf4f0;
    align-items: center;
    transition: background-color 0.15s ease;
  }

  .awardee-row-item:last-child {
    border-bottom: none;
  }

  .awardee-row-item:hover {
    background: #f4faf6;
  }

  .awardee-year {
    font-weight: 800;
    color: #059669;
    font-size: 14px;
    letter-spacing: 0.02em;
    line-height: 1.4;
  }

  .awardee-name {
    font-size: 14px;
    font-weight: 700;
    color: var(--deep-forest);
    line-height: 1.45;
  }

  .awardee-details {
    font-size: 12.5px;
    color: #4a6354;
    font-weight: 500;
    margin-top: 3px;
    line-height: 1.4;
  }

  /* Responsive Media Queries */
  @media (max-width: 900px) {
    .awards-portal-container {
      grid-template-columns: 1fr;
    }
    .awards-sidebar {
      border-right: none;
      border-bottom: 1px solid #e2ece5;
      max-height: 220px;
      overflow-y: auto;
    }
  }

  @media (max-width: 600px) {
    .awardee-row-item {
      grid-template-columns: 1fr;
      gap: 4px;
    }
    .awards-content-panel {
      padding: 16px 12px;
    }
  }
</style>
{% endblock %}

{% block content %}
<section class="awards-page-section">
  <!-- Title Bar -->
  <div class="awards-page-titlebar">
    <h1>PPAI Society Awards</h1>
  </div>

  <!-- Interactive Portal Card -->
  <div class="awards-portal-container">
    
    <!-- Left Category Navigation Sidebar -->
    <div class="awards-sidebar" id="awardsSidebar">
      <!-- Generated dynamically by JS -->
    </div>

    <!-- Right Content Area -->
    <div class="awards-content-panel">
      <h2 class="panel-header-title" id="panelAwardTitle">Award Title</h2>
      
      <!-- Award Description & Background from Document -->
      <div class="award-description-card">
        <h3>About the Award</h3>
        <p id="panelAwardDesc">Award Description</p>
      </div>

      <!-- Era Filter Pills -->
      <div class="era-filter-bar">
        <button class="era-filter-btn active" data-era="all">All</button>
        <button class="era-filter-btn" data-era="upto-2000">Up to 2000</button>
        <button class="era-filter-btn" data-era="2001-2010">2001 – 2010</button>
        <button class="era-filter-btn" data-era="2011-2023">2011 – 2023</button>
      </div>

      <!-- Recipients Section -->
      <div>
        <h3 class="recipients-section-title">
          <span class="dot"></span>
          Recipients
        </h3>

        <!-- Awardees List -->
        <div class="awardees-list-container" id="awardeesListContainer">
          <!-- Rendered dynamically by JS -->
        </div>
      </div>
    </div>

  </div>
</section>

<script>
  // Complete Dataset from the Official Golden Jubilee Souvenir Document
  const awardsDataset = DATASET_PLACEHOLDER;

  let currentCategoryIndex = 0;
  let activeEraFilter = "all";

  const sidebarEl = document.getElementById("awardsSidebar");
  const titleEl = document.getElementById("panelAwardTitle");
  const descEl = document.getElementById("panelAwardDesc");
  const listContainerEl = document.getElementById("awardeesListContainer");

  function renderSidebar() {
    sidebarEl.innerHTML = awardsDataset.map((cat, idx) => `
      <div class="award-nav-item ${idx === currentCategoryIndex ? 'active' : ''}" data-index="${idx}">
        <h3 class="award-nav-title">${cat.title}</h3>
      </div>
    `).join('');

    sidebarEl.querySelectorAll(".award-nav-item").forEach(item => {
      item.addEventListener("click", () => {
        currentCategoryIndex = parseInt(item.dataset.index);
        renderSidebar();
        renderContent();
      });
    });
  }

  function filterByEra(item) {
    if (activeEraFilter === "all") return true;

    if (item.year.includes("Before 2003")) {
      return activeEraFilter === "upto-2000";
    }

    const matches = item.year.match(/\\d{4}/g);
    if (!matches || matches.length === 0) return true;

    const startYear = parseInt(matches[0]);
    const endYear = matches.length > 1 ? parseInt(matches[1]) : startYear;

    if (activeEraFilter === "upto-2000") {
      return startYear <= 2000;
    } else if (activeEraFilter === "2001-2010") {
      return (startYear >= 2001 && startYear <= 2010) || (endYear >= 2001 && endYear <= 2010) || (startYear <= 2001 && endYear >= 2010);
    } else if (activeEraFilter === "2011-2023") {
      return (startYear >= 2011 && startYear <= 2023) || (endYear >= 2011 && endYear <= 2023) || (startYear <= 2011 && endYear >= 2023);
    }
    return true;
  }

  function renderContent() {
    const category = awardsDataset[currentCategoryIndex];
    titleEl.textContent = category.title;
    descEl.textContent = category.desc;

    const filtered = category.awardees.filter(filterByEra);

    if (filtered.length === 0) {
      listContainerEl.innerHTML = `
        <div style="padding: 32px 20px; text-align: center; color: var(--text-muted); font-size: 13.5px;">
          No recipient records found for the selected period.
        </div>
      `;
      return;
    }

    listContainerEl.innerHTML = filtered.map(item => `
      <div class="awardee-row-item">
        <div class="awardee-year">${item.year}</div>
        <div>
          <div class="awardee-name">${item.name}</div>
          ${item.details ? `<div class="awardee-details">${item.details}</div>` : ''}
        </div>
      </div>
    `).join('');

    // Reset scroll to top
    listContainerEl.scrollTop = 0;
  }

  // Setup Era Filter Buttons
  document.querySelectorAll(".era-filter-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".era-filter-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      activeEraFilter = btn.dataset.era;
      renderContent();
    });
  });

  // Init
  renderSidebar();
  renderContent();
</script>
{% endblock %}
"""

# Now build the full dataset
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

fellows_awardees = []
for yr, names in fellows_raw:
    for nm in names:
        fellows_awardees.append({"year": yr, "name": nm})

recognition_raw = [
    ("Lifetime Contribution Award", [
        "Dr Dodla V Raghava Reddy", "Dr V Raghunathan", "Dr P S Chandurkar",
        "Dr K S Varaprasad", "Dr K Krishnaiah", "Dr KSRK Murthy", "Dr B Sarath Babu"
    ]),
    ("Outstanding Contribution Award", [
        "Dr M Veera Bhadra Rao", "Dr B Julius Divakar", "Dr T B Gour",
        "Dr Rajan Sharma", "Dr T Ramesh Babu", "Dr Anitha Kodaru"
    ]),
    ("Recognition Award", [
        "Dr B Govinda Naik", "Dr Renu Sharma", "Dr S K Chakrabarty", "Dr R Jagadeeshwar",
        "Dr B Parameswari", "Dr R K Khetarpal", "Dr Harvir Singh", "Dr Gururaj Katti",
        "Dr A Raja Reddy", "Dr V Celia Chalam", "Dr M Srinivas Prasad", "Dr H C Sharma",
        "Dr L Saravanan", "Dr K M Azam", "Dr S Sithanantham", "Dr C Pramod Chandra Kumar",
        "Dr G Sreedevi", "Dr Prasanna Holajjer", "Dr Bhaskar Bajaru"
    ]),
    ("Award of Distinction", [
        "Dr S N Puri", "Dr C D Mayee", "Dr Chelliah", "Dr Anupam Varma", "Dr A K Dhawan",
        "Dr A N Mukhopadhyay", "Dr Srikant Kulkarni", "Dr J S Prasad", "Dr H S Gaur"
    ]),
    ("Special Award", ["Dr S N Sushil", "Dr J P Singh"]),
    ("Posthumous Award", ["Mr Vinod Kumar Samanthula"])
]

recognition_awardees = []
for category_title, names in recognition_raw:
    for nm in names:
        recognition_awardees.append({
            "year": "1972 – 2022",
            "name": nm,
            "details": category_title
        })

dataset = [
    {
      "id": "dodla-raghava-reddy",
      "title": "Dodla Raghava Reddy Memorial Gold Medal Award",
      "desc": "This award was instituted by Dr D V R Reddy, former President of PPAI and former Principal Scientist and Leader of Virology, International Crops Research Institute for the Semi-Arid Tropics (ICRISAT) in the year 1983 in memory of his late father Shri Dodla Raghava Reddy for outstanding contributions in the field of Plant Protection. The award is given to Indian citizens once in three years constituting a gold medal and a certificate from interest accrued from a fund of ₹3,00,000/- (Rupees three lakhs only).",
      "awardees": [
        { "year": "1997", "name": "Dr A Appa Rao" },
        { "year": "2006 – 2008", "name": "Dr C D Mayee" },
        { "year": "2008 – 2010", "name": "Dr K S Varaprasad" },
        { "year": "2010 – 2012", "name": "Dr T Ramesh Babu" },
        { "year": "2014 – 2016", "name": "Dr P Anand Kumar" },
        { "year": "2016 – 2018", "name": "Dr A G Sreenivas" },
        { "year": "2018 – 2020", "name": "Dr M Srinivasa Rao" },
        { "year": "2020 – 2022", "name": "Dr Basava Prabhu Patil" }
      ]
    },
    {
      "id": "dr-d-bap-reddy",
      "title": "Dr. Bap Reddy Award for Integrated Pest Management",
      "desc": "Dr Bap Reddy, an eminent scientist who contributed immensely for pest management in India and Asia Pacific for nearly 40 years and retired as FAO representative after serving the United Nations for two years, donated ₹15,000/- over three decades ago for instituting this award. The interest accrued from this amount is given as an award once in two years. The award constitutes a plaque, a certificate and cash. The purpose of the award is to promote the concept of Integrated Pest Management (IPM).",
      "awardees": [
        { "year": "1986 – 1988", "name": "Dr K Krishnaiah" },
        { "year": "1988 – 1990", "name": "Dr A D Pawar" },
        { "year": "1990 – 1992", "name": "Dr S Uthamasamy" },
        { "year": "1992 – 1994", "name": "Dr T M Manjunath" },
        { "year": "1994 – 1996", "name": "Dr V Muniappa" },
        { "year": "1998 – 2000", "name": "Dr H C Sharma" },
        { "year": "2000 – 2002", "name": "Dr I C Pasalu and Team" },
        { "year": "2002 – 2004", "name": "Dr B Srinivasulu" },
        { "year": "2006 – 2008", "name": "Dr N P Eswar Reddy" },
        { "year": "2008 – 2010", "name": "Dr S Suresh" },
        { "year": "2010 – 2012", "name": "Dr Y G Prasad" },
        { "year": "2014 – 2016", "name": "Dr U Sreedhar" },
        { "year": "2016 – 2018", "name": "Dr S Vennila" },
        { "year": "2018 – 2020", "name": "Dr Jameel Akthar" },
        { "year": "2020 – 2022", "name": "Dr NBV Chalapathi Rao" }
      ]
    },
    {
      "id": "fellows-fppai",
      "title": "Fellows of Plant Protection Association of India (FPPAI)",
      "desc": "Fellowship is conferred on distinguished individuals and scientists having completed five years of continuous membership in the Plant Protection Association of India in recognition of their valuable service and contributions to the cause of plant protection.",
      "awardees": fellows_awardees
    },
    {
      "id": "kavuri-sarada",
      "title": "Smt. Kavuri Sarada Memorial Award",
      "desc": "Candidates are not required to send proposals for this award as the screening committee appointed by Plant Protection Association of India chooses the Best Research Papers published in the Indian Journal of Plant Protection every year. The award consists of a certificate to each of the authors of the chosen research paper.",
      "awardees": [
        { "year": "1988", "name": "Dr K Abbaiah and Dr M Sugunakara Reddy" },
        { "year": "1989", "name": "Dr D V Singh, Dr P Arora, Dr K D Srivastava, Dr S Nagarajan and Dr R Agarwal" },
        { "year": "1992 – 1993", "name": "Dr M Veerabhadra Rao" },
        { "year": "1993 – 1994", "name": "Dr C Pramod Chandra Kumar" },
        { "year": "1994 – 1995", "name": "Dr B J Divakar, Dr P V Sharma, Dr V Raghunathan, Dr B V David, Dr G R S Reddy and Sri S V Swamy" },
        { "year": "1995 – 1996", "name": "Dr P P Shastry" },
        { "year": "1996 – 1997", "name": "Dr T P Sriharan" },
        { "year": "2001", "name": "Dr V Markandeya, Dr V Vasu, Dr PS Chandurkar, Dr T Rangarajan and Dr B J Divakar" },
        { "year": "2002", "name": "Dr M Mani and Dr A Krishnamoorthy" },
        { "year": "2004", "name": "Dr T K S Latha" },
        { "year": "2007", "name": "Satya Vir (2007)", "details": "Neem Genetic Diversity in India and its Use as Biopesticide and Biofertilizer (IJPP Vol. 35)" },
        { "year": "2008", "name": "V Ramesh Babu (2008)", "details": "F2 Screen Estimation of Alleles Population of Diamondback Moth (Plutella xylostella Linn.) (IJPP Vol. 36)" },
        { "year": "2010", "name": "V Manoj Kumar (2010)", "details": "Management economics of foot and stem rot of mesta incited by Phytophthora parasitica (IJPP Vol. 38)" },
        { "year": "2011", "name": "N Ramakrishnan (2011)", "details": "Standardization of X-Ray Radiography Methodology for the detection of hidden infestation in cereals (IJPP Vol. 39)" },
        { "year": "2012", "name": "Ratna Bhimineni" },
        { "year": "2013", "name": "P A Ahila Devi & V Prakasam (2013)", "details": "RAPD-based Genetic Variation among Colletotrichum Isolates causing Chilli Anthracnose (IJPP 41(3): 244-248)" },
        { "year": "2014", "name": "A Kandan, J Akhtar, B Singh, U Dev, R Goley, D Chand, A Roy, S Rajkumar, and P C Agarwal (2014)", "details": "Genetic diversity analysis of Alternaria alternata isolates infecting different crops using URP and ISSR markers (IJPP 42 (3): 229-236)" },
        { "year": "2015", "name": "D Balakrishna, K Srinivasa Babu, B Venkatesh Bhat, R Vinod, M Sreedhar, G Shyamprasad, D B Pawar, Shekharappa, M O Mohammed Ilyas and J V Patil (2015)", "details": "Improved shoot fly resistant sources by gamma irradiation induced mutation in sorghum (IJPP Vol 43 (4))" },
        { "year": "2016", "name": "K Susheela and N Sathyanarayana (2016)", "details": "Weed risk assessment of Ambrosia psilostachya for its invasiveness and potential endangered areas in India (IJPP Vol 44 (1))" },
        { "year": "2019", "name": "Isha Sharma, Mohinder Singh and P L Sharma", "details": "Efficacy of indigenous strains of entomopathogenic nematodes against white grub Brahmina coriacea (IJPP Vol. 47 No. 1&2, 21-28)" },
        { "year": "2019", "name": "S Vijay Kumar, M Srinivas Prasad, R Rambabu, B Bhaskar, R M Sundaram, V Prakasam, D Ladhalakshmi, G S Laha and M Sheshu Madhav", "details": "Marker assisted introgression of broad spectrum blast resistance gene Pi-2 into Samba Mahsuri (IJPP Vol. 47 No. 3&4, 154-163)" },
        { "year": "2020", "name": "E Sree Latha, S Jesurajan and Ch. Sreenivasa Rao", "details": "Ecological engineering in gourds and melons (Cucurbitaceae) for pest management and beneficial insects (IJPP Vol. 48 No. 3, 190-196)" },
        { "year": "2020", "name": "Shambhu Singh, A K Dave, D Padhee and Aman", "details": "Design and development of a mono wheel operated sprayer cum weeder (IJPP Vol. 48 No. 4, 296-300)" },
        { "year": "2021", "name": "B Sai Sushma, B Vidya Sagar, S Triveni, G Uma Devi", "details": "Isolation, characterization of endophytic bacteria against early blight of tomato (IJPP Vol. 49 No. 1, 40-53)" },
        { "year": "2021", "name": "K Selvaraj and B V Sumalatha", "details": "Increasing distribution, biology and population dynamics of invasive woolly whitefly on guava (IJPP Vol. 49 No. 4, 227-232)" },
        { "year": "2022", "name": "Prasanna Holajjer, Bharat H Gawade, Z Khan and N Sivaraj", "details": "Prediction of potential geographic distribution of exotic nematode in India based on MaxEnt (IJPP Vol. 50 No. 1, 51-55)" },
        { "year": "2022", "name": "C D Mayee, B Chaudhary, R Panchbhai, A R Annepu and R D Kapur", "details": "Mega-field demonstration of management of pink bollworm in rain-fed cotton using mating disruption technology (IJPP Vol. 50 No. 4, 115-119)" }
      ]
    },
    {
      "id": "dr-rdvj-prasada-rao",
      "title": "Dr. R D V J Prasada Rao Award",
      "desc": "Instituted to recognize outstanding research and meritorious service in the specialized fields of Plant Virology and Plant Quarantine.",
      "awardees": [
        { "year": "2012", "name": "Dr V Celia Chalam", "details": "Division of Plant Quarantine, ICAR-NBPGR, New Delhi" },
        { "year": "2016", "name": "Dr Kavita Gupta", "details": "ICAR-National Bureau of Plant Genetic Resources, New Delhi" }
      ]
    },
    {
      "id": "best-scientist-awards",
      "title": "Best Scientist Awards",
      "desc": "The Best Scientist Awards in Young (<=40 years) and Senior (40-60 years) Category were instituted by PPAI starting from the year 2023 marking the occasion of the Golden Jubilee Celebrations. The awards are given biannually to individuals in recognition of professional contributions in Entomology, Plant Pathology, Nematology, and Digital Agriculture.",
      "awardees": [
        { "year": "2023", "name": "Dr Shravan M Haldhar", "details": "Senior Category in Entomology" },
        { "year": "2023", "name": "Dr K Selvaraj", "details": "Senior Category in Entomology" },
        { "year": "2023", "name": "Dr V Bhuvaneswari", "details": "Senior Category in Plant Pathology" },
        { "year": "2023", "name": "Dr N Somasekhar", "details": "Senior Category in Nematology" },
        { "year": "2023", "name": "Dr Gadratagi Basana Gowda", "details": "Young Category in Entomology" },
        { "year": "2023", "name": "Dr K Sakthivel", "details": "Young Category in Plant Pathology" },
        { "year": "2023", "name": "Dr Satish N Chavan", "details": "Young Category in Nematology" },
        { "year": "2023", "name": "Dr Srikanth Rupavathara", "details": "Digital Agriculture" }
      ]
    },
    {
      "id": "recognition-awards",
      "title": "Recognition & Distinction Awards",
      "desc": "Conferred during the Golden Jubilee ICPHM 2023 for Lifetime Contribution, Outstanding Services, Golden Jubilee Recognition, Award of Distinction, Special Awards, and Posthumous Awards rendered during 1972–2022.",
      "awardees": recognition_awardees
    }
]

final_html = html_template.replace("DATASET_PLACEHOLDER", json.dumps(dataset, indent=2))

with open("templates/pages/awards.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("templates/pages/awards.html written successfully!")
