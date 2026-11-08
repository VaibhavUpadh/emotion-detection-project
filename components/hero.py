import streamlit as st


def show_hero():

    st.markdown("""
    <div class="hero">

        <div class="hero-left">

            <span class="badge">
            🚀 AI Powered Emotion Analysis
            </span>

            <h1>
            Understand Human Emotion<br>
            with Artificial Intelligence
            </h1>

            <p>
            Analyze text instantly using Machine Learning.
            Predict emotions, visualize confidence,
            and receive intelligent suggestions
            through an interactive dashboard.
            </p>

            <div class="hero-buttons">

                <button class="primary-btn">
                    🚀 Get Started
                </button>

                <button class="secondary-btn">
                    📖 Learn More
                </button>

            </div>

        </div>

        <div class="hero-right">

            <div class="brain">

                🧠

            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)