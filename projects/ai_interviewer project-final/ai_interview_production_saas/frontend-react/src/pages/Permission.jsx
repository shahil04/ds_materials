import React, { useEffect, useRef, useState } from "react";

export default function Permission({ onStart }) {
  const videoRef = useRef(null);
  const [status, setStatus] = useState("Checking permissions...");

  useEffect(() => {
    navigator.mediaDevices.getUserMedia({ video: true, audio: true })
      .then(stream => {
        videoRef.current.srcObject = stream;
        setStatus("Camera & Mic Ready");
      })
      .catch(() => setStatus("Permission Denied"));
  }, []);

  return (
    <div>
      <h2>Permission Check</h2>
      <video ref={videoRef} autoPlay muted width="320"/>
      <p>{status}</p>
      <button onClick={onStart}>Start Interview</button>
    </div>
  );
}
