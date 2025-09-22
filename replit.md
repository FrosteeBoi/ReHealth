# ReHealth - Health Tracking Desktop Application

## Overview
ReHealth is a Python-based desktop health tracking application that allows users to manage their fitness metrics, measurements, and health data. The application features user authentication, a dashboard interface, and measurement tracking functionality.

## Recent Changes (September 22, 2025)
- Set up the project for Replit environment
- Fixed hardcoded Windows file paths to use relative paths
- Fixed import issues for proper module structure
- Created main.py entry point
- Configured Python 3.11 with ttkbootstrap dependency
- Initialized SQLite database with proper schema
- Configured workflow for desktop application

## Project Architecture
- **Language**: Python 3.11
- **GUI Framework**: ttkbootstrap (themed tkinter)
- **Database**: SQLite3 (local file-based)
- **Project Structure**:
  - `main.py` - Application entry point
  - `ui/` - User interface modules (login, dashboard, measurement)
  - `logic/` - Business logic (user management, calculations)
  - `db/` - Database handlers and initialization
  - `requirements.txt` - Python dependencies

## Key Features
- User registration and authentication with password hashing
- Secure login system with form validation
- Dashboard interface for health metrics
- Measurement tracking for height, weight, and BMI
- SQLite database for persistent data storage
- Modern dark theme UI using ttkbootstrap

## Database Schema
- **User table**: Stores user credentials and basic info
- **MetricsTracking**: Height/weight measurements over time
- **Steps, Sleep, Food, Exercises**: Additional health tracking tables
- **UserExercises**: Links users to exercise logs

## Running the Application
The application is configured to run as a desktop app in the Replit environment:
- Main command: `python main.py`
- The workflow "ReHealth Desktop App" is configured for console output
- Database is automatically initialized on first run

## Dependencies
- `ttkbootstrap==1.10.1` - Modern themed tkinter widgets
- Standard Python libraries: sqlite3, hashlib, re, datetime, random

## User Preferences
- Application uses a dark theme by default
- GUI-based desktop application (not web-based)
- Local SQLite database for data persistence