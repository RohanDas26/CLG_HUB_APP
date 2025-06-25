import React from 'react';
import Sidebar from './components/Sidebar';
import './App.css'; // Global styles for our app layout

function App() {
  return (
    <div className="app-container">
      <Sidebar />
      <main className="main-content">
        {/* This is the main view area. */}
        {/* Let's put a welcome message here for now. */}
        <div className="welcome-view">
          <h1>Welcome to your CLG HUB ✨</h1>
          <p>Select a subject from the sidebar to view files, or use the quick links to access university portals.</p>
        </div>
      </main>
    </div>
  );
}

export default App;