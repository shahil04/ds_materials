import { useState } from 'react';
import axios from 'axios';

export default function ResumeAnalyzer() {
    const [file, setFile] = useState(null);
    const [jobRole, setJobRole] = useState('');
    const [jobDescription, setJobDescription] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);

    const handleUpload = async () => {
        if (!file) return;

        setLoading(true);
        const formData = new FormData();
        formData.append('file', file);
        formData.append('job_role', jobRole);
        formData.append('job_description', jobDescription);

        try {
            const response = await axios.post('http://localhost:8000/api/resume/analyze-resume', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            setResult(response.data);
        } catch (err) {
            console.error(err);
            alert('Error analyzing resume');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
            <h1 className="gradient-text" style={{ textAlign: 'center', marginBottom: '2rem' }}>AI Resume Analyzer</h1>

            <div className="glass-panel" style={{ padding: '3rem', textAlign: 'center', marginBottom: '2rem' }}>
                <div style={{ marginBottom: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem', maxWidth: '600px', margin: '0 auto' }}>

                    <input
                        type="file"
                        accept=".pdf"
                        onChange={(e) => setFile(e.target.files[0])}
                        style={{ margin: '0 auto' }}
                    />

                    <input
                        type="text"
                        placeholder="Target Job Role (e.g., Data Scientist)"
                        value={jobRole}
                        onChange={(e) => setJobRole(e.target.value)}
                        style={{ padding: '0.8rem', borderRadius: '8px', border: '1px solid #444', background: '#222', color: '#fff' }}
                    />

                    <textarea
                        placeholder="Paste Job Description here for ATS Score & Analysis..."
                        value={jobDescription}
                        onChange={(e) => setJobDescription(e.target.value)}
                        rows={6}
                        style={{ padding: '0.8rem', borderRadius: '8px', border: '1px solid #444', background: '#222', color: '#fff', resize: 'vertical' }}
                    />

                </div>

                <button
                    onClick={handleUpload}
                    className="btn-primary"
                    disabled={loading || !file}
                >
                    {loading ? 'Analyzing...' : 'Analyze Resume'}
                </button>
            </div>

            {result && (
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>

                    {/* Score Panel */}
                    <div className="glass-panel" style={{ padding: '1.5rem', textAlign: 'center' }}>
                        <h3>{result.job_description_snippet ? "JD Match Score" : "Resume Score"}</h3>
                        <div style={{
                            width: '120px', height: '120px', borderRadius: '50%',
                            border: `8px solid ${result.ats_score > 70 ? '#4caf50' : result.ats_score > 50 ? '#ff9800' : '#f44336'}`,
                            display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto'
                        }}>
                            <span className="gradient-text" style={{ fontSize: '2.5rem', fontWeight: 'bold' }}>{result.ats_score}%</span>
                        </div>
                        {result.hiring_recommendation && (
                            <div style={{ marginTop: '1rem', fontWeight: 'bold', color: '#ccc' }}>
                                Recommendation: <span style={{ color: '#fff' }}>{result.hiring_recommendation}</span>
                            </div>
                        )}
                    </div>

                    {/* Missing Keywords Panel (Only if JD provided) */}
                    {result.missing_keywords && result.missing_keywords.length > 0 && (
                        <div className="glass-panel" style={{ padding: '1.5rem' }}>
                            <h3 style={{ color: '#ff9830' }}>Missing Keywords</h3>
                            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                                {result.missing_keywords.map(k => (
                                    <span key={k} style={{ background: '#333', border: '1px solid #555', padding: '0.25rem 0.75rem', borderRadius: '15px', fontSize: '0.85rem' }}>{k}</span>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Main Analysis Text */}
                    <div className="glass-panel" style={{ padding: '1.5rem', gridColumn: '1 / -1' }}>
                        <h3>{result.job_description_snippet ? "Detailed Analysis" : "Career Suggestions"}</h3>
                        <p style={{ whiteSpace: 'pre-wrap', color: 'var(--text-secondary)' }}>{result.ai_analysis}</p>
                    </div>

                    {/* Skills Found Panel */}
                    <div className="glass-panel" style={{ padding: '1.5rem', gridColumn: '1 / -1' }}>
                        <h4>Resume Skills Detected</h4>
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                            {result.skills.map(s => (
                                <span key={s} style={{ background: 'var(--primary-color)', padding: '0.25rem 0.75rem', borderRadius: '15px', fontSize: '0.9rem' }}>{s}</span>
                            ))}
                        </div>
                    </div>

                    {/* NEW: Strengths & Weaknesses */}
                    {(result.strengths?.length > 0 || result.weaknesses?.length > 0) && (
                        <div className="glass-panel" style={{ padding: '1.5rem', gridColumn: '1 / -1', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
                            <div>
                                <h4 style={{ color: '#4caf50' }}>💪 Strengths</h4>
                                <ul style={{ paddingLeft: '1.2rem', color: '#ccc' }}>
                                    {result.strengths.map((item, i) => <li key={i}>{item}</li>)}
                                </ul>
                            </div>
                            <div>
                                <h4 style={{ color: '#f44336' }}>⚠️ Improvements Needed</h4>
                                <ul style={{ paddingLeft: '1.2rem', color: '#ccc' }}>
                                    {result.weaknesses.map((item, i) => <li key={i}>{item}</li>)}
                                </ul>
                            </div>
                        </div>
                    )}

                    {/* NEW: Interview Questions */}
                    {result.interview_questions?.length > 0 && (
                        <div className="glass-panel" style={{ padding: '1.5rem', gridColumn: '1 / -1' }}>
                            <h3>🎤 Recommended Interview Questions</h3>
                            <p style={{ color: '#888', marginBottom: '1rem' }}>Prepare for these questions based on your resume and the target role.</p>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
                                {result.interview_questions.map((q, i) => (
                                    <div key={i} style={{ background: 'rgba(255,255,255,0.05)', padding: '1rem', borderRadius: '8px', borderLeft: '4px solid var(--secondary-color)' }}>
                                        <strong>Q{i + 1}:</strong> {q}
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                </div>
            )}
        </div>
    );
}
