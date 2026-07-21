'use client';

import { useEffect, useRef, useState } from 'react';
import './globals.css';

const API = '';

const TABS = [
  { id: 'ingest', label: 'Pipeline Visualizer', icon: '>' },
  { id: 'chat', label: 'Query & Retrieval', icon: '?' },
  { id: 'dashboard', label: 'Dashboard', icon: '~' },
  { id: 'graph', label: 'Knowledge Graph', icon: 'o' },
];

export default function Home() {
  const [tab, setTab] = useState('ingest');
  const [health, setHealth] = useState(null);

  useEffect(() => {
    fetch(`${API}/health`).then(r => r.json()).then(setHealth).catch(() => setHealth(null));
  }, []);

  return (
    <div className="layout">
      <aside className="sidebar">
        <h1>AXIOM <span>GraphRAG Pipeline Visualizer</span></h1>
        <div className="nav-section">Pipeline</div>
        {TABS.map(t => (
          <div key={t.id} className={`nav-item ${tab === t.id ? 'active' : ''}`} onClick={() => setTab(t.id)}>
            <span style={{ fontFamily: 'monospace', width: 16 }}>{t.icon}</span> {t.label}
          </div>
        ))}
        <div className="nav-section" style={{ marginTop: 'auto', paddingTop: 24 }}>System</div>
        <div className="nav-item" style={{ color: health ? 'var(--green)' : 'var(--red)' }}>
          <span style={{ fontFamily: 'monospace', width: 16 }}>●</span>
          Backend: {health ? 'Connected' : 'Offline'}
        </div>
      </aside>
      <main className="main">
        <div className="header">
          <h2>{TABS.find(t => t.id === tab)?.label}</h2>
          <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>AXIOM v1.0</span>
        </div>
        <div className="content">
          {tab === 'ingest' && <PipelineVisualizerTab />}
          {tab === 'chat' && <QueryVisualizerTab />}
          {tab === 'dashboard' && <DashboardTab />}
          {tab === 'graph' && <GraphTab />}
        </div>
      </main>
    </div>
  );
}

