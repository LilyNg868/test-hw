import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang
st.set_page_config(page_title="Hệ thống BTVN Toán", layout="wide")

st.title("📝 Hệ thống Làm Bài Tập Trực Tuyến")
st.write("Cảnh báo: Không được rời khỏi tab này khi đang làm bài.")

# Nhập tên học sinh
name = st.text_input("Nhập họ và tên của em để bắt đầu:")

if name:
    # Đoạn mã theo dõi chuyển tab
    components.html(
        f"""
        <script>
        document.addEventListener("visibilitychange", function() {{
            if (document.hidden) {{
                alert("Cảnh báo {name}: Hệ thống đã ghi nhận em rời tab!");
            }}
        }});
        </script>
        """,
        height=0,
    )

    # NHÚNG LINK BÀI TẬP CỦA BẠN VÀO ĐÂY
    # Thay link dưới bằng link Google Form của bạn
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSd-p_YfK6U-vN9-f7vKzK-zN-zN-zN-zN/viewform?embedded=true"
    
    st.components.v1.iframe(form_url, height=900, scrolling=True)

else:
    st.info("Vui lòng nhập tên để hiện bài tập.")
