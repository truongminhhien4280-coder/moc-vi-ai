import streamlit as st
import google.generativeai as genai

# Cấu hình Web
st.set_page_config(page_title="Vấn Chẩn AI - Mộc Vị", page_icon="🌿", layout="centered")
st.title("🌿 Hệ Thống Vấn Chẩn YHCT - Mộc Vị")
st.markdown("Trả lời các câu hỏi dưới đây để AI phân tích thể trạng và tư vấn dòng sản phẩm phù hợp.")

# Lấy API Key bí mật từ hệ thống
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Chưa cấu hình API Key bảo mật!")
    st.stop()

# (BẠN COPY BỘ 20 CÂU HỎI VÀO ĐÂY, giữ nguyên cấu trúc như bài trước)
questions = [
    {"id": 1, "part": 1, "text": "Câu 1: Thời gian để bạn đi vào giấc ngủ mỗi đêm thường mất bao lâu?", 
     "options": {"A. Dưới 15 phút.": 0, "B. Khoảng 30 phút.": 1, "C. Trằn trọc 1 - 2 tiếng.": 2, "D. Thức trắng hoặc dùng thuốc an thần.": 3}},
    # ... Thêm các câu khác ...
    {"id": 14, "part": 3, "text": "Câu 14: Cảm giác sau khi ăn xong các bữa chính/phụ?", 
     "options": {"A. Nhẹ bụng.": 0, "B. Hơi no căng.": 1, "C. Đầy hơi khó tiêu.": 2, "D. Đau thắt dạ dày dữ dội, nôn mửa.": 3}}
]

with st.form("quiz_form"):
    st.subheader("Phần 1: Tâm & Tỳ")
    answers_p1 = {q["id"]: st.radio(q["text"], list(q["options"].keys())) for q in questions if q["part"] == 1}
    st.subheader("Phần 3: Tỳ Vị & Chuyển Hóa")
    answers_p3 = {q["id"]: st.radio(q["text"], list(q["options"].keys())) for q in questions if q["part"] == 3}
    submitted = st.form_submit_button("Nhận Kết Quả Tư Vấn", type="primary")

if submitted:
    # Logic tính điểm (Copy y nguyên logic tính điểm bài trước)
    score_p1 = sum(next(q["options"][ans] for q in questions if q["id"] == q_id) for q_id, ans in answers_p1.items())
    score_p3 = sum(next(q["options"][ans] for q in questions if q["id"] == q_id) for q_id, ans in answers_p3.items())
    
    red_flags = []
    all_answers = {**answers_p1, **answers_p3}
    for q_id, ans in all_answers.items():
        q_data = next(q for q in questions if q["id"] == q_id)
        if q_data["options"][ans] == 3:
            red_flags.append(q_data["text"])
    red_flags_str = "\n".join(red_flags) if red_flags else "Không có"

    prompt = f"""
    Bạn là Chuyên gia Tư vấn Dinh dưỡng và YHCT dự án Mộc Vị.
    Cờ đỏ (3 điểm): {red_flags_str}
    Điểm Tâm Tỳ: {score_p1}/14. Điểm Tỳ Vị: {score_p3}/14.
    
    Quy tắc:
    1. Có cờ đỏ -> Dừng tư vấn sản phẩm, khuyên đi khám bác sĩ.
    2. Không có cờ đỏ -> Điểm >=4 phần nào tư vấn phần đó. Tâm Tỳ -> Mộc An, Tỳ Vị -> Mộc Thanh.
    """
    with st.spinner("Đang phân tích biện chứng luận trị..."):
        response = model.generate_content(prompt)
        st.success("Hoàn tất!")
        st.write(response.text)
