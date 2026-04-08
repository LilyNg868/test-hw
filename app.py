import streamlit as st
import streamlit.components.v1 as components
import requests

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Math Online Assignment", layout="wide")

# --- TEACHER SETTINGS ---
WEBHOOK_URL = "YOUR_APPS_SCRIPT_URL_HERE"
FORM_URL = "YOUR_GOOGLE_FORM_URL_HERE"
# ------------------------

if 'is_monitored' not in st.session_state:
    st.session_state.is_monitored = True
if 'has_started' not in st.session_state:
    st.session_state.has_started = False

st.title("📝 Online Assignment System")

name = st.text_input("Enter your full name to start:", placeholder="Example: Jane Doe")

if name:
    # Send START signal
    if not st.session_state.has_started:
        try:
            requests.post(WEBHOOK_URL, json={
                "name": name, 
                "action": "START"
            })
            st.session_state.has_started = True
        except:
            pass

    # 2. MONITORING JAVASCRIPT (Merged Action & Counter)
    status_js = "true" if st.session_state.is_monitored else "false"
    components.html(
        f"""
        <script>
        var monitorActive = {status_js};
        if (window.parent.violationCount === undefined) {{
            window.parent.violationCount = 0;
        }}

        document.addEventListener("visibilitychange", function() {{
            if (monitorActive && document.hidden) {{
                window.parent.violationCount++;
                var currentCount = window.parent.violationCount;
                
                fetch('{WEBHOOK_URL}', {{
                    method: 'POST', 
                    mode: 'no-cors',
                    body: JSON.stringify({{
                        name: '{name}', 
                        action: 'LEAVE TAB ' + currentCount // Gộp số lần vào action
                    }})
                }});
                alert("WARNING: You left the tab! Violation #" + currentCount + " recorded.");
            }}
        }});
        </script>
        """, height=0
    )

    col1, col2 = st.columns([8, 2])
    with col1:
        st.markdown(f'<iframe src="{FORM_URL}" width="100%" height="800px" style="border:none;"></iframe>', unsafe_allow_html=True)

    with col2:
        st.write("---")
        if st.session_state.is_monitored:
            st.error("🔒 MONITORING ACTIVE")
            if st.button("CONFIRM FINISH"):
                try:
                    requests.post(WEBHOOK_URL, json={
                        "name": name, 
                        "action": "FINISH"
                    })
                except:
                    pass
                st.session_state.is_monitored = False
                st.rerun()
        else:
            st.success("✅ COMPLETED")
            st.write("Monitoring stopped. You can review your score now.")
else:
    st.warning("⚠️ Please enter your name.")
