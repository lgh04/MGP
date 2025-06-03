// src/components/CommentPopup.js
import React, { useState, useEffect, useCallback } from 'react';
import './CommentPopup.css';

function CommentPopup({ onClose, billId }) {
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const [nickname, setNickname] = useState(null);

  const fetchComments = useCallback(async () => {
    try {
      const token = sessionStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/comments/${billId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setComments(data);
      }
    } catch (err) {
      console.error("댓글을 불러오는데 실패했습니다:", err);
    }
  }, [billId]);

  useEffect(() => {
    const storedNickname = sessionStorage.getItem("nickname");
    if (storedNickname) {
      setNickname(storedNickname);
    }
    fetchComments();
  }, [fetchComments]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!nickname) {
      alert("댓글을 작성하려면 로그인이 필요합니다.");
      return;
    }
    if (!newComment.trim()) return;

    try {
      const token = sessionStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/comments/${billId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ content: newComment })
      });

      if (response.ok) {
        const data = await response.json();
        setComments(prevComments => [data, ...prevComments]);
        setNewComment('');
      } else {
        const error = await response.json();
        alert(error.detail || "댓글 작성에 실패했습니다.");
      }
    } catch (err) {
      console.error("댓글 작성 중 오류가 발생했습니다:", err);
      alert("댓글 작성에 실패했습니다.");
    }
  };

  const handleDelete = async (commentId) => {
    try {
      const token = sessionStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/comments/${commentId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        setComments(comments.filter(comment => comment.id !== commentId));
      } else {
        const error = await response.json();
        alert(error.detail || "댓글 삭제에 실패했습니다.");
      }
    } catch (err) {
      console.error("댓글 삭제 중 오류가 발생했습니다:", err);
      alert("댓글 삭제에 실패했습니다.");
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('ko-KR', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="comment-popup">
      <div className="comment-popup-content">
        <button className="close-button" onClick={onClose}>×</button>
        <h2>댓글</h2>
        
        <form onSubmit={handleSubmit} className="comment-form">
          <textarea
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            placeholder={nickname ? "댓글을 입력하세요..." : "로그인이 필요합니다."}
            disabled={!nickname}
          />
          <button type="submit" disabled={!nickname || !newComment.trim()}>
            작성
          </button>
        </form>

        <div className="comments-list">
          {[...comments].reverse().map(comment => (
            <div key={comment.id} className="comment">
              <div className="comment-header">
                <span className="comment-author">{comment.user_nickname}</span>
                <span className="comment-date">{formatDate(comment.created_at)}</span>
                {nickname === comment.user_nickname && (
                  <button 
                    className="delete-button"
                    onClick={() => handleDelete(comment.id)}
                  >
                    삭제
                  </button>
                )}
              </div>
              <p className="comment-text">{comment.content}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default CommentPopup;
