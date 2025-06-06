import React, { useState, useEffect } from 'react';
import DiscussionPopup from './DiscussionPopup';

const DiscussionList = () => {
  const [discussions, setDiscussions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedDiscussion, setSelectedDiscussion] = useState(null);

  useEffect(() => {
    const fetchDiscussions = async () => {
      try {
        const token = sessionStorage.getItem('token');
        const response = await fetch(`${process.env.REACT_APP_API_URL}/api/discussions`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        const data = await response.json();
        
        // 각 토론방의 법안 정보를 가져옵니다
        const discussionsWithBillNames = await Promise.all(
          data.map(async (discussion) => {
            try {
              const lawResponse = await fetch(`${process.env.REACT_APP_API_URL}/api/law/${discussion.bill_id}`, {
                headers: {
                  'Authorization': `Bearer ${token}`
                }
              });
              const lawData = await lawResponse.json();
              return {
                ...discussion,
                billName: lawData.BILL_NAME || "알 수 없는 법안"
              };
            } catch (error) {
              console.error(`법안 정보 로딩 실패 (ID: ${discussion.bill_id}):`, error);
              return {
                ...discussion,
                billName: "알 수 없는 법안"
              };
            }
          })
        );
        
        setDiscussions(discussionsWithBillNames);
        setLoading(false);
      } catch (error) {
        console.error("토론방 목록 로딩 실패:", error);
        setLoading(false);
      }
    };

    fetchDiscussions();
  }, []);

  const handleDiscussionClick = (discussion) => {
    setSelectedDiscussion(discussion);
  };

  return (
    <div className="discussion-list">
      {loading ? (
        <div>로딩 중...</div>
      ) : (
        <>
          {discussions.map((discussion) => (
            <div
              key={discussion.id}
              className="discussion-item"
              onClick={() => handleDiscussionClick(discussion)}
            >
              <h3>{discussion.billName}</h3>
              <p>참여자 수: {discussion.participant_count}</p>
            </div>
          ))}
          {selectedDiscussion && (
            <DiscussionPopup
              discussionId={selectedDiscussion.id}
              billId={selectedDiscussion.bill_id}
              onClose={() => setSelectedDiscussion(null)}
            />
          )}
        </>
      )}
    </div>
  );
};

export default DiscussionList; 