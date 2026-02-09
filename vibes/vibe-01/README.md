# Hollow Wooden Surfboard CAD (Project AtomBoard)

A browser-based CAD tool for designing hollow wooden surfboards, coupled with a Python backend for generating manufacturing blueprints.

## Project Architecture
This project follows a "Client-Server" separation pattern, though the server side is currently a local Python script.

1. **Frontend (Web App):** `surfboard_designer.html`
    - **Tech Stack:** React, Tailwind CSS, Three.js, Lucide Icons.
    - **Purpose:** Visual design. Allows you to tweak dimensions and view the board in 3D in real-time.
    - **Output:** Exports a .json file containing the design DNA.
2. Backend (Math Engine): `geometry_engine.py`
    - **Tech Stack:** Python 3, Numpy, Scipy.
    - **Purpose:** Takes the `.json` file, performs complex B-Spline interpolation, and calculates the specific 2D cross-sections (ribs) needed for construction.
    - **Output:** `.svg` or `.pdf` files for printing rib templates.

## File Schema

Recommended directory structure for your GitHub repository:

```text
/surfboard-cad-app
│
├── /src
│   ├── surfboard_designer.html   # The single-file Web App
│   └── /assets                   # Images/Textures (future use)
│
├── /engine
│   ├── geometry_engine.py        # Python calculation script
│   └── requirements.txt          # Python dependencies
│
├── /output                       # Folder where generated SVGs go
│
└── README.md                     # This file
```

## Step 1: Installation & Setup

### Prerequisites

1. Web Browser: Chrome (recommended), Firefox, or Edge.
2. Python 3: Installed on your Ubuntu machine (`sudo apt install python3`).

### Setup Python Environment

Open your terminal and run the following commands to install the required mathematical libraries:

```bash
# Update pip
pip install --upgrade pip

# Install Science libraries
pip install numpy scipy matplotlib
```

## Step 2: Running the Web App

1. Navigate to the folder containing `surfboard_designer.html`.
2. Simply double-click the file to open it in Chrome, OR run a simple local server if you encounter CORS issues (though the current version is designed to run standalone):

```bash
python3 -m http.server
```
3. Open `http://localhost:8000/surfboard_designer.html`.
4. Adjust the sliders to design your board.
5. Click "Export Design JSON". This will save `my_surfboard_design.json` to your Downloads folder.

## Step 3: Generating Ribs

1. Move the downloaded `my_surfboard_design.json` into the same folder as `geometry_engine.py`.
2. Run the engine:

```bash
python3 geometry_engine.py
```

3. The script will generate `.svg` files (e.g., `rib_station_12.svg`) representing the cross-sections of your board. You can open these in Inkscape or a browser to print them.

## Roadmap for Development

1. Phase 1 (Complete): Basic 3D visualization and parameter export. Basic Rib generation script.
2. Phase 2 (Next Steps):
    - Python: Add logic to subtract "skin thickness" (e.g., 0.25") from the rib shapes.
    - Python: Add logic to cut the "notch" in the center of the rib for the central spine.
    - Web: Add a visual representation of the internal skeleton in the 3D view.
3. Phase 3 (Polishing):
    - Convert the HTML file into a proper `create-react-app` structure if the code grows too large.
    - Wrap the app in Electron to combine the Python engine and Web App into a single installable `.deb` file for Ubuntu.