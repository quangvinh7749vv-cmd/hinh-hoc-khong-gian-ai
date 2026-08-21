import streamlit as st

def build_user_interface():
    st.markdown("""
        <style>
        .main-title { font-size:36px !important; color: #1E3A8A; font-weight: bold; text-align: center; }
        .sub-title { font-size:16px !important; color: #4B5563; text-align: center; margin-bottom: 25px; }
        .warning-box { padding: 12px; background-color: #f8d7da; color: #721c24; border-left: 5px solid #dc3545; border-radius: 4px; margin-bottom: 15px; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="main-title">🚀 Siêu Nền Tảng Hình Học Không Gian AI - Cosmic V6</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Hệ thống chuyển đổi cấu trúc Không Gian 2D/3D & Quản trị Sư phạm Độc quyền</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.4])
    
    with col1:
        st.markdown("### 🔐 Bản Quyền Phần Mềm")
        license_key = st.text_input("Nhập Mã Bản Quyền VIP cá nhân:", type="password", placeholder="Nhập mã...")
        VALID_VIP_KEYS = ["VIP_COSMIC_99", "GIAOVIEN_TOAN_2026", "HOCSINH_VIP_PRO", "QUANGVINH_TRIEUDO"]
        is_vip = (license_key in VALID_VIP_KEYS)
        
        if is_vip:
            st.sidebar.success("👑 KHÁCH HÀNG VIP: Đã kích hoạt đầy đủ đặc quyền!")
        
        st.markdown("---")
        # Chọn phân hệ người dùng thương mại
        user_role = st.selectbox("🎯 Chọn phân hệ người dùng:", ["Học Sinh Tự Học", "Giáo Viên Soạn Đề"])
        
        st.markdown("### 📝 Ô Nhập Đề Bài")
        cosmic_prompt = (
            "Cho hình chóp S.ABCD có đáy là hình vuông cạnh bằng 4.\n"
            "Biết cạnh bên SA vuông góc với đáy, SA = 5.\n"
            "Gọi M là trung điểm của SB.\n"
            "Kẻ thiết diện mặt phẳng AMN."
        )
        user_input = st.text_area("Nhập mô tả đề bài toán hình học phẳng:", value=cosmic_prompt, height=150)
        
        st.markdown("### 🎛️ Tùy chọn nâng cao")
        enable_hidden_lines = st.checkbox("Chế độ mô phỏng nét đứt khuất lý thuyết (SGK)", value=True)
        enable_shading = is_vip and st.checkbox("Đổ bóng màu chuyển sắc khối hình học", value=True)
        theme_color = st.color_picker("Tông màu thiết diện chủ đạo:", "#00f5d4") if is_vip else "#e9ecef"
            
    # ĐỒNG BỘ: Trả về chính xác và đầy đủ cả 7 tham số dữ liệu
    return user_input, col2, enable_hidden_lines, enable_shading, theme_color, is_vip, user_role
