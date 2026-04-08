import streamlit as st
import streamlit.components.v1 as components
import requests

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Math Online Assignment", layout="wide")

# --- TEACHER SETTINGS ---
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyKFr7YIkn5pM-lbkxaArABB7aRuAgIC4smJJh3Y8mcnEU-YG0yG8W2CFVIbAuRqY-b/exec"
FORM_URL = "https://forms.gle/WN7UGWBgrCasm3ZY7"
EXTRA_URL = "https://www.desmos.com/calculator" # Ví dụ link máy tính Online
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
            requests.post(WEBHOOK_URL, json={"name": name, "action": "START"})
            st.session_state.has_started = True
        except: pass

    # 2. MONITORING JAVASCRIPT
    status_js = "true" if st.session_state.is_monitored else "false"
    components.html(
        f"""
        <script>
        var monitorActive = {status_js};
        if (window.parent.violationCount === undefined) {{ window.parent.violationCount = 0; }}

        document.addEventListener("visibilitychange", function() {{
            if (monitorActive && document.hidden) {{
                window.parent.violationCount++;
                var currentCount = window.parent.violationCount;
                fetch('{WEBHOOK_URL}', {{
                    method: 'POST', mode: 'no-cors',
                    body: JSON.stringify({{ name: '{name}', action: 'LEAVE TAB ' + currentCount }})
                }});
                alert("WARNING: Violation #" + currentCount + " recorded.");
            }}
        }});
        </script>
        """, height=0
    )

    # 3. LAYOUT WITH TABS
    col1, col2 = st.columns([8, 2])
    
    with col1:
        # Tạo 2 Tab bên trái: 1 cho bài làm, 1 cho tài liệu tra cứu
        tab_assignment, tab_reference = st.tabs(["📝 Assignment", "🔍 Reference Tool"])
        
        with tab_assignment:
            st.markdown(f'<iframe src="{FORM_URL}" width="100%" height="800px" style="border:none;"></iframe>', unsafe_allow_html=True)
            
        with tab_reference:
            st.info(f"You can use this website: {EXTRA_URL}")
            st.markdown(f'<iframe src="{EXTRA_URL}" width="100%" height="800px" style="border:none;"></iframe>', unsafe_allow_html=True)

    with col2:
        st.write("---")
        if st.session_state.is_monitored:
            st.error("🔒 MONITORING")
            if st.button("CONFIRM FINISH"):
                try:
                    requests.post(WEBHOOK_URL, json={"name": name, "action": "FINISH"})
                except: pass
                st.session_state.is_monitored = False
                st.rerun()
        else:
            st.success("✅ COMPLETED")
            st.write("Monitoring stopped.")
else:
    st.warning("⚠️ Please enter your name.")
