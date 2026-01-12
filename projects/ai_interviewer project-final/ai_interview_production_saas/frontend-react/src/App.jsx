import React, { useState } from "react";
import Permission from "./pages/Permission";
import Interview from "./pages/Interview";

export default function App() {
  const [start, setStart] = useState(false);

  return start ? (
    <Interview />
  ) : (
    <Permission onStart={() => setStart(true)} />
  );
}
