import streamlit as st
import streamlit.components.v1 as components
import requests

st.set_page_config(page_title="Hệ thống BTVN Toán", layout="wide")

# --- SETTINGS ---
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyKFr7YIkn5pM-lbkxaArABB7aRuAgIC4smJJh3Y8mcnEU-YG0yG8W2CFVIbAuRqY-b/exec"
FORM_URL = "https://forms.gle/8Tv699JS13Y7M13o7"
# ----------------

if 'is_monitored' not in st.session_state:
    st.session_state.is_monitored = True

st.title("📝 Hệ thống Làm Bài Tập Trực Tuyến")
name = st.text_input("Nhập họ và tên:")

if name:
    # JavaScript giám sát dựa trên biến monitorActive
    status_js = "true" if st.session_state.is_monitored else "false"
    components.html(
        f"""
        <script>
        var monitorActive = {status_js};
        document.addEventListener("visibilitychange", function() {{
            if (monitorActive && document.hidden) {{
                fetch('{WEBHOOK_URL}', {{
                    method: 'POST', mode: 'no-cors',
                    body: JSON.stringify({{name: '{name}', action: 'RỜI TAB'}})
                }});
                alert("Cảnh báo: Hệ thống ghi nhận em rời tab!");
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
            st.error("🔒 ĐANG GIÁM SÁT")
            if st.button("XÁC NHẬN HOÀN THÀNH"):
                # Ghi mốc thời gian thoát vào Google Sheet
                try:
                    requests.post(WEBHOOK_URL, json={"name": name, "action": "TẮT GIÁM SÁT"})
                except:
                    pass
                st.session_state.is_monitored = False
                st.rerun()
        else:
            st.success("✅ ĐÃ KẾT THÚC")
            st.write("Hệ thống đã ghi nhận giờ thoát của em.")
            st.info("Em có thể xem điểm ở khung bên trái.")
