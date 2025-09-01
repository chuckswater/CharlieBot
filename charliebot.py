import streamlit as st
import pyttsx3
import threading
import time
import speech_recognition as sr
import sympy as sp
import pandas as pd
import os
import shutil
import datetime
import random
import sqlite3
from PIL import Image

st.set_page_config(page_title="CharlieBot Dashboard", layout="wide")

# Initialize voice engine globally
engine = pyttsx3.init()

def respond(text):
    engine.say(text)
    engine.runAndWait()

st.sidebar.title("CharlieBot Modules")
tab = st.sidebar.radio("Choose a module", [
    "Voice Settings",
    "Timers & Alarms",
    "Smart Calculator",
    "Master Coder Mode",
    "Agent Mode",
    "Photo Organizer",
    "Ad Assistant",
    "Job Tracker",
    "Quote Generator",
    "Follow-Up Reminders",
    "Email Drafts",
    "Memory Search"
])

if tab == "Voice Settings":
    st.header("🗣️ Voice Settings")
    voices = engine.getProperty('voices')
    voice_options = [f"{i}: {voice.name}" for i, voice in enumerate(voices)]
    selected_voice = st.selectbox("Choose a voice", voice_options)
    chosen_index = int(selected_voice.split(":")[0])
    engine.setProperty('voice', voices[chosen_index].id)
    test_phrase = st.text_input("Type something for CharlieBot to say", value="Hello Charlie, I'm ready to help.")
    if st.button("Test Voice"):
        respond(test_phrase)
        st.success("Voice test complete.")

elif tab == "Timers & Alarms":
    st.header("⏰ Timers & Alarms")
    def set_timer(seconds, message):
        def alarm():
            time.sleep(seconds)
            respond(f"⏰ Timer finished: {message}")
            st.warning(f"⏰ Timer finished: {message}")
        threading.Thread(target=alarm, daemon=True).start()
    timer_seconds = st.number_input("Duration (in seconds)", min_value=1)
    timer_message = st.text_input("Timer message", value="Time's up!")
    if st.button("Start Timer"):
        set_timer(timer_seconds, timer_message)
        st.success(f"Timer started for {timer_seconds} seconds.")

elif tab == "Smart Calculator":
    st.header("🧮 Smart Calculator")
    expression = st.text_input("Example: 12 * 8 or 2*x + 3 = 7")
    if expression:
        try:
            if "=" in expression:
                lhs, rhs = expression.split("=")
                x = sp.Symbol('x')
                solution = sp.solve(sp.Eq(eval(lhs), eval(rhs)), x)
                st.success(f"Solution: x = {solution}")
                respond(f"The solution is x equals {solution[0]}")
            else:
                result = eval(expression)
                st.success(f"Result: {result}")
                respond(f"The result is {result}")
        except Exception as e:
            st.error("Invalid expression. Try something like 12 * 8 or 2*x + 3 = 7.")
            respond("Sorry, I couldn't understand that expression.")

elif tab == "Master Coder Mode":
    st.header("👨‍💻 Master Coder Mode")
    mode = st.radio("Choose your mode", ["Beginner", "Expert"])
    topic = st.text_input("Enter a coding topic or snippet", value="for loop in Python")
    if st.button("Explain"):
        if mode == "Beginner":
            explanation = """
            A **for loop** in Python lets you repeat actions for each item in a list or range.
            Example:
            ```python
            for i in range(5):
                print(i)
            ```
            This prints numbers 0 to 4. The loop runs once for each number in `range(5)`.
            """
        else:
            explanation = """
            A **for loop** in Python is syntactic sugar for iterable traversal.
            Example:
            ```python
            for item in iterable:
                # process item
            ```
            Internally, it calls `iter()` and `next()` on the object until `StopIteration` is raised.
            """
        st.markdown(explanation)
        respond("Explanation complete.")

elif tab == "Agent Mode":
    st.header("🔄 Agent Mode")
    st.markdown("CharlieBot can perform tasks on your behalf — but only with your permission.")
    delete_duplicates = st.checkbox("Allow CharlieBot to delete duplicate files")
    log_job = st.checkbox("Allow CharlieBot to log a new job")
    send_email = st.checkbox("Allow CharlieBot to draft and send follow-up emails")
    if delete_duplicates and st.button("Delete Duplicates"):
        respond("Deleting duplicate files now.")
        st.success("Duplicates deleted. (Placeholder logic)")
    if log_job and st.button("Log Job"):
        respond("Logging job now.")
        st.success("Job logged. (Placeholder logic)")
    if send_email and st.button("Send Follow-Up Email"):
        respond("Sending email now.")
        st.success("Email sent. (Placeholder logic)")

