// src/ChangePoints.js
import React, { useEffect, useState } from 'react';

function ChangePoints() {
  const [data, setData] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch('http://localhost:5000/change-points')
      .then(res => res.json())
      .then(json => setData(json))
      .catch(err => setError('❌ Failed to fetch change points'));
  }, []);

  return (
    <div>
      <h2>Detected Change Points</h2>
      {error && <p>{error}</p>}
      <table border="1" cellPadding="5">
        <thead>
          <tr>
            <th>Date</th>
            <th>Index (Tau)</th>
          </tr>
        </thead>
        <tbody>
          {data.map((point, i) => (
            <tr key={i}>
              <td>{point.Date}</td>
              <td>{point.Tau_Mode}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ChangePoints;
