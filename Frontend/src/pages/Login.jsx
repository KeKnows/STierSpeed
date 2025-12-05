import React, { useState } from "react";
import { login } from "../api";

export default function Login({ onSwitch, onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    try {
      const r = await login({ email, password });
      const token = r.data.access_token;
      onLogin(token);
    } catch (err) {
      setMsg(err?.response?.data?.detail || "Login failed");
    }
  };

  return (
    <div style={{padding:20}}>
      <h2>Login</h2>
      <form onSubmit={submit}>
        <input placeholder="email" value={email} onChange={e=>setEmail(e.target.value)} /><br/>
        <input placeholder="password" type="password" value={password} onChange={e=>setPassword(e.target.value)} /><br/>
        <button type="submit">Login</button>
      </form>
      <div>{msg}</div>
      <button onClick={onSwitch}>Sign up</button>
    </div>
  );
}

