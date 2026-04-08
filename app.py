import streamlit as st
import streamlit.components.v1 as components

# 1. CẤU HÌNH
st.set_page_config(page_title="Hệ thống BTVN Toán", layout="wide")

# --- PHẦN CÀI ĐẶT ---
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyKFr7YIkn5pM-lbkxaArABB7aRuAgIC4smJJh3Y8mcnEU-YG0yG8W2CFVIbAuRqY-b/exec"
FORM_URL = "https://forms.gle/zCyo1bFcdMQQq6Lz6"
# --------------------

st.title("📝 Hệ thống Làm Bài Tập Trực Tuyến")

# Khởi tạo trạng thái nộp bài trong session_state
if 'is_done' not in st.session_state:
    st.session_state.is_done = False

name = st.text_input("Nhập họ và tên của em:", placeholder="Ví dụ: Nguyễn Văn A")

if name:
    # 2. JAVASCRIPT THÔNG MINH
    # Tự động phát hiện khi Iframe thay đổi nội dung (nộp bài xong)
    components.html(
        f"""
        <script>
        var count = 0;
        var isFinished = false;

        // Lắng nghe sự kiện rời tab
        document.addEventListener("visibilitychange", function() {{
            if (!isFinished && document.hidden) {{
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

        // Lắng nghe tin nhắn từ hệ thống để ngừng giám sát
        window.addEventListener("message", function(event) {{
            if (event.data === "STOP_MONITORING") {{
                isFinished = true;
                console.log("Đã dừng giám sát tự động.");
            }}
        }});
        </script>
        """,
        height=0,
    )

    if not st.session_state.is_done:
        st.info(f"Học sinh: **{name}**. Hệ thống đang giám sát tự động.")
        
        # 3. HIỂN THỊ KHUNG BÀI TẬP
        # Thêm nút bấm "Xong" thủ công đề phòng trường hợp tự động bị trình duyệt chặn
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
            if st.button("Nộp bài xong"):
                st.session_state.is_done = True
                st.rerun()

    else:
        st.balloons()
        st.success("Hệ thống đã ngừng giám sát. Em có thể nghỉ ngơi!")
else:
    st.warning("Vui lòng nhập tên.")
