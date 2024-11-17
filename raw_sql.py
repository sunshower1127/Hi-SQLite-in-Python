import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect("blog.db")  # 그냥 경로임. 없으면 파일 생성
c = conn.cursor()  # 커서로 데이터베이스에 접근할 수 있음

# 유저 테이블 생성
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL
)
""")

# 포스트 테이블 생성
c.execute("""
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
""")

# 데이터 삽입
c.execute("INSERT INTO users (username, email) VALUES ('user1', 'user1@example.com')")
c.execute("INSERT INTO users (username, email) VALUES ('user2', 'user2@example.com')")
c.execute(
    "INSERT INTO posts (user_id, title, content) VALUES (1, 'First Post', 'This is the first post')"
)
c.execute(
    "INSERT INTO posts (user_id, title, content) VALUES (2, 'Second Post', 'This is the second post')"
)

# 데이터 커밋
conn.commit()

# 조인 쿼리
c.execute("""
SELECT users.username, posts.title, posts.content
FROM posts
JOIN users ON posts.user_id = users.id
""")

# 결과 출력
for row in c.fetchall():  # fetchall()로 SELECT 결과를 row[]로 받아옴
    print(row)

# 데이터 업데이트
c.execute("UPDATE users SET email = 'newemail@example.com' WHERE username = 'user1'")
conn.commit()

# 업데이트된 데이터 확인
c.execute("SELECT * FROM users")
for row in c.fetchall():
    print(row)

# 연결 종료
conn.close()
