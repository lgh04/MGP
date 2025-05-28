import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // 🔹 페이지 이동을 위한 훅
import './list.css';

function ListPage() {
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages] = useState(50);
  const [filter, setFilter] = useState('latest');
  const [startPage, setStartPage] = useState(1);
  const pageSize = 10;

  const navigate = useNavigate(); // 🔹 페이지 이동 함수 사용

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  const handleFilterChange = (type) => {
    setFilter(type);
    setCurrentPage(1);
    setStartPage(1);
  };

  const handlePrevGroup = () => {
    setStartPage(Math.max(startPage - pageSize, 1));
  };

  const handleNextGroup = () => {
    if (startPage + pageSize <= totalPages) {
      setStartPage(startPage + pageSize);
    }
  };

  const renderPagination = () => {
    const pages = [];
    const endPage = Math.min(startPage + pageSize - 1, totalPages);

    pages.push(
      <button key="prev" onClick={handlePrevGroup} disabled={startPage === 1}>
        ◀
      </button>
    );

    for (let i = startPage; i <= endPage; i++) {
      pages.push(
        <button
          key={i}
          className={currentPage === i ? 'active' : ''}
          onClick={() => handlePageChange(i)}
        >
          {i}
        </button>
      );
    }

    pages.push(
      <button key="next" onClick={handleNextGroup} disabled={endPage >= totalPages}>
        ▶
      </button>
    );

    return pages;
  };

  return (
    <div className="list-page">
      <div className="list-header">
        <img className="logo" src="/logo.png" alt="ACT:ON Logo" />

        <div className="search-bar">
          <select>
            <option>발의</option>
            <option>공포</option>
          </select>
          <input type="text" placeholder="발의된 또는 공포된 법안을 검색해 주세요" />
          <button className="search-button">🔍</button>
        </div>

        <div className="auth-buttons">
          <button className="signin-btn" onClick={() => navigate('/login')}>
            Sign in
          </button>
          <button className="register-btn" onClick={() => navigate('/register')}>
            Register
          </button>
        </div>
      </div>

      <div className="billlist-container">
        <div className="billlist-filter">
          <button onClick={() => handleFilterChange('latest')} className={filter === 'latest' ? 'active' : ''}>
            최신순
          </button>
          <button onClick={() => handleFilterChange('views')} className={filter === 'views' ? 'active' : ''}>
            열람 횟수 순
          </button>
        </div>

        {Array.from({ length: 7 }).map((_, index) => (
          <div key={index} className="bill-box"></div>
        ))}

        <div className="pagination">{renderPagination()}</div>
      </div>
    </div>
  );
}

export default ListPage;
