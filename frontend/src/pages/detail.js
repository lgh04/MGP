import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // 🔹 추가
import './detail.css';
import CommentPopup from '../components/CommentPopup';

function DetailPage() {
  const [selected, setSelected] = useState(null);
  const [showComments, setShowComments] = useState(false);
  const agreePercent = 60;
  const disagreePercent = 40;
  const totalParticipants = '10만명 참여중';

  const navigate = useNavigate(); // 🔹 페이지 이동 함수

  return (
    <div className="detail-page">
      <header className="detail-header">
        <img src="/logo.png" alt="ACT:ON 로고" className="logo" />
        <div className="auth-buttons">
          <button className="signin-btn" onClick={() => navigate('/login')}>Sign in</button>
          <button className="register-btn" onClick={() => navigate('/register')}>Register</button>
        </div>
      </header>

      <main className="detail-container">
        <h1 className="bill-title">법안 제목</h1>

        {selected && (
          <div className="comment-toggle" onClick={() => setShowComments(true)}>
            댓글보기
          </div>
        )}

        <div className="vote-box">
          <div className="vote-bars">
            {/* 찬성 막대 */}
            <div className="bar-wrapper" onClick={() => setSelected('agree')}>
              <div className="bar-label-top">
                찬성 {selected === 'agree' && '✔️'}
              </div>
              <div className="bar-background">
                <div
                  className="bar-fill agree-bar"
                  style={{ width: selected ? `${agreePercent}%` : '0%' }}
                >
                  {selected && <span className="bar-percent-text">{agreePercent}%</span>}
                </div>
              </div>
            </div>

            <div className="vs-text">VS</div>

            {/* 반대 막대 */}
            <div className="bar-wrapper" onClick={() => setSelected('disagree')}>
              <div className="bar-label-top">
                {selected === 'disagree' && <span className="check">✔️</span>} 반대
              </div>
              <div className="bar-background disagree-background">
                <div
                  className="bar-fill disagree-bar"
                  style={{ width: selected ? `${disagreePercent}%` : '0%' }}
                >
                  {selected && <span className="bar-percent-text">{disagreePercent}%</span>}
                </div>
              </div>
              {selected && <div className="participant-count-inside">{totalParticipants}</div>}
            </div>
          </div>
        </div>

        {selected && <div className="discussion-text-outside">토론방 참여하기</div>}

        <div className="bill-image"></div>
        <div className="bill-content"></div>
      </main>

      {showComments && (
        <CommentPopup onClose={() => setShowComments(false)} />
      )}
    </div>
  );
}

export default DetailPage;
