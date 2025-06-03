// src/pages/Home.js

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import './home.css';
import MyPagePopup from '../components/MyPagePopup';

function Home() {
  const navigate = useNavigate();
  const [nickname, setNickname] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchMode, setSearchMode] = useState("발의");
  const [showPopup, setShowPopup] = useState(false);

  useEffect(() => {
    const storedNickname = sessionStorage.getItem("nickname");
    if (storedNickname) {
      setNickname(storedNickname);
    }
  }, []);

  // React Query를 사용한 법안 데이터 페칭
  const { data: laws = { 공포: [], 발의: [] }, isLoading } = useQuery({
    queryKey: ['home-laws'],
    queryFn: async () => {
      try {
        const response = await fetch("http://localhost:8000/api/laws", {
          headers: {
            'Accept': 'application/json'
          }
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      } catch (error) {
        console.error("법안 불러오기 실패:", error);
        return { 공포: [], 발의: [] };
      }
    },
    staleTime: 1000 * 60 * 5, // 5분 동안 데이터를 신선한 상태로 유지
    cacheTime: 1000 * 60 * 30, // 30분 동안 캐시 유지
    refetchInterval: 60000, // 1분마다 자동 갱신
    refetchOnWindowFocus: false, // 윈도우 포커스 시 자동 리페치 비활성화
  });

  const handleSearch = () => {
    const encodedQuery = encodeURIComponent(searchQuery.trim());
    const encodedMode = encodeURIComponent(searchMode);
    navigate(/list?query=${encodedQuery}&mode=${encodedMode}&sort=latest&page=1);
  };

  return (
    <div className="home-page">
      <header className="home-header">
        <img src="/logo.png" alt="ACT:ON 로고" className="logo-top" />
        <div className="auth-buttons">
          {nickname ? (
            <div
              className="user-nickname"
              style={{ cursor: 'pointer' }}
              onClick={() => setShowPopup(true)}
            >
              {nickname}
            </div>
          ) : (
            <>
              <button className="signin-btn" onClick={() => navigate('/login')}>Sign in</button>
              <button className="register-btn" onClick={() => navigate('/register')}>Register</button>
            </>
          )}
        </div>
      </header>

      <main className="home-center">
        <img src="/main-logo.png" alt="ACT:ON 중앙 로고" className="home-logo-center" />

        <div className="search-bar">
          <select
            value={searchMode}
            onChange={(e) => setSearchMode(e.target.value)}
          >
            <option value="발의">발의</option>
            <option value="공포">공포</option>
          </select>

          <input
            type="text"
            placeholder="발의된 또는 공포된 법안을 검색해 주세요"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />

          <button onClick={handleSearch}>
            <span role="img" aria-label="search">🔍</span>
          </button>
        </div>

        <img src="/banner.png" alt="배너 이미지" className="banner-image" />
      </main>

      <section className="law-section">
        <h2>법안 목록</h2>
        <p>공포된 법안과 발의된 법안을 구분해서 확인해요</p>

        {isLoading ? (
          <div className="loading">데이터를 불러오는 중...</div>
        ) : (
          <div className="law-boxes">
            {["공포", "발의"].map((mode) => (
              <div className="law-box" key={mode}>
                <div className="law-box-header">
                  <h3>{mode}된 법안</h3>
                </div>

                <div className="law-scroll-box">
                  {laws[mode].slice(0, 8).map((law, idx) => (
                    <div key={idx} className="law-item">
                      <div 
                        onClick={() => navigate(/detail/${law.bill_id})}
                        style={{ cursor: 'pointer' }}
                      >
                        {law.title}
                      </div>
                      <div className="law-date">{law.date}</div>
                    </div>
                  ))}
                </div>

                <div className="law-more-button">
                  <button onClick={() => navigate(/list?query=&mode=${mode}&sort=latest&page=1)}>＋</button>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {showPopup && <MyPagePopup onClose={() => setShowPopup(false)} />}
    </div>
  );
}

export default Home;
