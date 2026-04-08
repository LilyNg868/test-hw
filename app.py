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
    st.session_state.step = "DOING" 
if 'final_pwd' not in st.session_state:
    st.session_state.final_pwd = ''.join(random.choices(string.digits, k=4))

st.title("📝 Hệ thống Làm Bài Tập Trực Tuyến")

name = st.text_input("Nhập họ và tên để bắt đầu:", placeholder="Ví dụ: Nguyễn Văn A")

if name:
    # 2. SCRIPT GIÁM SÁT (Chỉ chạy khi is_monitored = True)
    if st.session_state.is_monitored:
        components.html(
            f"""
            <script>
            var count = 0;
            document.addEventListener("visibilitychange", function() {{
                if (document.hidden) {{
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

    # 3. BỐ CỤC GIAO DIỆN (LUÔN GIỮ NGUYÊN)
    col1, col2 = st.columns([8, 2])
    
    with col1:
        # KHUNG GOOGLE FORM: Luôn hiển thị, không phụ thuộc vào trạng thái step
        st.markdown(
            f"""
            <div style="width: 100%; height: 850px; border: 2px solid #f0f2f6; border-radius: 15px; overflow: hidden;">
                <iframe src="{FORM_URL}" width="100%" height="100%" style="border:none;"></iframe>
            </div>
            """, unsafe_allow_html=True
        )

    with col2:
        st.write("---")
        # CHỈ CỘT BÊN PHẢI NÀY LÀ THAY ĐỔI NỘI DUNG
        
        if st.session_state.step == "DOING":
            st.error("🔒 ĐANG GIÁM SÁT")
            st.write("Sau khi nhấn **GỬI** bài trong khung bên cạnh, hãy nhấn nút dưới đây:")
            if st.button("TÔI ĐÃ NỘP BÀI XONG"):
                st.session_state.step = "SUBMITTED"
                st.rerun()

        elif st.session_state.step == "SUBMITTED":
            st.warning("⚠️ LẤY MÃ THOÁT")
            st.info(f"Mã mở khóa của em là: **{st.session_state.final_pwd}**")
            
            pwd_input = st.text_input("Nhập mã vừa hiện để tắt giám sát:", type="password")
            if st.button("XÁC NHẬN KẾT THÚC"):
                if pwd_input == st.session_state.final_pwd:
                    st.session_state.is_monitored = False
                    st.session_state.step = "FINISHED"
                    st.rerun()
                else:
                    st.error("Mã không đúng!")

        elif st.session_state.step == "FINISHED":
            st.success("✅ ĐÃ XÁC NHẬN")
            st.balloons()
            st.write("Hệ thống đã ngừng giám sát.")
            st.write("Bây giờ em có thể chuyển tab thoải mái và **xem điểm** ở khung bên trái.")

else:
    st.warning("Vui lòng nhập tên để bắt đầu.")
