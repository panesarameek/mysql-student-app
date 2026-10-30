-- Database and table used by student_management.py
-- Run this once in MySQL Workbench before starting the app.

CREATE DATABASE IF NOT EXISTS Student;
USE Student;

CREATE TABLE IF NOT EXISTS students (
    student_id    INT AUTO_INCREMENT PRIMARY KEY,
    student_name  VARCHAR(100) NOT NULL,
    email         VARCHAR(100) NOT NULL UNIQUE,   -- the app shows "already registered" if repeated
    mobile        VARCHAR(10)  NOT NULL UNIQUE,   -- 10 digits
    age           INT,
    course        VARCHAR(100),
    address       VARCHAR(255),
    status        VARCHAR(10) DEFAULT 'Active',   -- Active or Inactive
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