function PipelineVisualizerTab() {
  const [steps, setSteps] = useState([]);
  const [isRunning, setIsRunning] = useState(false);
  const [completed, setCompleted] = useState(null);
  const fileRef = useRef(null);

  const upload = async file => {
    setIsRunning(true);
    setSteps([]);
    setCompleted(null);

    const fd = new FormData();
    fd.append('file', file);

    try {
      const response = await fetch(`${API}/api/v1/ingest/document/stream`, { method: 'POST', body: fd });
      await readEvents(response, event => {
        if (event.type === 'step') {
          setSteps(prev => {
            const index = prev.findIndex(s => s.step === event.data.step);
            if (index < 0) return [...prev, event.data];
            const copy = [...prev];
            copy[index] = event.data;
            return copy;
          });
        }
        if (event.type === 'complete') setCompleted(event.data);
      });
    } catch (error) {
      setSteps([{ step: 0, name: 'Error', status: 'error', description: error.message }]);
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="pipeline-layout">
      <div className="upload-section">
        <div className="upload-zone" onClick={() => !isRunning && fileRef.current?.click()}>
          <input
            type="file"
            ref={fileRef}
            accept=".pdf,.docx,.doc,.png,.jpg,.jpeg,.tiff,.txt,.json,.csv"
            onChange={e => e.target.files?.[0] && upload(e.target.files[0])}
          />
          {isRunning ? <><span className="spinner" /><div style={{ marginTop: 8 }}>Processing...</div></> : <><div style={{ fontSize: 28 }}>+</div><div>Upload a document</div><div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 4 }}>PDF, DOCX, TXT, images</div></>}
        </div>
      </div>

      <div className="pipeline-container">
        {steps.map(step => <StepCard key={step.step} step={step} />)}
        {completed && (
          <div className="completion-card">
            <div className="completion-header">Pipeline Complete</div>
            <div className="completion-grid">
              <Stat label="Pages" value={completed.total_pages} />
              <Stat label="Chunks" value={completed.total_chunks} />
              <Stat label="Entities" value={completed.total_entities} />
              <Stat label="Relationships" value={completed.total_relationships} />
              <Stat label="Time" value={`${completed.total_duration_ms}ms`} />
              <Stat label="Category" value={completed.category} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function QueryVisualizerTab() {
  const [question, setQuestion] = useState('');
  const [steps, setSteps] = useState([]);
  const [result, setResult] = useState(null);
  const [isRunning, setIsRunning] = useState(false);

  const ask = async () => {
    if (!question.trim() || isRunning) return;
    setIsRunning(true);
    setSteps([]);
    setResult(null);

    try {
      const response = await fetch(`${API}/api/v1/query/ask/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, top_k: 5 }),
      });
      await readEvents(response, event => {
        if (event.type === 'step') setSteps(prev => [...prev.filter(s => s.step !== event.data.step), event.data].sort((a, b) => a.step - b.step));
        if (event.type === 'complete') setResult(event.data);
      });
    } catch (error) {
      setSteps([{ step: 0, name: 'Error', status: 'error', description: error.message }]);
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="query-layout">
      <div className="query-input-section">
        <div className="query-input-row">
          <input value={question} onChange={e => setQuestion(e.target.value)} onKeyDown={e => e.key === 'Enter' && ask()} placeholder="Ask a question..." disabled={isRunning} />
          <button onClick={ask} disabled={isRunning}>{isRunning ? <span className="spinner" /> : 'Ask'}</button>
        </div>
        <div className="query-suggestions">
          {['What maintenance is required for P-101A?', 'Show me recent incidents', 'What does OISD-154 require?'].map(q => (
            <span key={q} className="suggestion" onClick={() => setQuestion(q)}>{q}</span>
          ))}
        </div>
      </div>
      <div className="query-steps-container">
        {steps.map(step => <StepCard key={step.step} step={step} />)}
        {result && (
          <div className="answer-card">
            <div className="answer-header">
              <span>Answer</span>
              <span className={`badge ${result.confidence}`}>{result.confidence} confidence</span>
              <span className="answer-time">{result.total_duration_ms}ms total</span>
            </div>
            <div className="answer-body">{result.answer}</div>
          </div>
        )}
      </div>
    </div>
  );
}

function DashboardTab() {
  const [stats, setStats] = useState(null);
  const load = () => fetch(`${API}/api/v1/graph/stats`).then(r => r.json()).then(setStats).catch(() => setStats(null));
  useEffect(() => { load(); }, []);

  return (
    <>
      <div className="card-grid">
        <div className="card"><h3>FAISS Vector Index</h3><div className="value">{stats?.faiss_total_chunks ?? '--'}</div><div className="sub">chunks indexed</div></div>
        <div className="card"><h3>Documents</h3><div className="value">{stats?.faiss_total_files ?? '--'}</div><div className="sub">files indexed</div></div>
        <div className="card"><h3>Neo4j Graph</h3><div className="value">{stats?.neo4j_connected ? stats.total_nodes : 'Offline'}</div><div className="sub">{stats?.neo4j_connected ? `${stats.total_relationships} relationships` : 'Neo4j unavailable'}</div></div>
        <div className="card"><h3>LLM Provider</h3><div className="value" style={{ fontSize: 22 }}>Groq</div><div className="sub">configured in backend env</div></div>
      </div>
      <button onClick={load} style={{ padding: '8px 20px', background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 8, color: 'var(--text)', cursor: 'pointer' }}>Refresh Stats</button>
    </>
  );
}

function GraphTab() {
  const [searchTerm, setSearchTerm] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const search = async () => {
    if (!searchTerm.trim()) return;
    setLoading(true);
    try {
      const response = await fetch(`${API}/api/v1/graph/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: searchTerm, limit: 20 }),
      });
      setResults(await response.json());
    } catch (error) {
      setResults({ error: error.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
        <input value={searchTerm} onChange={e => setSearchTerm(e.target.value)} onKeyDown={e => e.key === 'Enter' && search()} placeholder="Search graph and indexed documents..." style={{ flex: 1, padding: '10px 16px', background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 8, color: 'var(--text)' }} />
        <button onClick={search} disabled={loading} style={{ padding: '10px 20px', background: 'var(--primary)', color: 'white', border: 'none', borderRadius: 8 }}>{loading ? '...' : 'Search'}</button>
      </div>
      {results?.error && <div className="card" style={{ color: 'var(--red)' }}>{results.error}</div>}
      {results?.results && (
        <div className="card">
          <h3>Search Results ({results.total || 0})</h3>
          {results.results.map((r, i) => (
            <div key={i} className="chunk-item" style={{ marginTop: 8 }}>
              <div className="chunk-header"><span className="chunk-id">{r.props?.filename || r.label || r.source}</span><span className="chunk-meta">{r.source}</span></div>
              <div className="chunk-preview">{r.props?.preview || JSON.stringify(r.props)}</div>
            </div>
          ))}
        </div>
      )}
    </>
  );
}

function StepCard({ step }) {
  return (
    <div className={`step-card ${step.status}`} style={{ '--step-color': step.status === 'complete' ? 'var(--green)' : 'var(--primary)' }}>
      <div className="step-header">
        <div className="step-icon">{step.step}</div>
        <div className="step-info">
          <div className="step-name"><span className="step-number">Step {step.step}</span>{step.name}</div>
          <div className="step-desc">{step.description}</div>
        </div>
        <div className="step-status">{step.status === 'running' ? <span className="spinner" /> : <span className={`status-badge ${step.status}`}>{step.status}</span>}</div>
      </div>
      {step.result && <pre className="context-preview-box">{JSON.stringify(step.result, null, 2)}</pre>}
    </div>
  );
}

function Stat({ label, value }) {
  return <div className="completion-stat"><span className="stat-value">{value ?? '--'}</span><span className="stat-label">{label}</span></div>;
}

async function readEvents(response, onEvent) {
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  let type = null;

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop() || '';
    for (const line of lines) {
      if (line.startsWith('event: ')) type = line.slice(7);
      if (line.startsWith('data: ') && type) {
        onEvent({ type, data: JSON.parse(line.slice(6)) });
        type = null;
      }
    }
  }
}
