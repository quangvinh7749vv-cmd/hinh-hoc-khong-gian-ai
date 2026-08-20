import streamlit as st
import numpy as np
import pandas as pd
from core_parser import GeometryParser
from ui_layout import build_user_interface
from graphics_engine import render_graphics_engine

def main():
    # 1. Gọi giao diện người dùng
    user_text, display_column, enable_hidden_lines, enable_shading, theme_color = build_user_interface()
    
    # 2. Xử lý bộ dịch thuật toán hình học
    parser = GeometryParser()
    parser.parse_text(user_text)
    
    # 3. Kết xuất mô hình đồ họa 3D tương tác
    visual_model = render_graphics_engine(parser, enable_hidden_lines, enable_shading, theme_color)
    
    # 4. Khu vực phân phối hiển thị bên phải
    with display_column:
        st.markdown("### 📊 Phòng Thí Nghiệm Đồ Họa Không Gian 3D")
        
        # Công cụ tải ảnh PNG chất lượng in ấn cực cao
        st.plotly_chart(
            visual_model, 
            use_container_width=True, 
            config={
                'scrollZoom': True,
                'displaymodeBar': True,
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': 'cosmic_geometry_export',
                    'height': 900,
                    'width': 1400,
                    'scale': 3 
                }
            }
        )
        
        # 🌟 HỆ THỐNG PHÂN PHỐI TIỆN ÍCH DÀNH CHO GIÁO VIÊN & HỌC SINH (COMMERCIAL VALUE)
        tab1, tab2, tab3 = st.tabs(["📐 Trợ Lý Giải Toán Tự Động", "📋 Ma Trận Đo Đạc", "🔮 Trung Tâm Xuất Bản LaTeX/TikZ"])
        
        with tab1:
            st.markdown("#### 🤖 Kết quả phân tích & Tính toán Khối đa diện đại số:")
            if parser.analytics:
                for key, val in parser.analytics.items():
                    st.metric(label=key, value=val)
            else:
                st.info("💡 Điền từ khóa sách giáo khoa như 'hình chóp S.ABCD có đáy là hình vuông, SA vuông góc' để kích hoạt máy tính thể tích tự động.")
                
        with tab2:
            st.markdown("#### 📏 Khoảng cách thực tế giữa mọi cặp điểm trong bài toán:")
            if len(parser.points) >= 2:
                point_list = list(parser.points.keys())
                matrix = []
                for p1 in point_list:
                    row = []
                    for p2 in point_list:
                        if p1 == p2: row.append("-")
                        else:
                            c1, c2 = np.array(parser.points[p1]), np.array(parser.points[p2])
                            row.append(f"{round(np.sqrt(np.sum((c1-c2)**2)), 2)} cm")
                    matrix.append(row)
                df = pd.DataFrame(matrix, index=point_list, columns=point_list)
                st.dataframe(df, use_container_width=True)
                
        with tab3:
            st.markdown("#### 📝 Mã nguồn Vector TikZ / LaTeX dành cho Giáo viên soạn đề thi:")
            st.markdown("Thầy cô chỉ cần copy đoạn mã cấu trúc điểm này để dán thẳng vào tài liệu giảng dạy:")
            
            # Tự động sinh mã tọa độ định dạng LaTeX chuyên nghiệp
            latex_code = "\\begin{tikzpicture}[scale=1.0]\n"
            for name, coord in parser.points.items():
                latex_code += f"\\coordinate ({name}) at ({coord[0]}, {coord[1]}, {coord[2]});\n"
            for line in parser.lines:
                latex_code += f"\\draw[thick] ({line[0]}) -- ({line[1]});\n"
            latex_code += "\\end{tikzpicture}"
            
            st.code(latex_code, language="latex")

if __name__ == "__main__":
    main()
