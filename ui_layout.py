import streamlit as st

def build_user_interface():
    # Đã sửa toàn bộ thành unsafe_allow_html
    st.markdown("""
        <style>
        .main-title { font-size:40px !important; color: #1E3A8A; font-weight: bold; text-align: center; }
        .sub-title { font-size:18px !important; color: #4B5563; text-align: center; margin-bottom: 30px; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="main-title">🌌 Siêu Ứng Dụng Hình Học Không Gian AI - Cosmic V4</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Nền tảng trợ giảng số thế hệ mới dành cho Giáo viên & Học sinh chuyên nghiệp</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown("### 📝 Trung tâm Nhập liệu Ngôn ngữ tự nhiên")
        
        # Bài toán thiết diện mẫu đỉnh cao
        cosmic_prompt = (
            "Cho hình chóp S.ABCD có đáy là hình vuông, SA vuông góc với đáy.\n"
            "Gọi M là trung điểm của SB.\n"
            "Xác định điểm N trên cạnh SD sao cho N(0, 2, 2.5).\n"
            "Nối đoạn thẳng AM, MN, NA.\n"
            "Hãy hiển thị thiết diện mặt phẳng AMN."
        )
        
        user_input = st.text_area("Nhập mô tả đề toán hình học (SGK hoặc nâng cao):", value=cosmic_prompt, height=200)
        
        st.markdown("### 🎛️ Bảng Điều Khiển Vũ Trụ")
        enable_hidden_lines = st.checkbox("Chế độ SGK: Tự động phân tách Nét Đứt / Nét Liền", value=True)
        enable_shading = st.checkbox("Chế độ Thiết Diện: Tô màu mờ các bề mặt hình học", value=True)
        theme_color = st.color_picker("Chọn màu sắc đổ bóng thiết diện chủ đạo:", "#00f5d4")
        
        st.markdown("---")
        st.success("🛸 **Mẹo Không Gian:** Di chuột lên hình 3D để quét tọa độ, bấm biểu tượng máy ảnh trên thanh công cụ đồ họa để tải ảnh PNG chất lượng in ấn đề thi.")

    return user_input, col2, enable_hidden_lines, enable_shading, theme_color
