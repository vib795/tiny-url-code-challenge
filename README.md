# URL Shortener Service

A modern, containerized URL shortener service built with FastAPI, React, and PostgreSQL. This application allows users to create shortened URLs with optional custom paths and tracks usage statistics.

## Features

- Create shortened URLs with auto-generated or custom paths
- Track click statistics for each shortened URL
- Modern, responsive UI built with React and Tailwind CSS
- RESTful API with FastAPI
- Containerized deployment with Docker and Docker Compose
- Persistent storage with PostgreSQL

## Technology Stack

### Backend
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- PostgreSQL (Database)
- Uvicorn (ASGI server)

### Frontend
- React 18
- Vite
- Tailwind CSS
- Lucide Icons

### Infrastructure
- Docker
- PostgreSQL 16

## Getting Started

### Prerequisites

Before you begin, ensure you have installed:
- Docker
- Node.js 18+ (for local development)
- Python 3.9+ (for local development)

### Quick Start with Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/vib795/tiny-url-code-challenge.git
   cd tiny-url-code-challenge
   ```

2. Create environment files:
    <br/>Example file
   <br/><br/>Backend (.env in backend directory):
   ```bash
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=postgres
   POSTGRES_DB_NAME=urlshortener
   POSTGRES_APP_USER=urlshortener_user
   POSTGRES_APP_PASSWORD=your_secure_password
   DATABASE_URL=postgresql://urlshortener_user:your_secure_password@postgres:5432/urlshortener
   ```

   Frontend (.env in frontend directory):
   ```bash
   VITE_API_URL=http://localhost:8000
   ```

3. Start the application:
   ```bash
   docker compose --env-file ./backend/.env up --build
   ```

4. Access the application:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development

#### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the development server:
   ```bash
   python main.py
   ```

#### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

## API Endpoints

- `POST /shorten`: Create a shortened URL
  - Request body: `{"url": "https://example.com", "custom_path": "optional-custom-path"}`

- `GET /{short_url}`: Redirect to original URL

- `GET /stats/{short_url}`: Get URL statistics

- `GET /health`: Service health check

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/my-new-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details

## Acknowledgments

This project was built as part of the Coding Challenges (https://codingchallenges.fyi/challenges/challenge-url-shortener)