import streamlit as st
import streamlit.components.v1 as components

# 1. CẤU HÌNH
st.set_page_config(page_title="Hệ thống BTVN Toán", layout="wide")

# --- PHẦN CÀI ĐẶT ---
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyKFr7YIkn5pM-lbkxaArABB7aRuAgIC4smJJh3Y8mcnEU-YG0yG8W2CFVIbAuRqY-b/exec"
FORM_URL = "https://forms.gle/8Tv699JS13Y7M13o7"
# --------------------

st.title("📝 Hệ thống Làm Bài Tập Trực Tuyến")

# Khởi tạo trạng thái nộp bài
if 'is_done' not in st.session_state:
    st.session_state.is_done = False

name = st.text_input("Nhập họ và tên của em:", placeholder="Ví dụ: Nguyễn Văn A")

if name:
    # 2. JAVASCRIPT GIÁM SÁT CÓ ĐIỀU KIỆN
    # Sử dụng một biến 'isMonitoring' để bật/tắt cảnh báo
    # Khi st.session_state.is_done là True, biến này sẽ thành false
    monitoring_status = "false" if st.session_state.is_done else "true"
    
    components.html(
        f"""
        <script>
        var count = 0;
        var isMonitoring = {monitoring_status};

        document.addEventListener("visibilitychange", function() {{
            // CHỈ hiện cảnh báo nếu isMonitoring đang là true
            if (isMonitoring && document.hidden) {{
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

    # 3. HIỂN THỊ GIAO DIỆN
    cols = st.columns([8, 2])
    
    with cols[0]:
        # Khung bài tập luôn được hiển thị để học sinh có thể xem điểm sau khi nộp
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
        if not st.session_state.is_done:
            st.info("Hệ thống đang giám sát chuyển tab.")
            if st.button("XÁC NHẬN ĐÃ NỘP BÀI"):
                st.session_state.is_done = True
                st.rerun()
        else:
            st.success("✅ ĐÃ TẮT GIÁM SÁT")
            st.write("Bây giờ em có thể chuyển tab thoải mái và bấm 'Xem điểm' trong khung bên cạnh.")
            if st.button("Tiếp tục làm bài (Bật lại giám sát)"):
                st.session_state.is_done = False
                st.rerun()

else:
    st.warning("Vui lòng nhập tên để bắt đầu.")
