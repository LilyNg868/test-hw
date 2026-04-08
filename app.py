import streamlit as st
import streamlit.components.v1 as components
import requests

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Math Online Assignment", layout="wide")

# CUSTOM CSS: Hide "Press Enter to apply" and clean up input UI
st.markdown("""
    <style>
    div[data-testid="InputInstructions"] {
        display: none;
    }
    /* Optional: Make the Start button more prominent */
    div.stButton > button:first-child {
        background-color: #007bff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- TEACHER SETTINGS ---
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyKFr7YIkn5pM-lbkxaArABB7aRuAgIC4smJJh3Y8mcnEU-YG0yG8W2CFVIbAuRqY-b/exec"
FORM_URL = "https://forms.gle/9nMAH9yD3kFCUhaK8"

# Leave as None if you don't want to show these tabs
FORMULA_SHEET_URL = "https://drive.google.com/file/d/1jH5to8-4f0YSthKfxbwHm4ScCkhJ1SwO/preview"  # Example: "https://link-anh-cua-ban.jpg"
EXTRA_URL = "https://www.desmos.com/calculator"          # Example: "https://www.desmos.com/scientific"
# ------------------------

# Initialize Session States
if 'is_monitored' not in st.session_state:
    st.session_state.is_monitored = True
if 'has_started' not in st.session_state:
    st.session_state.has_started = False

# 2. HEADER SECTION (Control Panel)
header_left, header_right = st.columns([6, 4])

with header_left:
    st.title("📝 Assignment Portal")

with header_right:
    # CASE 1: NOT STARTED - Use Form to enable "Enter to Start"
    if not st.session_state.has_started:
        with st.form("start_form", clear_on_submit=False):
            st.write("Welcome! Please enter your name to begin.")
            name_input = st.text_input("Full Name:", placeholder="e.g. Jane Doe")
            submit_start = st.form_submit_button("🚀 START ASSIGNMENT", use_container_width=True)
            
            if submit_start:
                if name_input:
                    st.session_state.student_name = name_input
                    st.session_state.has_started = True
                    try:
                        requests.post(WEBHOOK_URL, json={"name": name_input, "action": "START"})
                    except: pass
                    st.rerun()
                else:
                    st.error("Name is required to start the session.")
    
    # CASE 2: ACTIVE SESSION - Show Finish Button
    elif st.session_state.is_monitored:
        st.write("")
        if st.button("🏁 CONFIRM FINISH & STOP MONITORING", type="primary", use_container_width=True):
            try:
                requests.post(WEBHOOK_URL, json={
                    "name": st.session_state.student_name, 
                    "action": "FINISH"
                })
            except: pass
            st.session_state.is_monitored = False
            st.rerun()
        st.caption(f"Student: **{st.session_state.student_name}** | Status: 🔒 Monitoring Active")

    # CASE 3: SESSION COMPLETED
    else:
        st.success("✅ Assignment Completed. Monitoring is now disabled.")

st.divider()

# 3. MONITORING & CONTENT (Only renders after Start)
if st.session_state.has_started:
    # Tab Violation Logic (JavaScript)
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
                    body: JSON.stringify({{ 
                        name: '{st.session_state.get('student_name', 'Unknown')}', 
                        action: 'LEAVE TAB ' + currentCount 
                    }})
                }});
                alert("WARNING: You left the tab! Violation #" + currentCount + " recorded.");
            }}
        }});
        </script>
        """, height=0
    )

    # Dynamic Tabs
    tabs_labels = ["✍️ Assignment"]
    if FORMULA_SHEET_URL: tabs_labels.append("📋 Formula Sheet")
    if EXTRA_URL: tabs_labels.append("🔍 Extra Tool")
    
    tabs = st.tabs(tabs_labels)
    
    # Tab 1: Google Form
    with tabs[0]:
        st.markdown(f'<iframe src="{FORM_URL}" width="100%" height="900px" style="border:none;"></iframe>', unsafe_allow_html=True)
            
    # Conditional Tabs
    current_idx = 1
    if FORMULA_SHEET_URL:
        with tabs[current_idx]:
            # Image check for GitHub raw links
            is_img = any(FORMULA_SHEET_URL.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg'])
            if is_img:
                st.image(FORMULA_SHEET_URL, use_container_width=True)
            else:
                st.markdown(f'<iframe src="{FORMULA_SHEET_URL}" width="100%" height="900px"></iframe>', unsafe_allow_html=True)
        current_idx += 1
        
    if EXTRA_URL:
        with tabs[current_idx]:
            st.markdown(f'<iframe src="{EXTRA_URL}" width="100%" height="900px"></iframe>', unsafe_allow_html=True)

else:
    st.info("Please enter your name above and click Start to begin your assignment.")
