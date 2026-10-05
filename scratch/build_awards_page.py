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
    padding: clamp(12px, 1.8vh, 20px) clamp(16px, 3vw, 36px) clamp(24px, 3.5vh, 38px) clamp(16px, 3vw, 36px);
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }

  .awards-page-titlebar {
    margin-bottom: clamp(8px, 1.2vh, 14px);
    flex-shrink: 0;
  }

  .awards-page-titlebar h1 {
    font-size: clamp(20px, 1.7vw, 26px);
    font-weight: 800;
    color: var(--deep-forest);
    margin: 0;
    letter-spacing: -0.02em;
  }

  /* Main Split-Panel Card - Scales smoothly from small (768p) to large (1080p+) desktops */
  .awards-portal-container {
    background: #ffffff;
    border: 1px solid var(--border-color);
    border-radius: 12px;
    box-shadow: 0 4px 18px rgba(11, 36, 23, 0.05);
    display: grid;
    grid-template-columns: clamp(270px, 25vw, 330px) 1fr;
    height: clamp(480px, calc(100vh - 185px), 640px);
    overflow: hidden;
    flex-shrink: 0;
  }

  /* Left Sidebar: Categories List */
  .awards-sidebar {
    background: #fbfdfc;
    border-right: 1px solid #e2ece5;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
  }

  .award-nav-item {
    padding: clamp(12px, 1.4vh, 15px) clamp(14px, 1.4vw, 18px);
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

  .award-nav-item.active .award-nav-title {
    color: #047857;
    font-weight: 800;
  }

  .award-nav-title {
    font-size: clamp(13.5px, 0.9vw, 14.5px);
    font-weight: 700;
    color: var(--deep-forest);
    margin: 0;
    line-height: 1.35;
  }

  /* Right Panel: Content Area */
  .awards-content-panel {
    padding: clamp(14px, 1.8vw, 22px);
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
    background: #ffffff;
    overflow: hidden;
  }

  /* Award Description Box with Justified Text */
  .award-description-card {
    background: #f4f9f6;
    border: 1px solid #d2e6dc;
    border-left: 4px solid #059669;
    border-radius: 8px;
    padding: clamp(10px, 1.3vh, 14px) clamp(14px, 1.4vw, 18px);
    margin-bottom: clamp(10px, 1.3vh, 14px);
    flex-shrink: 0;
  }

  .award-description-card h3 {
    font-size: clamp(13.5px, 0.9vw, 14.5px);
    font-weight: 800;
    color: #065f46;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin: 0 0 6px 0;
  }

  .award-description-card p {
    font-size: clamp(13.5px, 0.9vw, 14.5px);
    color: #1e3328;
    line-height: 1.6;
    text-align: justify;
    text-justify: inter-word;
    margin: 0;
  }

  /* Recipients Section Wrapper */
  .recipients-wrapper {
    display: flex;
    flex-direction: column;
    flex: 1 1 auto;
    min-height: 0;
    overflow: hidden;
  }

  .recipients-section-title {
    font-size: clamp(14.5px, 1vw, 16px);
    font-weight: 800;
    color: var(--deep-forest);
    margin: 0 0 8px 0;
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
  }

  .recipients-section-title .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #059669;
    display: inline-block;
  }

  /* Awardees List Container (Table Layout - Scrollable inside) */
  .awardees-list-container {
    border: 1px solid #d5e5dc;
    border-radius: 8px;
    overflow-y: auto;
    flex: 1 1 auto;
    min-height: 0;
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

  /* Group Row: Year on Left, 4-column Table on Right */
  .awardee-group-row {
    display: grid;
    grid-template-columns: clamp(110px, 12vw, 140px) 1fr;
    border-bottom: 1px solid #dce8e1;
    background: #ffffff;
  }

  .awardee-group-row:last-child {
    border-bottom: none;
  }

  .awardee-group-year {
    background: #f8fbf9;
    border-right: 1px solid #dce8e1;
    padding: 8px 12px;
    font-weight: 700;
    color: #047857;
    font-size: 12.5px;
    letter-spacing: 0.01em;
    display: flex;
    align-items: flex-start;
    user-select: none;
  }

  .awardee-names-table {
    display: flex;
    flex-direction: column;
  }

  .awardee-names-row {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    min-height: 36px;
    border-bottom: 1px solid #edf4f0;
    transition: background-color 0.12s ease;
  }

  .awardee-names-row:last-child {
    border-bottom: none;
  }

  .awardee-names-row:hover {
    background-color: #f5faf7;
  }

  .awardee-cell {
    padding: 7px 10px;
    font-size: 12px;
    color: #1e3328;
    font-weight: 600;
    line-height: 1.35;
    overflow-wrap: break-word;
    word-break: normal;
    display: flex;
    align-items: center;
    min-height: 36px;
    box-sizing: border-box;
  }

  /* Responsive Media Queries for Tablets and Small Screens */
  @media (max-width: 900px) {
    .awards-page-section {
      min-height: auto;
      padding-bottom: 40px;
    }
    .awards-portal-container {
      grid-template-columns: 1fr;
      min-height: auto;
    }
    .awards-sidebar {
      border-right: none;
      border-bottom: 1px solid #e2ece5;
      flex-direction: row;
      overflow-x: auto;
      white-space: nowrap;
      padding: 8px;
      gap: 6px;
    }
    .award-nav-item {
      border-left: none;
      border-bottom: 3px solid transparent;
      border-radius: 6px;
      padding: 9px 14px;
      flex: 0 0 auto;
    }
    .award-nav-item.active {
      border-bottom-color: #059669;
      border-left-color: transparent;
      background: #edf7f2;
    }
    .awardee-names-row {
      grid-template-columns: repeat(2, 1fr);
    }
    .awardees-list-container {
      max-height: 360px;
    }
  }

  @media (max-width: 600px) {
    .awardee-group-row {
      grid-template-columns: 1fr;
    }
    .awardee-group-year {
      border-right: none;
      border-bottom: 1px solid #dce8e1;
      background: #eef7f1;
      padding: 6px 10px;
    }
    .awardee-names-row {
      grid-template-columns: 1fr;
    }
    .awards-content-panel {
      padding: 14px 12px;
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
      
      <!-- Award Description Box with Justification -->
      <div class="award-description-card" id="awardDescCard">
        <h3>About the Award</h3>
        <p id="panelAwardDesc"></p>
      </div>

      <!-- Recipients Section -->
      <div class="recipients-wrapper">
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

  const sidebarEl = document.getElementById("awardsSidebar");
  const descCardEl = document.getElementById("awardDescCard");
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

  function renderContent() {
    const category = awardsDataset[currentCategoryIndex];
    
    // Update description text
    if (category.desc) {
      descEl.textContent = category.desc;
      descCardEl.style.display = "block";
    } else {
      descCardEl.style.display = "none";
    }

    const groups = category.groups || [];

    if (groups.length === 0) {
      listContainerEl.innerHTML = `
        <div style="padding: 28px 20px; text-align: center; color: var(--text-muted); font-size: 13px;">
          No recipient records found.
        </div>
      `;
      return;
    }

    listContainerEl.innerHTML = groups.map(group => {
      // Divide names into rows of 4
      const rows = [];
      for (let i = 0; i < group.names.length; i += 4) {
        rows.push(group.names.slice(i, i + 4));
      }
      
      const rowsHtml = rows.map(rowNames => {
        const cellsHtml = rowNames.map(name => `<div class="awardee-cell">${name}</div>`).join('');
        return `<div class="awardee-names-row">${cellsHtml}</div>`;
      }).join('');

      return `
        <div class="awardee-group-row">
          <div class="awardee-group-year">${group.year}</div>
          <div class="awardee-names-table">
            ${rowsHtml}
          </div>
        </div>
      `;
    }).join('');

    // Reset scroll to top
    listContainerEl.scrollTop = 0;
  }

  // Init
  renderSidebar();
  renderContent();
</script>
{% endblock %}
"""

# Complete structured datasets
dataset = [
    {
      "id": "dodla-raghava-reddy",
      "title": "Dodla Raghava Reddy Memorial Gold Medal Award",
      "desc": "This award was instituted by Dr D V R Reddy, former President of PPAI and former Principal Scientist and Leader of Virology, International Crops Research Institute for the Semi-Arid Tropics (ICRISAT) in the year 1983 in memory of his late father Shri Dodla Raghava Reddy for outstanding contributions in the field of Plant Protection. The award is given to Indian citizens once in three years constituting a gold medal and a certificate from interest accrued from a fund of ₹3,00,000/- (Rupees three lakhs only).",
      "groups": [
        { "year": "1997", "names": ["Dr A Appa Rao"] },
        { "year": "2006 – 2008", "names": ["Dr C D Mayee"] },
        { "year": "2008 – 2010", "names": ["Dr K S Varaprasad"] },
        { "year": "2010 – 2012", "names": ["Dr T Ramesh Babu"] },
        { "year": "2014 – 2016", "names": ["Dr P Anand Kumar"] },
        { "year": "2016 – 2018", "names": ["Dr A G Sreenivas"] },
        { "year": "2018 – 2020", "names": ["Dr M Srinivasa Rao"] },
        { "year": "2020 – 2022", "names": ["Dr Basava Prabhu Patil"] }
      ]
    },
    {
      "id": "dr-d-bap-reddy",
      "title": "Dr. Bap Reddy Award for Integrated Pest Management",
      "desc": "Dr Bap Reddy, an eminent scientist who contributed immensely for pest management in India and Asia Pacific for nearly 40 years and retired as FAO representative after serving the United Nations for two years, donated ₹15,000/- over three decades ago for instituting this award. The interest accrued from this amount is given as an award once in two years. The award constitutes a plaque, a certificate and cash. The purpose of the award is to promote the concept of Integrated Pest Management (IPM).",
      "groups": [
        { "year": "1986 – 1988", "names": ["Dr K Krishnaiah"] },
        { "year": "1988 – 1990", "names": ["Dr A D Pawar"] },
        { "year": "1990 – 1992", "names": ["Dr S Uthamasamy"] },
        { "year": "1992 – 1994", "names": ["Dr T M Manjunath"] },
        { "year": "1994 – 1996", "names": ["Dr V Muniappa"] },
        { "year": "1998 – 2000", "names": ["Dr H C Sharma"] },
        { "year": "2000 – 2002", "names": ["Dr I C Pasalu and Team"] },
        { "year": "2002 – 2004", "names": ["Dr B Srinivasulu"] },
        { "year": "2006 – 2008", "names": ["Dr N P Eswar Reddy"] },
        { "year": "2008 – 2010", "names": ["Dr S Suresh"] },
        { "year": "2010 – 2012", "names": ["Dr Y G Prasad"] },
        { "year": "2014 – 2016", "names": ["Dr U Sreedhar"] },
        { "year": "2016 – 2018", "names": ["Dr S Vennila"] },
        { "year": "2018 – 2020", "names": ["Dr Jameel Akthar"] },
        { "year": "2020 – 2022", "names": ["Dr NBV Chalapathi Rao"] }
      ]
    },
    {
      "id": "fellows-fppai",
      "title": "Fellows of Plant Protection Association of India (FPPAI)",
      "desc": "Fellowship is conferred on distinguished individuals and scientists having completed five years of continuous membership in the Plant Protection Association of India in recognition of their valuable service and contributions to the cause of plant protection.",
      "groups": [
        {
          "year": "1972 – 2003",
          "names": [
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
          ]
        },
        {
          "year": "2003",
          "names": ["Dr U Sreedhar", "Dr Prem Raj Gupta", "Dr Kanchan Baral", "Dr B K Sahoo", "Dr Rajgopal"]
        },
        {
          "year": "2005",
          "names": ["Dr M A Raoof", "Dr V B Nargund", "Dr Gururaj Katti", "Dr Asif Tanweer", "Dr P Nagaraja Rao"]
        },
        {
          "year": "2006",
          "names": ["Dr S Desai", "Dr Subrata Satpathy", "Dr P Sreerama Kumar", "Dr Ladu Kishore Rath", "Dr Anitha Kodaru"]
        },
        {
          "year": "2010",
          "names": [
            "Dr A Rajareddy", "Dr Satya Vir", "Dr V Ramesh Babu", "Dr RW Alexander Jesudasan", "Dr S Manickavasagam",
            "Dr V Jayalakshmi", "Dr Yashoda R Hegde", "Dr Pankaj Sharma", "Prof Ram Singh", "Dr V Selvanarayanan",
            "Dr Rajesh Pratap Singh", "Dr S Jeyarani", "Dr R Velazhahan", "Dr PS Vimaladevi", "Dr Mukesh K Dhillon",
            "Dr J Jayakumar", "Dr Abhishek Shukla", "Dr T V K Singh"
          ]
        },
        {
          "year": "2012",
          "names": [
            "Dr T S K Patro", "Dr P C Rath", "Dr P D Meena", "Dr Kavita Gupta", "Dr S R Pandravada",
            "Dr B Sree laxmi", "Dr T Saravanan", "Dr G Shyam Prasad", "Dr P G Padmaja", "Dr Chandish R Ballal",
            "Dr G M V Prasad", "Dr Dewa Ram Bajya", "Dr S Ramakrishnan", "Dr N Somasekhar", "Dr Arjun Lal",
            "Dr A P Padma Kumari", "Dr M Prabhakar", "Dr P K Behera", "Dr Sashi Bhalla", "Dr V Kamala"
          ]
        },
        {
          "year": "2016",
          "names": [
            "Dr V Lakshminarayanamma", "Dr Ch Padmavathi", "Dr Bharati N Bhat", "Dr K Shankarganesh", "Dr M Rajasri",
            "Dr R Jagadeeshwar", "Dr G Sridevi", "Dr K Karthikeyal", "Dr M Visalakshmi", "Dr B Bhavani",
            "Dr Ashish Kumar Tripathi", "Dr Aravindnath Singh", "Dr D Karthikeyan", "Dr T V Prasad", "Dr K Rameash"
          ]
        },
        {
          "year": "2017 – 2023",
          "names": [
            "Dr Srinivas Parimi", "Dr C Alice Retna Packia Sujeetha", "Dr M Srinivas Prasad", "Dr Suresh Kumar Khinchi",
            "Dr A Muthu Kumar", "Dr Jameel Akhtar", "Dr M Alagar", "Dr K P Manju", "Dr V Prakasam",
            "Dr R Maruthadurai", "Dr Pardeep Kumar", "Dr D Ladhalakshmi", "Dr Prasanna Holajjer",
            "Dr Veghra Durga Prasad Rao Nimmakayala", "Dr L Saravanan", "Dr M Punithavalli", "Dr B S Gotyal",
            "Dr K Selvaraj", "Dr Kuldeep Singh Jadon", "Dr P Duraimurugan", "Dr Issai Aruna Sri", "Dr V Jhansi Lakshmi",
            "Dr Kiran Babu Talluri", "Dr Satish Kumar Sain", "Dr SVS Gopala Swamy", "Dr Girish Anantrao Gunjotikar",
            "Dr K Vemana", "Dr MH Kodandaram", "Dr Bonthagorla Subbarayudu", "Dr J Gulsar Banu", "Dr M Visalakshi",
            "Dr D Krishnaveni", "Dr S Subramanian", "Dr MK Jyosthna", "Dr D Anitha Kumari"
          ]
        }
      ]
    },
    {
      "id": "kavuri-sarada",
      "title": "Smt. Kavuri Sarada Memorial Award",
      "desc": "Candidates are not required to send proposals for this award as the screening committee appointed by Plant Protection Association of India chooses the Best Research Papers published in the Indian Journal of Plant Protection every year. The award consists of a certificate to each of the authors of the chosen research paper.",
      "groups": [
        { "year": "1988", "names": ["Dr K Abbaiah", "Dr M Sugunakara Reddy"] },
        { "year": "1989", "names": ["Dr D V Singh", "Dr P Arora", "Dr K D Srivastava", "Dr S Nagarajan", "Dr R Agarwal"] },
        { "year": "1992 – 1993", "names": ["Dr M Veerabhadra Rao"] },
        { "year": "1993 – 1994", "names": ["Dr C Pramod Chandra Kumar"] },
        { "year": "1994 – 1995", "names": ["Dr B J Divakar", "Dr P V Sharma", "Dr V Raghunathan", "Dr B V David", "Dr G R S Reddy", "Sri S V Swamy"] },
        { "year": "1995 – 1996", "names": ["Dr P P Shastry"] },
        { "year": "1996 – 1997", "names": ["Dr T P Sriharan"] },
        { "year": "2001", "names": ["Dr V Markandeya", "Dr V Vasu", "Dr PS Chandurkar", "Dr T Rangarajan", "Dr B J Divakar"] },
        { "year": "2002", "names": ["Dr M Mani", "Dr A Krishnamoorthy"] },
        { "year": "2004", "names": ["Dr T K S Latha"] },
        { "year": "2007", "names": ["Dr Satya Vir"] },
        { "year": "2008", "names": ["Dr V Ramesh Babu"] },
        { "year": "2010", "names": ["Dr V Manoj Kumar"] },
        { "year": "2011", "names": ["Dr N Ramakrishnan"] },
        { "year": "2012", "names": ["Dr Ratna Bhimineni"] },
        { "year": "2013", "names": ["Dr P A Ahila Devi", "Dr V Prakasam"] },
        { "year": "2014", "names": ["Dr A Kandan", "Dr J Akhtar", "Dr B Singh", "Dr U Dev", "Dr R Goley", "Dr D Chand", "Dr A Roy", "Dr S Rajkumar", "Dr P C Agarwal"] },
        { "year": "2015", "names": ["Dr D Balakrishna", "Dr K Srinivasa Babu", "Dr B Venkatesh Bhat", "Dr R Vinod", "Dr M Sreedhar", "Dr G Shyamprasad", "Dr D B Pawar", "Dr Shekharappa", "Dr M O Mohammed Ilyas", "Dr J V Patil"] },
        { "year": "2016", "names": ["Dr K Susheela", "Dr N Sathyanarayana"] },
        { "year": "2019", "names": ["Dr Isha Sharma", "Dr Mohinder Singh", "Dr P L Sharma", "Dr S Vijay Kumar", "Dr M Srinivas Prasad", "Dr R Rambabu", "Dr B Bhaskar", "Dr R M Sundaram", "Dr V Prakasam", "Dr D Ladhalakshmi", "Dr G S Laha", "Dr M Sheshu Madhav"] },
        { "year": "2020", "names": ["Dr E Sree Latha", "Dr S Jesurajan", "Dr Ch. Sreenivasa Rao", "Dr Shambhu Singh", "Dr A K Dave", "Dr D Padhee", "Dr Aman"] },
        { "year": "2021", "names": ["Dr B Sai Sushma", "Dr B Vidya Sagar", "Dr S Triveni", "Dr G Uma Devi", "Dr K Selvaraj", "Dr B V Sumalatha"] },
        { "year": "2022", "names": ["Dr Prasanna Holajjer", "Dr Bharat H Gawade", "Dr Z Khan", "Dr N Sivaraj", "Dr C D Mayee", "Dr B Chaudhary", "Dr R Panchbhai", "Dr A R Annepu", "Dr R D Kapur"] }
      ]
    },
    {
      "id": "dr-rdvj-prasada-rao",
      "title": "Dr. R D V J Prasada Rao Award",
      "desc": "Instituted to recognize outstanding research and meritorious service in the specialized fields of Plant Virology and Plant Quarantine.",
      "groups": [
        { "year": "2012", "names": ["Dr V Celia Chalam"] },
        { "year": "2016", "names": ["Dr Kavita Gupta"] }
      ]
    },
    {
      "id": "best-scientist-awards",
      "title": "Best Scientist Awards",
      "desc": "The Best Scientist Awards in Young (<=40 years) and Senior (40-60 years) Category were instituted by PPAI starting from the year 2023 marking the occasion of the Golden Jubilee Celebrations. The awards are given biannually to individuals in recognition of professional contributions in Entomology, Plant Pathology, Nematology, and Digital Agriculture.",
      "groups": [
        {
          "year": "2023",
          "names": [
            "Dr Shravan M Haldhar", "Dr K Selvaraj", "Dr V Bhuvaneswari", "Dr N Somasekhar",
            "Dr Gadratagi Basana Gowda", "Dr K Sakthivel", "Dr Satish N Chavan", "Dr Srikanth Rupavathara"
          ]
        }
      ]
    },
    {
      "id": "recognition-awards",
      "title": "Recognition & Distinction Awards",
      "desc": "Conferred during the Golden Jubilee ICPHM 2023 for Lifetime Contribution, Outstanding Services, Golden Jubilee Recognition, Award of Distinction, Special Awards, and Posthumous Awards rendered during 1972–2022.",
      "groups": [
        {
          "year": "1972 – 2022",
          "names": [
            "Dr Dodla V Raghava Reddy", "Dr V Raghunathan", "Dr P S Chandurkar", "Dr K S Varaprasad",
            "Dr K Krishnaiah", "Dr KSRK Murthy", "Dr B Sarath Babu", "Dr M Veera Bhadra Rao",
            "Dr B Julius Divakar", "Dr T B Gour", "Dr Rajan Sharma", "Dr T Ramesh Babu",
            "Dr Anitha Kodaru", "Dr B Govinda Naik", "Dr Renu Sharma", "Dr S K Chakrabarty",
            "Dr R Jagadeeshwar", "Dr B Parameswari", "Dr R K Khetarpal", "Dr Harvir Singh",
            "Dr Gururaj Katti", "Dr A Raja Reddy", "Dr V Celia Chalam", "Dr M Srinivas Prasad",
            "Dr H C Sharma", "Dr L Saravanan", "Dr K M Azam", "Dr S Sithanantham",
            "Dr C Pramod Chandra Kumar", "Dr G Sreedevi", "Dr Prasanna Holajjer", "Dr Bhaskar Bajaru",
            "Dr S N Puri", "Dr C D Mayee", "Dr Chelliah", "Dr Anupam Varma",
            "Dr A K Dhawan", "Dr A N Mukhopadhyay", "Dr Srikant Kulkarni", "Dr J S Prasad",
            "Dr H S Gaur", "Dr S N Sushil", "Dr J P Singh", "Mr Vinod Kumar Samanthula"
          ]
        }
      ]
    }
]

final_html = html_template.replace("DATASET_PLACEHOLDER", json.dumps(dataset, indent=2))

with open("templates/pages/awards.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("templates/pages/awards.html written successfully!")
