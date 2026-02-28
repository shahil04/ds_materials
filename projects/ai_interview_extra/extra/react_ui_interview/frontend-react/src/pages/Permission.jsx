
import { useEffect, useRef, useState } from "react";

export default function Permission({ onStart }) {
  const videoRef = useRef(null);
  const [status, setStatus] = useState("Checking permissions...");

  useEffect(() => {
    navigator.mediaDevices.getUserMedia({ video: true, audio: true })
      .then(stream => {
        videoRef.current.srcObject = stream;
        setStatus("Camera & Microphone Granted ✅");
      })
      .catch(() => {
        setStatus("Permission Denied ❌");
      });
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h2>Recording Permission</h2>
      <video ref={videoRef} autoPlay muted width="400" />
      <p>{status}</p>
      <button onClick={onStart}>Start Interview</button>
    </div>
  );
}
