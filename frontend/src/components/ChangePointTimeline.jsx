import React, { useEffect, useState } from "react";
import { fetchChangePoints } from "../api";

export default function ChangePointTimeline() {
  const [points, setPoints] = useState([]);

  useEffect(() => {
    fetchChangePoints().then(res => setPoints(res.data)).catch(console.error);
  }, []);

  return (
    <div>
      <h2>🔻 Detected Change Points</h2>
      <ul>
        {points.map((point, i) => (
          <li key={i}>
            <strong>{point.Date}</strong> (tau = {point.Tau_Mode})
          </li>
        ))}
      </ul>
    </div>
  );
}
