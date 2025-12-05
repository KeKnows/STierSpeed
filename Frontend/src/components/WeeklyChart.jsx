import React from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";

export default function WeeklyChart({ workouts }) {
  // Basic example: if sprint workouts provide time_s in metadata, plot avg per day
  const grouped = {};
  workouts.forEach(w => {
    const d = new Date(w.created_at).toISOString().slice(0,10);
    grouped[d] = grouped[d] || { date: d, sprint_times: []};
    if (w.type === 'sprint' && w.metadata && w.metadata.time_s) {
      grouped[d].sprint_times.push(w.metadata.time_s);
    }
  });
  const data = Object.values(grouped).map(g => ({ date: g.date, avg: g.sprint_times.length ? (g.sprint_times.reduce((a,b)=>a+b,0)/g.sprint_times.length) : null })).sort((a,b)=>a.date.localeCompare(b.date));
  return (
    <div style={{width: '100%', height: 300}}>
      <ResponsiveContainer>
        <LineChart data={data}>
          <CartesianGrid />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="avg" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

