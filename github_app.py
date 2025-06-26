import streamlit as st
import requests
from collections import Counter, defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

# --- GitHub API Helpers ---
BASE_URL = "https://api.github.com"

def get_user_repos(username):
    repos = []
    page = 1
    while True:
        url = f"{BASE_URL}/users/{username}/repos?per_page=100&page={page}"
        response = requests.get(url)
        if response.status_code != 200:
            st.error(f"❌ Error fetching repos: {response.status_code} - {response.text}")
            break
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def get_user_commits(username, repo_name, owner):
    commits = []
    page = 1
    while True:
        url = f"{BASE_URL}/repos/{owner}/{repo_name}/commits?author={username}&per_page=100&page={page}"
        response = requests.get(url)
        if response.status_code == 403:
            st.warning("⚠ API rate limit hit. Please try again later.")
            break
        elif response.status_code != 200:
            break
        data = response.json()
        if not data:
            break
        commits.extend(data)
        page += 1
    return commits

def extract_commit_dates(commits):
    return [
        commit['commit']['author']['date'][:10]
        for commit in commits
        if 'commit' in commit and 'author' in commit['commit']
    ]

def get_weekdays(dates):
    return [
        datetime.strptime(date, "%Y-%m-%d").strftime("%A")
        for date in dates
    ]

def get_repo_languages(repo_owner, repo_name):
    url = f"{BASE_URL}/repos/{repo_owner}/{repo_name}/languages"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {}

# --- Plotting ---
def plot_commits_by_day(dates, username):
    counter = Counter(dates)
    sorted_dates = sorted(counter.items())
    x = [datetime.strptime(date, "%Y-%m-%d") for date, _ in sorted_dates]
    y = [count for _, count in sorted_dates]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, y, marker='o', linestyle='-', color='blue')
    ax.set_title(f"Total GitHub Commits Over Time for {username}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Commits")
    ax.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)

def plot_commits_by_weekday(weekdays, username):
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    counts = Counter(weekdays)
    values = [counts.get(day, 0) for day in weekday_order]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(weekday_order, values, color='orange')
    ax.set_title(f"Most lockedin days  for {username}")
    ax.set_xlabel("Weekday")
    ax.set_ylabel("Number of Commits")
    plt.xticks(rotation=45)
    st.pyplot(fig)

def build_repo_contributions_table(contribution_map):
    df = pd.DataFrame(contribution_map.items(), columns=["Repository", "Commits"])
    df = df.sort_values(by="Commits", ascending=False).reset_index(drop=True)
    st.subheader("📊 Contributions Per Repository")
    st.dataframe(df)

def plot_language_donut(language_map):
    if not language_map:
        st.warning("⚠ No language data found.")
        return
    total = sum(language_map.values())
    labels = list(language_map.keys())
    sizes = [round((v / total) * 100, 2) for v in language_map.values()]

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    ax.axis("equal")
    st.subheader("🧠 Languages Used")
    st.pyplot(fig)

# --- Streamlit App ---
st.title("🔥 GitHub Productivity Tracker for Devs")
st.markdown("[👉 View Dev's LinkedIn Profile](https://www.linkedin.com/in/dataanalyst-praisegabriel)")

person_name = st.text_input("What's your name?")
github_user = st.text_input(f"Hi {person_name}, enter your GitHub username:")

if st.button("Run Analysis"):
    if not github_user:
        st.warning("⚠ Please enter a GitHub username.")
    else:
        st.info("Fetching repos & analyzing data...")
        repos = get_user_repos(github_user)

        if not repos:
            st.warning("⚠ No public repositories found.")
        else:
            all_commit_dates = []
            weekdays_all = []
            contribution_map = {}
            language_totals = defaultdict(int)

            for repo in repos:
                repo_name = repo['name']
                owner = repo['owner']['login']

                # Get Commits
                commits = get_user_commits(github_user, repo_name, owner)
                commit_dates = extract_commit_dates(commits)
                all_commit_dates.extend(commit_dates)
                weekdays_all.extend(get_weekdays(commit_dates))
                contribution_map[repo_name] = len(commit_dates)

                # Get Languages
                lang_data = get_repo_languages(owner, repo_name)
                for lang, size in lang_data.items():
                    language_totals[lang] += size

            # Plot Visuals
            if all_commit_dates:
                st.subheader("📅 Commit History")
                plot_commits_by_day(all_commit_dates, github_user)

                st.subheader("📆 Most Active Days of the Week")
                plot_commits_by_weekday(weekdays_all, github_user)

                build_repo_contributions_table(contribution_map)

                plot_language_donut(language_totals)

            else:
                st.warning("⚠ No commit data found.")
