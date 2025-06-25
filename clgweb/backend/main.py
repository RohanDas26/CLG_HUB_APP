# File: D:\KLH\PROJECTS\CLG_HUB_APP\clgweb\backend\main.py

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- This is the same setup from your original app ---
# Define where our subject folders will be stored
STORAGE_PATH = os.path.join(os.getcwd(), "ClgBuddyFiles")
# Ensure this main storage directory exists
os.makedirs(STORAGE_PATH, exist_ok=True)

# --- For testing, let's create some dummy folders if they don't exist ---
# This saves us from having to create them manually every time.
DUMMY_FOLDERS = ["Maths", "Physics", "Computer Science"]
for folder in DUMMY_FOLDERS:
    folder_path = os.path.join(STORAGE_PATH, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
# --------------------------------------------------------------------


# Create the FastAPI application instance
app = FastAPI()

# --- CORS Middleware ---
# This is CRUCIAL. It allows our React frontend (running on http://localhost:5173)
# to make requests to this backend (running on http://localhost:8000).
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -------------------------


# This is our first real API endpoint!
@app.get("/api/folders")
def get_folders():
    """
    Scans the STORAGE_PATH and returns a list of all directories found inside.
    This replaces the `load_folders` logic from your PyQt5 app.
    """
    # List all items in the storage path
    all_items = os.listdir(STORAGE_PATH)
    # Filter this list to only include directories
    folders = [item for item in all_items if os.path.isdir(os.path.join(STORAGE_PATH, item))]
    
    return {"folders": folders}


# A simple root endpoint to easily check if the server is alive
@app.get("/")
def read_root():
    return {"message": "Welcome to the ClgHub Backend! API is running."}