import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./login.css";

function Login() {
  const navigate = useNavigate();
  const [userNickname, setUserNickname] = useState(null); // ✅ 닉네임 저장

  // ✅ 이메일/비밀번호 상태 추가
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();
      if (res.ok) {
        setUserNickname(data.nickname); // ✅ 닉네임 상태 저장
        localStorage.setItem("nickname", data.nickname); // 지속 저장 원할 경우 사용
        navigate("/"); // 로그인 성공 후 이동
      } else {
        alert(data.detail);
      }
    } catch (err) {
      console.error("로그인 실패", err);
    }
  };

  return (
    <div className="login-page">
      {/* 상단 헤더 */}
      <header className="login-header">
        <img src="/logo.png" alt="ACT:ON 로고" className="logo-top" />
        {userNickname ? (
          <div className="user-nickname">{userNickname}</div> // ✅ 닉네임 표시
        ) : (
          <div className="auth-buttons">
            <button className="signin-btn" onClick={() => navigate('/login')}>Sign in</button>
            <button className="register-btn" onClick={() => navigate('/register')}>Register</button>
          </div>
        )}
      </header>

      {/* 중앙 로고 */}
      <div className="logo-center">
        <img src="/main-logo.png" alt="중앙 슬로건 로고" className="center-logo" />
      </div>

      {/* 로그인 폼 */}
      <main className="login-form-container">
        <form className="login-form" onSubmit={handleSubmit}>
          <label>
            이메일
            <input
              type="email"
              placeholder="이메일 주소를 입력해주세요."
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </label>

          <label>
            비밀번호
            <input
              type="password"
              placeholder="비밀번호를 입력해주세요."
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </label>

          {/* ✅ 입력값이 없으면 비활성화 */}
          <button
            type="submit"
            className="submit-btn"
            disabled={!email || !password}
          >
            로그인
          </button>

          <div className="login-links">
            <button type="button" className="link-text" onClick={() => navigate('/register')}>
              회원가입
            </button>
          </div>
        </form>
      </main>
    </div>
  );
}

export default Login;

