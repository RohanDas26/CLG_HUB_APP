import React, { useState, useEffect } from 'react';
import axios from 'axios'; // Our API client
import './Sidebar.css';

// --- Type Definitions (The Power of TypeScript!) ---
// We are defining what the API response for folders should look like.
interface FoldersResponse {
  folders: string[];
}
// ----------------------------------------------------

const WEB_LINKS = {
    "Academics": "https://academics.klef.in/login",
    "ERP": "https://newerp.kluniversity.in/",
    "LMS": "https://bmp-lms.klh.edu.in/login/index.php?testsession=1014"
};

// The URL of our FastAPI backend
const API_URL = "http://127.0.0.1:8000";

function Sidebar() {
  // We tell TypeScript that 'folders' will be an array of strings.
  const [folders, setFolders] = useState<string[]>([]);
  const [selectedFolder, setSelectedFolder] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  // useEffect hook runs once when the component is first rendered.
  useEffect(() => {
    const fetchFolders = async () => {
      try {
        // We expect the response to match our 'FoldersResponse' interface.
        const response = await axios.get<FoldersResponse>(`${API_URL}/api/folders`);
        setFolders(response.data.folders);
      } catch (err) {
        console.error("Error fetching folders:", err);
        setError("Failed to load folders.");
      }
    };

    fetchFolders();
  }, []); // The empty array [] means this effect runs only once.

  const handleFolderClick = (folderName: string) => {
    setSelectedFolder(folderName);
    console.log(`Folder selected: ${folderName}`);
    // TODO: This will later trigger fetching files for this folder.
  };

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>Clg Hub</h2>
      </div>

      <div className="sidebar-section">
        <h3>🌐 Quick Links</h3>
        {Object.entries(WEB_LINKS).map(([name, url]) => (
          <a key={name} href={url} target="_blank" rel="noopener noreferrer" className="sidebar-button link-button">
            {name}
          </a>
        ))}
      </div>

      <div className="sidebar-section">
        <h3>📁 Subjects</h3>
        <div className="folder-list">
          {error && <p className="error-text">{error}</p>}
          {!error && folders.length > 0 ? (
            folders.map((folder) => (
              <button
                key={folder}
                className={`sidebar-button folder-button ${selectedFolder === folder ? 'selected' : ''}`}
                onClick={() => handleFolderClick(folder)}
              >
                {folder}
              </button>
            ))
          ) : (
            !error && <p className="loading-text">Loading...</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default Sidebar;