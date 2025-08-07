// frontend/src/ApiStatus.js
import React, { useEffect, useState } from 'react';

function ApiStatus() {
  const [message, setMessage] = useState('Loading...');

  useEffect(() => {
    fetch('http://localhost:5000/')
      .then(res => res.json())
      .then(data => setMessage(data.message))
      .catch(err => setMessage('Failed to connect to Flask API'));
  }, []);

  return (
    <div>
      <h2>Flask API Status</h2>
      <p>{message}</p>
    </div>
  );
}

export default ApiStatus;
