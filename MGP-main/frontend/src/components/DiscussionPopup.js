import React, { useState, useEffect, useRef } from 'react';
import './DiscussionPopup.css';

function DiscussionPopup({ discussionId, billName, onClose }) {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [ws, setWs] = useState(null);
  const messagesEndRef = useRef(null);
  const currentUserNickname = sessionStorage.getItem('nickname');

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
        console.log('Loaded messages:', data);
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
      console.log('New message received:', message);
      console.log('Current user nickname:', currentUserNickname);
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
  }, [discussionId, currentUserNickname]);

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
        {messages.map((message) => {
          const isMyMessage = message.user_nickname === currentUserNickname;
          console.log('Comparing nicknames:', {
            messageNickname: message.user_nickname,
            currentNickname: currentUserNickname,
            isMyMessage
          });
          
          return (
            <div
              key={message.id}
              className={`message ${isMyMessage ? 'my-message' : 'other-message'}`}
            >
              {!isMyMessage && (
                <div className="message-nickname">{message.user_nickname}</div>
              )}
              <div className="message-content">{message.content}</div>
              <div className="message-time">
                {new Date(message.created_at).toLocaleTimeString('ko-KR', { 
                  hour: '2-digit', 
                  minute: '2-digit',
                  hour12: false 
                })}
              </div>
            </div>
          );
        })}
        <div ref={messagesEndRef} />
      </div>

      <div className="message-input-container">
        <textarea
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="메시지를 입력하세요..."
          disabled={!ws || ws.readyState !== WebSocket.OPEN}
        />
        <button 
          onClick={handleSendMessage}
          disabled={!ws || ws.readyState !== WebSocket.OPEN || !newMessage.trim()}
        >
          전송
        </button>
      </div>
    </div>
  );
}

export default DiscussionPopup; 