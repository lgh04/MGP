// src/components/CommentPopup.js
import React, { useState } from 'react';
import './CommentPopup.css';

function CommentPopup({ onClose }) {
  const [comments, setComments] = useState([]); // 빈 배열로 시작
  const [newComment, setNewComment] = useState('');

  const handleAddComment = () => {
    if (newComment.trim() !== '') {
      const newEntry = {
        id: Date.now(),
        username: '사용자명',
        content: newComment,
      };
      // 최신 댓글을 맨 위에 추가
      setComments([newEntry, ...comments]);
      setNewComment('');
    }
  };

  return (
    <div className="popup-overlay">
      <div className="popup-box">
        <button className="close-button" onClick={onClose}>X</button>

        <div className="comment-input-box">
          <div className="profile-circle"></div>
          <div className="comment-input-content">
            <div className="username">사용자명</div>
            <input
              type="text"
              placeholder="댓글 추가..."
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleAddComment()}
            />
          </div>
        </div>

        <div className="comment-list">
          {comments.map((comment) => (
            <div className="comment-item" key={comment.id}>
              <div className="profile-circle"></div>
              <div className="comment-text">
                <div className="username">{comment.username}</div>
                <div>{comment.content}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default CommentPopup;
