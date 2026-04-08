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

# Khởi tạo mã ngẫu nhiên cố định cho mỗi phiên vào trang
if 'final_pwd' not in st.session_state:
    st.session_state.final_pwd = ''.join(random.choices(string.digits, k=4))

st.title("📝 Hệ thống Làm Bài Tập Trực Tuyến")

name = st.text_input("Nhập họ và tên để bắt đầu:", placeholder="Ví dụ: Nguyễn Văn A")

if name:
    # 2. JAVASCRIPT GIÁM SÁT THÔNG MINH
    # Script này sẽ tự hủy lệnh alert dựa trên một biến toàn cục trong trình duyệt
    components.html(
        f"""
        <script>
        // Tạo một biến nằm trên cửa sổ cha để kiểm tra trạng thái
        window.parent.is_finished = window.parent.is_finished || false;
        var count = 0;

        document.addEventListener("visibilitychange", function() {{
            // CHỈ chạy alert nếu biến is_finished trên cửa sổ cha vẫn là false
            if (!window.parent.is_finished && document.hidden) {{
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

    col1, col2 = st.columns([8, 2])
    
    with col1:
        # KHUNG GOOGLE FORM: Luôn đứng yên, không bị ảnh hưởng bởi st.rerun() của các nút phụ
        st.markdown(
            f"""
            <div style="width: 100%; height: 850px; border: 2px solid #f0f2f6; border-radius: 15px; overflow: hidden;">
                <iframe src="{FORM_URL}" width="100%" height="100%" style="border:none;"></iframe>
            </div>
            """, unsafe_allow_html=True
        )

    with col2:
        st.write("---")
        
        # Dùng radio hoặc một vùng chứa không gây reload iframe mạnh
        if 'step' not in st.session_state:
            st.session_state.step = 1

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
                    # Gửi lệnh JavaScript để tắt alert mà không cần load lại iframe
                    components.html(
                        """<script>window.parent.is_finished = true;</script>""", 
                        height=0
                    )
                    st.session_state.step = 3
                    st.rerun()
                else:
                    st.error("Mã không đúng!")

        else:
            st.success("✅ ĐÃ TẮT GIÁM SÁT")
            st.balloons()
            st.write("Bây giờ em có thể xem điểm ở khung bên trái.")
