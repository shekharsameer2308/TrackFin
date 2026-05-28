# TrackFin 🚀

**TrackFin** is an intelligent, modern personal finance management and analytics platform built as a lightweight Fintech SaaS product. 

It moves beyond standard expense tracking by offering smart heuristics, predictive analytics, and gamified savings goals, all wrapped in a premium glassmorphism UI.

![TrackFin Demo](https://img.shields.io/badge/Status-Live-success?style=for-the-badge) ![Python](https://img.shields.io/badge/Python-Flask-blue?style=for-the-badge) ![JavaScript](https://img.shields.io/badge/Vanilla_JS-ES6-yellow?style=for-the-badge)

## 🔗 Live Demo
Check out the live application hosted on Vercel:
**[https://track-fin-bay.vercel.app/](https://track-fin-bay.vercel.app/)**
*(Tip: Click "Continue as Guest" to test it out without creating an account!)*

---

## ✨ Key Features

* **Smart Categorization Engine**: Let the app do the heavy lifting! Add an expense with a note like *"Uber home"* and the engine automatically tags it as **Transportation**.
* **Financial Health Score**: An algorithm analyzes your savings ratio and discretionary spending to calculate a real-time health score (`Excellent`, `Good`, `Warning`, or `Critical`).
* **Subscription & Burn Rate Tracking**: Automatically detects recurring subscriptions (e.g., Netflix, Rent, Gym) and aggregates them into a Monthly Burn Rate dashboard widget so you always know your fixed costs.
* **Goal-Based Savings**: A gamified module where you can set targets (e.g., "New Laptop: $1500") and watch your progress bar fill up dynamically as you save.
* **Frictionless Authentication**: Secure JWT-based authentication with a seamless "Guest" mode that auto-generates temporary, isolated accounts for immediate platform testing.
* **Premium UI/UX**: Designed using pure CSS with dark-mode glassmorphism, fluid responsive layouts, and interactive Chart.js visualizations.
* **AI-Ready Infrastructure**: Built-in mock endpoints (`/api/transactions/ocr` and `/api/transactions/voice`) designed to act as drop-in replacements for OpenAI Whisper and Google Cloud Vision SDKs.

---

## 🛠️ Tech Stack

**Frontend:**
* HTML5 / CSS3 (Custom Glassmorphism Design System)
* Vanilla JavaScript (ES6+)
* Chart.js (Data Visualization)

**Backend:**
* Python 3
* Flask (Modular Blueprint Architecture)
* SQLite (Routed to `/tmp` for Serverless compatibility)
* SQLAlchemy (ORM)
* PyJWT & Werkzeug Security (Authentication)

**Deployment:**
* Vercel (Serverless Functions for Python Backend + Static Frontend Hosting)

---

## 💻 Local Development

Want to run TrackFin locally? Follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/shekharsameer2308/TrackFin.git
   cd TrackFin
   ```

2. **Set up the Python Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: .\venv\Scripts\Activate.ps1
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Run the Backend Server:**
   ```bash
   python backend/app.py
   ```

5. **Start the Frontend:**
   Open `frontend/index.html` in any modern web browser or use a live server extension!

---

## 🔮 Roadmap / Future Enhancements
- [ ] Connect real OpenAI Whisper API to the voice-logging endpoint.
- [ ] Connect Google Cloud Vision API to the receipt OCR endpoint.
- [ ] Migrate from SQLite to a managed PostgreSQL database for permanent production storage.
- [ ] Add CSV export functionality for financial reporting.

---

*Engineered as a Master Fintech SaaS implementation.*
