-- ==============================================================
-- A+ Academy Telegram Bot Database Schema (SQLite)
-- Tables: users, courses, payments, enrollments
-- ==============================================================

PRAGMA foreign_keys = ON;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    username TEXT,
    language TEXT NOT NULL DEFAULT 'en',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users (telegram_id);

-- 2. Courses Table
CREATE TABLE IF NOT EXISTS courses (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    price TEXT NOT NULL,
    telebirr_number TEXT NOT NULL,
    cbe_number TEXT NOT NULL,
    description TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 3. Payments Table (Each payment has its own unique ID)
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    course_id TEXT NOT NULL,
    file_type TEXT CHECK(file_type IN ('photo', 'document')) NOT NULL,
    file_id TEXT NOT NULL,
    status TEXT CHECK(status IN ('pending', 'approved', 'rejected')) NOT NULL DEFAULT 'pending',
    submission_count INTEGER NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    approved_at DATETIME,
    rejected_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_payments_status ON payments (status);
CREATE INDEX IF NOT EXISTS idx_payments_user ON payments (user_id);

-- 4. Enrollments Table
CREATE TABLE IF NOT EXISTS enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    course_id TEXT NOT NULL,
    payment_id INTEGER NOT NULL,
    status TEXT CHECK(status IN ('active', 'expired', 'revoked')) NOT NULL DEFAULT 'active',
    invite_link TEXT,
    enrolled_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE RESTRICT,
    FOREIGN KEY (payment_id) REFERENCES payments(id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_enrollments_user ON enrollments (user_id);
CREATE INDEX IF NOT EXISTS idx_enrollments_course ON enrollments (course_id);

-- Initial Course Data: Freshman Course
INSERT INTO courses (id, title, price, telebirr_number, cbe_number, description)
VALUES (
    'freshman',
    'Freshman Courses (English, Mathematics, Logic, Psychology, Economics, Entrepreneurship, Physics, Anthropology, History, Computer Programming, Physical Fitness...)',
    '400 ETB',
    '0929781996',
    '1000316427735',
    'PDFs + Videos Lessons + Past years Mid and final Exams, Department info and More'
)
ON CONFLICT(id) DO UPDATE SET
    title = excluded.title,
    price = excluded.price,
    telebirr_number = excluded.telebirr_number,
    cbe_number = excluded.cbe_number,
    description = excluded.description;
