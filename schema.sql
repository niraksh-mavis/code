DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS documents;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    email TEXT,
    role TEXT DEFAULT 'user',
    bio TEXT
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    author TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    filename TEXT NOT NULL,
    owner_id INTEGER,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

-- Seed Data
INSERT INTO users (username, password_hash, email, role, bio) VALUES 
('admin', '21232f297a57a5a743894a0e4a801fc3', 'admin@example.local', 'admin', 'System administrator account'),
('john_doe', '5f4dcc3b5aa765d61d8327deb882cf99', 'john@example.local', 'user', 'Software Engineer & Security Enthusiast');

INSERT INTO comments (user_id, author, content) VALUES 
(1, 'admin', 'Welcome to the corporate portal! Report any system issues to IT.'),
(2, 'john_doe', 'Hey everyone, glad to be on board.');

INSERT INTO documents (title, filename, owner_id) VALUES 
('Q3 Financial Overview', 'financials_q3.pdf', 1),
('Employee Handbook', 'handbook.txt', 1);
