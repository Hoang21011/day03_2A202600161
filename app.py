import streamlit as st
import os
from dotenv import load_dotenv

# Import các module cốt lõi của bạn
from src.core.gemini_provider import GeminiProvider 
from src.agent.agent import ReActAgent
from src.tools import TOOL_REGISTRY

# ==========================================
# 1. CẤU HÌNH TRANG WEB
# ==========================================
st.set_page_config(
    page_title="AI Course Advisor", 
    page_icon="🎓", 
    layout="centered"
)

# ==========================================
# 2. KHỞI TẠO AGENT (Chỉ load 1 lần)
# ==========================================
# Dùng @st.cache_resource để không bị tạo lại Agent mỗi lần gõ chat
@st.cache_resource
def init_agent():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        st.error("❌ Lỗi: Chưa tìm thấy GEMINI_API_KEY trong file .env!")
        st.stop()
        
    llm = GeminiProvider(model_name="gemini-2.5-flash")
    # Nạp công cụ y như bên chatbot.py
    return ReActAgent(llm=llm, tools=TOOL_REGISTRY, max_steps=5)

agent = init_agent()

# ==========================================
# 3. GIAO DIỆN CHÍNH
# ==========================================
st.title("🎓 Trợ lý AI Tư vấn Khóa học")
st.caption("Hệ thống Agent tự động tra cứu dữ liệu thời gian thực.")

# Khởi tạo bộ nhớ (Session State) để lưu lịch sử đoạn chat trên màn hình
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Chào bạn, mình là trợ lý AI. Mình có thể giúp bạn tìm kiếm thông tin, tính toán học phí khóa học. Bạn cần mình giúp gì?"}]

# In toàn bộ lịch sử tin nhắn cũ ra màn hình
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# 4. XỬ LÝ KHI NGƯỜI DÙNG NHẬP TIN NHẮN
# ==========================================
# st.chat_input tạo ra một thanh gõ chữ ở đáy màn hình
if prompt := st.chat_input("VD: Tìm khóa học AI ở Quận 1, TP.HCM..."):
    
    # 4.1. Hiển thị câu hỏi của người dùng
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 4.2. Khởi hoạt Agent và hiển thị quá trình chờ
    with st.chat_message("assistant"):
        # Vòng xoay Loading...
        with st.spinner("🤖 Hệ thống đang tra cứu và suy nghĩ... (Hãy xem log chi tiết dưới Terminal)"):
            try:
                # Gọi thẳng hàm run() của Agent như bạn đã làm ở chatbot.py
                final_answer = agent.run(prompt)
                
                # In câu trả lời ra web
                st.markdown(final_answer)
                
                # Lưu câu trả lời vào bộ nhớ
                st.session_state.messages.append({"role": "assistant", "content": final_answer})
                
            except Exception as e:
                st.error(f"❌ Đã xảy ra lỗi: {str(e)}")