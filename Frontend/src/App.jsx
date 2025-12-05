import React, { useState } from "react";
import Signup from "./pages/Signup";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";

export default function App() {
  const [page, setPage] = useState("login");
  const [token, setToken] = useState(null);

  if (!token) {
    return page === "signup" ? <Signup onSwitch={() => setPage("login")} /> : <Login onLogin={(t)=>{setToken(t); localStorage.setItem("token", t)}} onSwitch={() => setPage("signup")} />;
  }
  return <Dashboard token={token} />;
}

