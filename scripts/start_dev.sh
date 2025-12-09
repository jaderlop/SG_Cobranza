#!/bin/bash

# Development Environment Start Script
# SMB Financial Management System

echo "🚀 Starting SMB Financial Management System - Development Mode"
echo "================================================================"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js is not installed"
    exit 1
fi

if ! command_exists psql; then
    echo "❌ PostgreSQL is not installed"
    exit 1
fi

echo "✅ All prerequisites are installed"
echo ""

# Start PostgreSQL (if not running)
echo "🗄️  Checking PostgreSQL..."
if ! pg_isready -q; then
    echo "⚠️  PostgreSQL is not running. Please start PostgreSQL first."
    echo "   Example: sudo service postgresql start"
    exit 1
fi
echo "✅ PostgreSQL is running"
echo ""

# Start Backend
echo "🔧 Starting Backend (FastAPI)..."
cd backend

if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt -q

if [ ! -f ".env" ]; then
    echo "ℹ️  Creating .env from .env.example"
    cp .env.example .env
fi

echo "✅ Backend ready"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"
echo "   Backend URL: http://localhost:8000"
echo "   API Docs: http://localhost:8000/api/docs"
echo ""

# Start Frontend
echo "🎨 Starting Frontend (Next.js)..."
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "📦 Installing npm dependencies..."
    npm install
fi

if [ ! -f ".env.local" ]; then
    echo "ℹ️  Creating .env.local"
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
fi

echo "✅ Frontend ready"
npm run dev &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"
echo "   Frontend URL: http://localhost:3000"
echo ""

# Show status
echo "================================================================"
echo "✨ Development environment is running!"
echo ""
echo "Services:"
echo "  📄 Frontend:  http://localhost:3000"
echo "  🔌 Backend:   http://localhost:8000"
echo "  📚 API Docs:  http://localhost:8000/api/docs"
echo ""
echo "Default login:"
echo "  👤 Username: admin"
echo "  🔑 Password: admin123"
echo ""
echo "Press Ctrl+C to stop all services"
echo "================================================================"

# Cleanup function
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ All services stopped"
    exit 0
}

# Set up trap to cleanup on Ctrl+C
trap cleanup INT TERM

# Wait for processes
wait
