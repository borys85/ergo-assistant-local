import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def get_local_llm_response(messages, model="llama3.2", temperature=0.2):
    url = os.getenv('OLLAMA_URL')
    
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": temperature
        }
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()['message']['content']
    except Exception as e:
        return f"❌ Ошибка связи с Ollama: {e}"

def start_chat():
    print("👋 Привет! Я твой локальный Эрго-ассистент (Llama 3.2).")
    print("💡 Введи 'выход' или 'exit', чтобы закончить.")
    
    # Начальный системный промпт
    system_prompt = """
    Ты — эксперт по эргономике и здоровью IT-специалистов. 
    Твоя задача — давать советы по организации перерывов, разминке и настройке рабочего места.
    Отвечай дружелюбно, но профессионально. 
    Если пользователь просит план, используй формат JSON: {"title": "...", "steps": ["..."], "notes": ["..."]}.
    """
    
    history = [
        {"role": "system", "content": system_prompt}
    ]

    while True:
        user_input = input("\n👤 Ты: ")
        
        if user_input.lower() in ['выход', 'exit', 'q']:
            print("👋 До встречи! Береги спину.")
            break
        
        if not user_input.strip():
            continue

        # Добавляем сообщение пользователя в историю
        history.append({"role": "user", "content": user_input})
        
        print("🤖 Ассистент печатает...")
        
        # Получаем ответ от локальной модели
        ai_response = get_local_llm_response(history)
        
        print(f"\n🤖 Ассистент:\n{ai_response}\n")
        
        # Добавляем ответ ассистента в историю для сохранения контекста
        history.append({"role": "assistant", "content": ai_response})

if __name__ == "__main__":
    start_chat()