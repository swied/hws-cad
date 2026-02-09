# BoardCAD Refactored (React + Python)

This repository contains a complete refactor of the legacy Java-based BoardCAD application. It separates the application into a modern React frontend for interaction and visualization, and a Python backend for scientific computing, CAD mathematics, and CAM generation.

## Repository Schema

```text
/
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
├── docker-compose.yml          # Container orchestration (Optional)
├── backend/                    # Python Backend (Replaces Java Core/CAM)
│   ├── app.py                  # Application Entry Point (FastAPI)
│   ├── config.py               # Configuration settings
│   ├── api/                    # API Routes
│   │   ├── __init__.py
│   │   ├── board.py            # Endpoints for board manipulation
│   │   └── cam.py              # Endpoints for G-code/Toolpaths
│   ├── core/                   # Mathematical Core (Replaces 'cadcore')
│   │   ├── __init__.py
│   │   ├── bezier.py           # Bezier curve logic
│   │   ├── nurbs.py            # NURBS surface logic
│   │   └── vectors.py          # Vector math (numpy based)
│   ├── models/                 # Data Models (Replaces 'board')
│   │   ├── __init__.py
│   │   └── surfboard.py        # The Surfboard object definition
│   ├── io/                     # File Readers/Writers
│   │   ├── __init__.py
│   │   ├── brd_reader.py       # Legacy .brd parser
│   │   └── stl_writer.py       # STL export logic
│   └── cam/                    # Manufacturing Logic (Replaces 'boardcam')
│       ├── __init__.py
│       └── toolpath.py         # G-Code generation logic
└── frontend/                   # React Frontend (Replaces Swing GUI)
    ├── package.json
    ├── public/
    │   └── index.html
    └── src/
        ├── App.jsx             # Main Component
        ├── index.js            # Entry Point
        ├── api/                # API Connectors
        │   └── client.js
        ├── components/         # UI Components
        │   ├── Controls.jsx    # Sidebar controls
        │   └── Toolbar.jsx     # Top menu
        ├── three/              # 3D Visualization (Replaces JOGL)
        │   ├── BoardScene.jsx  # Main 3D Scene (R3F)
        │   └── BoardMesh.jsx   # The Surfboard Mesh
        └── store/              # State Management
            └── boardStore.js   # Zustand/Redux store
```

## Setup Instructions

### Prerequisites

1. Python 3.9+
2. Node.js 16+

### 1. Backend Setup (Python)

We use `FastAPI` for the web server and `numpy`/`scipy` for the scientific computing previously handled by Java.

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fastapi uvicorn numpy scipy pydantic
# Run the server
uvicorn app:app --reload --port 8000
```

### 2. Frontend Setup (React)

We use `Vite` or `CRA` for the build tool and `react-three-fiber` for 3D rendering.

```bash
cd frontend
npm install react react-dom three @react-three/fiber @react-three/drei axios zustand
# Run the client
npm start
```

## Migration Notes

- Math: All functionality from `cadcore` (Java) has been ported to `backend/core` using NumPy.
- 3D View: Java3D/JOGL has been replaced by WebGL via Three.js in `frontend/src/three`.
- Files: The legacy `.brd` files are parsed in Python and converted to JSON for the frontend.

## Start from Docker

```bash
sudo docker-compose up --build
```
