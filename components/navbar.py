import streamlit as st

def show_navbar():

    st.markdown("""
<div class="navbar">

<div class="logo">
🧠 EmotionAI
</div>

<div class="nav-links">

<span class="nav-item">Home</span>
                
<span class="nav-item">Features</span>
                
<span class="nav-item">Dashboard</span>
                
<span class="nav-item">About</span>

</div>

</div>
""", unsafe_allow_html=True)