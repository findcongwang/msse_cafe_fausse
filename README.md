# Café Fausse Website

A full-stack (monorepo) web application for Café Fausse, a fine dining establishment. The application provides restaurant information, menu display, table reservations, and customer engagement features.

## 🍽️ Project Overview

Café Fausse's website combines a modern, responsive frontend with a robust backend to deliver a seamless dining experience for customers. The application allows users to:

- Browse the restaurant's menu
- Make table reservations
- View restaurant information and gallery
- Subscribe to newsletters
- Read customer testimonials and awards

## 🛠️ Tech Stack

### Frontend
- **Astro** - Static Site Generator
- **React** - For interactive components
- **TypeScript** - Type safety
- **TailwindCSS** - Utility-first CSS
- **DaisyUI** - UI Component library

### Backend
- **Flask** - Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL** - Database
- **Poetry** - Python dependency management

## 📁 Project Structure 

```plaintext
msse_cafe_fausse/
├── frontend/       # Frontend application
│ ├── src/
│ │ ├── components/       # Reusable UI components
│ │ ├── layouts/          # Page layouts
│ │ ├── pages/            # Route pages
│ │ └── styles/           # Global styles
│ ├── public/             # Static assets
│ └── astro.config.mjs    # Astro configuration
│
├── backend/       # Backend application
│ ├── app/
│ │ ├── api/              # API endpoints
│ │ ├── core/             # Core configurations
│ │ ├── crud/             # CRUD operations
│ │ ├── db/               # Database setup
│ │ ├── models.py         # SQLAlchemy models
│ │ └── schemas/          # Pydantic schemas
│ ├── migrations/         # Database migrations
│ └── tests/              # Backend tests
│
└── README.md             # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL
- Poetry
- npm

### Environment Setup

1. Clone the repository:

```bash
git clone https://github.com/findcongwang/msse_cafe_fausse.git
cd msse_cafe_fausse
```

2. Set up backend environment:
```bash
cd backend-python
poetry install
cp .env.example .env  # Configure your environment variables
```

3. Set up frontend environment:
```bash
cd ../frontend-astro
npm install
```

4. Configure database:
```bash
cd ../backend
poetry run alembic upgrade head
```

### Running Locally

1. Start the backend server (default port 8080):
```bash
cd backend
poetry run python -m app.main
```

2. In a new terminal, start the frontend server (default port 4321):
```bash
cd frontend
npm run dev
```

The application will be available at:
- Frontend: http://localhost:4321
- Backend API: http://localhost:8080/api

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
