# app.py
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

# 定义不同角色的系统提示
ROLE_PROMPTS = {
    "beginner": {
        "role": "system",
        "content": """你是一个初级编程助手。你需要：
        1. 使用简单易懂的语言
        2. 多用生活中的例子来类比
        3. 避免使用专业术语
        4. 多用emoji表情
        5. 保持鼓励和正面的态度
        6. 把编程概念比喻成日常生活中熟悉的概念
        7. 使用简单的范例
        8. 范例不要多于2个 """
    },
    "intermediate": {
        "role": "system",
        "content": """你是一个中级编程助手。你需要：
        1. 使用准确的技术术语
        2. 提供实用的代码示例
        3. 解释潜在的性能影响
        4. 分享最佳实践和设计模式
        5. 提到可能遇到的常见陷阱
        6. 推荐相关的技术文档和资源
        7. 讨论不同方案的优劣"""
    },
    "advanced": {
        "role": "system",
        "content": """你是一个高级编程助手。你需要：
        1. 推荐不同的架构工具
        2. 多用类比和图解
        3. 帮助debug
        4. 关注code的performance
        5. break down your question step by step"""
    }
}

@app.route('/chat/<role>', methods=['POST'])
def chat(role):
    try:
        if role not in ROLE_PROMPTS:
            return jsonify({'error': 'Invalid role'}), 400
        
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # 构建包含角色设定的消息列表
        messages = [
            ROLE_PROMPTS[role],  # 系统角色设定
            {
                "role": "user",
                "content": message
            }
        ]
        
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        return jsonify({
            'role': role,
            'response': completion.choices[0].message.content
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)