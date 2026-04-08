import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 1. PHẦN CÀI ĐẶT CỦA GIÁO VIÊN (THAY TẠI ĐÂY)
# ==========================================
# Dán link Web App bạn vừa copy từ Google Apps Script vào đây
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyKFr7YIkn5pM-lbkxaArABB7aRuAgIC4smJJh3Y8mcnEU-YG0yG8W2CFVIbAuRqY-b/exec"

# Dán link Google Form bài tập của bạn vào đây (nên dùng link có đuôi /viewform)
FORM_URL = "https://forms.gle/GUoUFW4vJAZ2gWTy9"
# ==========================================

# Cấu hình giao diện trang web
st.set_page_config(page_title="Hệ thống BTVN Toán", layout="wide")

# CSS để tối ưu hiển thị khung bài tập
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .iframe-container {
        position: relative;
        width: 100%;
        height: 850px;
        border: 2px solid #f0f2f6;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    iframe {
        width: 100%;
        height: 100%;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📝 Hệ thống Làm Bài Tập Trực Tuyến")
st.write("Vui lòng nhập tên và giữ tab này luôn mở trong suốt quá trình làm bài.")

# Nhập tên học sinh
name = st.text_input("Nhập họ và tên của em:", placeholder="Ví dụ: Nguyễn Văn A")

if name:
    # 2. JAVASCRIPT: THEO DÕI RỜI TAB VÀ GỬI DỮ LIỆU SANG GOOGLE SHEETS
    # Script này sẽ tự động chạy ngầm, học sinh không thể tắt
    components.html(
        f"""
        <script>
        var count = 0;
        document.addEventListener("visibilitychange", function() {{
            if (document.hidden) {{
                count++;
                // 1. Hiển thị cảnh báo ngay trên máy học sinh
                alert("Cảnh báo {name}: Em đã rời tab " + count + " lần. Hành vi này đã được báo về giáo viên!");
                
                // 2. Gửi dữ liệu thầm lặng về Google Sheets
                fetch('{WEBHOOK_URL}', {{
                    method: 'POST',
                    mode: 'no-cors',
                    cache: 'no-cache',
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify({{
                        name: '{name}',
                        action: 'Rời tab',
                        count: count
                    }})
                }});
            }}
        }});

        // Chặn chuột phải để hạn chế dùng công cụ tìm kiếm bên ngoài
        document.addEventListener('contextmenu', event => event.preventDefault());
        </script>
        """,
        height=0,
    )

    st.success(f"Đã xác nhận học sinh: **{name}**. Em có thể bắt đầu làm bài bên dưới.")

    # 3. HIỂN THỊ KHUNG BÀI TẬP (Có hỗ trợ cuộn mượt mà)
    st.markdown(
        f"""
        <div class="iframe-container">
            <iframe src="{FORM_URL}">Đang tải bài tập...</iframe>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.info("💡 Sau khi làm xong hết các câu hỏi, hãy nhớ nhấn nút **'Gửi' (Submit)** trong khung bài tập phía trên.")

else:
    st.warning("⚠️ Hệ thống đang chờ em nhập tên để mở đề bài.")
    # Hình ảnh hướng dẫn hoặc minh họa nếu muốn
    st.markdown("---")
    st.caption("Lưu ý: Mọi hành vi chuyển tab, mở tab mới đều sẽ bị hệ thống ghi lại tự động.")
