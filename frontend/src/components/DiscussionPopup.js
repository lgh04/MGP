import React, { useState, useEffect, useRef } from 'react';
import './DiscussionPopup.css';

function DiscussionPopup({ discussionId, billName, onClose }) {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [contextMenu, setContextMenu] = useState({ visible: false, x: 0, y: 0, messageId: null });
  const messagesEndRef = useRef(null);
  const nickname = sessionStorage.getItem('nickname');
  const [ws, setWs] = useState(null);
  const [userRestrictions, setUserRestrictions] = useState({});

  const formatTime = (timeString) => {
    const date = new Date(timeString);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

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
        const response = await fetch(`${process.env.REACT_APP_API_URL}/api/discussions/${discussionId}/messages`, {
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

  const handleSubmit = (e) => {
    e.preventDefault();
    handleSendMessage();
  };

  const checkUserRestriction = async (userId, discussionId) => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/api/discussions/users/${userId}/report-status/${discussionId}`, {
        headers: {
          'Authorization': `Bearer ${sessionStorage.getItem('token')}`
        }
      });
      
      if (!response.ok) {
        console.error('제한 상태 확인 실패:', await response.text());
        return null;
      }

      const data = await response.json();
      setUserRestrictions(prev => ({
        ...prev,
        [userId]: data
      }));
      return data;
    } catch (error) {
      console.error('제한 상태 확인 실패:', error);
      return null;
    }
  };

  const handleSendMessage = () => {
    if (newMessage.trim() && ws) {
      const currentUserRestriction = userRestrictions[sessionStorage.getItem('user_id')];
      if (currentUserRestriction?.is_restricted) {
        const endTime = new Date(currentUserRestriction.restriction_end);
        const remainingTime = Math.ceil((endTime - new Date()) / (1000 * 60 * 60));
        alert(`채팅이 제한되었습니다. ${remainingTime}시간 후에 다시 시도해주세요.`);
        return;
      }
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

  const handleContextMenu = (e, messageId) => {
    e.preventDefault();
    setContextMenu({
      visible: true,
      messageId
    });
  };

  const handleReportMessage = async (messageId) => {
    try {
      const message = messages.find(m => m.id === messageId);
      if (!message) {
        throw new Error('메시지를 찾을 수 없습니다.');
      }

      const response = await fetch(`${process.env.REACT_APP_API_URL}/api/discussions/${discussionId}/report`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          reported_user_id: message.user_id,
          message_id: messageId
        })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail);
      }

      alert('신고가 접수되었습니다.');
      
      // 신고된 사용자의 상태 업데이트
      if (message) {
        await checkUserRestriction(message.user_id, discussionId);
      }
    } catch (error) {
      alert(error.message);
    } finally {
      setContextMenu({ visible: false, messageId: null });
    }
  };

  useEffect(() => {
    // 컴포넌트 마운트 시 모든 사용자의 제한 상태 확인
    const checkAllUsers = async () => {
      const uniqueUserIds = [...new Set(messages.map(m => m.user_id))];
      for (const userId of uniqueUserIds) {
        await checkUserRestriction(userId, discussionId);
      }
    };
    checkAllUsers();
  }, [messages, discussionId]);

  useEffect(() => {
    const handleClickOutside = () => {
      setContextMenu({ visible: false, x: 0, y: 0, messageId: null });
    };

    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  }, []);

  return (
    <>
      <div className="discussion-overlay" />
      <div className="discussion-popup" onClick={(e) => e.stopPropagation()}>
        <div className="discussion-popup-content">
          <div className="discussion-header">
            <h2>{billName}</h2>
            <button className="close-button" onClick={onClose}>×</button>
          </div>
          
          <div className="messages-container">
            {messages.map(message => (
              <div
                key={message.id}
                className={`message-container ${message.user_nickname === nickname ? 'my-message' : 'other-message'}`}
                onContextMenu={(e) => message.user_nickname !== nickname && handleContextMenu(e, message.id)}
              >
                <div className="message">
                  <div className="message-header">
                    <span className="message-author">{message.user_nickname}</span>
                  </div>
                  <div className="message-text">{message.content}</div>
                  <div className="message-time">{formatTime(message.created_at)}</div>
                </div>
                {contextMenu.visible && contextMenu.messageId === message.id && (
                  <div className="message-context-menu">
                    <button className="report-button" onClick={() => handleReportMessage(message.id)}>
                      <span className="report-icon">🚨</span>
                      신고하기
                    </button>
                  </div>
                )}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          <form onSubmit={handleSubmit} className="message-form">
            <textarea
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="메시지를 입력하세요..."
            />
            <button type="submit">전송</button>
          </form>
        </div>
      </div>
    </>
  );
}

export default DiscussionPopup;
