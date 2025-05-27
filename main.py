from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os

app = FastAPI(title="辅助教学系统", description="智能化学习助手")

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# 配置模板目录
templates = Jinja2Templates(directory="web/templates")

# 聊天请求模型
class ChatRequest(BaseModel):
    message: str

# 聊天响应模型
class ChatResponse(BaseModel):
    response: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """首页路由 - 返回教学系统主页"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/chat", response_model=ChatResponse)
async def chat(chat_request: ChatRequest):
    """聊天API - 处理用户对话请求"""
    user_message = chat_request.message
    
    # 这里可以集成您的AI模型或聊天逻辑
    # 目前返回一个简单的回复
    if "你好" in user_message or "hello" in user_message.lower():
        bot_response = "您好！我是您的智能助教，很高兴为您服务。请问有什么学习问题需要帮助吗？"
    elif "作业" in user_message:
        bot_response = "关于课后作业，建议您按照以下步骤进行：\n1. 仔细阅读题目要求\n2. 回顾相关知识点\n3. 逐步解答问题\n4. 检查答案的合理性\n\n如果遇到具体问题，请告诉我题目内容，我会详细为您解答。"
    elif "例题" in user_message:
        bot_response = "例题是理解知识点的重要途径。建议您：\n1. 先独立思考解题思路\n2. 对比标准解答过程\n3. 总结解题方法和技巧\n4. 举一反三，尝试类似题目\n\n请问您对哪个例题有疑问？"
    elif "目标" in user_message or "学习" in user_message:
        bot_response = "学习目标的制定很重要！建议您：\n1. 明确短期和长期目标\n2. 将大目标分解为小目标\n3. 制定具体的学习计划\n4. 定期检查学习进度\n\n请问您想了解哪方面的学习目标设定？"
    else:
        bot_response = f"您提到了：{user_message}\n\n这是一个很好的问题！作为您的智能助教，我建议您：\n1. 先回顾相关的课程内容\n2. 查阅教材中的相关章节\n3. 尝试从不同角度思考问题\n\n如果您需要更具体的帮助，请详细描述您的问题，我会为您提供更精准的指导。"
    
    return ChatResponse(response=bot_response)