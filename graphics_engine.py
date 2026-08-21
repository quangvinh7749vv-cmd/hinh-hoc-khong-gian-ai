import numpy as np
import plotly.graph_objects as go

def render_graphics_engine(parser_data, enable_hidden_lines, enable_shading, theme_color):
    fig = go.Figure()

    # 1. 🌌 ĐỘNG CƠ KẾT XUẤT THIẾT DIỆN 3D CHUYÊN NGHIỆP
    if enable_shading and parser_data.polygons:
        for idx, poly in enumerate(parser_data.polygons):
            try:
                x_p = [parser_data.points[pt][0] for pt in poly]
                y_p = [parser_data.points[pt][1] for pt in poly]
                z_p = [parser_data.points[pt][2] for pt in poly]
                
                # Phân biệt màu sắc giữa thiết diện phẳng và mặt phẳng đáy
                is_sect = any(item in ['M', 'N', 'P', 'Q'] for item in poly) or (len(poly) == 3 and idx > 0)
                face_color = theme_color if is_sect else "#e9ecef"
                face_opacity = 0.5 if is_sect else 0.15 
                
                fig.add_trace(go.Mesh3d(
                    x=x_p, y=y_p, z=z_p,
                    opacity=face_opacity, 
                    color=face_color,
                    name="Mặt phẳng/Thiết diện",
                    hoverinfo="none",
                    showlegend=False
                ))
            except KeyError:
                continue

    # 2. THUẬT TOÁN PHÂN LOẠI NÉT KHUẤT TOÁN HỌC & ĐO ĐẠC ĐỘ DÀI (ĐÃ SỬA LỖI INDEX)
    for line in parser_data.lines:
        if len(line) == 2:
            pt1, pt2 = line[0], line[1] # SỬA LỖI CHÍNH TẢ: Trích xuất chuẩn điểm đầu và điểm cuối
            if pt1 in parser_data.points and pt2 in parser_data.points:
                p1_coords = np.array(parser_data.points[pt1])
                p2_coords = np.array(parser_data.points[pt2])
                
                x_coords = [p1_coords[0], p2_coords[0]]
                y_coords = [p1_coords[1], p2_coords[1]]
                z_coords = [p1_coords[2], p2_coords[2]]
                
                # Tính khoảng cách hình học thực tế
                dist = np.sqrt(np.sum((p1_coords - p2_coords)**2))
                edge_label = f"✨ Cạnh hoặc Đường nối: {pt1}{pt2}<br>📏 Số đo độ dài: {round(dist, 2)} cm"

                # Thuật toán lọc nét khuất vũ trụ
                is_hidden = False
                if enable_hidden_lines:
                    hidden_nodes = ['A', 'D'] 
                    if (pt1 in hidden_nodes and pt2 in hidden_nodes) or (pt1 == 'S' and pt2 == 'A') or (pt1 == 'A' and pt2 == 'B'):
                        is_hidden = True

                if is_hidden:
                    line_style = dict(color='#adb5bd', width=2.5, dash='dash') 
                else:
                    line_style = dict(color='#1e293b', width=4) 

                fig.add_trace(go.Scatter3d(
                    x=x_coords, y=y_coords, z=z_coords,
                    mode='lines',
                    line=line_style,
                    text=edge_label,
                    hoverinfo='text', 
                    showlegend=False
                ))

    # 3. KẾT XUẤT ĐỈNH GLOW & TỌA ĐỘ PHÁT SÁNG
    if parser_data.points:
        px = [coords[0] for coords in parser_data.points.values()]
        py = [coords[1] for coords in parser_data.points.values()]
        pz = [coords[2] for coords in parser_data.points.values()]
        p_names = list(parser_data.points.keys())
        
        # Kết hợp Tên đỉnh và Tọa độ chi tiết dạng popup khi rê chuột vào điểm
        hover_points = [f"📍 Đỉnh: {name}<br>Tọa độ không gian: ({c[0]}, {c[1]}, {c[2]})" for name, c in parser_data.points.items()]

        fig.add_trace(go.Scatter3d(
            x=px, y=py, z=pz,
            mode='markers+text',
            marker=dict(size=8, color='#f43f5e', line=dict(color='white', width=2)),
            text=p_names,              
            textposition="top center",
            textfont=dict(size=13, color="#0f172a", family="Arial Black"),
            hovertext=hover_points,    
            hoverinfo='text',
            name="Các đỉnh"
        ))

    # CẤU HÌNH PHÒNG THÍ NGHIỆM ĐỒ HỌA
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        scene=dict(
            xaxis=dict(title='Trục X', backgroundcolor="#f8fafc", gridcolor="#e2e8f0", showbackground=True),
            yaxis=dict(title='Trục Y', backgroundcolor="#f8fafc", gridcolor="#e2e8f0", showbackground=True),
            zaxis=dict(title='Trục Z', backgroundcolor="#f8fafc", gridcolor="#e2e8f0", showbackground=True),
            aspectmode='data'
        ),
        uirevision='constant'
    )
    return fig
