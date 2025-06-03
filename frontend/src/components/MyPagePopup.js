import React, { useState, useEffect } from 'react';
import './MyPagePopup.css';

function MyPagePopup({ onClose }) {
  // 추후 토론방 기능 구현 시 사용할 상태
  const [debates] = useState([]);

  useEffect(() => {
    // 추후 토론방 목록을 가져오는 API가 구현되면 연결
    // fetchDebates();
  }, []);

  return (
    <div className="mypage-popup">
      <div className="mypage-popup-content">
        <div className="popup-top-bar"></div>
        <button className="close-button" onClick={onClose}>×</button>
        <div className="mypage-header">
          <img src="/main-logo.png" alt="ACT:ON" className="mypage-logo" />
          <h1 className="mypage-title">마이페이지</h1>
        </div>
        
        <div className="mypage-content">
          <h2 className="debate-title">토론방 목록</h2>
          <div className="debate-subtitle">참여중인 토론</div>
          
          <div className="debates-list">
            {debates.length > 0 ? (
              debates.map(debate => (
                <div key={debate.id} className="debate-item">
                  <span className="debate-name">{debate.title}</span>
                  <span className="debate-date">{debate.created_at}</span>
                </div>
              ))
            ) : (
              <div className="no-debates">
                아직 참여한 토론방이 없습니다
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default MyPagePopup; 