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
st.title("📈 Github Tracker for Recruiters")

# Dev's LinkedIn profile
st.markdown("[👉 View Dev's LinkedIn Profile](https://www.linkedin.com/in/YOUR-LINK/)")

person_name = st.text_input("Hello,What is your name?")
github_user = st.text_input(f" Hi {person_name} Enter GitHub username to analyze:")

if st.button("Run Analysis"):
    if not github_user:
        st.warning("⚠ Please enter a GitHub username.")
    else:
        st.info(f"Hi {person_name}, fetching activity for **{github_user}**...")
        events = fetch_github_events(github_user)

        if events:
            dates = get_event_days(events)
            if dates:
                plot_event_days(dates, github_user)
            else:
                st.warning("⚠ No recent activity found to plot.")

            # Weekday activity
            weekday_counter = get_event_weekdays(events)
            if weekday_counter:
                plot_weekday_activity(weekday_counter, github_user)
            else:
                st.warning("⚠ No weekday data to plot.")
        else:
            st.warning("⚠ No events found or failed to fetch data.")
