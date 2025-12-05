import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8080";

export function setAuthToken(token) {
  axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
}

export async function signup(payload) {
  return axios.post(`${API_BASE}/signup`, payload);
}

export async function login(payload) {
  return axios.post(`${API_BASE}/login`, payload);
}

export async function createWorkout(payload) {
  return axios.post(`${API_BASE}/workouts`, payload);
}

export async function listWorkouts() {
  return axios.get(`${API_BASE}/workouts`);
}

export async function getWeeklySummary() {
  return axios.get(`${API_BASE}/ai/weekly-summary`);
}

