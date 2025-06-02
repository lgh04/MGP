import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./login.css";

function Login() {
  const navigate = useNavigate();
  const [userNickname, setUserNickname] = useState(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const formData = new FormData();
      formData.append('username', email);  // OAuth2 형식에 맞춰 username으로 전송
      formData.append('password', password);

      const res = await fetch("http://localhost:8000/api/login", {
        method: "POST",
        body: formData,
        credentials: 'include'
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || '로그인에 실패했습니다.');
      }

      const data = await res.json();
      setUserNickname(data.user.nickname);
      sessionStorage.setItem("nickname", data.user.nickname);
      sessionStorage.setItem("token", data.access_token);
      navigate("/");
    } catch (err) {
      console.error("로그인 실패:", err);
      alert(err.message);
    }
  };

  return (
    <div className="login-page">
      <header className="login-header">
        <img src="/logo.png" alt="ACT:ON 로고" className="logo-top" />
        {userNickname ? (
          <div className="user-nickname">{userNickname}</div>
        ) : (
          <div className="auth-buttons">
            <button className="signin-btn" onClick={() => navigate('/login')}>Sign in</button>
            <button className="register-btn" onClick={() => navigate('/register')}>Register</button>
          </div>
        )}
      </header>

      <div className="logo-center">
        <img src="/main-logo.png" alt="중앙 슬로건 로고" className="center-logo" />
      </div>

      <main className="login-form-container">
        <form className="login-form" onSubmit={handleSubmit}>
          <label>
            이메일
            <input
              type="email"
              placeholder="이메일 주소를 입력해주세요."
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </label>

          <label>
            비밀번호
            <input
              type="password"
              placeholder="비밀번호를 입력해주세요."
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </label>

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
