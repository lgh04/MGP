import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import './detail.css';
import CommentPopup from '../components/CommentPopup';

function DetailPage() {
  const [selected, setSelected] = useState(null);
  const [showComments, setShowComments] = useState(false);
  const [lawData, setLawData] = useState(null);
  const [voteData, setVoteData] = useState({
    agree_percent: 0,
    disagree_percent: 0,
    total_count: 0
  });
  const [nickname, setNickname] = useState(null);

  const navigate = useNavigate();
  const { billId } = useParams();

  useEffect(() => {
    const storedNickname = sessionStorage.getItem("nickname");
    if (storedNickname) {
      setNickname(storedNickname);
    }
  }, []);

  useEffect(() => {
    if (!billId) return;
    
    const fetchLawDetail = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/law/${billId}`);
        const data = await response.json();
        
        if (!response.ok) {
          console.error("법안 정보 조회 실패:", data.detail || data.error);
          return;
        }
        
        setLawData(data);
      } catch (err) {
        console.error("법안 정보를 불러오는 데 실패했습니다:", err);
      }
    };

    fetchLawDetail();
  }, [billId]);

  useEffect(() => {
    if (!billId) return;

    const fetchVoteStatus = async () => {
      try {
        const token = sessionStorage.getItem('token');
        const response = await fetch(`http://localhost:8000/api/vote/${billId}`, {
          credentials: 'include',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        const data = await response.json();
        
        if (response.ok) {
          setVoteData(data);
        }
      } catch (err) {
        console.error("투표 현황을 불러오는 데 실패했습니다:", err);
      }
    };

    fetchVoteStatus();

    const fetchUserVote = async () => {
      if (!nickname) return;

      try {
        const token = sessionStorage.getItem('token');
        const response = await fetch(`http://localhost:8000/api/vote/${billId}/user`, {
          credentials: 'include',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        const data = await response.json();
        
        if (response.ok && data.vote_type) {
          setSelected(data.vote_type);
        }
      } catch (err) {
        console.error("사용자 투표 정보를 불러오는 데 실패했습니다:", err);
      }
    };

    fetchUserVote();
  }, [billId, nickname]);

  const handleVote = async (voteType) => {
    if (!nickname) {
      alert("투표하려면 로그인이 필요합니다.");
      navigate("/login");
      return;
    }

    try {
      const token = sessionStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/vote/${billId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        credentials: 'include',
        body: JSON.stringify({ vote_type: voteType })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "투표에 실패했습니다.");
      }

      const data = await response.json();
      
      if (response.ok) {
        setSelected(voteType);
        setVoteData(data);
      } else {
        alert(data.detail || "투표에 실패했습니다.");
      }
    } catch (err) {
      console.error("투표 처리 중 오류가 발생했습니다:", err);
      alert(err.message || "투표 처리 중 오류가 발생했습니다.");
    }
  };

  const formatNumber = (num) => {
    if (num >= 10000) {
      return Math.floor(num / 10000) + "만";
    }
    return num.toLocaleString();
  };

  return (
    <div className="detail-page">
      <header className="detail-header">
        <img src="/logo.png" alt="ACT:ON 로고" className="logo" />
        <div className="auth-buttons">
          {nickname ? (
            <div className="user-nickname">{nickname}</div>
          ) : (
            <>
              <button className="signin-btn" onClick={() => navigate('/login')}>Sign in</button>
              <button className="register-btn" onClick={() => navigate('/register')}>Register</button>
            </>
          )}
        </div>
      </header>

      <main className="detail-container">
        <h1 className="bill-title">{lawData?.BILL_NAME || '법안 제목 불러오는 중...'}</h1>

        {selected && (
          <div className="comment-toggle" onClick={() => setShowComments(true)}>
            댓글보기
          </div>
        )}

        <div className="vote-box">
          <div className="vote-bars">
            <div className="bar-wrapper" onClick={() => handleVote('agree')}>
              <div className="bar-label-top">
                찬성 {selected === 'agree' && '✔'}
              </div>
              <div className="bar-background">
                <div 
                  className="bar-fill agree-bar" 
                  style={{ width: `${voteData.agree_percent}%` }}
                >
                  <span className="bar-percent-text">{voteData.agree_percent}%</span>
                </div>
              </div>
            </div>

            <div className="vs-text">VS</div>

            <div className="bar-wrapper" onClick={() => handleVote('disagree')}>
              <div className="bar-label-top">
                {selected === 'disagree' && '✔'} 반대
              </div>
              <div className="bar-background disagree-background">
                <div 
                  className="bar-fill disagree-bar" 
                  style={{ width: `${voteData.disagree_percent}%` }}
                >
                  <span className="bar-percent-text">{voteData.disagree_percent}%</span>
                </div>
              </div>
            </div>
          </div>
          <div className="participant-count">
            {formatNumber(voteData.total_count)}명 참여중
          </div>
        </div>

        {selected && <div className="discussion-text-outside">토론방 참여하기</div>}

        <div className="bill-image"></div>
        <div className="bill-content">
          {lawData ? (
            <>
              <p><strong>법안 ID:</strong> {lawData.BILL_ID}</p>
              <p><strong>법안번호:</strong> {lawData.BILL_NO}</p>
              <p><strong>대수:</strong> {lawData.AGE}</p>
              <p><strong>법안명:</strong> {lawData.BILL_NAME}</p>
              <p><strong>제안자:</strong> {lawData.PROPOSER}</p>
              <p><strong>제안자 구분:</strong> {lawData.PROPOSER_KIND}</p>
              <p><strong>제안일:</strong> {lawData.PROPOSE_DT}</p>
              <p><strong>소관위원회 ID:</strong> {lawData.CURR_COMMITTEE_ID}</p>
              <p><strong>소관위:</strong> {lawData.CURR_COMMITTEE}</p>
              <p><strong>소관위 회부일:</strong> {lawData.COMMITTEE_DT}</p>
              <p><strong>위원회 처리일:</strong> {lawData.COMMITTEE_PROC_DT}</p>
              <p><strong>법안 링크:</strong> <a href={lawData.LINK_URL} target="_blank" rel="noreferrer">{lawData.LINK_URL}</a></p>
              <p><strong>대표 발의자:</strong> {lawData.RST_PROPOSER}</p>
              <p><strong>법사위 처리결과:</strong> {lawData.LAW_PROC_RESULT_CD}</p>
              <p><strong>법사위 처리일:</strong> {lawData.LAW_PROC_DT}</p>
              <p><strong>법사위 상정일:</strong> {lawData.LAW_PRESENT_DT}</p>
              <p><strong>법사위 회부일:</strong> {lawData.LAW_SUBMIT_DT}</p>
              <p><strong>소관위 처리결과:</strong> {lawData.CMT_PROC_RESULT_CD}</p>
              <p><strong>소관위 처리일:</strong> {lawData.CMT_PROC_DT}</p>
              <p><strong>소관위 상정일:</strong> {lawData.CMT_PRESENT_DT}</p>
              <p><strong>대표발의자 코드:</strong> {lawData.RST_MONA_CD}</p>
              <p><strong>본회의 심의결과:</strong> {lawData.PROC_RESULT_CD}</p>
              <p><strong>의결일:</strong> {lawData.PROC_DT}</p>
            </>
          ) : (
            <p>법안 상세 정보를 불러오는 중...</p>
          )}
        </div>

        {showComments && (
          <CommentPopup 
            onClose={() => setShowComments(false)} 
            billId={billId}
          />
        )}
      </main>
    </div>
  );
}

export default DetailPage;

