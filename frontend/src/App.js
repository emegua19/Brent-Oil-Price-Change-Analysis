import React, { useEffect, useState } from 'react';
import './App.css';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ReferenceLine, ResponsiveContainer, Brush } from 'recharts';
import { parseISO, isAfter, isBefore } from 'date-fns';

function App() {
  const [logReturns, setLogReturns] = useState([]);
  const [changePoints, setChangePoints] = useState([]);
  const [events, setEvents] = useState([]);
  const [apiStatus, setApiStatus] = useState('Checking...');
  const [showEvents, setShowEvents] = useState(true);
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [searchKeyword, setSearchKeyword] = useState('');

  useEffect(() => {
    fetch('http://localhost:5000/')
      .then((res) => res.ok ? setApiStatus("✅ API is running") : setApiStatus("❌ API error"))
      .catch(() => setApiStatus("❌ API error"));

    fetch('http://localhost:5000/log-returns')
      .then(res => res.json())
      .then(data => setLogReturns(data));

    fetch('http://localhost:5000/change-points')
      .then(res => res.json())
      .then(data => setChangePoints(data));

    fetch('http://localhost:5000/matched-events')
      .then(res => res.json())
      .then(data => setEvents(data));
  }, []);

  const filteredLogReturns = logReturns.filter(d => {
    const date = parseISO(d.Date);
    return (!startDate || isAfter(date, startDate)) && (!endDate || isBefore(date, endDate));
  });

  const filteredEvents = events.filter(e =>
    e.Event_Description.toLowerCase().includes(searchKeyword.toLowerCase())
  );

  const logValues = filteredLogReturns.map(d => d.LogReturn);
  const mean = logValues.reduce((a, b) => a + b, 0) / logValues.length || 0;
  const std = Math.sqrt(logValues.map(x => Math.pow(x - mean, 2)).reduce((a, b) => a + b, 0) / logValues.length) || 0;
  const volatility = std * Math.sqrt(252);

  return (
    <div className="App" style={{ fontFamily: 'Arial, sans-serif', padding: '20px' }}>
      <h1 style={{ textAlign: 'center', color: '#222' }}> Brent Oil Change Point Dashboard</h1>

      <section style={sectionStyle}>
        <h3>🚦 Flask API Status: <span>{apiStatus}</span></h3>
      </section>

      <section style={sectionStyle}>
        <h3> Date Range Filter</h3>
        <div style={rowStyle}>
          <div>
            <label>Start Date: </label>
            <DatePicker selected={startDate} onChange={(date) => setStartDate(date)} />
          </div>
          <div>
            <label>End Date: </label>
            <DatePicker selected={endDate} onChange={(date) => setEndDate(date)} />
          </div>
        </div>
      </section>

      <section style={sectionStyle}>
        <h3> Summary Metrics (Filtered Range)</h3>
        <ul style={listStyle}>
          <li><b>Mean:</b> {mean.toFixed(5)}</li>
          <li><b>Standard Deviation:</b> {std.toFixed(5)}</li>
          <li><b>Volatility:</b> {volatility.toFixed(5)}</li>
        </ul>
      </section>

      <section style={sectionStyle}>
        <h3> Log Return Chart with Change Points</h3>
        <div style={{ width: '100%', height: 400 }}>
          <ResponsiveContainer>
            <LineChart data={filteredLogReturns}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="Date" minTickGap={50} />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="LogReturn" stroke="#007bff" dot={false} strokeWidth={1.5} />
              <Brush dataKey="Date" height={30} stroke="#007bff" />
              {changePoints.map((cp, index) => (
                <ReferenceLine key={index} x={cp.Date} stroke="red" strokeDasharray="3 3" label={`CP ${index + 1}`} />
              ))}
              {showEvents && filteredEvents.map((e, idx) => (
                <ReferenceLine
                  key={`event-${idx}`}
                  x={e.Event_Date}
                  stroke="green"
                  strokeDasharray="2 2"
                  label={{ value: `Event ${idx + 1}`, position: 'top', fontSize: 10 }}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>
      </section>

      <section style={sectionStyle}>
        <div style={rowStyle}>
          <label>
            <input
              type="checkbox"
              checked={showEvents}
              onChange={() => setShowEvents(!showEvents)}
              style={{ marginRight: 8 }}
            />
            Show Matched Events
          </label>
          <input
            type="text"
            placeholder="🔍 Filter Events (e.g., OPEC)"
            value={searchKeyword}
            onChange={(e) => setSearchKeyword(e.target.value)}
            style={{ padding: 5, minWidth: 250, borderRadius: 5, border: '1px solid #ccc' }}
          />
        </div>

        {showEvents && (
          <table style={tableStyle}>
            <thead>
              <tr>
                <th>Change Point</th>
                <th>Event</th>
                <th>Event Date</th>
                <th>Impact (%)</th>
              </tr>
            </thead>
            <tbody>
              {filteredEvents.map((e, idx) => (
                <tr key={idx}>
                  <td>{e.Change_Point_Date}</td>
                  <td>{e.Event_Description}</td>
                  <td>{e.Event_Date}</td>
                  <td>{e.Impact_Percent ? e.Impact_Percent.toFixed(2) : 'N/A'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      <section style={sectionStyle}>
        <h3> All Change Points</h3>
        <table style={tableStyle}>
          <thead>
            <tr>
              <th>Date</th>
              <th>Index (Tau)</th>
            </tr>
          </thead>
          <tbody>
            {changePoints.map((cp, idx) => (
              <tr key={idx}>
                <td>{cp.Date}</td>
                <td>{cp.Tau_Mode}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}

const sectionStyle = {
  backgroundColor: '#f9f9f9',
  padding: '20px',
  margin: '30px auto',
  borderRadius: '10px',
  boxShadow: '0 0 5px rgba(0,0,0,0.1)',
  maxWidth: '1000px'
};

const rowStyle = {
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  flexWrap: 'wrap',
  gap: '10px'
};

const listStyle = {
  listStyle: 'none',
  fontSize: '16px',
  paddingLeft: '0'
};

const tableStyle = {
  width: '100%',
  marginTop: '20px',
  borderCollapse: 'collapse',
  textAlign: 'left'
};

export default App;
