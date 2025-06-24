# 🚀 GitHub Activity Tracker for Recruiters

A simple Streamlit web app that visualizes the public GitHub activity of any user. Enter a GitHub username to see their recent activity history and discover which days they're most active. 🔍

## ✨ Features

- 📦 Fetches and displays a user's recent public GitHub events.
- 📈 Plots activity history over time.
- 📅 Shows which weekdays the user is most active.
- 🧑‍💼 Clean, recruiter-friendly UI.

## 🛠️ Getting Started

### ✅ Prerequisites

- 🐍 Python 3.7+
- [pip](https://pip.pypa.io/en/stable/)

### 📦 Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/praise8mb/github-activity-tracker-for-Developers.git
    cd github-activity-tracker-for-Developers
    ```

2. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

## 🚦 Running the App

```sh
streamlit run github_app.py
```

The app will open in your browser at [http://localhost:8501](http://localhost:8501). 🌐

## 📝 Usage

1. Enter your name (optional). ✍️
2. Enter the GitHub username you want to analyze (e.g., `octocat`). 🐙
3. Click **Run Analysis**. ▶️
4. View the user's activity history and most active weekdays. 📊

## 📁 Project Structure

- `github_app.py`: Main Streamlit app.
- `requirements.txt`: Python dependencies.

## ⚙️ How It Works

- Fetches up to 10 pages of public events from the GitHub API for the specified user.
- Aggregates events by date and weekday.
- Visualizes activity using matplotlib charts embedded in Streamlit.

## ⚠️ Notes

- Only public events are shown (private activity is not available via the GitHub API).
- GitHub API rate limits apply for unauthenticated requests.

## 👥 Authors

- [Praise Gabriel (LinkedIn)](https://www.linkedin.com/in/dataanalyst-praisegabriel)
- [Victor Zion (LinkedIn)](https://www.linkedin.com/in/victor-zion)

---

Made with ❤️ using [Streamlit](https://streamlit.io).