elif tab == "Photo Organizer":
    st.header("🖼️ Photo Organizer")
    photo_folder = st.text_input("Enter photo folder path", value="F:/CharlieBotData/photos")
    date_filter = st.date_input("Filter images modified after:")
    detect_faces = st.checkbox("Enable face detection (placeholder)")
    auto_sort = st.checkbox("Auto-sort into work and personal folders")
    if st.button("Scan Folder"):
        if os.path.exists(photo_folder):
            files = os.listdir(photo_folder)
            image_files = [f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg"))]
            if date_filter:
                cutoff = datetime.datetime.combine(date_filter, datetime.datetime.min.time())
                image_files = [
                    f for f in image_files
                    if datetime.datetime.fromtimestamp(
                        os.path.getmtime(os.path.join(photo_folder, f))
                    ) > cutoff
                ]
            st.success(f"Found {len(image_files)} image files.")
            respond(f"I found {len(image_files)} images in your folder.")
            # Detect duplicates by filename
            duplicates = []
            seen = set()
            for img in image_files:
                if img in seen:
                    duplicates.append(img)
                else:
                    seen.add(img)
            # Detect duplicates by file size
            size_map = {}
            size_duplicates = []
            for img in image_files:
                path = os.path.join(photo_folder, img)
                size = os.path.getsize(path)
                if size in size_map:
                    size_duplicates.append(img)
                else:
                    size_map[size] = img
            if duplicates or size_duplicates:
                st.warning("Duplicate files detected:")
                for dup in set(duplicates + size_duplicates):
                    st.write(dup)
                respond("I found duplicate files in your folder.")
            else:
                st.info("No duplicates found.")
                respond("No duplicates found.")
            if detect_faces:
                respond("Face detection is not yet implemented, but it's coming soon.")
                st.info("Face detection placeholder activated.")
            if auto_sort:
                work_dir = os.path.join(photo_folder, "work_photos")
                personal_dir = os.path.join(photo_folder, "personal_photos")
                os.makedirs(work_dir, exist_ok=True)
                os.makedirs(personal_dir, exist_ok=True)
                for img in image_files:
                    if "job" in img.lower() or "site" in img.lower() or "repair" in img.lower():
                        shutil.move(os.path.join(photo_folder, img), os.path.join(work_dir, img))
                    else:
                        shutil.move(os.path.join(photo_folder, img), os.path.join(personal_dir, img))
                st.success("Photos sorted into work and personal folders.")
                respond("Photos have been sorted into work and personal folders.")
        else:
            st.error("Folder not found. Check the path and try again.")
            respond("I couldn't find that folder.")

elif tab == "Ad Assistant":
    st.title("CharlieBot: Home Repair Ad Assistant")
    job_type = st.text_input("What kind of job did you complete?")
    location = st.text_input("Where was it?")
    detail = st.text_input("Any cool detail or challenge you solved?")
    if st.button("Generate Ad"):
        ad = f"Just finished a {job_type} in {location}. {detail}. If your home needs structural help or waterproofing, give us a call!"
        st.success(ad)
    save_path = "F:/CharlieBotData/ads.txt"
    if st.button("Save Ad"):
        with open(save_path, "a") as file:
            file.write(ad + "\n\n")
        st.info("Ad saved to your archive.")
    if st.button("View Saved Ads"):
        if os.path.exists(save_path):
            with open(save_path, "r") as file:
                ads = file.read()
            st.text_area("Your Saved Ads", ads, height=300)
        else:
            st.warning("No ads saved yet.")

elif tab == "Job Tracker":
    st.header("Job Tracker")
    client_name = st.text_input("Client Name")
    job_location = st.text_input("Job Location")
    job_type = st.selectbox("Type of Repair", ["Foundation", "Waterproofing", "Crawlspace", "Other"])
    job_date = st.date_input("Date of Job")
    job_log_path = "F:/CharlieBotData/jobs.txt"
    if st.button("Log Job"):
        job_entry = f"{job_date} | {client_name} | {job_location} | {job_type}"
        with open(job_log_path, "a") as file:
            file.write(job_entry + "\n")
        st.success("Job logged successfully.")
    if st.button("View Job History"):
        if os.path.exists(job_log_path):
            with open(job_log_path, "r") as file:
                jobs = file.read()
            st.text_area("Logged Jobs", jobs, height=300)
        else:
            st.warning("No jobs logged yet.")
    tips = [
        "Fall is coming — offer gutter sealing and foundation checks before the rain hits.",
        "Bundle waterproofing with mold inspection for added value.",
        "Offer a free crawlspace inspection with every foundation repair.",
        "Post before/after photos to build trust in local Facebook groups.",
        "Use yard signs after each job to build neighborhood visibility."
    ]
    if st.button("Get Business Tip"):
        st.info(random.choice(tips))
    if st.button("View Job Stats"):
        if os.path.exists(job_log_path):
            df = pd.read_csv(job_log_path, sep="|", header=None, names=["Date", "Client", "Location", "Type"])
            job_counts = df["Type"].value_counts()
            st.bar_chart(job_counts)
        else:
            st.warning("No job data available.")

elif tab == "Quote Generator":
    st.header("Quote Generator")
    quote_type = st.selectbox("Repair Type", ["Foundation", "Waterproofing", "Crawlspace"])
    square_feet = st.number_input("Square Footage", min_value=0)
    base_rates = {"Foundation": 8, "Waterproofing": 6, "Crawlspace": 5}
    rate = base_rates.get(quote_type, 5)
    estimated_cost = square_feet * rate
    if st.button("Generate Quote"):
        st.success(f"Estimated cost for {quote_type} repair: ${estimated_cost:,.2f}")
    quote_path = "F:/CharlieBotData/quotes.txt"
    if st.button("Save Quote"):
        with open(quote_path, "a") as file:
            file.write(f"{quote_type} | {square_feet} sqft | ${estimated_cost:,.2f}\n")
        st.info("Quote saved.")

elif tab == "Follow-Up Reminders":
    st.header("Client Follow-Up")
    followup_name = st.text_input("Client to Follow Up With")
    from datetime import datetime, timedelta
    followup_date = st.date_input("Follow-Up Date", value=datetime.today() + timedelta(days=7))
    followup_path = "F:/CharlieBotData/followups.txt"
    if st.button("Schedule Follow-Up"):
        entry = f"{followup_date} | {followup_name}"
        with open(followup_path, "a") as file:
            file.write(entry + "\n")
        st.success("Follow-up scheduled.")
    if st.button("View Upcoming Follow-Ups"):
        if os.path.exists(followup_path):
            with open(followup_path, "r") as file:
                lines = file.readlines()
            today = datetime.today().date()
            upcoming = [line for line in lines if datetime.strptime(line.split(" | ")[0], "%Y-%m-%d").date() >= today]
            st.text_area("Upcoming Follow-Ups", "\n".join(upcoming), height=300)
        else:
            st.warning("No follow-ups scheduled.")

elif tab == "Email Drafts":
    st.header("Email Draft Assistant")
    client_email = st.text_input("Client Name or Email")
    job_summary = st.text_area("Job Summary")
    if st.button("Generate Email"):
        email = f"""Hi {client_email},\n\nJust wanted to follow up on the recent work we completed: {job_summary}.\nIf you have any questions or need additional support, feel free to reach out.\n\nThanks again for choosing us!\n\n— CharlieBot Structural & Waterproofing"""
        st.text_area("Email Draft", email, height=200)
    email_path = "F:/CharlieBotData/emails.txt"
    if st.button("Save Email"):
        with open(email_path, "a") as file:
            file.write(email + "\n\n")
        st.info("Email saved.")

elif tab == "Memory Search":
    st.header("Memory Search")
    conn = sqlite3.connect("F:/CharlieBotData/memory.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS memory (timestamp TEXT, user_input TEXT, bot_response TEXT)")
    search_term = st.text_input("Search memory")
    if st.button("Search"):
        cursor.execute("SELECT * FROM memory WHERE user_input LIKE ?", ('%' + search_term + '%',))
        results = cursor.fetchall()
        for row in results:
            st.write(f"{row[0]} — You said: {row[1]} → Bot replied: {row[2]}")

    # Example: number input for seconds, message input, start button

elif tab == "Smart Calculator":
    st.header("🧮 Smart Calculator")

    st.subheader("Enter a Math Expression")

    expression = st.text_input("Example: 12 * 8 or 2*x + 3 = 7")

    if expression:
        try:
            if "=" in expression:
                # Solve equation
                lhs, rhs = expression.split("=")
                x = sp.Symbol('x')
                solution = sp.solve(sp.Eq(eval(lhs), eval(rhs)), x)
                st.success(f"Solution: x = {solution}")
                respond(f"The solution is x equals {solution[0]}")
            else:
                # Evaluate expression
                result = eval(expression)
                st.success(f"Result: {result}")
                respond(f"The result is {result}")
        except Exception as e:
            st.error("Invalid expression. Try something like 12 * 8 or 2*x + 3 = 7.")
            respond("Sorry, I couldn't understand that expression.")

    # Example: math expression input, solve button, result display

elif tab == "Master Coder Mode":
    st.header("👨‍💻 Master Coder Mode")
    st.subheader("Explain or Generate Python Code")

    mode = st.radio("Choose your mode", ["Beginner", "Expert"])
    topic = st.text_input("Enter a coding topic or snippet", value="for loop in Python")

    if st.button("Explain"):
        if mode == "Beginner":
            explanation = f"""
            A **for loop** in Python lets you repeat actions for each item in a list or range.
            
            Example:
            ```python
            for i in range(5):
                print(i)
            ```
            This prints numbers 0 to 4. The loop runs once for each number in `range(5)`.
            """
        else:
            explanation = f"""
            A **for loop** in Python is syntactic sugar for iterable traversal.
            
            Example:
            ```python
            for item in iterable:
                # process item
            ```
            Internally, it calls `iter()` and `next()` on the object until `StopIteration` is raised.
            """

        st.markdown(explanation)
        respond("Explanation complete.")

elif tab == "Agent Mode":
    st.header("🔄 Agent Mode")
    st.subheader("Permission-Based Actions")

    st.markdown("CharlieBot can perform tasks on your behalf — but only with your permission.")

    # Toggle permissions
    delete_duplicates = st.checkbox("Allow CharlieBot to delete duplicate files")
    log_job = st.checkbox("Allow CharlieBot to log a new job")
    send_email = st.checkbox("Allow CharlieBot to draft and send follow-up emails")

    # Action buttons
    if delete_duplicates and st.button("Delete Duplicates"):
        respond("Deleting duplicate files now.")
        st.success("Duplicates deleted. (Placeholder logic)")

    if log_job and st.button("Log Job"):
        respond("Logging job now.")
        st.success("Job logged. (Placeholder logic)")

    if send_email and st.button("Send Follow-Up Email"):
        respond("Sending email now.")
        st.success("Email sent. (Placeholder logic)")

    # Example: toggle for Assistant vs Agent, buttons for sending emails, deleting files, etc.

elif tab == "Photo Organizer":
    st.header("🖼️ Photo Organizer")
    st.subheader("📸 Photo Organizer")

    import os
    import shutil
    import datetime

    # Inputs
    photo_folder = st.text_input("Enter photo folder path", value="F:/CharlieBotData/photos")
    date_filter = st.date_input("Filter images modified after:")
    detect_faces = st.checkbox("Enable face detection (placeholder)")
    auto_sort = st.checkbox("Auto-sort into work and personal folders")

    if st.button("Scan Folder"):
        if os.path.exists(photo_folder):
            files = os.listdir(photo_folder)
            image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

            # Apply date filter
            if date_filter:
                cutoff = datetime.datetime.combine(date_filter, datetime.datetime.min.time())
                image_files = [
                    f for f in image_files
                    if datetime.datetime.fromtimestamp(
                        os.path.getmtime(os.path.join(photo_folder, f))
                    ) > cutoff
                ]

            st.success(f"Found {len(image_files)} image files.")
            respond(f"I found {len(image_files)} images in your folder.")

            # Detect duplicates by filename
            duplicates = []
            seen = set()
            for img in image_files:
                if img in seen:
                    duplicates.append(img)
                else:
                    seen.add(img)

            # Detect duplicates by file size
            size_map = {}
            size_duplicates = []
            for img in image_files:
                path = os.path.join(photo_folder, img)
                size = os.path.getsize(path)
                if size in size_map:
                    size_duplicates.append(img)
                else:
                    size_map[size] = img

            # Display duplicates
            if duplicates or size_duplicates:
                st.warning("Duplicate files detected:")
                for dup in set(duplicates + size_duplicates):
                    st.write(dup)
                respond("I found duplicate files in your folder.")
            else:
                st.info("No duplicates found.")
                respond("No duplicates found.")

            # Face detection placeholder
            if detect_faces:
                respond("Face detection is not yet implemented, but it's coming soon.")
                st.info("Face detection placeholder activated.")

            # Auto-sort logic
            if auto_sort:
                work_dir = os.path.join(photo_folder, "work_photos")
                personal_dir = os.path.join(photo_folder, "personal_photos")
                os.makedirs(work_dir, exist_ok=True)
                os.makedirs(personal_dir, exist_ok=True)

                for img in image_files:
                    if "job" in img.lower() or "site" in img.lower() or "repair" in img.lower():
                        shutil.move(os.path.join(photo_folder, img), os.path.join(work_dir, img))
                    else:
                        shutil.move(os.path.join(photo_folder, img), os.path.join(personal_dir, img))

                st.success("Photos sorted into work and personal folders.")
                respond("Photos have been sorted into work and personal folders.")
        else:
            st.error("Folder not found. Check the path and try again.")
            respond("I couldn't find that folder.")

    # Example: folder selector, date filter, face detection toggle, duplicate scan button

import streamlit as st

st.title("CharlieBot: Home Repair Ad Assistant")

job_type = st.text_input("What kind of job did you complete?")
location = st.text_input("Where was it?")
detail = st.text_input("Any cool detail or challenge you solved?")

if st.button("Generate Ad"):
    ad = f"Just finished a {job_type} in {location}. {detail}. If your home needs structural help or waterproofing, give us a call!"
    st.success(ad)
import os

save_path = "/mnt/f/CharlieBotData/ads.txt"

if st.button("Save Ad"):
    with open(save_path, "a") as file:
        file.write(ad + "\n\n")
    st.info("Ad saved to your archive.")
if st.button("View Saved Ads"):
    if os.path.exists(save_path):
        with open(save_path, "r") as file:
            ads = file.read()
        st.text_area("Your Saved Ads", ads, height=300)
    else:
        st.warning("No ads saved yet.")
st.header("Job Tracker")

client_name = st.text_input("Client Name")
job_location = st.text_input("Job Location")
job_type = st.selectbox("Type of Repair", ["Foundation", "Waterproofing", "Crawlspace", "Other"])
job_date = st.date_input("Date of Job")

job_log_path = "/mnt/f/CharlieBotData/jobs.txt"

if st.button("Log Job"):
    job_entry = f"{job_date} | {client_name} | {job_location} | {job_type}"
    with open(job_log_path, "a") as file:
        file.write(job_entry + "\n")
    st.success("Job logged successfully.")

if st.button("View Job History"):
    if os.path.exists(job_log_path):
        with open(job_log_path, "r") as file:
            jobs = file.read()
        st.text_area("Logged Jobs", jobs, height=300)
    else:
        st.warning("No jobs logged yet.")
import random

tips = [
    "Fall is coming — offer gutter sealing and foundation checks before the rain hits.",
    "Bundle waterproofing with mold inspection for added value.",
    "Offer a free crawlspace inspection with every foundation repair.",
    "Post before/after photos to build trust in local Facebook groups.",
    "Use yard signs after each job to build neighborhood visibility."
]

if st.button("Get Business Tip"):
    st.info(random.choice(tips))
from datetime import datetime, timedelta

followup_path = "/mnt/f/CharlieBotData/followups.txt"

st.header("Client Follow-Up")

followup_name = st.text_input("Client to Follow Up With")
followup_date = st.date_input("Follow-Up Date", value=datetime.today() + timedelta(days=7))

if st.button("Schedule Follow-Up"):
    entry = f"{followup_date} | {followup_name}"
    with open(followup_path, "a") as file:
        file.write(entry + "\n")
    st.success("Follow-up scheduled.")

if st.button("View Upcoming Follow-Ups"):
    if os.path.exists(followup_path):
        with open(followup_path, "r") as file:
            lines = file.readlines()
        today = datetime.today().date()
        upcoming = [line for line in lines if datetime.strptime(line.split(" | ")[0], "%Y-%m-%d").date() >= today]
        st.text_area("Upcoming Follow-Ups", "\n".join(upcoming), height=300)
    else:
        st.warning("No follow-ups scheduled.")
st.header("Quote Generator")

quote_type = st.selectbox("Repair Type", ["Foundation", "Waterproofing", "Crawlspace"])
square_feet = st.number_input("Square Footage", min_value=0)

base_rates = {"Foundation": 8, "Waterproofing": 6, "Crawlspace": 5}
rate = base_rates.get(quote_type, 5)
estimated_cost = square_feet * rate

if st.button("Generate Quote"):
    st.success(f"Estimated cost for {quote_type} repair: ${estimated_cost:,.2f}")
st.header("Email Draft Assistant")

client_email = st.text_input("Client Name or Email")
job_summary = st.text_area("Job Summary")

if st.button("Generate Email"):
    email = f"""Hi {client_email},

Just wanted to follow up on the recent work we completed: {job_summary}.
If you have any questions or need additional support, feel free to reach out.

Thanks again for choosing us!

— CharlieBot Structural & Waterproofing"""
    st.text_area("Email Draft", email, height=200)
import pandas as pd

if st.button("View Job Stats"):
    if os.path.exists(job_log_path):
        df = pd.read_csv(job_log_path, sep="|", header=None, names=["Date", "Client", "Location", "Type"])
        job_counts = df["Type"].value_counts()
        st.bar_chart(job_counts)
    else:
        st.warning("No job data available.")
mode = st.radio("Choose Mode", ["Assistant", "Agent"])

if mode == "Assistant":
    st.info("CharlieBot will suggest ideas and guide you step-by-step.")
else:
    st.success("CharlieBot is now in Agent mode — ready to perform tasks with your permission.")
import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def listen_and_respond():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            response = f"I heard you say: {command}. What would you like me to do next?"
            engine.say(response)
            engine.runAndWait()
        except sr.UnknownValueError:
            engine.say("Sorry, I didn't catch that.")
            engine.runAndWait()
import sympy as sp

expr = st.text_input("Enter a math expression (e.g., 2*x + 3 = 7)")
if st.button("Solve"):
    x = sp.Symbol('x')
    solution = sp.solve(expr, x)
    st.success(f"Solution: {solution}")
import sqlite3

conn = sqlite3.connect("F:/CharlieBotData/memory.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS memory (timestamp TEXT, user_input TEXT, bot_response TEXT)")

def save_memory(user_input, bot_response):
    cursor.execute("INSERT INTO memory VALUES (datetime('now'), ?, ?)", (user_input, bot_response))
    conn.commit()
search_term = st.text_input("Search memory")
if st.button("Search"):
    cursor.execute("SELECT * FROM memory WHERE user_input LIKE ?", ('%' + search_term + '%',))
    results = cursor.fetchall()
    for row in results:
        st.write(f"{row[0]} — You said: {row[1]} → Bot replied: {row[2]}")
if mode == "Agent" and st.button("Send Email"):
    # perform action
save_path = "/mnt/f/CharlieBotData/ads.txt"
job_log_path = "/mnt/f/CharlieBotData/jobs.txt"
    followup_path = "/mnt/f/CharlieBotData/followups.txt"
    st.success("Email sent successfully.")
followup_path = "/mnt/f/CharlieBotData/followups.txt"
quote_path = "/mnt/f/CharlieBotData/quotes.txt"
if st.button("Save Quote"):
    with open(quote_path, "a") as file:
        file.write(f"{quote_type} | {square_feet} sqft | ${estimated_cost:,.2f}\n")
    st.info("Quote saved.")
email_path = "/mnt/f/CharlieBotData/emails.txt"
if st.button("Save Email"):
    with open(email_path, "a") as file:
        file.write(email + "\n\n")
    st.info("Email saved.")
import sqlite3

conn = sqlite3.connect("/mnt/f/CharlieBotData/memory.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS memory (timestamp TEXT, user_input TEXT, bot_response TEXT)")

def save_memory(user_input, bot_response):
    cursor.execute("INSERT INTO memory VALUES (datetime('now'), ?, ?)", (user_input, bot_response))
    conn.commit()
import threading
import time

def set_timer(seconds, message):
    def alarm():
        time.sleep(seconds)
        st.warning(f"⏰ Alarm: {message}")
    threading.Thread(target=alarm).start()

timer_seconds = st.number_input("Set timer (seconds)", min_value=1)
timer_message = st.text_input("Alarm message")

if st.button("Start Timer"):
    set_timer(timer_seconds, timer_message)
    st.success(f"Timer set for {timer_seconds} seconds.")
import sympy as sp

st.header("Smart Calculator")

calc_input = st.text_input("Enter a math expression (e.g., 2*x + 3 = 7)")
x = sp.Symbol('x')

if st.button("Solve Expression"):
    try:
        solution = sp.solve(calc_input, x)
        st.success(f"Solution: {solution}")
    except Exception as e:
        st.error(f"Error: {e}")
coder_mode = st.checkbox("Enable Master Coder Mode")

if coder_mode:
    st.info("CharlieBot will now explain every coding step in full detail.")
if coder_mode:
    st.markdown("""
    **Step 1:** Import necessary libraries  
    `import streamlit as st` — This loads the Streamlit interface tools.

    **Step 2:** Create input fields  
    `st.text_input()` lets users type in job details.

    **Step 3:** Generate ad copy  
    We use Python's f-strings to format the ad dynamically.
    """)
mode = st.radio("Choose Mode", ["Assistant", "Agent"])

if mode == "Agent":
    if st.button("Send Email to Client"):
        # Add SMTP logic here
        st.success("Email sent.")
    if st.button("Auto-Save Job"):
        # Save to jobs.txt
        st.info("Job saved automatically.")
else:
    st.info("CharlieBot is in Assistant mode — no tasks will be performed without permission.")
import os
from PIL import Image
import streamlit as st

st.header("📸 Photo Organizer")

photo_type = st.radio("Choose photo category", ["Personal", "Work"])
photo_folder = f"/mnt/f/CharlieBotData/Photos/{photo_type}"

filter_date = st.date_input("Filter by date")
show_faces = st.checkbox("Show only photos with faces (Personal only)")

photos = [f for f in os.listdir(photo_folder) if f.endswith((".jpg", ".png"))]

for photo in photos:
    photo_path = os.path.join(photo_folder, photo)
    img = Image.open(photo_path)
    # Optional: Add face detection logic here
    st.image(img, caption=photo, use_column_width=True)
st.sidebar.title("CharlieBot Modules")
tab = st.sidebar.radio("Choose a module", [
    "Ad Assistant",
    "Job Tracker",
    "Quote Generator",
    "Follow-Up Reminders",
    "Email Drafts",
    "Smart Calculator",
    "Voice Assistant",
    "Photo Organizer",
    "Agent Mode"
])
import os
from PIL import Image
import streamlit as st

st.header("📸 Photo Organizer")

photo_type = st.radio("Choose photo category", ["Personal", "Work"])
photo_folder = f"/mnt/f/CharlieBotData/Photos/{photo_type}"

filter_date = st.date_input("Filter by date")
show_faces = st.checkbox("Show only photos with faces (Personal only)")

photos = [f for f in os.listdir(photo_folder) if f.endswith((".jpg", ".png"))]

for photo in photos:
    photo_path = os.path.join(photo_folder, photo)
    img = Image.open(photo_path)
    # Optional: Add face detection logic here
    st.image(img, caption=photo, use_column_width=True)
st.sidebar.title("CharlieBot Modules")
tab = st.sidebar.radio("Choose a module", [
    "Ad Assistant",
    "Job Tracker",
    "Quote Generator",
    "Follow-Up Reminders",
    "Email Drafts",
    "Smart Calculator",
    "Voice Assistant",
    "Photo Organizer",
    "Agent Mode"
])
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

# List available voices
for i, voice in enumerate(voices):
    print(f"{i}: {voice.name}")

# Set chosen voice
engine.setProperty('voice', voices[chosen_index].id)
engine.say("Hello Charlie, I'm ready to help.")
engine.runAndWait()
import hashlib

def get_image_hash(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def scan_for_duplicates(folder):
    hashes = {}
    duplicates = []
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        if os.path.isfile(path):
            img_hash = get_image_hash(path)
            if img_hash in hashes:
                duplicates.append(path)
            else:
                hashes[img_hash] = path
    return duplicates
import schedule
import time

def daily_photo_scan():
    # Run duplicate check, metadata fix, and tagging
    pass

schedule.every(24).hours.do(daily_photo_scan)

while True:
    schedule.run_pending()
    time.sleep(1)
if mode == "Agent":
    if st.button("Run Daily Scan"):
        # Perform scan and prompt for actions
        st.success("Scan complete. Ready to clean up duplicates.")
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[chosen_index].id)
engine.setProperty('rate', 150)  # Adjust speed
engine.setProperty('volume', 1.0)
def set_timer(seconds, message):
    def alarm():
        time.sleep(seconds)
        engine.say(f"Alarm: {message}")
        engine.runAndWait()
    threading.Thread(target=alarm).start()
expr = st.text_input("Enter expression (e.g., 2*x + 3 = 7)")
solution = sp.solve(expr, x)
if coder_mode:
    st.markdown("""
    **Step 1:** Import libraries  
    `import streamlit as st` — loads UI tools.

    **Step 2:** Create input fields  
    `st.text_input()` lets users enter data.
    """)
if mode == "Agent":
    if st.button("Delete duplicate photos"):
        st.warning("Are you sure?")
        # Perform action only if confirmed
def scan_photos():
    # Check EXIF, correct dates, detect duplicates
    # Save results to photo_log.txt
def listen_for_wake_word():
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        command = recognizer.recognize_google(audio)
        if "hey charliebot" in command.lower():
            launch_charliebot()
import speech_recognition as sr
import threading

recognizer = sr.Recognizer()

def listen_loop():
    with sr.Microphone() as source:
        while True:
            try:
                print("Listening...")
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")
                if "set a timer for" in command:
                    words = command.split()
                    try:
                        # Extract number and unit
                        index = words.index("for") + 1
                        duration = int(words[index])
                        unit = words[index + 1]

                        # Convert to seconds
                        if "minute" in unit:
                            seconds = duration * 60
                        elif "second" in unit:
                            seconds = duration
                        else:
                            respond("I only support seconds or minutes for now.")
                            continue

                        respond(f"Timer set for {duration} {unit}.")
                        set_timer(seconds, f"{duration} {unit} timer")
                    except Exception as e:
                        respond("Sorry, I couldn't understand the timer duration.")

                if "charliebot" in command:
                    print("Wake word detected.")
                    # You can expand this to trigger specific actions
                elif "set a timer" in command:
                    print("Timer command detected.")
                    # Add timer logic here
                elif "quote" in command:
                    print("Quote command detected.")
                    # Add quote logic here

            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                print("Voice recognition is offline.")
                break
threading.Thread(target=listen_loop, daemon=True).start()
with open("F:/CharlieBotData/voice_log.txt", "a") as log:
    log.write(f"{command}\n")
def listen_loop():
    with sr.Microphone() as source:
        while True:
            try:
                print("Listening...")
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")

                # Log command
                with open("F:/CharlieBotData/voice_log.txt", "a") as log:
                    log.write(f"{command}\n")

                # Wake word
                if "charliebot" in command:
                    respond("Yes Charlie, I'm listening.")

                # Explain coding topic
                elif "explain" in command:
                    topic = command.replace("explain", "").strip()
                    respond(f"Explaining {topic}")

                    if "list comprehension" in topic:
                        explanation = "List comprehensions are a concise way to create lists in Python. Example: [x for x in range(5)]"
                        respond(explanation)
                    elif "lambda" in topic:
                        explanation = "Lambda functions are anonymous functions. Example: lambda x: x * 2"
                        respond(explanation)
                    else:
                        respond("Sorry, I don't have an explanation for that yet.")

                # Set timer
                elif "set a timer for" in command:
                    words = command.split()
                    try:
                        index = words.index("for") + 1
                        duration = int(words[index])
                        unit = words[index + 1]

                        if "minute" in unit:
                            seconds = duration * 60
                        elif "second" in unit:
                            seconds = duration
                        else:
                            respond("I only support seconds or minutes for now.")
                            continue

                        respond(f"Timer set for {duration} {unit}.")
                        set_timer(seconds, f"{duration} {unit} timer")
                    except Exception:
                        respond("Sorry, I couldn't understand the timer duration.")

                # Quote logic placeholder
                elif "quote" in command:
                    respond("Let me calculate that for you.")
                    # Add quote logic here

                # Scan photo folder
                elif "scan photo folder" in command:
                    respond("Scanning your photo folder now.")
                    # You can trigger a scan or set a flag here

            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                respond("Voice recognition is offline.")
                break

# Start voice listener in background
threading.Thread(target=listen_loop, daemon=True).start()
