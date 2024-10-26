import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

function Home() {
  const [currentTime, setCurrentTime] = useState('');

  useEffect(() => {
    const updateCurrentTime = () => {
      const now = new Date();
      setCurrentTime(now.toLocaleTimeString());
    };

    const intervalId = setInterval(updateCurrentTime, 1000);
    updateCurrentTime(); // Initialize immediately

    return () => clearInterval(intervalId); // Cleanup on unmount
  }, []);

  return (
    <div className="home">
      <h1 className="title">Welcome to TO-DO App</h1>
      <p className="subtitle">Your tasks organized, your goals achieved.</p>
      <div className="time">Current Time: {currentTime}</div>
      <div className="features">
        <h2>Features:</h2>
        <ul>
          <li className="feature-item">✔️ Add, edit, and delete tasks</li>
          <li className="feature-item">✔️ Mark tasks as completed</li>
          <li className="feature-item">✔️ User authentication for secure access</li>
          <li className="feature-item">✔️ Responsive design for all devices</li>
        </ul>
      </div>
      <div className="buttons">
        <Link to="/login" className="btn btn-signin">Sign In</Link>
        <Link to="/signup" className="btn btn-signup">Sign Up</Link>
      </div>

      {/* Footer */}
      <footer className="footer">
        <div className="contact-info">
          <h2>Contact Us</h2>
          <p>Email: support@todoapp.com</p>
          <p>Phone: (123) 123-123</p>
        </div>
        <div className="location-info">
          <h2>Location</h2>
          <p>Somewhere between 0s and 1s</p>
        </div>
      </footer>
    </div>
  );
}

export default Home;
