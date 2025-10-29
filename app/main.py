from fastapi import FastAPI
import asyncio
from app.gtfs_fetcher import GTFSFetcher
from app.gtfs_parser import parse_feed
from app.ghost_detector import GhostDetector
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(title="Ghost Bus Detector")

# Enable CORS so React (frontend) can call FastAPI (backend)
# Allowing all origins (*) for development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create fetcher and ghost detector
fetcher = GTFSFetcher()
detector = GhostDetector(stale_threshold=60)  # 1 minute

# Store latest vehicles in memory
latest_vehicles = []

# Store ghosts separately
latest_ghosts = []


# Callback function that runs whenever GTFS feed is fetched
async def handle_feed(data: bytes):
    global latest_vehicles, latest_ghosts

    # Parse GTFS feed into a list of vehicle dicts
    vehicles = parse_feed(data)

    # Filter out invalid coordinates
    vehicles = [v for v in vehicles if v["lat"] != 0.0 and v["lon"] != 0.0]

    # Update the global cache
    latest_vehicles = vehicles

    # Run ghost detector (detects buses that stop updating)
    ghosts = detector.update(vehicles)

    latest_ghosts = ghosts  # cache ghosts

    print(f"Currently {len(vehicles)} active vehicles")
    if ghosts:
        print(f"🚨 Detected {len(ghosts)} ghost buses!")
        for g in ghosts[:3]:  # print only first few
            print(g)
    else:
        print(f"🚨 Detected {len(ghosts)} ghost buses!")


# Run the fetcher in the background when FastAPI starts
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(fetcher.start(handle_feed))


# Root endpoint (just for testing API health)
@app.get("/")
async def root():
    return {"message": "Ghost Bus Detector API is running"}


#  Endpoint for frontend to fetch current buses
@app.get("/buses")
async def get_buses():
    return latest_vehicles


@app.get("/ghosts")
async def get_ghosts():
    return latest_ghosts
