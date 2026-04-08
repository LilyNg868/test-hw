import streamlit as st
import streamlit.components.v1 as components

# 1. CẤU HÌNH
st.set_page_config(page_title="Hệ thống BTVN Toán", layout="wide")

# --- PHẦN CÀI ĐẶT ---
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyKFr7YIkn5pM-lbkxaArABB7aRuAgIC4smJJh3Y8mcnEU-YG0yG8W2CFVIbAuRqY-b/exec"
FORM_URL = "https://forms.gle/8Tv699JS13Y7M13o7"
# --------------------

st.title("📝 Hệ thống Làm Bài Tập Trực Tuyến")

# Khởi tạo trạng thái
if 'is_done' not in st.session_state:
    st.session_state.is_done = False

name = st.text_input("Nhập họ và tên của em:", placeholder="Ví dụ: Nguyễn Văn A")

if name:
    # CHỈ CHẠY GIÁM SÁT NẾU CHƯA NỘP BÀI
    if not st.session_state.is_done:
        st.info(f"Học sinh: **{name}**. Hệ thống đang giám sát chuyển tab...")

        # JavaScript giám sát: Chỉ được chèn vào khi is_done == False
        components.html(
            f"""
            <script>
            var count = 0;
            document.addEventListener("visibilitychange", function() {{
                if (document.hidden) {{
                    count++;
                    alert("Cảnh báo: Em vừa rời tab " + count + " lần!");
                    
                    fetch('{WEBHOOK_URL}', {{
                        method: 'POST',
                        mode: 'no-cors',
                        body: JSON.stringify({{
                            name: '{name}',
                            action: 'Rời tab',
                            count: count
                        }})
                    }});
                }}
            }});
            </script>
            """,
            height=0,
        )

        # Hiển thị bài tập và nút nộp bài
        cols = st.columns([8, 2])
        with cols[0]:
            st.markdown(
                f"""
                <div style="width: 100%; height: 800px; border: 2px solid #f0f2f6; border-radius: 15px; overflow: hidden;">
                    <iframe src="{FORM_URL}" width="100%" height="100%" style="border:none;"></iframe>
                </div>
                """,
                unsafe_allow_html=True
            )
        with cols[1]:
            st.write("---")
            st.write("Sau khi nhấn GỬI trong Form, hãy nhấn nút dưới đây:")
            if st.button("XÁC NHẬN HOÀN THÀNH"):
                st.session_state.is_done = True
                st.rerun() # Lệnh này sẽ xóa sạch script cũ và vẽ lại trang
    
    else:
        # TRẠNG THÁI ĐÃ NỘP BÀI: Không có bất kỳ dòng JavaScript giám sát nào ở đây
        st.balloons()
        st.success(f"Hệ thống đã ngừng giám sát. Chúc mừng **{name}** đã hoàn thành!")
        st.info("Bây giờ em có thể thoải mái chuyển tab hoặc đóng trình duyệt.")
        if st.button("Làm bài lại (Nếu cần)"):
            st.session_state.is_done = False
            st.rerun()
else:
    st.warning("Vui lòng nhập tên để bắt đầu.")
