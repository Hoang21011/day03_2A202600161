import os
from dotenv import load_dotenv
import google.generativeai as genai

# 1. Tải cấu hình API
load_dotenv()
my_api_key = os.environ.get("GEMINI_API_KEY")

if not my_api_key:
    raise ValueError("❌ Chưa tìm thấy GEMINI_API_KEY trong file .env!")

# 2. Khởi tạo model
genai.configure(api_key=my_api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# 3. BẬT TÍNH NĂNG CHAT CÓ TRÍ NHỚ (Lưu lịch sử)
# Thay vì dùng model.generate_content(), ta dùng model.start_chat()
chat_session = model.start_chat(history=[])

print("==================================================")
print("🤖 TRỢ LÝ TƯ VẤN KHÓA HỌC ĐÃ SẴN SÀNG!")
print("💡 Mẹo: Gõ 'thoát', 'quit' hoặc 'exit' để dừng chat.")
print("==================================================\n")

# VÒNG LẶP PHẢN HỒI CHÍNH (RESPONSE LOOP)
while True:
    # Bước 1: Chờ người dùng nhập câu hỏi
    user_msg = input("👤 Bạn: ")
    
    # Bước 2: Kiểm tra lệnh thoát
    if user_msg.lower() in ['thoát', 'quit', 'exit']:
        print("👋 Trợ lý: Cảm ơn bạn. Hẹn gặp lại!")
        break
        
    # Bỏ qua nếu lỡ nhấn Enter mà chưa gõ gì
    if not user_msg.strip():
        continue

    try:
        # Bước 3: Gửi tin nhắn vào phiên chat (tự động mang theo lịch sử)
        # print("⏳ Đang suy nghĩ...")
        response = chat_session.send_message(user_msg)
        
        # Bước 4: In câu trả lời
        print(f"🤖 Trợ lý: {response.text}\n")
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ Có lỗi xảy ra: {e}")