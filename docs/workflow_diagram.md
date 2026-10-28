# PPAI / IJPP Manuscript Submission & Peer-Review Workflow

This workflow represents the end-to-end editorial pipeline for the **Indian Journal of Plant Protection (IJPP)** hosted by the **Plant Protection Association of India (PPAI)**.

> [!NOTE]
> The **Associate Editor** role is currently bypassed in this active operational pipeline. All editorial screenings, assignments, reviews, and decision releases route directly through the **Chief Editor Console**.

---

## 1. System Architecture & Flowchart

```mermaid
flowchart TD
    subgraph S1["Phase 1: Submission & Payment"]
        A["Author Form Submission"] -->|"Uploads manuscript & payment proof"| B["Submission Handler"]
        B -->|"Saves tracking ID, title, abstract & payment proof"| DB[("PostgreSQL / SQLite Database")]
        B -->|"Trigger Email 1"| M1["Author Acknowledgment Email<br/>(Tracking ID, Title, Abstract, Txn ID, Screenshot)"]
        B -->|"Trigger Email 2"| M2["Chief Editor Alert Email<br/>(Txn ID, Screenshot & Manuscript File Attached)"]
    end

    subgraph S2["Phase 2: Chief Editor Console & Reviewer Assignment"]
        DB -->|"Loads manuscript cards"| CE["Chief Editor Console (/portal/admin/)"]
        CE -->|"Screening: ID, Title, Date, Payment Verification"| CE_DEC{"Initial Screening"}
        CE_DEC -->|"Assign Reviewer & Window Time"| ASG["Review Assignment Created"]
        ASG -->|"Trigger Email 3"| M3["Reviewer Invitation Email<br/>(Deadline Window & Action Link)"]
        M3 -.->|"If no response within window"| M4["Automated Reminder Email"]
    end

    subgraph S3["Phase 3: Reviewer Onboarding & Evaluation"]
        M3 -->|"Reviewer Accepts"| ACC["Reviewer Acceptance Registered"]
        ACC -->|"Chief Editor triggers credentials"| M5["Reviewer Login Credentials Email<br/>(Username & Password)"]
        M5 -->|"Reviewer logs in at /login/"| RC["Reviewer Console (/portal/reviewer/)"]
        RC -->|"Clicks Assignment Card"| RW["Review Workspace (/portal/reviewer/evaluate/)"]
        RW -->|"Submits Scores, Recommendation & Dual Comments"| REV_SUB["Review Submitted"]
    end

    subgraph S4["Phase 4: Chief Editor Moderation & Author Release"]
        REV_SUB -->|"Trigger Email 4"| M6["Chief Editor Review Alert Email<br/>(Review Completed Notification)"]
        REV_SUB -->|"Visible in Chief Editor Console"| CE_MOD["Chief Editor Moderation Screen"]
        CE_MOD -->|"Inspects confidential remarks & approves author comments"| APPR["Comments Approved & Decision Finalized"]
        APPR -->|"Trigger Email 5"| M7["Author Decision & Feedback Email<br/>(Decision, Moderated Comments & Next Steps)"]
    end

    classDef primary fill:#E8F7F0,stroke:#00B272,stroke-width:2px,color:#0B2417;
    classDef mail fill:#FEF3C7,stroke:#D97706,stroke-width:1.5px,color:#78350F;
    classDef editor fill:#EDE9FE,stroke:#7C3AED,stroke-width:2px,color:#4C1D95;
    classDef reviewer fill:#EFF6FF,stroke:#2563EB,stroke-width:1.5px,color:#1E40AF;

    class A,B,RW,REV_SUB primary;
    class M1,M2,M3,M4,M5,M6,M7 mail;
    class CE,CE_DEC,ASG,CE_MOD,APPR editor;
    class ACC,RC reviewer;
```

---

## 2. Detailed Sequential Workflow (Step-by-Step)

