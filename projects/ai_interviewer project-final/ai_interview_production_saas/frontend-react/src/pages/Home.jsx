import { Link } from 'react-router-dom';

export default function Home() {
    return (
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
            <section style={{ textAlign: 'center', padding: '4rem 0' }}>
                <h1 style={{ fontSize: '3.5rem', marginBottom: '1rem' }}>
                    Master Your Next <span className="gradient-text">Interview</span>
                </h1>
                <p style={{ fontSize: '1.2rem', color: 'var(--text-secondary)', marginBottom: '2rem', maxWidth: '600px', margin: '0 auto 2rem auto' }}>
                    AI-powered mock interviews, resume analysis, and real-time feedback to help you land your dream job.
                </p>
                <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
                    {localStorage.getItem('token') ? (
                        <>
                            <Link to="/resume-analyzer" className="btn-primary" style={{ textDecoration: 'none' }}>Analyze Resume</Link>
                            <Link to="/interview" className="glass-panel" style={{ color: 'white', padding: '0.75rem 1.5rem', cursor: 'pointer', background: 'transparent', textDecoration: 'none' }}>
                                Take Mock Interview
                            </Link>
                        </>
                    ) : (
                        <Link to="/register" className="btn-primary" style={{ textDecoration: 'none', padding: '0.75rem 2rem', fontSize: '1.1rem' }}>
                            Register to Start
                        </Link>
                    )}
                </div>
            </section>

            <section style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem', marginTop: '4rem' }}>
                <div className="glass-panel" style={{ padding: '2rem' }}>
                    <h3 className="gradient-text">AI Resume Screening</h3>
                    <p style={{ color: 'var(--text-secondary)' }}>Get instant feedback on your resume with ATS scoring and improvement tips.</p>
                </div>
                <div className="glass-panel" style={{ padding: '2rem' }}>
                    <h3 className="gradient-text">Mock Interviews</h3>
                    <p style={{ color: 'var(--text-secondary)' }}>Practice with our AI interviewer that adapts to your responses and job role.</p>
                </div>
                <div className="glass-panel" style={{ padding: '2rem' }}>
                    <h3 className="gradient-text">Detailed Analytics</h3>
                    <p style={{ color: 'var(--text-secondary)' }}>Track your progress and identify weak areas to focus your preparation.</p>
                </div>
            </section>
        </div>
    );
}
