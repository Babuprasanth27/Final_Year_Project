import { useState } from "react";
import { manualDetect } from "../services/api";

function ManualDetect() {
  const [form, setForm] = useState({
    src_ip: "",
    dst_ip: "",
    protocol: 17,
    flow_duration: 0,
    total_forward_packets: 0,
    total_backward_packets: 0,
    total_forward_packets_length: 0,
    total_backward_packets_length: 0,
    flow_packets_per_seconds: 0,
    flow_bytes_per_seconds: 0,
  });

  const handleChange = e =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async () => {
    const res = await manualDetect(form);
    alert(`Attack: ${res.data.prediction} | Severity: ${res.data.severity}`);
  };

  return (
    <div className="panel">
      <h2>Manual Traffic Analysis</h2>

      {Object.keys(form).map(key => (
        <input
          key={key}
          name={key}
          placeholder={key.replaceAll("_", " ")}
          onChange={handleChange}
        />
      ))}

      <button onClick={handleSubmit}>Run Detection</button>
    </div>
  );
}

export default ManualDetect;
