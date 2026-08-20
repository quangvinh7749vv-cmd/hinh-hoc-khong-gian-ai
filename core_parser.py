import re
import numpy as np

class GeometryParser:
    def __init__(self):
        self.points = {}
        self.lines = []
        self.polygons = [] 
        self.shapes_detected = []
        self.analytics = {} # Lưu trữ kết quả tính toán tự động (Thể tích, Diện tích...)

    def parse_text(self, text):
        self.points = {}
        self.lines = []
        self.polygons = []
        self.analytics = {}
        
        raw_text = text.lower()
        
        # 🤖 HỆ THỐNG NLP TOÁN HỌC CAO CẤP
        # Trường hợp 1: Hình chóp S.ABCD đáy hình vuông/chữ nhật, SA vuông góc đáy
        if "s.abcd" in raw_text and "vuông góc" in raw_text:
            self.points['A'] = [0.0, 0.0, 0.0]
            self.points['B'] = [4.0, 0.0, 0.0]
            self.points['C'] = [4.0, 4.0, 0.0]
            self.points['D'] = [0.0, 4.0, 0.0]
            self.points['S'] = [0.0, 0.0, 5.0]
            self.polygons.append(['A', 'B', 'C', 'D'])
            self.shapes_detected.append("pyramid_square")
            
            # Tự động tính toán đại số không gian
            s_day = 4.0 * 4.0
            h = 5.0
            v = (1/3) * s_day * h
            self.analytics["Diện tích đáy (S_abcd)"] = f"{s_day} đvdt"
            self.analytics["Chiều cao hình chóp (SA)"] = f"{h} đvđd"
            self.analytics["Thể tích khối chóp V(S.abcd)"] = f"{round(v, 2)} đvtt"

        # Trường hợp 2: Hình lăng trụ tam giác đều/đứng ABC.A'B'C'
        elif "lăng trụ" in raw_text or "abc.a'b'c'" in raw_text:
            self.points['A'] = [0.0, 0.0, 0.0]
            self.points['B'] = [4.0, 0.0, 0.0]
            self.points['C'] = [2.0, 3.46, 0.0] # Tam giác đều cạnh 4
            self.points["A'"] = [0.0, 0.0, 5.0]
            self.points["B'"] = [4.0, 0.0, 5.0]
            self.points["C'"] = [2.0, 3.46, 5.0]
            self.polygons.append(['A', 'B', 'C'])
            self.polygons.append(["A'", "B'", "C'"])
            self.shapes_detected.append("prism_triangular")
            
            s_day = (4.0**2 * np.sqrt(3)) / 4
            h = 5.0
            v = s_day * h
            self.analytics["Diện tích đáy tam giác đều"] = f"{round(s_day, 2)} đvdt"
            self.analytics["Chiều cao lăng trụ"] = f"{h} đvđd"
            self.analytics["Thể tích khối lăng trụ V(ABC.A'B'C')"] = f"{round(v, 2)} đvtt"

        # CƠ CHẾ QUÉT ĐIỂM ĐẶC BIỆT THỦ CÔNG / TRUNG ĐIỂM / TRỌNG TÂM
        point_coord_match = re.findall(r"([A-Z]'?)\s*\(\s*([-\d.]+)\s*,\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\)", text)
        for match in point_coord_match:
            name, x, y, z = match
            self.points[name] = [float(x), float(y), float(z)]

        # TỰ ĐỘNG TÍNH TOÁN TRUNG ĐIỂM NẾU CÓ YÊU CẦU (Ví dụ: "M là trung điểm SB")
        midpoint_match = re.search(r"([a-z])\s+là\s+trung\s+điểm\s+của?\s+([a-z])([a-z])", raw_text)
        if midpoint_match:
            m_name = midpoint_match.group(1).upper()
            p1 = midpoint_match.group(2).upper()
            p2 = midpoint_match.group(3).upper()
            if p1 in self.points and p2 in self.points:
                c1, c2 = np.array(self.points[p1]), np.array(self.points[p2])
                self.points[m_name] = list(np.round((c1 + c2) / 2, 2))

        # DỰNG KHUNG HÌNH HỌC TỰ ĐỘNG
        if "pyramid_square" in self.shapes_detected:
            base = ['A', 'B', 'C', 'D']
            for i in range(len(base)):
                self.lines.append([base[i], base[(i+1)%len(base)]])
                self.lines.append(['S', base[i]])
        elif "prism_triangular" in self.shapes_detected:
            self.lines.extend([['A','B'], ['B','C'], ['C','A'], ["A'","B'"], ["B'","C'"], ["C'","A'"]])
            self.lines.extend([['A',"A'"], ['B',"B'"], ['C',"C'"]])

        # Tìm các đoạn thẳng nối thêm thủ công bằng chữ in hoa (Ví dụ: nối MN, kẻ AH)
        line_matches = re.findall(r"\b([A-Z]'?)([A-Z]'?)\b", text)
        for match in line_matches:
            p1, p2 = match
            if p1 in self.points and p2 in self.points and [p1, p2] not in self.lines:
                self.lines.append([p1, p2])

        # 🎯 THUẬT TOÁN NHẬN DIỆN MẶT PHẲNG THIẾT DIỆN (Ví dụ: "thiết diện thiết lập bởi M, N, P" hoặc "mặt phẳng MNP")
        surface_matches = re.findall(r"(?:mặt phẳng|thiết diện)\s*([a-z']{3,4})", raw_text)
        for match in surface_matches:
            upper_poly = [c.upper() for c in match]
            if all(pt in self.points for pt in upper_poly):
                self.polygons.append(upper_poly)