```mermaid
sequenceDiagram
    autonumber
    actor Author
    participant Web as Portal Web App
    participant DB as Database
    participant Mail as Email Notification Engine
    actor ChiefEditor as Chief Editor
    actor Reviewer

    %% Phase 1
    Note over Author,Mail: Phase 1: Manuscript Submission & Payment
    Author->>Web: Submits Manuscript (Title, Abstract, File, Txn ID, Payment Screenshot)
    Web->>DB: Stores Manuscript & Payment Record (Status: submitted)
    Web->>Mail: Trigger Email A: Author Acknowledgment
    Mail-->>Author: Sends Acknowledgment (Tracking ID, Title, Abstract, Txn ID, Payment Proof)
    Web->>Mail: Trigger Email B: Chief Editor Notification
    Mail-->>ChiefEditor: Sends Alert (Tracking ID, Details, Payment Proof + Attached Manuscript)

    %% Phase 2
    Note over ChiefEditor,Reviewer: Phase 2: Chief Editor Screening & Reviewer Assignment
    ChiefEditor->>Web: Views Chief Editor Console (/portal/admin/)
    Note right of ChiefEditor: Card shows ID, Title, Submitted Date, Payment Txn ID & Screenshot
    ChiefEditor->>Web: Assigns Reviewer & sets deadline window
    Web->>DB: Records ReviewAssignment (Status: pending)
    Web->>Mail: Trigger Email C: Reviewer Invitation
    Mail-->>Reviewer: Sends Invitation with Manuscript Details & Deadline Window
    
    alt Reviewer does not respond within deadline window
        Web->>Mail: Trigger Reminder Email
        Mail-->>Reviewer: Sends Follow-up Reminder
    end

    %% Phase 3
    Note over ChiefEditor,Reviewer: Phase 3: Reviewer Acceptance & Account Setup
    Reviewer->>Web: Clicks Accept Invitation Link
    Web->>DB: Updates Assignment (Status: accepted)
    ChiefEditor->>Web: Generates/Confirms Reviewer Credentials
    Web->>Mail: Trigger Email D: Reviewer Credentials
    Mail-->>Reviewer: Sends Login Credentials (Email & Password)
    Reviewer->>Web: Logs in as 'Reviewer' at /login/
    Web->>Reviewer: Opens Reviewer Console (/portal/reviewer/)
    Reviewer->>Web: Clicks Assignment Card -> Opens Workspace (/portal/reviewer/evaluate/)
    Reviewer->>Web: Submits Rubric, Recommendation, Author Comments & Confidential Editor Remarks
    Web->>DB: Saves Review (Status: completed, is_approved_by_editor: False)

    %% Phase 4
    Note over ChiefEditor,Author: Phase 4: Chief Editor Moderation & Author Notification
    Web->>Mail: Trigger Email E: Review Complete Alert
    Mail-->>ChiefEditor: Alerts Chief Editor that Review is ready for inspection
    ChiefEditor->>Web: Inspects Scores, Recommendation, Author Comments & Confidential Notes
    ChiefEditor->>Web: Approves Comments & Issues Decision (Accept / Minor / Major / Reject)
    Web->>DB: Updates is_approved_by_editor = True & Sets Manuscript Status
    Web->>Mail: Trigger Email F: Author Decision & Moderated Feedback
    Mail-->>Author: Sends Final Editorial Decision & Moderated Peer-Review Comments
```

---

## 3. Workflow Specification Table

| Stage | Trigger Event | Action / Actor | Data Included | Automated Output / Email |
| :--- | :--- | :--- | :--- | :--- |
| **1. Submission** | Author clicks *Submit Manuscript* | Author uploads paper & payment proof | Tracking ID, Title, Abstract, Discipline, Txn ID, Screenshot | **Email to Author:** Submission confirmation with full details.<br/>**Email to Chief Editor:** Full alert with attached manuscript file. |
| **2. Admin Console** | Chief Editor logs into `/portal/admin/` | Chief Editor reviews card queue | Single card per paper: ID, Title, Submission Date, Author details, Payment Proof | Chief Editor verifies payment and manuscript scope. |
| **3. Assignment** | Chief Editor selects Reviewer & Window | Chief Editor assigns peer reviewer | Reviewer name, email, assignment due date (e.g. 14 days) | **Email to Reviewer:** Review invitation with time window.<br/>*(Auto-reminder triggered if not acknowledged)*. |
| **4. Credentials** | Reviewer accepts review invitation | Chief Editor issues login access | Reviewer portal credentials | **Email to Reviewer:** Login email, password, and portal URL. |
| **5. Evaluation** | Reviewer logs in & clicks card | Reviewer evaluates paper in `/portal/reviewer/evaluate/` | Rubric scores, Recommendation, Author comments, Confidential Editor notes | Submission saved as `completed`, confidential remarks locked to Chief Editor. |
| **6. Chief Editor Moderation** | Review submission triggers event | Chief Editor inspects review feedback | Reviewer scores, Author comments, Confidential remarks | **Email to Chief Editor:** Notification of review completion. |
| **7. Author Release** | Chief Editor approves feedback | Chief Editor releases editorial decision | Final decision (Accept / Revision / Reject), moderated review comments | **Email to Author:** Official decision letter with peer review comments. |
