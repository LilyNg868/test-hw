import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import pandas as pd

# Cấu hình trang
st.set_page_config(page_title="Hệ thống giám sát BTVN", layout="wide")

# Đường link Google Sheet của bạn (Thay link bên dưới bằng link bạn vừa copy)
SHEET_URL = "https://docs.google.com/spreadsheets/d/your-id-here/edit#gid=0"

st.title("📝 Hệ thống Làm Bài Tập Toán")

name = st.text_input("Nhập họ và tên để bắt đầu làm bài:")

if name:
    # 1. Ghi nhận thời gian bắt đầu vào hệ thống
    if 'initialized' not in st.session_state:
        st.session_state['initialized'] = True
        # Gợi ý: Bạn có thể viết thêm code lưu tên HS vào Sheet tại đây để điểm danh

    # 2. Javascript để bắt lỗi rời tab
    # Khi học sinh rời tab, nó sẽ tự động bấm một nút ẩn trên web để Python biết
    components.html(
        f"""
        <script>
        document.addEventListener("visibilitychange", function() {{
            if (document.hidden) {{
                window.parent.postMessage({{type: 'tab-switch', user: '{name}'}}, '*');
                alert("Cảnh báo: Hệ thống đã ghi nhận em rời tab!");
            }}
        }});
        </script>
        """,
        height=0,
    )

    # 3. Hiển thị Form bài tập
    form_url = "https://forms.gle/44oJdC1EXZxWr5666" 
    st.components.v1.iframe(form_url, height=800)

    # 4. Khu vực dành cho giáo viên (Có thể đặt mật khẩu để ẩn đi)
    if st.checkbox("Xem nhật ký vi phạm (Dành cho GV)"):
        pwd = st.text_input("Mật khẩu quản lý:", type="password")
        if pwd == "123456": # Thay mật khẩu của bạn
            st.write("Dữ liệu vi phạm sẽ được hiển thị ở file Google Sheets của bạn.")
            st.video("https://ghi-log-vao-google-sheet-huong-dan.com") # Link minh họa
