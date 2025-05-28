import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './home.css';

function Home() {
  const navigate = useNavigate();
  const [nickname, setNickname] = useState(null);
  const [laws, setLaws] = useState({ 공포: [], 발의: [] });

  useEffect(() => {
    const storedNickname = localStorage.getItem("nickname");
    if (storedNickname) {
      setNickname(storedNickname);
    }

    const fetchData = async () => {
      try {
        const res = await axios.get("http://localhost:8000/api/laws");
        setLaws(res.data); // { 공포: [...], 발의: [...] }
      } catch (error) {
        console.error("법안 불러오기 실패:", error);
      }
    };

    fetchData(); // 첫 호출
    const interval = setInterval(fetchData, 60000); // ✅ 1분마다 재호출

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="home-page">
      <header className="home-header">
        <img src="/logo.png" alt="ACT:ON 로고" className="logo-top" />
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

      <main className="home-center">
        <img src="/main-logo.png" alt="ACT:ON 중앙 로고" className="home-logo-center" />
        <div className="search-bar">
          <select>
            <option>발의</option>
            <option>공포</option>
          </select>
          <input type="text" placeholder="발의된 또는 공포된 법안을 검색해 주세요" />
          <button><span role="img" aria-label="search">🔍</span></button>
        </div>
        <img src="/banner.png" alt="배너 이미지" className="banner-image" />
      </main>

      <section className="law-section">
        <h2>법안 목록</h2>
        <p>공포된 법안과 발의된 법안을 구분해서 확인해요</p>

        <div className="law-boxes">
          {["공포", "발의"].map((mode) => (
            <div className="law-box" key={mode}>
              <div className="law-box-header">
                <h3>{mode}된 법안</h3>
              </div>

              <div className="law-scroll-box">
                {laws[mode].slice(0, 8).map((law, idx) => (
                  <div key={idx} className="law-item">
                    <a href={law.link} target="_blank" rel="noreferrer">
                      {law.title}
                    </a>
                    <div className="law-date">{law.date}</div>
                  </div>
                ))}
              </div>

              <div className="law-more-button">
                <button onClick={() => navigate(`/laws?type=${mode}`)}>＋</button>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

export default Home;

