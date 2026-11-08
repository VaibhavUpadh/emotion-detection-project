import streamlit as st
import joblib
import re
import pandas as pd
# --------------------------
# Page Configuration
# --------------------------

st.set_page_config(
    page_title="Emotion Detection AI",
    page_icon="😊",
    layout="wide"
)
st.markdown("""
<style>

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main App Background */
.stApp{
    background: linear-gradient(135deg,#0F172A,#111827,#1E293B);
    color:white;
}

/* Main Title */
h1{
    color:white;
    text-align:center;
    font-size:48px;
    font-weight:800;
}

/* Subtitle */
h3{
    color:#CBD5E1;
    text-align:center;
}

/* Text Area */
textarea{
    border-radius:18px !important;
    border:1px solid #334155 !important;
    background:#1E293B !important;
    color:white !important;
    font-size:18px !important;
}

/* Button */
.stButton>button{

    background:linear-gradient(90deg,#6366F1,#8B5CF6);

    color:white;

    border:none;

    border-radius:15px;

    height:60px;

    width:100%;

    font-size:20px;

    font-weight:bold;

    transition:0.3s;
}

.stButton>button:hover{

    transform:scale(1.03);

    box-shadow:0px 0px 25px #8B5CF6;

}

/* Sidebar */

section[data-testid="stSidebar"]{

background:#111827;

}

/* Metric Cards */

[data-testid="stMetric"]{

background:#1E293B;

padding:20px;

border-radius:20px;

border:1px solid #334155;

}
/* Prediction Result Card */
.result-card{
    background: linear-gradient(135deg,#22c55e,#16a34a);
    padding:30px;
    border-radius:20px;
    text-align:center;
    color:white;
    box-shadow:0px 12px 35px rgba(34,197,94,0.30);
    margin-top:20px;
    margin-bottom:20px;
}

.result-card h1{
    font-size:42px;
    margin-bottom:10px;
}

.result-card h2{
    font-size:34px;
    margin:0;
}

.result-card p{
    font-size:18px;
    opacity:0.9;
}
/* Confidence Card */

.confidence-card{
    background:#1E293B;
    padding:22px;
    border-radius:18px;
    margin-top:20px;
    margin-bottom:20px;
    border:1px solid rgba(255,255,255,.08);
}

.progress-bar{
    width:100%;
    height:14px;
    background:#334155;
    border-radius:30px;
    overflow:hidden;
    margin-top:12px;
}

.progress-fill{
    height:100%;
    background:linear-gradient(90deg,#22C55E,#10B981,#06B6D4);
    border-radius:30px;
    transition:width .8s ease;
}
</style>
""", unsafe_allow_html=True)
# -----------------------
# Load Saved Model
# -----------------------
model = joblib.load("models/model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")
if "history" not in st.session_state:
    st.session_state.history = []
# -----------------------
# Sidebar
# -----------------------

st.sidebar.title("🧠 Emotion Detection AI")

st.sidebar.markdown("""
### Project Information

**Project Title**

Context-Aware Emotion Detection and Response Suggestion System

**Model Used**

✔ TF-IDF

✔ Logistic Regression

**Dataset**

Emotion Dataset (6 Classes)

**Developed By**

Vaibhav Upadhyay

---

This application predicts emotions from text using Machine Learning.
""")
# -----------------------
# Text Cleaning Function
# -----------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

# -----------------------
# Streamlit UI
# -----------------------
st.markdown("""
<style>

/* Background */
.main{
    background:#0F172A;
}

/* Card Design */
.card{
    background:#1E293B;
    padding:25px;
    border-radius:18px;
    border:1px solid rgba(255,255,255,0.08);
    box-shadow:0px 10px 30px rgba(0,0,0,0.25);
    margin-bottom:25px;
}

/* Card Hover */
.card:hover{
    transform:translateY(-4px);
    transition:0.3s;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">

<h1 style="text-align:center;">
🧠 Emotion Detection AI
</h1>

<h4 style="text-align:center;color:#A78BFA;">
Understand Human Emotions with Artificial Intelligence
</h4>

<p style="text-align:center;font-size:18px;">
Analyze emotions from text using Machine Learning and receive intelligent response suggestions.
</p>

<hr>

<h4>Supported Emotions</h4>

😊 Joy &nbsp;&nbsp;&nbsp;
😢 Sadness &nbsp;&nbsp;&nbsp;
😠 Anger &nbsp;&nbsp;&nbsp;
😨 Fear &nbsp;&nbsp;&nbsp;
❤️ Love &nbsp;&nbsp;&nbsp;
😲 Surprise

</div>
""", unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("✍ Analyze Your Emotion")

st.write("Type any sentence below and let the AI understand your emotional state.")

user_input = st.text_area(
    "",
    height=180,
    placeholder="Example: I am feeling really excited today!"
)

predict = st.button(
    "🔍 Analyze Emotion",
    use_container_width=True
)

st.markdown("</div>", unsafe_allow_html=True)

if predict:
    if user_input.strip() == "":
        st.warning("⚠ Please enter some text.")

    else:

        cleaned = clean_text(user_input)

        vector = vectorizer.transform([cleaned])

        prediction = model.predict(vector)[0]

        probabilities = model.predict_proba(vector)[0]

        confidence = max(probabilities) * 100

        emotion_names = model.classes_

        prob_df = pd.DataFrame({
            "Emotion": emotion_names,
            "Probability": probabilities * 100
        })

        st.subheader("📊 Emotion Probability")

        st.bar_chart(
            prob_df.set_index("Emotion")
        )
 
        emoji = {
            "joy": "😊",
            "sadness": "😢",
            "anger": "😠",
            "fear": "😨",
            "love": "❤️",
            "surprise": "😲"
        }
        st.markdown(f"""
<div class="result-card">
    <h1>{emoji.get(prediction, "🙂")}</h1>
    <h2>{prediction.upper()}</h2>
    <p>Emotion Detected Successfully</p>
</div>
""", unsafe_allow_html=True)
        st.markdown(f"""
<div class="confidence-card">

<h3 style="margin:0;color:white;">
📊 Confidence Score
</h3>

<h2 style="color:#60A5FA;">
{confidence:.2f}%
</h2>

<div class="progress-bar">
    <div class="progress-fill" style="width:{confidence}%"></div>
</div>

</div>
""", unsafe_allow_html=True)


        

        suggestions = {
            "joy": "Keep enjoying the positive moments and spread happiness!",
            "sadness": "Take some rest, talk to someone you trust.",
            "anger": "Try taking a deep breath before reacting.",
            "fear": "Take one step at a time. Most fears become easier when broken into smaller tasks.",
            "love": "Cherish your relationships and express your gratitude.",
            "surprise": "Stay curious and embrace new experiences."
        }

        st.info(f"💡 **Suggested Response:** {suggestions[prediction]}")
        st.session_state.history.append({
    "Input": user_input,
    "Emotion": prediction.upper(),
    "Confidence": f"{confidence:.2f}%"
})
        # -----------------------
# Prediction History Table
# -----------------------

# -----------------------
# Prediction History
# -----------------------

if len(st.session_state.history) > 0:

    st.markdown("---")

    st.subheader("📜 Prediction History")

    history_df = pd.DataFrame(st.session_state.history)

    st.dataframe(
        history_df,
        use_container_width=True
    )

    st.subheader("📈 Emotion Statistics")

    emotion_count = history_df["Emotion"].value_counts()

    st.bar_chart(emotion_count)
   
   