import os
from dotenv import load_dotenv

# 1. Import các module cốt lõi từ thư mục src của bạn
from src.core.gemini_provider import GeminiProvider # (Hoặc class tương ứng trong file của bạn)
from src.agent.agent import ReActAgent
from src.tools import TOOL_REGISTRY

def main():
    # 2. Tải biến môi trường (API Keys)
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ Lỗi: Chưa tìm thấy GEMINI_API_KEY trong file .env!")
        return

    print("⚙️ Đang khởi động hệ thống và kết nối API...")

    # 3. Khởi tạo "Bộ não" (LLM) và "Người điều phối" (Agent)
    # Lưu ý: Tham số khởi tạo GeminiProvider có thể chỉnh sửa tùy theo code trong file của bạn
    llm = GeminiProvider(model_name="gemini-2.5-flash") 
    
    # Nạp danh sách Tool Registry vào Agent
    agent = ReActAgent(
        llm=llm,
        tools=TOOL_REGISTRY,
        max_steps=5 # Cho phép AI tự suy nghĩ/tra cứu tối đa 5 vòng
    )

    print("="*60)
    print("🎓 TRỢ LÝ AI TƯ VẤN KHÓA HỌC (Phiên bản ReAct Agent)")
    print("💡 Gõ 'thoát', 'quit' hoặc 'exit' để dừng chương trình.")
    print("="*60)

    # 4. Vòng lặp giao tiếp liên tục (Interactive Chat Loop)
    while True:
        try:
            # Chờ người dùng nhập câu hỏi
            user_input = input("\n🧑 Người dùng: ")
            
            # Kiểm tra lệnh thoát
            if user_input.lower() in ['thoát', 'quit', 'exit']:
                print("\n👋 Hệ thống: Cảm ơn bạn. Hẹn gặp lại!")
                break
                
            # Bỏ qua nếu lỡ bấm Enter mà chưa nhập gì
            if not user_input.strip():
                continue

            print("\n⏳ Đang phân tích yêu cầu (Theo dõi luồng Thought/Action ở Log bên trên)...")
            
            # KÍCH HOẠT AGENT! (Toàn bộ logic ReAct sẽ chạy ở đây)
            final_answer = agent.run(user_input)
            
            # In ra câu trả lời cuối cùng
            print("\n" + "="*60)
            print(f"🤖 Trợ lý: \n{final_answer}")
            print("="*60)

        except KeyboardInterrupt:
            # Xử lý khi bạn bấm Ctrl+C để ép dừng
            print("\n👋 Đã ép buộc dừng chương trình. Hẹn gặp lại!")
            break
        except Exception as e:
            print(f"\n❌ Đã xảy ra lỗi hệ thống: {e}")

if __name__ == "__main__":
    main()