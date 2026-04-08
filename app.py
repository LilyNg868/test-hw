import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime

# 1. CẤU HÌNH TRANG
st.set_page_config(page_title="Hệ thống BTVN Toán", layout="wide")

# --- PHẦN CÀI ĐẶT CỦA GIÁO VIÊN ---
FORM_URL = "https://forms.gle/81Q8tE3wn2koLVgc8"
# --------------------------------

st.title("📝 Hệ thống Làm Bài Tập Trực Tuyến")

# Khởi tạo biến đếm trong phiên làm việc
if 'log_data' not in st.session_state:
    st.session_state.log_data = []

name = st.text_input("Nhập họ và tên của em để bắt đầu:", placeholder="Ví dụ: Nguyễn Văn A")

if name:
    # 2. THEO DÕI RỜI TAB QUA JAVASCRIPT
    components.html(
        f"""
        <script>
        document.addEventListener("visibilitychange", function() {{
            if (document.hidden) {{
                let time = new Date().toLocaleTimeString();
                alert("Cảnh báo {name}: Em vừa rời tab lúc " + time);
                // Gửi tín hiệu về Python (không cần Apps Script)
                window.parent.postMessage({{type: 'tab_switch', time: time}}, '*');
            }}
        }});
        </script>
        """,
        height=0,
    )

    st.info(f"Chào **{name}**, hãy tập trung làm bài trong khung dưới đây.")

    # 3. HIỂN THỊ BÀI TẬP
    st.markdown(
        f"""
        <style>
            .iframe-container {{ width: 100%; height: 800px; overflow: auto; border: 1px solid #ddd; }}
            iframe {{ width: 100%; height: 100%; border: none; }}
        </style>
        <div class="iframe-container">
            <iframe src="{FORM_URL}"></iframe>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 4. PHẦN DÀNH CHO GIÁO VIÊN KIỂM TRA TẠI CHỖ
    # Vì Apps Script bị lỗi, bạn có thể xem nhanh danh sách vi phạm ngay dưới cuối trang
    with st.expander("Dành cho Giáo viên: Xem lịch sử vi phạm của phiên này"):
        st.write("Dữ liệu này sẽ mất khi bạn load lại trang (F5).")
        st.table(st.session_state.log_data)

else:
    st.warning("⚠️ Vui lòng nhập tên để nhận đề bài.")
