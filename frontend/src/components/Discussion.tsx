import React, { useEffect, useState, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import styled from 'styled-components';

const DiscussionContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f5f5f5;
  padding: 20px;
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
`;

const MessageWrapper = styled.div<{ isMine: boolean }>`
  display: flex;
  flex-direction: column;
  align-items: ${props => props.isMine ? 'flex-end' : 'flex-start'};
  margin-bottom: 16px;
  width: 100%;
`;

const MessageBubble = styled.div<{ isMine: boolean }>`
  max-width: 70%;
  padding: 12px 16px;
  border-radius: ${props => props.isMine ? '16px 0 16px 16px' : '0 16px 16px 16px'};
  margin: 2px 0;
  background-color: ${props => props.isMine ? '#4a90e2' : 'white'};
  color: ${props => props.isMine ? 'white' : 'black'};
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  word-wrap: break-word;
`;

const UserName = styled.div<{ isMine: boolean }>`
  font-size: 12px;
  color: #666;
  margin: ${props => props.isMine ? '0 4px 4px 0' : '0 0 4px 4px'};
`;

const TimeStamp = styled.div<{ isMine: boolean }>`
  font-size: 10px;
  color: #999;
  margin-top: 4px;
  margin-right: ${props => props.isMine ? '4px' : '0'};
  margin-left: ${props => props.isMine ? '0' : '4px'};
`;

const InputContainer = styled.div`
  display: flex;
  gap: 10px;
  padding: 20px;
  background-color: white;
  border-radius: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const Input = styled.input`
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  &:focus {
    outline: none;
    border-color: #4a90e2;
  }
`;

const SendButton = styled.button`
  padding: 12px 24px;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: background-color 0.2s;
  
  &:hover {
    background-color: #357abd;
  }
  
  &:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
`;

interface Message {
  id: number;
  content: string;
  user_id: number;
  user_nickname: string;
  created_at: string;
  discussion_id: number;
}

const Discussion = () => {
  const { id } = useParams<{ id: string }>();
  const { user, token } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [ws, setWs] = useState<WebSocket | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [isConnecting, setIsConnecting] = useState(false);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const formatTime = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString('ko-KR', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    });
  };

  useEffect(() => {
    if (!user?.id || !token) {
      console.log('No user or token available');
      return;
    }

    console.log('Current user ID:', user.id);

    const loadMessages = async () => {
      try {
        const response = await fetch(`/api/discussions/${id}/messages`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        if (response.ok) {
          const data = await response.json();
          console.log('Loaded messages:', data);
          setMessages(data);
          setTimeout(scrollToBottom, 100);
        }
      } catch (error) {
        console.error('메시지 로드 실패:', error);
      }
    };

    loadMessages();

    const connectWebSocket = () => {
      if (isConnecting) return;
      setIsConnecting(true);

      const wsUrl = `ws://${window.location.host}/api/discussions/${id}/ws?token=${token}`;
      const socket = new WebSocket(wsUrl);

      socket.onopen = () => {
        console.log('WebSocket 연결됨');
        setWs(socket);
        setIsConnecting(false);
      };

      socket.onmessage = (event) => {
        const message = JSON.parse(event.data);
        console.log('Received message:', message, 'Current user ID:', user.id);
        setMessages(prev => [...prev, message]);
        setTimeout(scrollToBottom, 100);
      };

      socket.onclose = () => {
        console.log('WebSocket 연결 끊김');
        setWs(null);
        setIsConnecting(false);
        setTimeout(connectWebSocket, 3000);
      };

      socket.onerror = (error) => {
        console.error('WebSocket 에러:', error);
        socket.close();
      };
    };

    connectWebSocket();

    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, [id, token, user]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = () => {
    if (!user?.id) {
      console.log('No user ID available');
      return;
    }

    if (ws && ws.readyState === WebSocket.OPEN && newMessage.trim()) {
      console.log('Sending message as user:', user.id);
      ws.send(newMessage.trim());
      setNewMessage('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <DiscussionContainer>
      <MessagesContainer>
        {messages.map((message) => {
          const isMine = user?.id === message.user_id;
          console.log('Message comparison:', {
            messageUserId: message.user_id,
            currentUserId: user?.id,
            isMine
          });
          return (
            <MessageWrapper key={message.id} isMine={isMine}>
              <UserName isMine={isMine}>
                {message.user_nickname}
              </UserName>
              <MessageBubble isMine={isMine}>
                {message.content}
              </MessageBubble>
              <TimeStamp isMine={isMine}>
                {formatTime(message.created_at)}
              </TimeStamp>
            </MessageWrapper>
          );
        })}
        <div ref={messagesEndRef} />
      </MessagesContainer>
      <InputContainer>
        <Input
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="메시지를 입력하세요..."
        />
        <SendButton
          onClick={handleSendMessage}
          disabled={!ws || ws.readyState !== WebSocket.OPEN || !newMessage.trim()}
        >
          전송
        </SendButton>
      </InputContainer>
    </DiscussionContainer>
  );
};

export default Discussion; 