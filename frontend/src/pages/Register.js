import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./Register.css";

function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    phone: "",
    email: "",
    password: "",
    passwordConfirm: "",
    nickname: ""
  });

  const [emailCode, setEmailCode] = useState("");
  const [isVerified, setIsVerified] = useState(false);
  const [nicknameError, setNicknameError] = useState(false);
  const [nicknameCheckTimer, setNicknameCheckTimer] = useState(null);

  const [secondsLeft, setSecondsLeft] = useState(0);
  const [showTimer, setShowTimer] = useState(false);

  useEffect(() => {
    if (secondsLeft <= 0) return;
    const interval = setInterval(() => {
      setSecondsLeft(prev => prev - 1);
    }, 1000);
    return () => clearInterval(interval);
  }, [secondsLeft]);

  const handleChange = (e) => {
    const { name, value } = e.target;

    if (name === "phone") {
      const onlyNumbers = value.replace(/[^0-9]/g, "");
      setForm({ ...form, phone: onlyNumbers });
      return;
    }

    setForm({ ...form, [name]: value });

    if (name === "nickname") {
      setNicknameError(false);
      if (nicknameCheckTimer) clearTimeout(nicknameCheckTimer);

      const timer = setTimeout(async () => {
        if (value.trim().length < 2) return;
        try {
          const res = await fetch(`${process.env.REACT_APP_API_URL}/api/check-nickname?nickname=${value}`);
          const data = await res.json();
          setNicknameError(!data.available);
        } catch (err) {
          console.error("닉네임 중복 확인 실패", err);
        }
      }, 500);

      setNicknameCheckTimer(timer);
    }
  };

  const sendEmailCode = async () => {
    try {
      const res = await fetch(`${process.env.REACT_APP_API_URL}/api/send-email-code`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: form.email })
      });
      const data = await res.json();
      alert(data.message);
      setShowTimer(true);
      setSecondsLeft(180);
    } catch (err) {
      alert("이메일 전송 오류: " + err.message);
    }
  };

  const verifyEmailCode = async () => {
    try {
      const res = await fetch(`${process.env.REACT_APP_API_URL}/api/verify-email-code`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: form.email, code: emailCode })
      });
      const data = await res.json();
      alert(data.message);
      setIsVerified(true);
    } catch (err) {
      alert("인증 오류: " + err.message);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!isVerified) {
      alert("이메일 인증을 완료해주세요.");
      return;
    }

    if (form.password !== form.passwordConfirm) {
      alert("비밀번호가 일치하지 않습니다.");
      return;
    }

    const payload = {
      name: form.name,
      phone: form.phone,
      email: form.email,
      password: form.password,
      nickname: form.nickname
    };

    try {
      const res = await fetch(`${process.env.REACT_APP_API_URL}/api/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        const data = await res.json();
        if (data.detail && data.detail.includes("닉네임")) {
          setNicknameError(true);
        }
        alert(data.detail || "회원가입 실패");
        return;
      }

      alert("회원가입이 완료되었습니다.");
      navigate("/login");
    } catch (error) {
      alert("에러 발생: " + error.message);
    }
  };

  return (
    <div className="register-page">
      <header className="register-header">
        <img 
          src="/logo.png" 
          alt="ACT:ON 로고 상단" 
          className="logo-top" 
          onClick={() => navigate('/')}
          style={{ cursor: 'pointer' }}
        />
        <div className="auth-buttons">
          <button className="signin-btn" onClick={() => navigate("/login")}>Sign in</button>
          <button className="register-btn" onClick={() => navigate("/register")}>Register</button>
        </div>
      </header>

      <div className="logo-center">
        <img src="/main-logo.png" alt="ACT:ON 중앙 로고" className="center-logo" />
      </div>

      <main className="register-form-container">
        <form className="register-form" onSubmit={handleSubmit}>
          <label>
            이름
            <input name="name" type="text" placeholder="실명을 입력해주세요." value={form.name} onChange={handleChange} />
          </label>

          <label>
            휴대폰 번호
            <input name="phone" type="text" placeholder="숫자만 입력해주세요." value={form.phone} onChange={handleChange} />
          </label>

          <label>
            이메일
            <div className="input-with-button">
              <input name="email" type="email" placeholder="Gmail 주소를 입력해주세요." value={form.email} onChange={handleChange} />
              <button type="button" className="verify-btn" onClick={sendEmailCode}>인증번호 전송</button>
            </div>
          </label>

          <label>
            인증번호
            <div className="input-with-button">
              <input type="text" placeholder="인증번호를 입력해주세요." value={emailCode} onChange={e => setEmailCode(e.target.value)} />
              {showTimer && (
                <span className="timer-text">
                  {Math.floor(secondsLeft / 60)}:{String(secondsLeft % 60).padStart(2, "0")}
                </span>
              )}
              <button type="button" className="confirm-btn" onClick={verifyEmailCode}>확인</button>
            </div>
            {!isVerified && emailCode && (
              <span className="error-msg">이메일 인증을 완료해주세요.</span>
            )}
          </label>

          <label>
            비밀번호
            <input name="password" type="password" placeholder="영문자, 숫자, 특수문자 포함 8자 이상 입력해주세요." value={form.password} onChange={handleChange} />
          </label>

          <label>
            비밀번호 확인
            <input name="passwordConfirm" type="password" placeholder="비밀번호를 다시 입력해주세요." value={form.passwordConfirm} onChange={handleChange} />
            {form.password && form.passwordConfirm && form.password !== form.passwordConfirm && (
              <span className="error-msg">비밀번호가 일치하지 않습니다. 다시 입력해주세요.</span>
            )}
          </label>

          <label>
            닉네임
            <input name="nickname" type="text" placeholder="사이트에서 사용할 이름을 입력해주세요." value={form.nickname} onChange={handleChange} />
            {nicknameError && (
              <span className="error-msg">이미 사용 중인 닉네임입니다. 다른 닉네임을 사용해주세요.</span>
            )}
          </label>

          <button
            type="submit"
            className="submit-btn"
            disabled={
              !form.name ||
              !form.phone ||
              !form.email ||
              !emailCode ||
              !form.password ||
              !form.passwordConfirm ||
              !form.nickname ||
              !isVerified ||
              form.password !== form.passwordConfirm ||
              nicknameError
            }
          >
            회원가입
          </button>
        </form>
      </main>
    </div>
  );
}

export default Register;
