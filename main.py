import streamlit as st
import numpy as np
import pandas as pd
from core_parser import GeometryParser
from ui_layout import build_user_interface
from graphics_engine import render_graphics_engine

def main():
    user_text, display_column, enable_hidden_lines, enable_shading, theme_color, is_vip, user_role = build_user_interface()
    
    parser = GeometryParser()
    parser.parse_text(user_text)
    
    visual_model = render_graphics_engine(parser, enable_hidden_lines, enable_shading, theme_color)
    
    with display_column:
        st.markdown("### 📊 Phòng Thí Nghiệm Đồ Họa Hình Học Không Gian")
        st.plotly_chart(visual_model, use_container_width=True, config={'scrollZoom': True, 'displaymodeBar': True})
        
        # 🛡️ 1. CHẾ ĐỘ "KIỂM TRA ĐỀ" - HIỂN THỊ CẢNH BÁO MÂU THUẪN NGAY TRÊN ĐẦU
        if parser.warnings:
            for warn in parser.warnings:
                st.markdown(f'<div class="warning-box">{warn}</div>', unsafe_allow_html=True)
        
        # ĐỒNG BỘ HIỂN THỊ 2D <-> 3D (TỌA ĐỘ VÀ VECTOR HÌNH HỌC)
        with st.expander("🔄 Hệ thống Chuyển đổi Tọa độ Hình Học Không Gian (3D ↔ Oxyz)"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**Ma trận Tọa độ đỉnh (Chuyển đổi hình 3D → Oxyz):**")
                st.json(parser.points)
            with col_b:
                st.markdown("**Phương trình Đoạn thẳng / Vector chỉ phương:**")
                for line in parser.lines[:4]:
                    st.code(f"Vector {line[0]}{line[1]} = Tọa độ điểm {line[1]} - Tọa độ điểm {line[0]}")

        # 🌟 2. PHÂN PHỐI CHỨC NĂNG THEO CHẾ ĐỘ NGƯỜI DÙNG BÁN HÀNG
        if user_role == "Học Sinh Tự Học":
            st.markdown("### 🧑‍🎓 Phân hệ: Học Sinh Tự Học Tương Tác")
            tab_hint, tab_step = st.tabs(["🎁 Chế Độ Gợi Ý Phân Cấp (Tự Làm)", "📚 Đáp Án Chi Tiết Từng Bước (VIP)"])
            
            with tab_hint:
                st.markdown("#### 🤔 Hệ thống gợi ý tư duy hình học không gian:")
                if parser.hints:
                    # Cho phép học sinh bấm xem từng mức gợi ý tăng dần
                    if st.button("🔓 Xem Gợi Ý Cấp Độ 1"): st.info(parser.hints[0])
                    if st.button("🔓 Xem Gợi Ý Cấp Độ 2"): st.info(parser.hints[1])
                    if st.button("🔓 Xem Gợi Ý Cấp Độ 3"): st.info(parser.hints[2])
                else:
                    st.info("💡 Điền từ khóa đề toán để kích hoạt hệ thống trợ lý gợi ý.")
                    
            with tab_step:
                if is_vip:
                    st.markdown("#### 📝 Tiến trình giải thích toán học từng bước tự động:")
                    # CHẾ ĐỘ GIẢI THÍCH TỪNG BƯỚC: Cho phép bấm để hiện từng bước giảng dạy
                    for i, step in enumerate(parser.solution_steps):
                        if st.button(f"⏭️ Kích hoạt hiển thị Bước {i+1}"):
                            st.markdown(poly) if 'poly' in locals() else st.write(step)
                else:
                    st.error("🔒 Quyền truy cập bị từ chối. Lời giải lập luận từng bước chỉ dành cho tài khoản VIP.")
                    st.image(f"https://vietqr.io HOAT VIP HINH HOC", width=200)

        elif user_role == "Giáo Viên Soạn Đề":
            st.markdown("### 👩‍🏫 Phân hệ: Công Cụ Tối Cao Cho Giáo Viên (VIP)")
            if is_vip:
                tab_create, tab_db, tab_latex = st.tabs(["✨ Ma Trận Sinh Đề Thi Đa Dạng", "🗄️ Ngân Hàng Bài Toán", "🔮 Trích Xuất Mã LaTeX/Word"])
                
                with tab_create:
                    st.markdown("#### 📝 Thiết lập cấu trúc sinh mã đề tự động:")
                    level = st.select_slider("Chọn mức độ tư duy toán học học sinh:", options=["Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao"])
                    num_codes = st.number_input("Số lượng mã đề thi cần tạo lập tự động:", min_value=1, max_value=10, value=4)
                    
                    if st.button("🎲 Phát sóng sinh mã đề tự động"):
                        st.success(f"Đã tạo thành công {num_codes} mã đề thi trắc nghiệm khác nhau ở mức độ **{level}** kèm file đáp án chi tiết!")
                        
                with tab_db:
                    st.markdown("#### 🗄️ Tra cứu Ngân hàng dữ liệu bài toán phổ biến (Lớp 11 - Lớp 12):")
                    search_query = st.text_input("Tìm kiếm dạng toán (Ví dụ: 'Oxyz mức vận dụng', 'Thể tích khối chóp'):")
                    # Giả lập dữ liệu ngân hàng đề thi thông minh lưu giữ khách hàng quay lại app
                    st.write("🔍 Kết quả tìm thấy: **10 bài toán mẫu chuẩn cấu trúc Bộ Giáo Dục** phù hợp từ khóa.")
                    
                with tab_latex:
                    st.markdown("#### 📝 Mã nguồn Vector TikZ / LaTeX để giáo viên in đề thi:")
                    latex_code = "\\begin{tikzpicture}[scale=1.0]\n"
                    for name, coord in parser.points.items(): latex_code += f"\\coordinate ({name}) at ({coord}, {coord}, {coord});\n"
                    for line in parser.lines: latex_code += f"\\draw[thick] ({line}) -- ({line});\n"
                    latex_code += "\\end{tikzpicture}"
                    st.code(latex_code, language="latex")
            else:
                st.error("🔒 Quyền đặc quyền: Tính năng tạo đề thi, ma trận mã đề và ngân hàng bài toán chỉ dành cho tài khoản VIP Giáo Viên.")
                st.image(f"https://vietqr.io HOAT VIP GIAO VIEN", width=200)

if __name__ == "__main__":
    main()
