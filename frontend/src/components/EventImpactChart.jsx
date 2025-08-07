import React, { useEffect, useState } from "react";
import { fetchMatchedEvents } from "../api";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function EventImpactChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchMatchedEvents().then(res => setData(res.data)).catch(console.error);
  }, []);

  return (
    <div>
      <h2>📊 Event Impact on Log Return</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <XAxis dataKey="Change_Point_Date" />
          <YAxis domain={['auto', 'auto']} />
          <Tooltip />
          <Bar dataKey="Impact_Percent" fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
