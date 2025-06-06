// src/App.js
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Home from './pages/home';     // ✅ 홈 컴포넌트 추가
import Register from './pages/Register';
import Login from './pages/login';   // ✅ 경로 대소문자 확인!
import BillListPage from './pages/list';
import DetailPage from './pages/detail';

// React Query 클라이언트 생성
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5분
      cacheTime: 1000 * 60 * 30, // 30분
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />         {/* ✅ 홈 라우트 추가 */}
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/list" element={<BillListPage />} /> 
          <Route path="/detail/:billId" element={<DetailPage />} />
        </Routes>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
