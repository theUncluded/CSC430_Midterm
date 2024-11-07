import React from 'react';
import './AdminPage.css';

// This is the Admin component
function Admin() {
  return (
    // Main container for the admin page
    <div className="AdminPage">
      <h1>Admin Page</h1>
      {/* Welcome message for admins */}
      <p>Welcome to the Admin page. This area is for authorized users only.</p>
      {/* Button for admin settings */}
      <button onClick={() => alert("Admin settings will go here!")}>
        Settings
      </button>
    </div>
  );
}

// Export the Admin component
export default Admin;
