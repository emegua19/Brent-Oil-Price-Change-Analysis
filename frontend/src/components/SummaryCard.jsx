import React from "react";

export default function SummaryCard({ title, value, description }) {
  return (
    <div className="card">
      <h3>{title}</h3>
      <p>{value}</p>
      <small>{description}</small>
    </div>
  );
}
