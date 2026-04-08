import streamlit as st
import streamlit.components.v1 as components
import requests
import time

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Math Online Assignment", layout="wide")

# --- TEACHER SETTINGS ---
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyKFr7YIkn5pM-lbkxaArABB7aRuAgIC4smJJh3Y8mcnEU-YG0yG8W2CFVIbAuRqY-b/exec"
FORM_URL = "https://forms.gle/8Tv699JS13Y7M13o7"
# ------------------------

# Initialize session states
if 'is_monitored' not in st.session_state:
    st.session_state.is_monitored = True
if 'has_started' not in st.session_state:
    st.session_state.has_started = False
if 'violation_count' not in st.session_state:
    st.session_state.violation_count = 0

st.title("📝 Online Assignment System")

# Input student name
name = st.text_input("Enter your full name to start:", placeholder="Example: Jane Doe")

if name:
    # Trigger START event only once
    if not st.session_state.has_started:
        try:
            requests.post(WEBHOOK_URL, json={
                "name": name, 
                "action": "START", 
                "details": "Started the assignment"
            })
            st.session_state.has_started = True
        except:
            pass

    # 2. MONITORING JAVASCRIPT
    status_js = "true" if st.session_state.is_monitored else "false"
    components.html(
        f"""
        <script>
        var monitorActive = {status_js};
        var count = 0;
        document.addEventListener("visibilitychange", function() {{
            if (monitorActive && document.hidden) {{
                count++;
                // Send violation to Google Sheet
                fetch('{WEBHOOK_URL}', {{
                    method: 'POST', 
                    mode: 'no-cors',
                    body: JSON.stringify({{
                        name: '{name}', 
                        action: 'TAB_LEAVE', 
                        details: 'Violation #' + count
                    }})
                }});
                alert("WARNING: You have left the tab! This incident is recorded.");
            }}
        }});
        </script>
        """, height=0
    )

    # 3. MAIN LAYOUT
    col1, col2 = st.columns([8, 2])
    
    with col1:
        # Google Form Frame
        st.markdown(
            f"""
            <div style="width: 100%; height: 850px; border: 2px solid #f0f2f6; border-radius: 15px; overflow: hidden;">
                <iframe src="{FORM_URL}" width="100%" height="100%" style="border:none;"></iframe>
            </div>
            """, unsafe_allow_html=True
        )

    with col2:
        st.write("---")
        if st.session_state.is_monitored:
            st.error("🔒 MONITORING ACTIVE")
            st.info("Complete the form on the left, then click the button below to finish.")
            
            if st.button("CONFIRM FINISH"):
                # Send FINISH event to Google Sheet
                try:
                    requests.post(WEBHOOK_URL, json={
                        "name": name, 
                        "action": "FINISH", 
                        "details": "Assignment submitted"
                    })
                except:
                    pass
                st.session_state.is_monitored = False
                st.rerun()
        else:
            st.success("✅ COMPLETED")
            st.balloons()
            st.write("Your finish time has been recorded.")
            st.write("You may now review your score or close the tab.")

else:
    st.warning("⚠️ Please enter your name to access the assignment.")
