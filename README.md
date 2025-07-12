# TrackFin

**TrackFin** is a modern, lightweight personal finance tracking web application designed for individuals seeking control over their daily income and expenses. With an intuitive UI, robust backend, and insightful analytics, TrackFin enables users to categorize transactions, analyze financial behavior, and make informed budgeting decisions.

Built using **Flask (Python)** for the backend and **SQLite** for persistent local storage, TrackFin is optimized for speed, security, and privacy. The frontend leverages **Tailwind CSS** and **JavaScript** for responsive, interactive dashboards. It is ideal for students, professionals, and developers looking for an extendable finance tool or full-stack boilerplate.

---

## **Key Features**

* Log income and expense transactions with notes and timestamps
* Categorize transactions (e.g., Food, Travel, Utilities)
* Monthly analytics: income, expenses, net savings
* Interactive data visualizations (bar/pie charts using Chart.js)
* Full transaction history with filters
* Offline-compatible (SQLite)
* RESTful API endpoints for extensibility
* Optional: user authentication, CSV export, budget alerts

---

## **Technology Stack**

| Layer          | Technology                                 |
| -------------- | ------------------------------------------ |
| Frontend       | HTML, Tailwind CSS, JavaScript             |
| Backend        | Python, Flask, Flask-CORS                  |
| Database       | SQLite (via SQLAlchemy or raw SQL)         |
| Visualization  | Chart.js                                   |
| DevOps/Hosting | Vercel (frontend), Render/Heroku (backend) |

---

## **Project Architecture**

### Directory Structure

```
trackfin/
├── backend/
│   ├── app.py              # Flask app factory & routes
│   ├── models.py           # SQLAlchemy models
│   ├── config.py           # Configuration settings
│   ├── database.db         # SQLite database file
│   └── requirements.txt    # Python dependencies
│
├── frontend/
│   ├── index.html          # Main UI layout
│   ├── styles.css          # Tailwind custom styles
│   └── app.js              # Fetch API calls and DOM updates
│
├── .gitignore              # Files to ignore in version control
├── README.md               # Project documentation
```

### High-Level Architecture Design

**Client Layer (Browser)**

* Static frontend using HTML, Tailwind CSS, and JavaScript
* Handles UI rendering and user interaction
* Sends HTTP requests to Flask backend

**Application Layer (Flask Backend)**

* RESTful routes to handle transactions, summaries, categories
* Business logic for validation, categorization, and aggregation
* CORS enabled for local frontend-backend separation

**Data Layer (SQLite)**

* Lightweight relational DB
* Stores transaction data: amount, date, category, type (income/expense), notes
* SQLAlchemy ORM or raw SQL queries to interact with the DB

**Visualization Layer**

* Charts rendered in the frontend using Chart.js
* Receives processed data from Flask endpoints for rendering dynamic visuals

**Deployment (optional)**

* Frontend: Deployable to Vercel or GitHub Pages as static assets
* Backend: Flask app deployable to Render or Heroku with SQLite or external PostgreSQL

---

## **Quick Start**

Development is currently in the planning phase. Setup instructions and environment details will be added here once backend and frontend implementation begins.

### **Frontend Setup**

```bash
cd trackfin/frontend
# Open index.html directly or serve locally
npx serve .
```

---

---

## **Python Dependencies**

```text
Flask
Flask-CORS
SQLAlchemy
python-dotenv
```

Install via:

```bash
pip install -r requirements.txt
```

---

## **Roadmap**

* [ ] User authentication with session management
* [ ] CSV export of financial data
* [ ] Budget setting and alerts for overspending
* [ ] Responsive mobile-first design improvements
* [ ] Advanced filtering by date, category, keyword
* [ ] Deployment automation using Docker or CI/CD

---

## **License**

TrackFin is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for complete terms and conditions.

---

## **Author**

Crafted with care by **Sameer Shekhar**  
**LinkedIn:** [linkedin.com/in/shekharsameer2308](https://www.linkedin.com/in/shekharsameer2308)  
**GitHub:** [github.com/shekharsameer2308](https://github.com/shekharsameer2308)

---

## **Tagline**

**TrackFin** – *Smarter spending, simplified.*
