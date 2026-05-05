
# =======================
# app_streamlit.py (Updated with your design requests)
# =======================
import base64
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from model_logic import plot_predictions
import os
import streamlit as st
import requests


# Page Config
# -----------------------
st.set_page_config(page_title="EcoTrack", layout="wide")


# -----------------------
# Helper: set background
# -----------------------
def set_background(image_file):
    try:
        with open(image_file, "rb") as f:
            data = f.read()
        encoded = base64.b64encode(data).decode()
        st.markdown(
            f"""
            <style>
            [data-testid="stAppViewContainer"] {{
                background: url("data:image/jpeg;base64,{encoded}") no-repeat center center fixed;
                background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
    except Exception as e:
        st.warning(f"Could not load background '{image_file}': {e}")

# -----------------------
# Load dataset
# -----------------------
@st.cache_data
def load_csv():
    df = pd.read_csv("EcoTrack_Waste_Bins_Dataset.csv")
    if "Start_Date" in df.columns:
        df["Start_Date"] = pd.to_datetime(df["Start_Date"], format="%d-%m-%Y", errors="coerce")
    if "Fill_Duration(days)" in df.columns:
        df["Fill_Duration(days)"] = pd.to_numeric(df["Fill_Duration(days)"], errors="coerce")
    return df, sorted(df["Location_Name"].dropna().unique()), sorted(df["Zone_Type"].dropna().unique())

df, locations, zones = load_csv()

# -----------------------
# Session State
# -----------------------
if "page" not in st.session_state:
    st.session_state.page = 0

def go_to_page(n):
    st.session_state.page = n

def navigation_buttons(show_back=True, show_next=True):
    col_left, col_space, col_right = st.columns([1, 6, 1])

    st.markdown(
        """
        <style>
        /* Force override Streamlit default styles */
        div.stButton > button {
            background-color: #444444 !important;  
            color: white !important;
            border: none !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            border-radius: 10px !important;
            width: 100% !important;
            height: 45px !important;
            transition: all 0.25s ease !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.25) !important;
        }
        div.stButton > button:hover {
            background-color: #45a049 !important; /* hover color */
            transform: scale(1.05);
            box-shadow: 0 6px 14px rgba(0,0,0,0.3);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with col_left:
        if show_back:
            st.button("← Back", on_click=lambda: st.session_state.update(page=max(0, st.session_state.page - 1)))

    with col_right:
        if show_next:
            st.button("Next →", on_click=lambda: st.session_state.update(page=min(3, st.session_state.page + 1)))



# -----------------------
# Page 0 - Home
# -----------------------
if st.session_state.page == 0:
    set_background("images/background_home.jpg")
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Poppins:wght@400;600&display=swap');
        .eco-title {
            font-family: 'Great Vibes', cursive !important;
            font-size: 90px !important;
            font-weight: bold;
            text-align: center;
            color: #444444;
            margin-top: 40px;
            text-shadow: 6px 6px 14px rgba(0,0,0,0.75);
        }
        .eco-box {
            width: 80%;
            margin: 20px auto;
            padding: 20px 30px;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 6px 18px rgba(0,0,0,0.25);
            font-family: 'Poppins', sans-serif;
            font-size: 18px;
            color: #222;
            background: rgba(255,255,255,0.92);
            border:2px solid #444444
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='eco-title'>Welcome to EcoTrack</div>", unsafe_allow_html=True)
    st.markdown("<div class='eco-box'>EcoTrack is an intelligent waste management system designed to make cities cleaner, smarter, and more sustainable.</div>", unsafe_allow_html=True)

    st.markdown("<div class='eco-box'>It combines the power of IoT and Machine Learning to monitor bin levels, predict waste accumulation, and assist authorities in timely collection.</div>", unsafe_allow_html=True)

    st.markdown("<div class='eco-box'>Our platform delivers real-time insights and promotes responsible waste segregation — paving the way for a greener Bengaluru.</div>", unsafe_allow_html=True)

    st.markdown("<div class='eco-box'>Together, we can revolutionize urban cleanliness and move closer to a zero-waste future.</div>", unsafe_allow_html=True)

    navigation_buttons(show_back=False, show_next=True)

# # -----------------------
# Page 1 - Team
# -----------------------
elif st.session_state.page == 1:
    set_background("images/background_home.jpg")

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Poppins:wght@400;700&display=swap');
        .project-title {
            font-family: 'Great Vibes', cursive !important;
            font-size: 80px !important;
            font-weight: bold;
            text-align:center;
            color:#444444;
            text-shadow:5px 5px 12px rgba(0,0,0,0.6);
            margin-top:20px;
        }
        .meet-title {
            font-family: 'Poppins', sans-serif !important;
            font-size:30px;
            font-weight:600;
            color:#444444;
            text-align:center;
            margin-top:18px;
        }
        .member-box {
            background: rgba(255,255,255,0.95);
            border-radius:16px;
            padding:26px;
            margin:16px;
            box-shadow:0 6px 20px rgba(0,0,0,0.3);
            text-align:center;
            transition: transform 0.2s ease;
            border:2px solid #444444
        }
        .member-box:hover {
            transform: scale(1.05);
        }
        .member-name {
            font-family: 'Poppins', sans-serif;
            font-weight:700;
            font-size:20px;
            color:#111;
            margin-bottom:8px;
        }
        .member-link a {
            color: #0077b5;
            font-weight: 600;
            text-decoration: none;
        }
        .member-link a:hover {
            text-decoration: underline;
        }
        .member-email {
            color:#333;
            font-size:16px;
            margin-top:8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='project-title'>EcoTrack</div>", unsafe_allow_html=True)
    st.markdown("<div class='meet-title'>Meet The Team</div>", unsafe_allow_html=True)

    # 👥 Team member data (Name + LinkedIn + Email)
    team_members = [
        {"name": "Prajwal B S", "linkedin": "https://www.linkedin.com/in/prajwal-bs-489182262", "email": "prajwal@example.com"},
        {"name": "Sneha M D", "linkedin": "https://www.linkedin.com/in/sneha-m-d-0b43992b5/", "email": "sneha@example.com"},
        {"name": "Harshitha R Gowda", "linkedin": "https://www.linkedin.com/in/harshitha-r-gowda-57a350333", "email": "harshitha@example.com"},
        {"name": "Shashank Harihar", "linkedin": "https://www.linkedin.com/in/shashank-harihar-381642357", "email": "shashank@example.com"},
    ]

    # Display team members in two columns
    cols = st.columns(2)
    for i, member in enumerate(team_members):
        col = cols[i % 2]
        col.markdown(
            f"""
            <div class="member-box">
                <div class="member-name">{member['name']}</div>
                <div class="member-link">🔗 <a href="{member['linkedin']}" target="_blank">LinkedIn</a></div>
                <div class="member-email">📧 {member['email']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Navigation buttons at bottom
    navigation_buttons()


# ========================
# Page 2 - Features
# ========================
elif st.session_state.page == 2:
    set_background("images/background_home.jpg")

    # --- Title styled same as Page 0 ---
    st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Poppins:wght@400;600&display=swap');

    .eco-title {
        font-family: 'Great Vibes', cursive !important;
        font-size: 90px !important;
        font-weight: bold;
        text-align: center;
        color: #444444;
        margin-top: 40px;
        text-shadow: 6px 6px 14px rgba(0,0,0,0.75);
    }

    /* --- Tab container style --- */
    .stTabs [data-baseweb="tab-list"] {
        justify-content: center;
        gap: 25px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff; /* White box */
        border: 2px solid #0f5132; /* Dark green border */
        border-radius: 16px;
        padding: 18px 32px;
        font-size: 26px; /* Increased font size */
        font-weight: 700;
        color: #0f5132; /* Dark green text */
        transition: all 0.3s ease;
    }

    /* Selected tab style */
    .stTabs [aria-selected="true"] {
        background-color: #0f5132; /* Dark green background when active */
        color: #ffffff !important; /* White text when active */
        border-color: #0f5132;
        box-shadow: 0 0 15px rgba(15,81,50,0.6);
    }

    /* Tab content box */
    .stTabs [data-baseweb="tab-panel"] {
        background-color: rgba(255, 255, 255, 0.85); /* Light white content area */
        padding: 35px;
        border-radius: 20px;
        margin-top: 25px;
        color: #000000; /* Ensure content text is visible */
    }
    </style>

    <div class='eco-title'>EcoTrack Features</div>
    """,
    unsafe_allow_html=True
)

    # --- Tabs Section ---
    tab1, tab2, tab3 = st.tabs(["Bin Fill Prediction", "EcoBot", "Waste Management Tips"])
    
    # -----------------------
    # TAB 1 - Bin Fill Prediction
    # -----------------------
    with tab1:
        st.subheader("Predict Bin Fill Levels")

        # --- Custom Styling for labels, inputs, buttons, messages, and table ---
        st.markdown(
            """
            <style>
            /* Label text */
            label, .stMarkdown p, .stTextInput label, .stSelectbox label {
                color: black !important;
                font-weight: 600 !important;
            }

            /* Input boxes (date, select) green background with white text */
            div[data-baseweb="input"] input,
            div[data-baseweb="select"] > div {
                background-color: #2e7d32 !important;  /* Dark green */
                color: white !important;
                border-radius: 10px;
                border: 2px solid #1b5e20;
            }

            div[data-baseweb="select"] span {
                color: white !important;
            }

            /* Predict Button Styling */
            div.stButton > button {
                background-color: #43a047 !important;
                color: white !important;
                font-size: 18px !important;
                font-weight: bold !important;
                border-radius: 10px !important;
                border: 2px solid #1b5e20 !important;
                height: 45px !important;
                width: 220px !important;
                transition: all 0.3s ease !important;
            }
            div.stButton > button:hover {
                background-color: #66bb6a !important;
                color: white !important;  /* keep text white on hover */
                transform: scale(1.05);
            }

            /* Success message styling */
            div.stAlert.stAlert.success {
                color: black !important;               /* text color */
                background-color: #c8e6c9 !important;  /* light green background */
                font-weight: 600;
                border-radius: 8px;
                padding: 10px;
            }


            /* Download button styling */
            div.stDownloadButton > button {
                background-color: #43a047 !important;
                color: white !important;
                font-weight: bold !important;
                border-radius: 10px !important;
                border: 2px solid #1b5e20 !important;
                height: 45px !important;
                width: 250px !important;
                font-size: 16px !important;
                transition: all 0.3s ease !important;
            }
            div.stDownloadButton > button:hover {
                background-color: #66bb6a !important;
                color: #ffffff !important;
                transform: scale(1.05);
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # --- Inputs ---
        api_url = "http://127.0.0.1:8000/predict/"

        start_date = st.date_input("Select Start Date")
        location = st.selectbox("Select Location", locations)
        zone = st.selectbox("Select Zone Type", zones)

        # --- Prediction Button ---
        if st.button("Predict Fill Dates"):
            try:
                params = {
                    "start_date": start_date.strftime("%d-%m-%Y"),
                    "location": location,
                    "zone": zone,
                }

                with st.spinner("Fetching predictions..."):
                    response = requests.get(api_url, params=params)

                if response.status_code == 200:
                    result = response.json()
                    df_pred = pd.DataFrame(result)
                    
                    # Success message
                    st.success("Prediction successful!")

                    # Display DataFrame with green theme
                    st.dataframe(
                        df_pred.style.set_table_styles([
                            {'selector': 'th', 'props': [
                                ('background-color', '#1b5e20'),
                                ('color', 'white'),
                                ('font-weight', 'bold'),
                                ('text-align', 'center')
                            ]},
                            {'selector': 'td', 'props': [
                                ('background-color', '#a5d6a7'),
                                ('color', '#0b3d00'),
                                ('text-align', 'center')
                            ]}
                        ]),
                        use_container_width=True
                    )

                    # Download CSV
                    csv = df_pred.to_csv(index=False).encode()
                    st.download_button(
                        "Download Predictions as CSV",
                        csv,
                        "EcoTrack_Predictions.csv",
                        "text/csv"
                    )

                    # =======================
                    # Bin Predictions Overview (Moved Up)
                    # =======================
                    st.markdown("## 🗑️ Bin Predictions Overview")

                    st.markdown(
                        """
                        <div style='background-color:#1a3d2b; padding:15px; border-radius:10px; color:white; width:80%; margin:auto'>
                            <b>Color Coding Criteria:</b><br>
                            🟢 <b>Green</b> = Safe (> 5 days to fill)<br>
                            🟡 <b>Yellow</b> = Moderate (3–5 days to fill)<br>
                            🔴 <b>Red</b> = Urgent (< 3 days to fill)
                        </div><br>
                        """,
                        unsafe_allow_html=True
                    )

                    # Helper: choose color
                    def get_color(duration):
                        if duration > 5:
                            return "#00c853"  # Green
                        elif 3 <= duration <= 5:
                            return "#ffeb3b"  # Yellow
                        else:
                            return "#e53935"  # Red

                    # Create visual grid
                    cols = st.columns(5)
                    for i, row in df_pred.iterrows():
                        color = get_color(row["Predicted_Fill_Duration(days)"])
                        col = cols[i % 5]
                        with col:
                            st.markdown(
                                f"""
                                <div style="
                                    background-color: rgba(255,255,255,0.9);
                                    border-radius:12px;
                                    padding:10px;
                                    text-align:center;
                                    box-shadow:0 3px 6px rgba(0,0,0,0.2);
                                    margin-bottom:10px;
                                ">
                                    <div style="
                                        background-color:{color};
                                        width:35px;
                                        height:35px;
                                        border-radius:50%;
                                        margin:auto;
                                        margin-bottom:8px;
                                        border:2px solid #333;
                                    "></div>
                                    <b style='font-size:14px;'>ID: {row["Bin_ID"]}</b><br>
                                    <span style='font-size:13px;'>Duration: {row["Predicted_Fill_Duration(days)"]} days</span>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                    # =======================
                    # Compute Actuals and Plot
                    # =======================
                    actuals = []
                    for b in df_pred["Bin_ID"]:
                        g = df[df["Bin_ID"] == b].sort_values("Start_Date")
                        if not g.empty:
                            actuals.append(g["Fill_Duration(days)"].values[-1])
                        else:
                            actuals.append(None)
                    df_pred["Actual_Fill_Duration(days)"] = actuals

                    # --- Plot Predicted vs Actual ---
                    if "Predicted_Fill_Duration(days)" in df_pred.columns and "Actual_Fill_Duration(days)" in df_pred.columns:
                        fig, ax = plt.subplots(figsize=(8, 4))

                        # Predicted in green
                        ax.plot(
                            df_pred["Bin_ID"],
                            df_pred["Predicted_Fill_Duration(days)"],
                            marker="o",
                            color="green",
                            label="Predicted Fill Duration"
                        )

                        # Actual in black
                        ax.plot(
                            df_pred["Bin_ID"],
                            df_pred["Actual_Fill_Duration(days)"],
                            marker="x",
                            color="black",
                            label="Actual Fill Duration"
                        )

                        ax.set_xlabel("Bin ID")
                        ax.set_ylabel("Fill Duration (days)")
                        ax.set_title("Bin Fill Duration: Predicted vs Actual")
                        ax.legend()
                        ax.grid(True, linestyle="--", alpha=0.5)
                        st.pyplot(fig)
                    else:
                        st.warning("Expected columns 'Predicted_Fill_Duration(days)' and 'Actual_Fill_Duration(days)' not found in the dataset.")

                else:
                    st.error("Backend error: could not get prediction data.")

            except Exception as e:
                st.error(f"Error fetching prediction: {e}")


# -----------------------
# TAB 2 - Know About EcoTrack (FAQ-based)
# -----------------------
    with tab2:
        st.subheader("💡 Know About EcoTrack — Smart Waste Management System")

        # Initialize chat history
        if "faq_history" not in st.session_state:
            st.session_state.faq_history = []

        # Predefined Q&A from your presentation
        faq_data = {
            "what is ecotrack": "EcoTrack is a smart waste monitoring and collection system using IoT and Machine Learning to keep cities clean and sustainable.",
            "what problem does ecotrack solve": "It addresses urban waste challenges like overflowing bins and delayed pickups by enabling real-time monitoring and predictive collection.",
            "what sensors are used": "EcoTrack uses ultrasonic, moisture, rain, and gas sensors to monitor bin fill level, humidity, gas leakage, and water entry.",
            "how does the system send alerts": "When waste is dumped outside the bin or when sensors detect overflow, gas, or rainwater, a buzzer is triggered and alerts are sent to the municipal authority through the app/dashboard.",
            "how does ecotrack use machine learning": "EcoTrack uses an ARIMA model to analyze historical waste data and predict future bin fill levels, helping authorities plan efficient collection routes.",
            "what is the role of the mobile app": "The mobile app/dashboard displays bin status, alerts, and predicted fill levels, helping authorities monitor the system remotely.",
            "what is the communication medium": "Data from sensors is transmitted via a Bluetooth module connected to an Arduino microcontroller, which communicates with the mobile app/dashboard.",
            "how does ecotrack help the environment": "It prevents waste overflow, reduces pollution, optimizes fuel use through predictive routing, and promotes public responsibility for cleanliness.",
            "what are the main features": "EcoTrack features include real-time monitoring, predictive waste collection, moisture and gas alerts, rain detection, and mobile notifications.",
            "what machine learning model is used": "ARIMA (AutoRegressive Integrated Moving Average) is used for time-series prediction of bin fill levels.",
            "what are the benefits of ecotrack": "It enables early waste collection, ensures hygiene, prevents gas-related hazards, saves fuel, and promotes sustainability in urban areas.",
            "who guides the project": "The project was carried out under the guidance of Mrs. Shridevi Sali, Assistant Professor, AIML Department, SJBIT.",
            "who are the team members": "The project was developed by Harshitha R Gowda, Sneha M D, Prajwal B S, and Shashank Harihar from the AIML Department, SJBIT.",
            "what is the main goal": "The goal is to make waste management smarter, safer, and more efficient through IoT-driven automation and predictive analytics.",
            "how does the alert mechanism work": "A buzzer and notification system triggers alerts when bins reach 80% capacity, detect gases, moisture, or rainwater entry, ensuring timely action.",
            "how does predictive collection work": "Machine learning predicts when bins will fill, allowing authorities to plan optimized routes and avoid overflow.",
            "how does ecotrack contribute to smart cities": "EcoTrack supports sustainability goals by reducing waste overflow, improving route efficiency, and fostering environmental responsibility."
        }

        # Function to find best match using fuzzy matching
        from difflib import get_close_matches

        def find_best_answer(user_question):
            question = user_question.lower()
            keys = list(faq_data.keys())
            match = get_close_matches(question, keys, n=1, cutoff=0.4)  # approximate matching
            if match:
                return faq_data[match[0]]
            else:
                return "Sorry, I don't have an exact answer for that. Please try asking about sensors, ML model, or system working."

        # User input
        user_input = st.text_input("Ask something about the EcoTrack project:")

        if st.button("Ask"):
            if not user_input.strip():
                st.warning("Please enter a question.")
            else:
                answer = find_best_answer(user_input)
                st.session_state.faq_history.append((user_input, answer))
                st.success(answer)

        # Display conversation history
        if st.session_state.faq_history:
            st.markdown("### Recent Questions")
            for q, a in st.session_state.faq_history[-5:]:
                st.markdown(f"**You:** {q}")
                st.markdown(f"**EcoTrack:** {a}")
                st.markdown("---")


    # -----------------------
    # TAB 3 - Waste Management Tips
    # -----------------------
    with tab3:
        st.subheader("Waste Management Tips")

        tips = [
    "1. Segregate waste into wet and dry before disposal.",
    "2. Compost kitchen waste to reduce landfill load.",
    "3. Use reusable cloth bags instead of plastic.",
    "4. Donate old clothes, toys, and electronics.",
    "5. Avoid food wastage — cook only what’s needed.",
    "6. Reuse glass jars and containers creatively.",
    "7. Participate in local clean-up drives.",
    "8. Encourage your community to install smart bins.",
    "9. Buy products with minimal packaging.",
    "10. Recycle paper, cardboard, plastics, metals, and glass wherever possible.",
    "11. Avoid single-use plastics like straws and cutlery.",
    "12. Repair broken items instead of discarding them.",
    "13. Use cloth napkins and towels instead of disposable ones.",
    "14. Support local recycling programs and initiatives.",
    "15. Properly dispose of hazardous waste like batteries and chemicals.",
    "16. Opt for digital receipts and bills to reduce paper waste.",
    "17. Practice mindful purchasing — buy only what you need.",
    "18. Donate leftover food to food banks or shelters.",
    "19. Refill containers for household cleaning products.",
    "20. Use energy-efficient appliances to reduce indirect waste.",
    "21. Educate family and friends about waste segregation.",
    "22. Collect rainwater and reduce water wastage.",
    "23. Compost garden waste like leaves and grass clippings.",
    "24. Choose biodegradable or compostable packaging when possible.",
    "25. Encourage local schools and workplaces to implement waste reduction programs."
]



        for tip in tips:
            st.markdown(f"{tip}")

    navigation_buttons()

# ========================
# Page 3 - End Page
# ========================
elif st.session_state.page == 3:
    set_background("images/background_home.jpg")

    st.markdown(
        """
        <style>
        .end-title {
            font-family: 'Great Vibes', cursive;
            font-size: 90px;
            color: #444444;
            text-align: center;
            margin-top: 60px;
            text-shadow: 4px 4px 12px rgba(0,0,0,0.6);
        }
        .end-slogan {
            font-family: 'Poppins', sans-serif;
            font-size: 28px;
            color: #fff;
            text-align: center;
            margin-top: 40px;
            background: rgba(0,0,0,0.5);
            padding: 20px;
            border-radius: 16px;
            width: 70%;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='end-title'>Thank You for Visiting EcoTrack</div>", unsafe_allow_html=True)
    st.markdown("<div class='end-slogan'>🌱 EcoTrack is not just a project—it's our pledge to a better Bengaluru 🌱</div>", unsafe_allow_html=True)

    navigation_buttons(show_next=False)
