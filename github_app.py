import streamlit as st
import requests
from collections import Counter, defaultdict
from datetime import datetime
import matplotlib.pyplot as plt

def fetch_github_events(username, max_pages=10):
    url = f"https://api.github.com/users/{username}/events/public"
    all_events = []
    page_count = 0

    while url and page_count < max_pages:
        response = requests.get(url)
        if response.status_code != 200:
            st.error(f"❌ Error: {response.status_code} - {response.text}")
            break
        data = response.json()
        all_events.extend(data)
        next_url = response.links.get('next', {}).get('url')
        url = next_url
        page_count += 1

    return all_events

def get_event_days(events):
    dates = [
        event.get('created_at', '')[:10]
        for event in events
        if 'created_at' in event
    ]
    return dates

def get_event_weekdays(events):
    """
    Return a Counter with weekday names.
    """
    weekdays = [
        datetime.strptime(event['created_at'][:10], "%Y-%m-%d").strftime("%A")
        for event in events
        if 'created_at' in event
    ]
    return Counter(weekdays)

def plot_event_days(dates, github_user):
    counter = Counter(dates)
    sorted_dates = sorted(counter.items())
    x = [datetime.strptime(date, "%Y-%m-%d") for date, _ in sorted_dates]
    y = [count for _, count in sorted_dates]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, y, marker='o', linestyle='-')
    ax.set_title(f"Activity History for  {github_user}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Events")
    ax.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)

def plot_weekday_activity(weekday_counter, github_user):
    weekdays_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    counts = [weekday_counter.get(day, 0) for day in weekdays_order]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(weekdays_order, counts, color='teal')
    ax.set_title(f"Most active days  when {github_user} gets locked in")
    ax.set_xlabel("Weekday")
    ax.set_ylabel("Number of Events")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# --- STREAMLIT UI ---
st.set_page_config(page_title="GitHub Activity Tracker", page_icon="📈", layout="centered")
st.title("📈 GitHub Activity Tracker for Recruiters")

st.markdown(
    """
    <style>
    .main { background-color: #f5f6fa; }
    .stButton>button { background-color: #008CBA; color: white; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("[View Praise Gabriel's LinkedIn Profile](https://www.linkedin.com/in/dataanalyst-praisegabriel)")
st.markdown("[View Victor Zion's LinkedIn Profile](https://www.linkedin.com/in/victor-zion)")

with st.form("github_form"):
    person_name = st.text_input("What is your name?", placeholder="Enter your name")
    github_user = st.text_input("GitHub username to analyze:", placeholder="e.g. octocat")
    submitted = st.form_submit_button("Run Analysis")

if submitted:
    if not github_user:
        st.warning("⚠ Please enter a GitHub username.")
    else:
        with st.spinner("🧪 Running analysis..."):
            events = fetch_github_events(github_user)

        if events:
            dates = get_event_days(events)
            weekday_counter = get_event_weekdays(events)

            col1, col2 = st.columns(2)
            with col1:
                if dates:
                    st.subheader("Activity History")
                    plot_event_days(dates, github_user)
                else:
                    st.info("No recent activity found to plot.")

            with col2:
                if weekday_counter:
                    st.subheader("Most Active Days")
                    plot_weekday_activity(weekday_counter, github_user)
                else:
                    st.info("No weekday data to plot.")
        else:
            st.error("No events found or failed to fetch data.")
