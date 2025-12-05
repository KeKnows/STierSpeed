import React, { useState } from "react";
import { signup } from "../api";

export default function Signup({ onSwitch }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [event, setEvent] = useState("");
  const [msg, setMsg] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    try {
      await signup({ email, password, event });
      setMsg("Signup success. Please log in.");
    } catch (err) {
      setMsg(err?.response?.data?.detail || "Error signing up");
    }
  };

  return (
    <div style={{padding:20}}>
      <h2>Signup</h2>
      <form onSubmit={submit}>
        <input placeholder="email" value={email} onChange={e=>setEmail(e.target.value)} /><br/>
        <input placeholder="password" type="password" value={password} onChange={e=>setPassword(e.target.value)} /><br/>
        <input placeholder="event (e.g., 100m)" value={event} onChange={e=>setEvent(e.target.value)} /><br/>
        <button type="submit">Sign up</button>
      </form>
      <div>{msg}</div>
      <button onClick={onSwitch}>Go to login</button>
    </div>
  );
}

