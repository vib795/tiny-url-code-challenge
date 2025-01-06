# URL Shortener Service
![](demo.gif)<br/>

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
- [FastAPI:](https://fastapi.tiangolo.com/) A modern, high-performance web framework for building APIs with Python. It provides automatic API documentation, request/response validation, and asynchronous support out of the box, making it ideal for building fast and reliable web services.

- [SQLAlchemy:](https://www.sqlalchemy.org/) A comprehensive database toolkit for Python that provides both a SQL abstraction layer (ORM) and a powerful query builder. As our ORM (Object-Relational Mapper), it allows us to work with database objects in a Pythonic way while maintaining fine-grained control over SQL performance.

- [PostgreSQL:](https://www.postgresql.org/) Our chosen database system, known for its reliability, feature richness, and excellent performance with structured data. PostgreSQL excels at handling concurrent users and complex queries, making it perfect for storing URL mappings and tracking analytics.

- [Uvicorn:](https://www.uvicorn.org/) A lightning-fast ASGI (Asynchronous Server Gateway Interface) server implementation that powers our FastAPI application. It provides the production-grade server capabilities needed to handle concurrent requests efficiently, which is crucial for a URL shortening service that needs to process many redirects quickly.

### Frontend
- [React (18):](https://react.dev/) A declarative JavaScript library for building user interfaces, providing powerful features like hooks and component-based architecture.

- [Vite:](https://vite.dev/) A modern frontend build tool that offers lightning-fast development server and optimized production builds.

- [Tailwind CSS:](https://tailwindcss.com/) A highly customizable, low-level CSS framework that enables rapid UI development through utility classes.

- [Lucide Icons:](https://lucide.dev/icons/) A comprehensive icon library that provides consistent, high-quality SVG icons.

### Infrastructure
- [Docker](https://www.docker.com/)
- PostgreSQL 16

## Getting Started

### Prerequisites

Before starting, ensure you have:
- Docker for containerized deployment
- [Node.js](https://nodejs.org/en) runtime (version 18+) to run the development tools for the React/Vite frontend
- Python 3.9 or higher for backend development

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