
import { useEffect, useState } from "react";
import api from "../services/api";

export default function Interview() {
  const [question, setQuestion] = useState("");
  const [count, setCount] = useState(0);

  const nextQuestion = async () => {
    const res = await api.get("/interview/next");

    if (res.data.done) {
      setQuestion("Interview Completed 🎉");
      return;
    }

    setQuestion(res.data.text);
    setCount(prev => prev + 1);
  };

  useEffect(() => {
    nextQuestion();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h2>AI Interview</h2>
      <h3>Question {count}</h3>
      <p>{question}</p>
      {count < 8 && <button onClick={nextQuestion}>Next Question</button>}
    </div>
  );
}
