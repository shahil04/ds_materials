import React, { useEffect, useState } from "react";
import api from "../services/api";

export default function Interview() {
  const [question, setQuestion] = useState("Waiting for interviewer...");
  const [count, setCount] = useState(0);

  const askQuestion = async () => {
    try {
      setQuestion("Interviewer is asking...");

      const res = await api.get("/interview/next");

      if (res.data.done) {
        setQuestion("Interview Completed 🎉");
        return;
      }

      // Delay to simulate human interviewer
      setTimeout(() => {
        setQuestion(res.data.text);
        setCount((c) => c + 1);

        // Speak question (after user click = allowed)
        const utterance = new SpeechSynthesisUtterance(res.data.text);
        speechSynthesis.speak(utterance);

      }, 1200);

    } catch (err) {
      console.error(err);
      setQuestion("Error connecting to interviewer");
    }
  };

  // Ask first question AFTER component mounts
  useEffect(() => {
    askQuestion();
  }, []);

 return (
  <div style={{ padding: "30px", maxWidth: "900px" }}>
    <h2>AI Interview</h2>

    <div style={{ display: "flex", gap: "20px", marginTop: "20px" }}>

      {/* AI Interviewer */}
      <div style={{ flex: 1 }}>
        <h4>AI Interviewer</h4>

        <div
          style={{
            height: "200px",
            background: "#000",
            color: "#fff",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            borderRadius: "10px",
            fontSize: "20px"
          }}
        >
          🎤 Interviewer
        </div>

        <p style={{ marginTop: "10px", fontSize: "18px" }}>
          {question}
        </p>
      </div>

      {/* Candidate */}
      <div style={{ flex: 1 }}>
        <h4>You</h4>

        <video
          autoPlay
          muted
          style={{
            width: "100%",
            height: "200px",
            background: "#333",
            borderRadius: "10px"
          }}
          ref={(video) => {
            if (video && navigator.mediaDevices) {
              navigator.mediaDevices
                .getUserMedia({ video: true })
                .then((stream) => {
                  video.srcObject = stream;
                });
            }
          }}
        />
      </div>

    </div>

    <br />

    {count < 8 && (
      <button onClick={askQuestion} style={{ padding: "10px 20px" }}>
        Next Question
      </button>
    )}
  </div>
);

}

setTimeout(() => {
  console.log("QUESTION FROM API:", res.data.text);

  setQuestion(res.data.text);
  setCount((c) => c + 1);

  speechSynthesis.speak(
    new SpeechSynthesisUtterance(res.data.text)
  );
}, 1200);




// import React, { useEffect, useState } from "react";
// import api from "../services/api";

// export default function Interview() {
//   const [question, setQuestion] = useState("Waiting for interviewer...");
//   const [loading, setLoading] = useState(false);
//   const [count, setCount] = useState(0);

//   const next = async () => {
//   try {
//     setLoading(true);

//     const res = await api.get("/interview/next");

//     if (res.data.done) {
//       setQuestion("Interview Completed 🎉");
//       return;
//     }

//     setQuestion("Interviewer is asking...");

//     setTimeout(() => {
//       setQuestion(res.data.text);
//       setCount((c) => c + 1);

//       speechSynthesis.speak(
//         new SpeechSynthesisUtterance(res.data.text)
//       );
//     }, 1200);

//   } catch (err) {
//     console.error(err);
//     setQuestion("Error connecting to interviewer");
//   } finally {
//     setLoading(false);
//   }
// };

//   // Ask FIRST question automatically
//   useEffect(() => {
//     next();
//   }, []);

//   return (
//     <div style={{ padding: "30px", maxWidth: "700px" }}>
//       <h2>AI Interview</h2>

//       <div
//         style={{
//           border: "1px solid #ccc",
//           padding: "20px",
//           borderRadius: "10px",
//           minHeight: "120px",
//           background: "#f9f9f9",
//           fontSize: "18px"
//         }}
//       >
//         {loading ? "Interviewer is thinking..." : question}
//       </div>

//       <br />

//       {count < 8 && (
//         <button onClick={next} style={{ padding: "10px 20px" }}>
//           Next Question
//         </button>
//       )}
//     </div>
//   );
// }


// import React, { useEffect, useRef, useState } from "react";

// import api from "../services/api";

// export default function Interview() {
//   const [question, setQuestion] = useState("");

//   const next = async () => {
//     const res = await api.get("/interview/next");
//     setQuestion(res.data.done ? "Interview Completed" : res.data.text);
//   };

//   useEffect(() => { next(); }, []);

//   return (
//     <div>
//       <h2>Interview</h2>
//       <p>{question}</p>
//       <button onClick={next}>Next</button>
//     </div>
//   );
// }
