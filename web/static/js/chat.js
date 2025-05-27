// 聊天功能JavaScript
class ChatSystem {
    constructor() {
        this.messagesContainer = document.getElementById('chat-messages');
        this.messageInput = document.getElementById('message-input');
        this.sendButton = document.getElementById('send-button');
        this.loadingIndicator = document.getElementById('loading');
        
        this.initEventListeners();
        this.addWelcomeMessage();
    }
    
    initEventListeners() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
    }
    
    addWelcomeMessage() {
        this.addMessage('欢迎使用辅助教学系统！我可以帮助您解答学习中的问题。', 'bot');
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;
        
        // 添加用户消息
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        
        // 显示加载状态
        this.showLoading(true);
        
        try {
            // 发送请求到后端
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            if (!response.ok) {
                throw new Error('网络请求失败');
            }
            
            const data = await response.json();
            this.addMessage(data.response, 'bot');
            
        } catch (error) {
            console.error('Error:', error);
            this.addMessage('抱歉，系统暂时无法响应，请稍后再试。', 'bot');
        } finally {
            this.showLoading(false);
        }
    }
    
    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const timestamp = new Date().toLocaleTimeString();
        messageDiv.innerHTML = `
            <div style="font-weight: bold; margin-bottom: 5px;">
                ${sender === 'user' ? '您' : '助教'} <span style="font-size: 0.8em; color: #718096;">${timestamp}</span>
            </div>
            <div>${text}</div>
        `;
        
        this.messagesContainer.appendChild(messageDiv);
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
    
    showLoading(show) {
        this.loadingIndicator.style.display = show ? 'block' : 'none';
        this.sendButton.disabled = show;
        this.messageInput.disabled = show;
        
        if (show) {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        }
    }
}

// 页面加载完成后初始化聊天系统
document.addEventListener('DOMContentLoaded', () => {
    new ChatSystem();
});