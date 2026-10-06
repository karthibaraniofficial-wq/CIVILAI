# CIVICFLOW AI (CIVILAI)

> **Autonomous Civic Grievance Orchestration Platform**  
> *Transforming citizen reports into verified, automated municipal action pipelines.*

<div align="center">

[![Live App](https://img.shields.io/badge/Live%20App-civilai--mu.vercel.app-10b981?style=for-the-badge&logo=vercel&logoColor=white)](https://civilai-mu.vercel.app)
[![Developer Portfolio](https://img.shields.io/badge/Developer%20Portfolio-karthi--portfolio--delta.vercel.app-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://karthi-portfolio-delta.vercel.app)
[![GitHub](https://img.shields.io/badge/Source-GitHub-1e293b?style=for-the-badge&logo=github&logoColor=white)](https://github.com/karthibaraniofficial-wq/CIVILAI)

</div>

---

## 🏛️ Overview

**CIVICFLOW AI (CIVILAI)** eliminates the manual sorting bottlenecks of traditional municipal grievance redressal systems. By implementing a deterministic **6-Agent Autonomous DAG Pipeline**, the system analyzes incoming complaint descriptions, detects and scores hazards from submitted photos using Computer Vision (severity scale $1–10$), dynamically routes work orders to municipal departments, calculates enforceable SLAs, and triggers automated escalations.

---

## ⚡ 6-Agent Autonomous Pipeline

1. **Intake & Intent Agent:** Normalizes voice/text submissions across regional languages into structured JSON schemas.
2. **Computer Vision Hazard Agent:** Inspects image evidence, verifies hazard authenticity, and computes a deterministic $1–10$ severity score.
3. **Department Routing Agent:** Matches incident taxonomy to municipal jurisdictions (Roads, Electrical, Water & Sanitation, Health).
4. **Dynamic SLA Engine:** Calculates dynamic resolution deadlines factoring in weather, hazard severity, and crew availability.
5. **Tamper-Proof Audit Agent:** Logs immutable timestamped audit proofs on state transitions.
6. **Escalation & Notification Agent:** Automatically escalates stalled tickets to senior zonal officers when SLAs expire.

---

## 🛠️ Technology Stack

- **Frontend:** React 18, TypeScript, Tailwind CSS, Lucide React
- **Backend:** Python 3.12, FastAPI, Pydantic v2
- **Database & Auth:** Supabase (PostgreSQL with Row Level Security)
- **Deployment:** Vercel Edge Network

---

## 🚀 Getting Started

### Local Setup
```bash
# Clone repository
git clone https://github.com/karthibaraniofficial-wq/CIVILAI.git
cd CIVILAI

# Install frontend dependencies
cd frontend
npm install
npm run dev
```

---

## 👤 Author & Ecosystem

- **Architect & Developer:** **Karthikeyan M**
- **🌐 Live Developer Portfolio:** [https://karthi-portfolio-delta.vercel.app](https://karthi-portfolio-delta.vercel.app)
- **GitHub:** [@karthibaraniofficial-wq](https://github.com/karthibaraniofficial-wq)
- **Direct Email:** `karthibaraniofficial@gmail.com`

---

## 📄 License
This project is licensed under the MIT License.
