import React, { useState } from "react";

export default function WorkoutForm({ onSubmit }) {
  const [type, setType] = useState("sprint");
  const [metadata, setMetadata] = useState('{}');
  const [notes, setNotes] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    let meta;
    try { meta = JSON.parse(metadata); } catch {
      alert("metadata must be valid JSON")
      return;
    }
    await onSubmit({ type, metadata: meta, notes });
    setMetadata('{}');
    setNotes('');
  };

  return (
    <form onSubmit={submit}>
      <select value={type} onChange={e=>setType(e.target.value)}>
        <option value="sprint">Sprint</option>
        <option value="strength">Strength</option>
      </select><br/>
      <textarea value={metadata} onChange={e=>setMetadata(e.target.value)} rows={4} cols={50} /><br/>
      <input placeholder="notes" value={notes} onChange={e=>setNotes(e.target.value)} /><br/>
      <button type="submit">Add workout</button>
    </form>
  );
}

