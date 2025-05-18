import sqlite3
from datetime import datetime

def send_message(user_id: str, room_id: str, message: str) -> bool:
    try:
        conn = sqlite3.connect("acton.db")
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO chat_messages (user_id, room_id, message, sent_at)
            VALUES (?, ?, ?, ?)
        """, (user_id, room_id, message, datetime.now()))
        conn.commit()
        return True
    except Exception as e:
        print("메시지 전송 실패:", e)
        return False
    finally:
        conn.close()

def get_chat_history(room_id: str) -> list:
    conn = sqlite3.connect("acton.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT user_id, message, sent_at 
        FROM chat_messages 
        WHERE room_id = ? 
        ORDER BY sent_at ASC
    """, (room_id,))
    rows = cur.fetchall()
    conn.close()
    return [{"user_id": r[0], "message": r[1], "sent_at": r[2]} for r in rows]



"""
/services/chat_service.py
역할:
사용자 간의 채팅 메시지를 저장하고 조회하는 기능을 제공하는 서비스 레이어.
SQLite 데이터베이스를 이용하여 채팅 내역을 관리한다.

주요 기능:
-채팅 메시지를 DB에 저장
-지정된 채팅방의 전체 메시지 이력을 시간순으로 조회

함수 목록 및 설명:
-def send_message(user_id, room_id, message): 주어진 메시지를 `chat_messages` 테이블에 저장. 저장 성공 여부를 bool로 반환
-def get_chat_history(room_id): 지정된 room_id의 채팅 이력을 시간순으로 조회해 리스트로 반환

동작 흐름 요약
사용자가 메시지를 전송하면 send_message 함수가 acton.db에 연결해 데이터를 삽입하고 커밋
get_chat_history 함수는 해당 채팅방의 모든 메시지를 시간순으로 정렬하여 반환
"""
