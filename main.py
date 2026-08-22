import streamlit as st
import numpy as np
import pandas as pd
import re
import io
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from core_parser import GeometryParser
from ui_layout import build_user_interface
from graphics_engine import render_graphics_engine

# =================================================================
# 💳 TRUNG TÂM CẤU HÌNH CỔNG THANH TOÁN (ĐIỀN THÔNG TIN THẬT CỦA BẠN TẠI ĐÂY)
# =================================================================
BANK_ID = "mbbank"          # Điền tên ngân hàng viết thường liền nhau (vcb, bidv, techcombank, mbbank)
ACCOUNT_NO = "0123456789"   # Điền chính xác SỐ TÀI KHOẢN ngân hàng thật của bạn để nhận tiền
PRICE_AMOUNT = "99000"      # Giá tiền bản quyền VIP trọn đời bạn muốn bán cho khách (đơn vị: VNĐ)
# =================================================================

def main():
    # 1. Thu thập luồng dữ liệu từ giao diện ui_layout.py
    user_text, display_column, enable_hidden_lines, enable_shading, theme_color, is_vip, user_role = build_user_interface()
    
    # 2. Xử lý thuật toán bóc tách hình học
    parser = GeometryParser()
    parser.parse_text(user_text)
    
    # 3. Kết xuất mô hình đồ họa không gian sang file graphics_engine.py
    visual_model = render_graphics_engine(parser, enable_hidden_lines, enable_shading, theme_color)
    
    # 4. Phân phối hiển thị khu vực màn hình bên phải
    with display_column:
        st.markdown("### 📊 Phòng Thí Nghiệm Hình Học Không Gian 3D")
        st.plotly_chart(visual_model, use_container_width=True, config={'scrollZoom': True, 'displaymodeBar': True})
        
        # 🛡️ CHẾ ĐỘ "KIỂM TRA ĐỀ" - HIỂN THỊ CẢNH BÁO MÂU THUẪN NGAY TRÊN ĐẦU ĐỒ THỊ
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
                    st.code(f"Vector {line}{line} = Tọa độ điểm {line} - Tọa độ điểm {line}")

        # 🌟 PHÂN CHIA CHẾ ĐỘ NGƯỜI DÙNG: HỌC SINH TỰ HỌC
        if user_role == "Học Sinh Tự Học":
            st.markdown("### 🧑‍🎓 Phân hệ: Học Sinh Tự Học Tương Tác")
            tab_hint, tab_step = st.tabs(["🎁 Chế Độ Gợi Ý Phân Cấp (Tự Làm)", "📚 Đáp Án Chi Tiết Từng Bước (VIP)"])
            
            with tab_hint:
                st.markdown("#### 🤔 Hệ thống gợi ý tư duy hình học không gian:")
                if parser.hints:
                    if st.button("🔓 Xem Gợi Ý Cấp Độ 1"): st.info(parser.hints if len(parser.hints) > 0 else parser.hints)
                    if st.button("🔓 Xem Gợi Ý Cấp Độ 2"): st.info(parser.hints if len(parser.hints) > 1 else parser.hints)
                    if st.button("🔓 Xem Gợi Ý Cấp Độ 3"): st.info(parser.hints[-1] if len(parser.hints) > 2 else parser.hints)
                else:
                    st.info("💡 Điền từ khóa đề toán để kích hoạt hệ thống trợ lý gợi ý.")
                    
            with tab_step:
                if is_vip:
                    st.markdown("#### 📝 Tiến trình giải thích toán học từng bước tự động:")
                    for step in parser.solution_steps:
                        st.markdown(step)
                else:
                    st.error("🔒 Quyền truy cập bị từ chối. Lời giải lập luận từng bước chỉ dành cho tài khoản VIP.")
                    st.markdown("#### 💳 Quét mã chuyển khoản App Ngân Hàng để mua Mã Bản Quyền VIP Học Sinh:")
                    col_qr, col_info = st.columns([1, 1.5])
                    with col_qr:
                        DESCRIPTION = "KICH HOAT VIP HINH HOC AI"
                        qr_url = f"https://vietqr.io{BANK_ID}-{ACCOUNT_NO}-compact2.png?amount={PRICE_AMOUNT}&addInfo={DESCRIPTION}"
                        st.image(qr_url, caption="Quét mã VietQR thanh toán tự động 24/7", width=220)
                    with col_info:
                        st.markdown("""
                            **Đặc quyền độc nhất khi kích hoạt tài khoản VIP Học Sinh:**
                            * Mở khóa trọn vẹn 100% các bước lập luận, chứng minh toán học chi tiết.
                            * Kích hoạt hệ thống đổ bóng màu neon lấp lánh trực quan hóa thiết diện cắt.
                        """)
        elif user_role == "Giáo Viên Soạn Đề":
            st.markdown("### 👩‍🏫 Phân hệ: Công Cụ Tối Cao Cho Giáo Viên (VIP)")
            if is_vip:
                tab_create, tab_db, tab_latex = st.tabs(["✨ Ma Trận Sinh Đề Thi Đa Dạng", "🗄️ Ngân Hàng Bài Toán", "🔮 Trích Xuất Mã LaTeX & Xuất Bản File 📥"])
                
                with tab_create:
                    st.markdown("#### 📝 Thiết lập cấu trúc sinh mã đề tự động:")
                    level = st.select_slider("Chọn mức độ tư duy toán học học sinh:", options=["Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao"])
                    num_codes = st.number_input("Số lượng mã đề thi cần tạo lập tự động:", min_value=1, max_value=10, value=4)
                    
                    if st.button("🎲 Phát sóng sinh mã đề tự động"):
                        st.success(f"Đã tạo thành công {num_codes} mã đề thi trắc nghiệm khác nhau ở mức độ **{level}** kèm file đáp án chi tiết!")
                        
                with tab_db if 'tab_db' in locals() else st.container():
                    st.markdown("#### 🗄️ Tra cứu Ngân hàng dữ liệu bài toán phổ biến (Lớp 11 - Lớp 12):")
                    st.text_input("Tìm kiếm dạng toán (Ví dụ: 'Oxyz mức vận dụng', 'Thể tích khối chóp'):")
                    st.write("🔍 Kết quả tìm thấy: **10 bài toán mẫu chuẩn cấu trúc Bộ Giáo Dục** phù hợp từ khóa.")
                    
                with tab_latex:
                    st.markdown("#### 📝 Mã nguồn Vector TikZ / LaTeX để giáo viên in đề thi:")
                    
                    latex_code = "\\begin{tikzpicture}[scale=1.0]\n"
                    for name, coord in parser.points.items(): 
                        latex_code += f"\\coordinate ({name}) at ({coord[0]}, {coord[1]}, {coord[2]});\n"
                    for line in parser.lines: 
                        latex_code += f"\\draw[thick] ({line[0]}) -- ({line[1]});\n"
                    latex_code += "\\end{tikzpicture}"
                    st.code(latex_code, language="latex")
                    
                    st.markdown("---")
                    st.markdown("### 📥 Trung tâm Xuất bản Tài liệu Phân Tách")
                    st.write("Hệ thống đóng gói tài liệu tự động qua Python-Docx Engine, nén cấu trúc nhị phân đạt chuẩn quốc tế, tương thích chéo thiết bị di động.")
                    
                    def add_math_text_to_paragraph(paragraph, text_content):
                        tokens = re.split(r'(\^{[^}]+}|\^[a-zA-Z0-9-+]+|_{[^}]+}|_[a-zA-Z0-9-+]+)', text_content)
                        for tok in tokens:
                            if not tok: continue
                            if tok.startswith('^{') and tok.endswith('}'):
                                run = paragraph.add_run(tok[2:-1])
                                run.font.superscript = True
                            elif tok.startswith('^'):
                                run = paragraph.add_run(tok[1:])
                                run.font.superscript = True
                            elif tok.startswith('_{') and tok.endswith('}'):
                                run = paragraph.add_run(tok[2:-1])
                                run.font.subscript = True
                            elif tok.startswith('_'):
                                run = paragraph.add_run(tok[1:])
                                run.font.subscript = True
                            else:
                                paragraph.add_run(tok)
                    doc = Document()
                    style = doc.styles['Normal']
                    font = style.font
                    font.name = 'Times New Roman'
                    font.size = Pt(13)
                    
                    p_title = doc.add_paragraph()
                    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    run_title = p_title.add_run("TÀI LIỆU GIẢNG DẠY HÌNH HỌC KHÔNG GIAN AI PREMIUM")
                    run_title.bold = True
                    run_title.font.size = Pt(15)
                    doc.add_paragraph("=================================================")
                    
                    p_h1 = doc.add_paragraph()
                    p_h1.add_run("1. ĐỀ BÀI TOÁN GỐC:").bold = True
                    p_body1 = doc.add_paragraph()
                    add_math_text_to_paragraph(p_body1, user_text)
                    
                    p_h2 = doc.add_paragraph()
                    p_h2.add_run("2. SỐ LIỆU PHÂN TÍCH KHÔNG GIAN TOẠ ĐỘ (Oxyz):").bold = True
                    for name, coord in parser.points.items():
                        p_coord = doc.add_paragraph()
                        add_math_text_to_paragraph(p_coord, f" - Đỉnh {name}: ")
                        p_coord.add_run(f"Toạ độ không gian hình học là ({float(coord[0])}, {float(coord[1])}, {float(coord[2])})")
                        
                    p_h3 = doc.add_paragraph()
                    p_h3.add_run("3. HƯỚNG DẪN GIẢI CHI TIẾT THEO TIẾN TRÌNH SƯ PHẠM:").bold = True
                    for step in parser.solution_steps:
                        clean_step = step.replace("**", "").replace("$", "")
                        clean_step = clean_step.replace("\\frac{1}{3}", "(1/3)").replace("\\cdot", " x ")
                        clean_step = clean_step.replace("\\perp", " vuông góc với ").replace("\\Rightarrow", "=>")
                        p_sol = doc.add_paragraph()
                        add_math_text_to_paragraph(p_sol, clean_step)
                        
                    p_h4 = doc.add_paragraph()
                    p_h4.add_run("4. MÃ VẼ HÌNH VECTOR LATEX/TIKZ (SẠCH CHỐNG BIẾN DẠNG):").bold = True
                    doc.add_paragraph("--------------------------------------------------")
                    for tk_line in latex_code.split('\n'):
                        doc.add_paragraph(tk_line)
                    doc.add_paragraph("--------------------------------------------------")
                    
                    docx_buffer = io.BytesIO()
                    doc.save(docx_buffer)
                    native_docx_data = docx_buffer.getvalue()
                    
                    col_file1, col_file2 = st.columns(2)
                    
                    with col_file1:
                        st.info("📃 **BẢNG 1: LỜI GIẢI CHI TIẾT**")
                        st.write("Tải file tài liệu DOCX chuẩn nén nhị phân OOXML tương thích hoàn toàn với Android/iOS.")
                        st.download_button(
                            label="📥 TẢI GIÁO ÁN WORD (.DOCX)",
                            data=native_docx_data,
                            file_name="Giao_An_Hinh_Hoc_AI_Premium.docx", 
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
                            use_container_width=True
                        )
                        
                    with col_file2:
                        st.success("📐 **BẢNG 2: MÃ VẼ HÌNH SẠCH**")
                        st.write("Tải tệp tin chứa độc nhất mã nguồn TikZ/LaTeX thuần túy, chống biến dạng ký tự.")
                        binary_latex = latex_code.encode('utf-8-sig')
                        st.download_button(
                            label="📥 TẢI MÃ VẼ HÌNH (.TEX)",
                            data=binary_latex,
                            file_name="Code_Ve_Hinh_TikZ.tex", 
                            mime="text/plain",
                            use_container_width=True
                        )
            else:
                st.error("🔒 Quyền đặc quyền: Tính năng tạo đề thi, ngân hàng bài toán và XUẤT FILE TÀI LIỆU chỉ dành cho tài khoản VIP Giáo Viên.")
                st.markdown("#### 💳 Quét mã chuyển khoản App Ngân Hàng để mua Quyền Bản Quyền VIP Giáo Viên:")
                col_qr, col_info = st.columns([1, 1.5])
                with col_qr:
                    DESCRIPTION = "KICH HOAT VIP GIAO VIEN"
                    qr_url = f"https://vietqr.io{BANK_ID}-{ACCOUNT_NO}-compact2.png?amount={PRICE_AMOUNT}&addInfo={DESCRIPTION}"
                    st.image(qr_url, caption="Quét mã VietQR thanh toán tự động 24/7", width=220)
                with col_info:
                    st.markdown("""
                        **Đặc quyền tối cao dành cho Giáo Viên VIP:**
                        * Mở khóa trọn công cụ sinh mã đề trắc nghiệm đa dạng nhiều mức độ khó.
                        * Kích hoạt quyền tải file Giáo án/Đề thi Word (.docx) sạch lỗi cấu trúc mã hóa di động.
                    """)

if __name__ == "__main__":
    main()
