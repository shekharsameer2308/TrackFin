# TrackFin 🚀

**TrackFin** is a premium, modern personal finance tracking application designed to give you complete control over your financial life. Built with a focus on intuitive user experience and stunning aesthetics, TrackFin makes managing your income, expenses, and savings goals both effortless and visually engaging.

Whether you're tracking daily coffee runs or managing a complex monthly budget, TrackFin provides the analytics and insights you need, wrapped in a beautiful, responsive interface that works flawlessly across desktop and mobile devices.

---

## ✨ Key Features

* **Premium Glassmorphism UI**: A gorgeous whitish-grey theme with striking magenta accents, featuring smooth micro-animations and depth-enhancing glassmorphism effects.
* **Smart Dashboard**: Instantly view your total balance, income, and expenses at a glance.
* **Dynamic Analytics**: Interactive Chart.js visualizations that break down your spending habits by category.
* **Seamless Transaction Logging**: Quickly add income or expenses with automatic categorization and date tracking.
* **Fully Responsive**: Engineered with flexible CSS Grid and Flexbox to deliver a native-app feel on smartphones, tablets, and desktop monitors.
* **Serverless Ready**: Configured for seamless deployment on Vercel, bridging a powerful Python backend with a lightning-fast static frontend.

---

## 🛠️ Technology Stack

TrackFin is built using a modern, lightweight, and highly extensible stack:

| Layer | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | HTML5, Vanilla CSS, JavaScript | Pure, dependency-free frontend leveraging CSS variables, Flexbox, and Grid for maximum performance and customizability. |
| **Visualizations**| Chart.js | Renders dynamic, responsive, and interactive charts. |
| **Backend API** | Python, Flask | A robust RESTful API handling data validation, categorization, and aggregation. |
| **Database** | SQLite & SQLAlchemy | Lightweight relational database managed via Python's leading ORM. |
| **Deployment** | Vercel | Configured via `vercel.json` to serve the static frontend and run the Flask API as Serverless Functions. |

---

## 🚀 Quick Start

### 1. Local Development Setup
Clone the repository and set up the backend:

```bash
git clone https://github.com/shekharsameer2308/TrackFin.git
cd TrackFin

# Set up the Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Start the Flask API server
python backend/app.py
```
The backend API will run on `http://localhost:5000`.

### 2. Launch the Frontend
Simply open `frontend/index.html` in any modern web browser. The app will automatically connect to your local Flask server.

---

## 🌐 Production Deployment

TrackFin includes a `vercel.json` file, making it ready for immediate deployment on Vercel. 
1. Import the repository into your Vercel account.
2. Vercel will automatically serve the `/frontend` directory and map the `/api/*` routes to the Python Serverless Functions in `backend/app.py`.

*(Note: SQLite is used for local development. For persistent data in production on Vercel, update the `SQLALCHEMY_DATABASE_URI` in `config.py` to point to a cloud database like Vercel Postgres or Supabase).*

---

## 🎨 Design Philosophy
TrackFin departs from bulky CSS frameworks. By utilizing **Vanilla CSS**, the project maintains a tiny footprint while achieving a highly customized, premium look. The design prioritizes:
- **Clarity**: High-contrast typography and clear visual hierarchy.
- **Feedback**: Subtle hover states and smooth transitions for a responsive feel.
- **Adaptability**: Fluid layouts that gracefully restructure across screen sizes.

---

Crafted with ❤️ to make personal finance tracking smarter and simpler.
