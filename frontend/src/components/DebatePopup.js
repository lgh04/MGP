// src/components/DebatePopup.jsx

import React from "react";
import './DebatePopup.css';

export default function DebatePopup({ onClose }) {
  return (
    <div className="popup-overlay">
      <div className="popup-box">
        <div className="popup-header">
          <span>Frame 20</span>
          <button onClick={onClose} className="popup-close">✕</button>
        </div>

        <div className="popup-body">
          <div className="popup-title">
            <img src="/logo.png" alt="Logo" />
            <span>마이페이지</span>
          </div>

          <div className="popup-content">
            <h2>토론방 목록</h2>
            <div className="placeholder-line">아직 참여한 토론방이 없습니다</div>
          </div>
        </div>
      </div>
    </div>
  );
}