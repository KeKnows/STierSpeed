import React, { useEffect, useState } from "react";
import { setAuthToken, listWorkouts, createWorkout, getWeeklySummary } from "../api";
import WorkoutForm from "./WorkoutForm";
import WeeklyChart from "../components/WeeklyChart";

export default function Dashboard({ token }) {
  setAuthToken(token);
  const [workouts, setWorkouts] = useState([]);
  const [summary, setSummary] = useState("");

  async function refresh() {
    const r = await listWorkouts();
    setWorkouts(r.data);
  }

  async function submitWorkout(payload) {
    await createWorkout(payload);
    await refresh();
  }

  async function loadSummary() {
    const r = await getWeeklySummary();
    setSummary(r.data.summary);
  }

  useEffect(()=>{ refresh(); loadSummary(); }, []);

  return (
    <div style={{padding:20}}>
      <h2>Dashboard</h2>
      <WorkoutForm onSubmit={submitWorkout} />
      <h3>Workouts</h3>
      <ul>
        {workouts.map(w => <li key={w.id}>{w.type} — {JSON.stringify(w.metadata)}</li>)}
      </ul>
      <h3>Weekly AI Summary</h3>
      <pre>{summary}</pre>
      <h3>Weekly Chart</h3>
      <WeeklyChart workouts={workouts} />
    </div>
  );
}

