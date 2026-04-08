import streamlit as st
import streamlit.components.v1 as components
import requests

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Math Assignment System", layout="wide")

# --- TEACHER SETTINGS ---
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyKFr7YIkn5pM-lbkxaArABB7aRuAgIC4smJJh3Y8mcnEU-YG0yG8W2CFVIbAuRqY-b/exec"
FORM_URL = "https://forms.gle/9nMAH9yD3kFCUhaK8"

# NẾU KHÔNG DÙNG, HÃY ĐỂ LÀ None HOẶC ""
FORMULA_SHEET_URL = "https://github.com/LilyNg868/test-hw/blob/main/Reference.pdf"  # Ví dụ: "https://link-anh-cua-ban.jpg"
EXTRA_URL = "https://www.desmos.com/calculator"          # Ví dụ: "https://www.desmos.com/scientific"
# ------------------------

# Initialize session states
if 'is_monitored' not in st.session_state:
    st.session_state.is_monitored = True
if 'has_started' not in st.session_state:
    st.session_state.has_started = False

# 2. TOP BAR (CONTROL PANEL)
header_col1, header_col2 = st.columns([6, 4])

with header_col1:
    st.subheader("📝 Assignment Portal")

with header_col2:
    if not st.session_state.has_started:
        temp_name = st.text_input("Enter Full Name to Start:", key="input_name")
        if st.button("🚀 START ASSIGNMENT"):
            if temp_name:
                st.session_state.student_name = temp_name
                try:
                    requests.post(WEBHOOK_URL, json={"name": temp_name, "action": "START"})
                    st.session_state.has_started = True
                    st.rerun()
                except: pass
            else:
                st.error("Please enter your name first!")
    else:
        f_col1, f_col2 = st.columns([1, 1])
        with f_col1:
            status_text = "🔒 MONITORING ON" if st.session_state.is_monitored else "✅ MONITORING OFF"
            st.info(status_text)
        with f_col2:
            if st.session_state.is_monitored:
                if st.button("🏁 CONFIRM FINISH"):
                    try:
                        requests.post(WEBHOOK_URL, json={"name": st.session_state.student_name, "action": "FINISH"})
                    except: pass
                    st.session_state.is_monitored = False
                    st.rerun()

st.divider()

# 3. MONITORING JAVASCRIPT
if st.session_state.has_started:
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
                        name: '{st.session_state.get('student_name', '')}', 
                        action: 'LEAVE TAB ' + currentCount 
                    }})
                }});
                alert("WARNING: Violation #" + currentCount + " recorded.");
            }}
        }});
        </script>
        """, height=0
    )

    # 4. DYNAMIC TAB LOGIC (Tự động ẩn hiện tab)
    tabs_to_create = ["✍️ Assignment"]
    if FORMULA_SHEET_URL: tabs_to_create.append("📋 Formula Sheet")
    if EXTRA_URL: tabs_to_create.append("🔍 Extra Tool")
    
    # Tạo các tab dựa trên danh sách trên
    all_tabs = st.tabs(tabs_to_create)
    
    # Tab 1: Luôn là Assignment
    with all_tabs[0]:
        st.markdown(f'<iframe src="{FORM_URL}" width="100%" height="900px" style="border:none;"></iframe>', unsafe_allow_html=True)
            
    # Xử lý các Tab phụ nếu có
    current_tab_index = 1
    if FORMULA_SHEET_URL:
        with all_tabs[current_tab_index]:
            st.markdown(f'<iframe src="{FORMULA_SHEET_URL}" width="100%" height="900px" style="border:none;"></iframe>', unsafe_allow_html=True)
        current_tab_index += 1
        
    if EXTRA_URL:
        with all_tabs[current_tab_index]:
            st.markdown(f'<iframe src="{EXTRA_URL}" width="100%" height="900px" style="border:none;"></iframe>', unsafe_allow_html=True)

else:
    st.info("Please enter your name above and click Start to begin.")
