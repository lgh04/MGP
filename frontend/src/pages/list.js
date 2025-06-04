import React, { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import "./list.css";
import MyPagePopup from '../components/MyPagePopup';

function ListPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const [nickname, setNickname] = useState(null);
  const [showMyPage, setShowMyPage] = useState(false);

  useEffect(() => {
    const storedNickname = sessionStorage.getItem("nickname");
    if (storedNickname) {
      setNickname(storedNickname);
    }
  }, []);

  const initialQuery = searchParams.get("query") || "";
  const initialMode = searchParams.get("mode") || "공포";
  const initialSort = searchParams.get("sort") || "latest";
  const initialPage = parseInt(searchParams.get("page") || "1");

  const [query, setQuery] = useState(initialQuery);
  const [searchText, setSearchText] = useState(initialQuery);
  const [mode, setMode] = useState(initialMode);
  const [filter, setFilter] = useState(initialSort);
  const [currentPage, setCurrentPage] = useState(initialPage);
  const [totalPages, setTotalPages] = useState(1);
  const [items, setItems] = useState([]);

  const [startPage, setStartPage] = useState(1);
  const pageSize = 10;
  const maxPageNumbers = 10; // 한 번에 보여줄 페이지 번호 개수

  useEffect(() => {
    const fetchData = () => {
      fetch(
        `${process.env.REACT_APP_API_URL}/api/law-list?query=${searchText}&mode=${mode}&sort=${filter}&page=${currentPage}`
      )
        .then((res) => res.json())
        .then((data) => {
          setItems(data.items || []);
          setTotalPages(data.total_pages || 1);
        })
        .catch((err) => {
          console.error("❌ API 호출 실패:", err);
          setItems([]);
        });
    };

    fetchData();
  }, [searchText, mode, filter, currentPage]);

  const handleSearchClick = () => {
    setCurrentPage(1);
    setStartPage(1);
    setSearchText(query);
    navigate(
      `/list?query=${encodeURIComponent(query)}&mode=${mode}&sort=${filter}&page=1`
    );
  };

  const handleFilterChange = (newFilter) => {
    setFilter(newFilter);
    setCurrentPage(1);
    setStartPage(1);
    navigate(
      `/list?query=${encodeURIComponent(query)}&mode=${mode}&sort=${newFilter}&page=1`
    );
  };

  const handlePageChange = (newPage) => {
    setCurrentPage(newPage);
    if (newPage < startPage) {
      setStartPage(Math.max(1, newPage - Math.floor(maxPageNumbers / 2)));
    } else if (newPage >= startPage + maxPageNumbers) {
      setStartPage(Math.max(1, newPage - maxPageNumbers + 1));
    }
    navigate(
      `/list?query=${encodeURIComponent(query)}&mode=${mode}&sort=${filter}&page=${newPage}`
    );
  };

  const handlePageGroupChange = (direction) => {
    if (direction === 'prev') {
      const newStartPage = Math.max(1, startPage - pageSize);
      setStartPage(newStartPage);
      if (currentPage > newStartPage + pageSize - 1) {
        setCurrentPage(newStartPage);
        navigate(
          `/list?query=${encodeURIComponent(query)}&mode=${mode}&sort=${filter}&page=${newStartPage}`
        );
      }
    } else {
      const newStartPage = Math.min(
        Math.ceil(totalPages / pageSize) * pageSize - pageSize + 1,
        startPage + pageSize
      );
      setStartPage(newStartPage);
      if (currentPage < newStartPage) {
        setCurrentPage(newStartPage);
        navigate(
          `/list?query=${encodeURIComponent(query)}&mode=${mode}&sort=${filter}&page=${newStartPage}`
        );
      }
    }
  };

  const renderPagination = () => {
    const pages = [];
    const endPage = Math.min(startPage + maxPageNumbers - 1, totalPages);

    // 이전 10페이지로 이동
    if (startPage > 1) {
      pages.push(
        <button 
          key="first" 
          onClick={() => handlePageGroupChange('prev')}
          className="page-arrow"
        >
          ≪
        </button>
      );
    }

    // 이전 페이지로 이동
    if (currentPage > 1) {
      pages.push(
        <button 
          key="prev" 
          onClick={() => handlePageChange(currentPage - 1)}
          className="page-arrow"
        >
          ＜
        </button>
      );
    }

    // 페이지 번호
    for (let i = startPage; i <= endPage; i++) {
      pages.push(
        <button
          key={i}
          onClick={() => handlePageChange(i)}
          className={currentPage === i ? "active" : ""}
        >
          {i}
        </button>
      );
    }

    // 다음 페이지로 이동
    if (currentPage < totalPages) {
      pages.push(
        <button 
          key="next" 
          onClick={() => handlePageChange(currentPage + 1)}
          className="page-arrow"
        >
          ＞
        </button>
      );
    }

    // 다음 10페이지로 이동
    if (endPage < totalPages) {
      pages.push(
        <button 
          key="last" 
          onClick={() => handlePageGroupChange('next')}
          className="page-arrow"
        >
          ≫
        </button>
      );
    }

    return pages;
  };

  return (
    <div className="list-page">
      <div className="list-header">
        <img 
          className="logo" 
          src="/logo.png" 
          alt="ACT:ON Logo" 
          onClick={() => navigate('/')}
          style={{ cursor: 'pointer' }}
        />

        <div className="search-bar">
          <select value={mode} onChange={(e) => setMode(e.target.value)}>
            <option value="공포">공포</option>
            <option value="발의">발의</option>
          </select>
          <input
            type="text"
            placeholder="발의된 또는 공포된 법안을 검색해 주세요"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button className="search-button" onClick={handleSearchClick}>
            🔍
          </button>
        </div>

        <div className="auth-buttons">
          {nickname ? (
            <div 
              className="user-nickname"
              style={{ cursor: 'pointer' }}
              onClick={() => setShowMyPage(true)}
            >
              {nickname}
            </div>
          ) : (
            <>
              <button className="signin-btn" onClick={() => navigate("/login")}>
                Sign in
              </button>
              <button className="register-btn" onClick={() => navigate("/register")}>
                Register
              </button>
            </>
          )}
        </div>
      </div>

      <div className="billlist-container">
        <div className="billlist-filter">
          <button
            onClick={() => handleFilterChange("latest")}
            className={filter === "latest" ? "active" : ""}
          >
            최신순
          </button>
        </div>

        {items.length === 0 && <div>검색 결과가 없습니다.</div>}

        {items.map((item, index) => (
          <div key={index} className="bill-box">
            <div
              onClick={() => navigate(`/detail/${item.bill_id}`)}
              style={{ cursor: "pointer" }}
            >
              <h3>{item.title}</h3>
            </div>
            <p><strong>제안일자:</strong> {item.date}</p>
            <p><strong>제안자:</strong> {item.proposer}</p>
            <p><strong>의안번호:</strong> {item.bill_no}</p>
            <p><strong>소관위:</strong> {item.committee}</p>
            <p><strong>처리결과:</strong> {item.result}</p>
          </div>
        ))}

        <div className="pagination">{renderPagination()}</div>
      </div>

      {/* 마이페이지 팝업 */}
      {showMyPage && <MyPagePopup onClose={() => setShowMyPage(false)} />}
    </div>
  );
}

export default ListPage;
