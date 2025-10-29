#Ghost Bus Detector

A small FastAPI-based project that fetches GTFS-Realtime vehicle positions, parses them, and detects "ghost" vehicles (vehicles that stop updating or remain at the same location for an extended time). This repo contains a lightweight backend API and WebSocket utilities intended to be paired with a frontend (e.g., React) for real-time visualization.

Repository layout
ghost-bus-detector/
├── .gitignore
├── README.md
├── requirements.txt
└── app/
├── __init__.py
├── config.py
├── gtfs_fetcher.py
├── gtfs_parser.py
├── ghost_detector.py
├── main.py
├── websocket_manager.py
└── ws_test.py

Quick features

>Polls a GTFS-Realtime vehicle positions feed on an interval.
>Parses GTFS protobuf into Python dictionaries.
>Detects "ghost" buses (stale / one-time vehicles) using a configurable threshold.
>Exposes simple HTTP endpoints: / (health), /buses, /ghosts.
>WebSocket manager utilities and a ws_test.py sample server.

Installation

1.Create a Python virtual environment (recommended):
python -m venv venv
source venv/bin/activate # macOS / Linux
venv\Scripts\activate

2.Install dependencies:
pip install -r requirements.txt

3.Run the app with uvicorn (from project root):
uvicorn main:app --reload --port 8000
# or if your FastAPI app object is inside app/main.py use:
# uvicorn app.main:app --reload --port 8000


4.Visit http://127.0.0.1:8000 to see the health endpoint. Access /buses and /ghosts for JSON responses.
