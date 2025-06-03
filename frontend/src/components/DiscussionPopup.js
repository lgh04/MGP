import React, { useState, useEffect, useRef } from 'react';
import './DiscussionPopup.css';

function DiscussionPopup({ discussionId, billName, onClose }) {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [ws, setWs] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // 기존 메시지 로드
    const fetchMessages = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/discussions/${discussionId}/messages`, {
          headers: {
            'Authorization': `Bearer ${sessionStorage.getItem('token')}`
          }
        });
        const data = await response.json();
        setMessages(data);
      } catch (error) {
        console.error('메시지 로드 실패:', error);
      }
    };

    fetchMessages();

    // WebSocket 연결
    const token = sessionStorage.getItem('token');
    const wsConnection = new WebSocket(`ws://localhost:8000/api/discussions/${discussionId}/ws?token=${token}`);

    wsConnection.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setMessages(prev => [...prev, message]);
    };

    wsConnection.onerror = (error) => {
      console.error('WebSocket 에러:', error);
    };

    setWs(wsConnection);

    return () => {
      if (wsConnection) {
        wsConnection.close();
      }
    };
  }, [discussionId]);

  const handleSendMessage = () => {
    if (newMessage.trim() && ws) {
      ws.send(newMessage);
      setNewMessage('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="discussion-popup">
      <div className="discussion-header">
        <h2>{billName}</h2>
        <button className="close-button" onClick={onClose}>×</button>
      </div>

      <div className="messages-container">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.user_nickname === sessionStorage.getItem('nickname') ? 'my-message' : 'other-message'}`}
          >
            {message.user_nickname !== sessionStorage.getItem('nickname') && (
              <div className="message-nickname">{message.user_nickname}</div>
            )}
            <div className="message-content">{message.content}</div>
            <div className="message-time">
              {new Date(message.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="message-input-container">
        <textarea
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="메시지를 입력하세요..."
        />
        <button onClick={handleSendMessage}>전송</button>
      </div>
    </div>
  );
}

export default DiscussionPopup;
