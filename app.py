import streamlit as st
import streamlit.components.v1 as components
import requests

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Math Online Assignment", layout="wide")


# --- TEACHER SETTINGS ---
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyKFr7YIkn5pM-lbkxaArABB7aRuAgIC4smJJh3Y8mcnEU-YG0yG8W2CFVIbAuRqY-b/exec"
FORM_URL = "https://forms.gle/9nMAH9yD3kFCUhaK8"

# NẾU KHÔNG DÙNG, HÃY ĐỂ LÀ None HOẶC ""
FORMULA_SHEET_URL = "https://drive.google.com/file/d/1jH5to8-4f0YSthKfxbwHm4ScCkhJ1SwO/view?usp=sharing"  # Ví dụ: "https://link-anh-cua-ban.jpg"
EXTRA_URL = "https://www.desmos.com/calculator"          # Ví dụ: "https://www.desmos.com/scientific"
# ------------------------

# Initialize session states
if 'is_monitored' not in st.session_state:
    st.session_state.is_monitored = True
if 'has_started' not in st.session_state:
    st.session_state.has_started = False

# 2. HEADER SECTION
header_left, header_right = st.columns([6, 4])

with header_left:
    st.title("📝 Assignment Portal")

with header_right:
    # TRƯỜNG HỢP 1: CHƯA BẮT ĐẦU
    if not st.session_state.has_started:
        st.write("") 
        # Sử dụng on_change hoặc kiểm tra nút bấm chặt chẽ hơn
        name_input = st.text_input("Enter Full Name to Start:", placeholder="e.g. Lily")
        
        if st.button("🚀 START ASSIGNMENT", use_container_width=True):
            if name_input:
                # Ghi đè trực tiếp vào session_state
                st.session_state.student_name = name_input
                st.session_state.has_started = True
                
                # Gửi tín hiệu về Google Sheet
                try:
                    requests.post(WEBHOOK_URL, json={
                        "name": name_input, 
                        "action": "START"
                    })
                except:
                    pass
                
                # Ép app chạy lại ngay lập tức để hiện nút FINISH
                st.rerun()
            else:
                st.error("Please enter your name first!")
    
    # TRƯỜNG HỢP 2: ĐANG LÀM BÀI (Hiện nút Finish ngay)
    elif st.session_state.is_monitored:
        st.write("")
        if st.button("🏁 CONFIRM FINISH & STOP MONITORING", type="primary", use_container_width=True):
            try:
                requests.post(WEBHOOK_URL, json={
                    "name": st.session_state.student_name, 
                    "action": "FINISH"
                })
            except:
                pass
            st.session_state.is_monitored = False
            st.rerun()
        st.caption(f"Student: **{st.session_state.student_name}** | Status: 🔒 Monitoring Active")

    # TRƯỜNG HỢP 3: ĐÃ KẾT THÚC
    else:
        st.success("✅ Session Completed. Monitoring Disabled.")

st.divider()

# 3. MONITORING & CONTENT (Chỉ hiện khi has_started là True)
if st.session_state.has_started:
    # JavaScript Giám sát
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
                        name: '{st.session_state.student_name}', 
                        action: 'LEAVE TAB ' + currentCount 
                    }})
                }});
                alert("WARNING: Violation #" + currentCount + " recorded.");
            }}
        }});
        </script>
        """, height=0
    )

    # Tabs Content
    tabs_list = ["✍️ Assignment"]
    if FORMULA_SHEET_URL: tabs_list.append("📋 Formula Sheet")
    if EXTRA_URL: tabs_list.append("🔍 Extra Tool")
    
    tabs = st.tabs(tabs_list)
    
    with tabs[0]:
        st.markdown(f'<iframe src="{FORM_URL}" width="100%" height="900px" style="border:none;"></iframe>', unsafe_allow_html=True)
            
    idx = 1
    if FORMULA_SHEET_URL:
        with tabs[idx]:
            st.markdown(f'<iframe src="{FORMULA_SHEET_URL}" width="100%" height="900px" style="border:none;"></iframe>', unsafe_allow_html=True)
        idx += 1
    if EXTRA_URL:
        with tabs[idx]:
            st.markdown(f'<iframe src="{EXTRA_URL}" width="100%" height="900px" style="border:none;"></iframe>', unsafe_allow_html=True)
else:
    st.info("Waiting for you to start the assignment...")
