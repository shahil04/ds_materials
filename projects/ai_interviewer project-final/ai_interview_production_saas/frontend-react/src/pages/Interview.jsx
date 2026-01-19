import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

export default function Interview() {
  const [question, setQuestion] = useState(null);
  const [started, setStarted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [finished, setFinished] = useState(false);
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  useEffect(() => {
    if (videoRef.current && streamRef.current) {
      videoRef.current.srcObject = streamRef.current;
    }
  }, [started]);

  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (err) {
      console.error("Error accessing media devices:", err);
      alert("Could not access camera/microphone. Please check permissions.");
    }
  };

  const fetchNextQuestion = async () => {
    setLoading(true);
    try {
      const response = await axios.get('http://localhost:8000/api/interview/next');
      if (response.data.done) {
        setFinished(true);
        setQuestion(null);
        if (streamRef.current) {
          streamRef.current.getTracks().forEach(track => track.stop());
        }
      } else {
        setQuestion(response.data.text);
      }
    } catch (err) {
      console.error(err);
      alert('Error connecting to interview server');
    } finally {
      setLoading(false);
    }
  };

  const startInterview = async () => {
    await startCamera();
    setStarted(true);
    fetchNextQuestion();
  };

  if (finished) {
    return (
      <div style={{ textAlign: 'center', padding: '4rem' }}>
        <h2 className="gradient-text">Interview Completed!</h2>
        <p style={{ color: 'var(--text-secondary)' }}>Great job. You have answered all the questions.</p>
        <Link to="/" className="btn-primary" style={{ textDecoration: 'none', display: 'inline-block', marginTop: '2rem' }}>Return Home</Link>
      </div>
    )
  }

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '2rem' }}>
      {!started ? (
        <div className="glass-panel" style={{ padding: '3rem', textAlign: 'center', maxWidth: '800px', margin: '0 auto' }}>
          <h1 className="gradient-text" style={{ marginBottom: '1rem' }}>Ready for your Interview?</h1>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
            Our AI interviewer will ask you a series of questions.
            We need access to your <span style={{ color: '#fff' }}>Camera</span> and <span style={{ color: '#fff' }}>Microphone</span>.
          </p>
          <div style={{ width: '100%', maxWidth: '500px', height: '300px', background: '#000', margin: '0 auto 2rem auto', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden', position: 'relative' }}>
            <video ref={videoRef} autoPlay muted playsInline style={{ width: '100%', height: '100%', objectFit: 'cover' }}></video>
            {!started && <span style={{ position: 'absolute', color: '#666' }}>Camera Preview will start here</span>}
          </div>
          <button onClick={startInterview} className="btn-primary" style={{ fontSize: '1.2rem' }}>
            Start Interview & Enable Camera
          </button>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'minmax(300px, 1fr) 2fr', gap: '2rem', height: '80vh' }}>
          {/* Left Panel: Camera */}
          <div className="glass-panel" style={{ padding: '1rem', display: 'flex', flexDirection: 'column', position: 'relative' }}>
            <video ref={videoRef} autoPlay muted playsInline style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: '8px', background: '#000' }}></video>
            <div style={{ position: 'absolute', bottom: '20px', left: '20px', background: 'rgba(0,0,0,0.6)', padding: '0.25rem 0.75rem', borderRadius: '4px', fontSize: '0.9rem' }}>
              You
            </div>
          </div>

          {/* Right Panel: AI Interviewer */}
          <div className="glass-panel" style={{ padding: '3rem', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', textAlign: 'center' }}>
            {loading ? (
              <p>Thinking...</p>
            ) : (
              <>
                <div style={{ marginBottom: 'auto', width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                  <div style={{ width: '150px', height: '150px', borderRadius: '50%', overflow: 'hidden', border: '3px solid var(--primary-color)', marginBottom: '1.5rem', boxShadow: '0 0 20px rgba(99, 102, 241, 0.3)' }}>
                    <img
                      src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=800&q=80"
                      alt="AI Interviewer"
                      style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                    />
                  </div>
                  <h4 style={{ color: 'var(--text-secondary)', marginBottom: '1rem', textTransform: 'uppercase', letterSpacing: '2px', fontSize: '0.9rem' }}>AI Interviewer</h4>
                  <h2 style={{ fontSize: '2.5rem', marginBottom: '3rem', lineHeight: '1.3' }}>{question}</h2>
                </div>

                <div style={{ marginTop: 'auto', display: 'flex', flexDirection: 'column', gap: '1rem', width: '100%', maxWidth: '400px' }}>
                  <div style={{ display: 'flex', justifyContent: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
                    <div style={{ width: '10px', height: '10px', background: 'red', borderRadius: '50%', animation: 'pulse 1s infinite' }}></div>
                    <span style={{ color: 'red', fontSize: '0.9rem' }}>Microphone Active</span>
                  </div>

                  <div style={{ display: 'flex', gap: '1rem' }}>
                    <button className="glass-panel" style={{ flex: 1, background: 'rgba(239, 68, 68, 0.1)', color: '#fca5a5', border: '1px solid rgba(239, 68, 68, 0.3)', padding: '1rem' }}>
                      End Interview
                    </button>
                    <button onClick={fetchNextQuestion} className="btn-primary" style={{ flex: 1 }}>
                      Next Question
                    </button>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
