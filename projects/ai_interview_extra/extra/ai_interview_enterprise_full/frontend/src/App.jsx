
import { useState } from "react";
import Permission from "./pages/Permission";
import Interview from "./pages/Interview";

function App() {
  const [started, setStarted] = useState(false);

  return (
    <>
      {!started ? (
        <Permission onStart={() => setStarted(true)} />
      ) : (
        <Interview />
      )}
    </>
  );
}

export default App;
