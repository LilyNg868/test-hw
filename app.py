import streamlit as st
import streamlit.components.v1 as components
import random
import string

# 1. CẤU HÌNH
st.set_page_config(page_title="Hệ thống BTVN Toán", layout="wide")

# --- THÔNG TIN CỦA BẠN ---
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyKFr7YIkn5pM-lbkxaArABB7aRuAgIC4smJJh3Y8mcnEU-YG0yG8W2CFVIbAuRqY-b/exec"
FORM_URL = "https://forms.gle/8Tv699JS13Y7M13o7"
# -------------------------

# Khởi tạo trạng thái
if 'is_monitored' not in st.session_state:
    st.session_state.is_monitored = True
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'final_pwd' not in st.session_state:
    st.session_state.final_pwd = ''.join(random.choices(string.digits, k=4))

st.title("📝 Hệ thống Làm Bài Tập Trực Tuyến")

name = st.text_input("Nhập họ và tên để bắt đầu:", placeholder="Ví dụ: Quynh")

if name:
    # 2. JAVASCRIPT GIÁM SÁT CÓ "CÔNG TẮC"
    # Quan trọng: Biến monitorActive sẽ quyết định có hiện alert hay không
    monitor_active_js = "true" if st.session_state.is_monitored else "false"
    
    components.html(
        f"""
        <script>
        // Đồng bộ trạng thái từ Python sang JS
        var monitorActive = {monitor_active_js};
        var count = 0;

        document.addEventListener("visibilitychange", function() {{
            // CHỈ chạy nếu monitorActive đang là true
            if (monitorActive && document.hidden) {{
                count++;
                alert("Cảnh báo: Em đang rời tab! Lần vi phạm: " + count);
                fetch('{WEBHOOK_URL}', {{
                    method: 'POST', mode: 'no-cors',
                    body: JSON.stringify({{name: '{name}', action: 'Rời tab', count: count}})
                }});
            }}
        }});
        </script>
        """, height=0,
    )

    # 3. GIAO DIỆN
    col1, col2 = st.columns([8, 2])
    
    with col1:
        # Giữ nguyên Iframe để học sinh xem điểm
        st.markdown(
            f"""
            <div style="width: 100%; height: 850px; border: 2px solid #f0f2f6; border-radius: 15px; overflow: hidden;">
                <iframe src="{FORM_URL}" width="100%" height="100%" style="border:none;"></iframe>
            </div>
            """, unsafe_allow_html=True
        )

    with col2:
        st.write("---")
        
        if st.session_state.step == 1:
            st.error("🔒 ĐANG GIÁM SÁT")
            if st.button("TÔI ĐÃ NỘP BÀI XONG"):
                st.session_state.step = 2
                st.rerun()

        elif st.session_state.step == 2:
            st.warning("⚠️ LẤY MÃ THOÁT")
            st.info(f"Mã thoát: **{st.session_state.final_pwd}**")
            pwd_input = st.text_input("Nhập mã để tắt cảnh báo:", type="password")
            
            if st.button("XÁC NHẬN KẾT THÚC"):
                if pwd_input == st.session_state.final_pwd:
                    st.session_state.is_monitored = False # Tắt giám sát ở phía Python
                    st.session_state.step = 3
                    st.rerun() # Load lại trang để cập nhật biến monitorActive sang JS
                else:
                    st.error("Mã không đúng!")

        else:
            st.success("✅ ĐÃ TẮT GIÁM SÁT")
            st.balloons()
            st.write("Hệ thống đã ngừng giám sát hoàn toàn.")
            st.caption("Em có thể chuyển tab thoải mái ngay bây giờ.")

else:
    st.warning("Vui lòng nhập tên.")
