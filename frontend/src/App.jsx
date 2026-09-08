import React, { useState } from "react";
import { Languages, Sparkles, Copy, Trash2, CheckCircle2, BookOpen } from "lucide-react";

const API = "http://127.0.0.1:5000/api/translate";

export default function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);

  async function translate() {
    setError("");
    setResult("");
    if (!text.trim()) {
      setError("Please enter educational content first.");
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(API, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, source: "English", target: "Tamil" })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Translation failed.");
      setResult(data.translation);
    } catch (e) {
      setError(e.message + " Make sure the Flask backend is running.");
    } finally {
      setLoading(false);
    }
  }

  async function copyResult() {
    if (!result) return;
    await navigator.clipboard.writeText(result);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  }

  function clearAll() {
    setText("");
    setResult("");
    setError("");
  }

  return (
    <div className="app">
      <header className="navbar">
        <div className="brand">
          <div className="logo"><Languages size={22}/></div>
          <div>
            <strong>Vernacular AI</strong>
            <span>Mother Tongue Learning</span>
          </div>
        </div>
        <div className="status"><span className="dot"/> AI Translation Ready</div>
      </header>

      <main className="container">
        <section className="hero">
          <div className="eyebrow"><Sparkles size={15}/> AI-POWERED EDUCATION</div>
          <h1>Learn in the language<br/><span>that feels like home.</span></h1>
          <p>Translate educational content into a child's mother tongue with an AI-ready vernacular learning platform.</p>
        </section>

        <section className="languagebar">
          <div><label>Source language</label><b>🇬🇧 English</b></div>
          <div className="arrow">→</div>
          <div><label>Target language</label><b>🇮🇳 தமிழ் (Tamil)</b></div>
          <div className="model"><CheckCircle2 size={16}/> IndicTrans2</div>
        </section>

        <section className="workspace">
          <div className="card">
            <div className="cardhead"><span>Educational content</span><small>{text.length}/2000</small></div>
            <textarea
              maxLength="2000"
              value={text}
              onChange={e => setText(e.target.value)}
              placeholder="Type or paste an English lesson, sentence, or paragraph here..."
            />
            <div className="example">Try: “The Sun gives us light and heat.”</div>
          </div>

          <div className="card result">
            <div className="cardhead"><span>Tamil translation</span>{result && <button className="iconbtn" onClick={copyResult}>{copied ? <CheckCircle2 size={17}/> : <Copy size={17}/>}</button>}</div>
            <div className={"output " + (!result ? "empty" : "")}>
              {loading ? <div className="loader"><div className="spinner"/>AI is translating...</div> : result || "Your Tamil translation will appear here."}
            </div>
          </div>
        </section>

        {error && <div className="error">{error}</div>}

        <div className="actions">
          <button className="primary" onClick={translate} disabled={loading}>
            <Sparkles size={18}/> {loading ? "Translating..." : "Translate with AI"}
          </button>
          <button className="secondary" onClick={clearAll}><Trash2 size={17}/> Clear</button>
        </div>

        <section className="feature">
          <div className="featureicon"><BookOpen size={21}/></div>
          <div>
            <b>Built for vernacular pedagogy</b>
            <p>This Module 1 prototype focuses on English → Tamil translation. Future modules can add child-friendly explanations, speech, quizzes and learning analytics.</p>
          </div>
        </section>
      </main>
    </div>
  );
}
