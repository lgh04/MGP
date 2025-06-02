// src/App.js
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/home';     // ✅ 홈 컴포넌트 추가
import Register from './pages/Register';
import Login from './pages/login';   // ✅ 경로 대소문자 확인!
import BillListPage from './pages/list';
import DetailPage from './pages/detail';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />         {/* ✅ 홈 라우트 추가 */}
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/list" element={<BillListPage />} /> 
         <Route path="/detail/:billId" element={<DetailPage />} />
      </Routes>
    </Router>
  );
}

export default App;
