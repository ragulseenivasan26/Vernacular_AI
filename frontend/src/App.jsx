import React, { useState, useEffect, useRef } from "react";
import {
  Languages,
  Sparkles,
  Copy,
  Trash2,
  CheckCircle2,
  BookOpen,
  MessageSquare,
  Send,
  Mic,
  MicOff,
  Volume2,
  RefreshCw,
  HelpCircle,
  Film
} from "lucide-react";

const BACKEND_URL = "http://127.0.0.1:5000";

const SAMPLE_PROMPTS = [
  "🧮 45 * 12 எவ்வளவு?",
  "💻 Python string reverse program",
  "🌱 ஒளிச்சேர்க்கை என்றால் என்ன?",
  "🎬 Interstellar படத்தின் அர்த்தம் என்ன?",
  "🪐 Earth yen suthuthu? (Tanglish)"
];

const LANGUAGES = [
  { code: "Tamil", name: "Tamil (தமிழ்)", speech: "ta-IN" },
  { code: "Hindi", name: "Hindi (हिन्दी)", speech: "hi-IN" },
  { code: "Telugu", name: "Telugu (తెలుగు)", speech: "te-IN" },
  { code: "Malayalam", name: "Malayalam (മലയാളം)", speech: "ml-IN" },
  { code: "Kannada", name: "Kannada (ಕನ್ನಡ)", speech: "kn-IN" },
  { code: "Bengali", name: "Bengali (বাংলা)", speech: "bn-IN" },
  { code: "Marathi", name: "Marathi (मराठी)", speech: "mr-IN" },
  { code: "English", name: "English", speech: "en-US" }
];

export default function App() {
  const [activeTab, setActiveTab] = useState("chat"); // 'chat' | 'translate'
  const [targetLang, setTargetLang] = useState("Tamil");

  // Chatbot State
  const [chatInput, setChatInput] = useState("");
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "வணக்கம்! நான் உங்கள் Luthar AI (லூதர் AI) — Universal Multilingual Intelligence & AI Tutor. கணிதம் (Math), நிரலாக்கம் (Coding), அறிவியல் (Science), அல்லது சினிமா சந்தேகங்கள் எதுவானாலும் எந்த மொழியிலும் என்னிடம் கேளுங்கள்!",
      suggestions: [
        "🧮 45 * 12 எவ்வளவு?",
        "💻 Python string reverse program",
        "🌱 ஒளிச்சேர்க்கை என்றால் என்ன?",
        "🎬 Interstellar படத்தின் அர்த்தம் என்ன?"
      ],
      mode: "TUTOR",
      lang: "Tamil",
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [chatLoading, setChatLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const chatBottomRef = useRef(null);

  // Translation Workspace State
  const [transText, setTransText] = useState("");
  const [transResult, setTransResult] = useState("");
  const [transLoading, setTransLoading] = useState(false);
  const [transError, setTransError] = useState("");
  const [copied, setCopied] = useState(false);

  // Scroll chat to bottom
  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Send message to AI Chatbot
  async function handleSendChat(customMsg) {
    const textToSend = (customMsg || chatInput).trim();
    if (!textToSend || chatLoading) return;

    const userMsg = {
      role: "user",
      text: textToSend,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    if (!customMsg) setChatInput("");
    setChatLoading(true);

    try {
      const res = await fetch(`${BACKEND_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: textToSend,
          history: messages.slice(-6),
          language: targetLang
        })
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Chatbot service unavailable.");

      const botMsg = {
        role: "assistant",
        text: data.reply,
        suggestions: data.suggestions || [],
        lang: data.language || data.detected_language || targetLang,
        mode: (data.mode || "tutor").toUpperCase(),
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages(prev => [...prev, botMsg]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          text: `⚠️ மன்னிக்கவும், பதில் பெறுவதில் தாமதம் ஏற்பட்டது: ${err.message}. Backend சர்வர் இயங்குகிறதா என பார்க்கவும் (http://127.0.0.1:5000).`,
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    } finally {
      setChatLoading(false);
    }
  }

  // Voice speech synthesis
  function speakText(text) {
    if (!("speechSynthesis" in window) || !text) return;
    window.speechSynthesis.cancel();
    const cleanText = text.replace(/[*#💡🔬📝🎯📖]/g, "").trim();
    const utter = new SpeechSynthesisUtterance(cleanText);
    const langObj = LANGUAGES.find(l => l.code === targetLang);
    utter.lang = langObj ? langObj.speech : "ta-IN";
    utter.rate = 1.0;
    window.speechSynthesis.speak(utter);
  }

  // Speech-to-Text Microphone
  function toggleSpeechMic() {
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRec) {
      alert("Speech recognition is not supported in this browser. Please use Google Chrome or Edge.");
      return;
    }

    if (isListening) {
      setIsListening(false);
      return;
    }

    const recognition = new SpeechRec();
    recognition.lang = targetLang === "Tamil" ? "ta-IN" : "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
    recognition.onerror = () => setIsListening(false);

    recognition.onresult = event => {
      const transcript = event.results[0][0].transcript;
      setChatInput(prev => (prev ? prev + " " + transcript : transcript));
    };

    recognition.start();
  }

  // Handle Lesson Translation
  async function handleTranslate() {
    setTransError("");
    setTransResult("");
    if (!transText.trim()) {
      setTransError("Please enter educational content first.");
      return;
    }
    setTransLoading(true);
    try {
      const res = await fetch(`${BACKEND_URL}/api/translate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: transText, source: "English", target: targetLang })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Translation failed.");
      setTransResult(data.translation);
    } catch (e) {
      setTransError(e.message + " Make sure the Flask backend is running on http://127.0.0.1:5000.");
    } finally {
      setTransLoading(false);
    }
  }

  async function copyResult() {
    if (!transResult) return;
    await navigator.clipboard.writeText(transResult);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  }

  return (
    <div className="app">
      {/* Navbar */}
      <header className="navbar">
        <div className="brand">
          <div className="logo"><Languages size={22} /></div>
          <div>
            <strong>Vernacular AI</strong>
            <span>Multimodal Mother Tongue Tutor & Pedagogy Platform</span>
          </div>
        </div>

        {/* Tab Switcher */}
        <div style={{ display: "flex", gap: "8px", background: "#f0efff", padding: "4px", borderRadius: "12px" }}>
          <button
            onClick={() => setActiveTab("chat")}
            style={{
              display: "flex",
              alignItems: "center",
              gap: "6px",
              border: "none",
              padding: "8px 16px",
              borderRadius: "9px",
              fontWeight: 700,
              fontSize: "13px",
              cursor: "pointer",
              background: activeTab === "chat" ? "#5b5bea" : "transparent",
              color: activeTab === "chat" ? "#fff" : "#5b5bea"
            }}
          >
            <MessageSquare size={16} /> AI Tutor Chatbot
          </button>
          <button
            onClick={() => setActiveTab("translate")}
            style={{
              display: "flex",
              alignItems: "center",
              gap: "6px",
              border: "none",
              padding: "8px 16px",
              borderRadius: "9px",
              fontWeight: 700,
              fontSize: "13px",
              cursor: "pointer",
              background: activeTab === "translate" ? "#5b5bea" : "transparent",
              color: activeTab === "translate" ? "#fff" : "#5b5bea"
            }}
          >
            <Sparkles size={16} /> Lesson Translator
          </button>
        </div>

        <div className="status"><span className="dot" /> AI Ready (50+ Languages)</div>
      </header>

      <main className="container" style={{ maxWidth: "980px", paddingTop: "32px" }}>
        {/* Language Selector Bar */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px", flexWrap: "wrap", gap: "12px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
            <span style={{ fontSize: "13px", fontWeight: 700, color: "#64748b" }}>Choose Mother Tongue:</span>
            <select
              value={targetLang}
              onChange={e => setTargetLang(e.target.value)}
              style={{ padding: "8px 14px", borderRadius: "10px", border: "1px solid #cbd5e1", fontWeight: 700, fontSize: "14px", color: "#1e293b", background: "#fff" }}
            >
              {LANGUAGES.map(l => (
                <option key={l.code} value={l.code}>{l.name}</option>
              ))}
            </select>
          </div>

          <div style={{ fontSize: "12px", color: "#64748b" }}>
            ⚡ <strong>100% Offline Resilient</strong> with local lexicon
          </div>
        </div>

        {/* TAB 1: AI TUTOR CHATBOT */}
        {activeTab === "chat" && (
          <div style={{ display: "flex", flexDirection: "column", background: "#fff", border: "1px solid #e2e8f0", borderRadius: "20px", boxShadow: "0 10px 30px rgba(0,0,0,0.06)", overflow: "hidden", minHeight: "560px" }}>
            {/* Chat Header */}
            <div style={{ padding: "16px 22px", background: "linear-gradient(135deg, #1e1b4b 0%, #311042 50%, #0f172a 100%)", color: "#fff", display: "flex", justifyContent: "space-between", alignItems: "center", borderBottom: "1px solid rgba(255,255,255,0.1)" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                <div style={{ width: "38px", height: "38px", borderRadius: "12px", background: "linear-gradient(135deg, #06b6d4, #6366f1)", display: "grid", placeItems: "center", boxShadow: "0 0 12px rgba(6,182,212,0.5)" }}>
                  <Sparkles size={20} color="#fff" />
                </div>
                <div>
                  <strong style={{ fontSize: "16px", display: "flex", alignItems: "center", gap: "8px" }}>
                    <span>⚡ LUTHAR AI</span>
                    <span style={{ fontSize: "12px", background: "rgba(244,63,94,0.2)", color: "#fda4af", padding: "1px 8px", borderRadius: "6px" }}>லூதர் AI</span>
                  </strong>
                  <span style={{ fontSize: "11px", color: "#94a3b8" }}>Universal Multilingual Intelligence Core • 51 Languages • Math • Code</span>
                </div>
              </div>
              <button
                onClick={() => setMessages([messages[0]])}
                style={{ background: "rgba(255,255,255,0.1)", border: "1px solid rgba(255,255,255,0.2)", color: "#fff", padding: "6px 12px", borderRadius: "8px", fontSize: "12px", cursor: "pointer", fontWeight: 600 }}
              >
                Clear Chat
              </button>
            </div>

            {/* Quick Topic Chips */}
            <div style={{ padding: "12px 20px", background: "#f8fafc", borderBottom: "1px solid #f1f5f9", display: "flex", gap: "8px", overflowX: "auto" }}>
              <span style={{ fontSize: "11px", fontWeight: 700, color: "#94a3b8", alignSelf: "center", textTransform: "uppercase" }}>Try Luthar AI:</span>
              {SAMPLE_PROMPTS.map((p, i) => (
                <button
                  key={i}
                  onClick={() => handleSendChat(p)}
                  style={{ whiteSpace: "nowrap", border: "1px solid #cbd5e1", background: "#fff", padding: "6px 12px", borderRadius: "20px", fontSize: "12px", fontWeight: 600, color: "#475569", cursor: "pointer" }}
                >
                  {p}
                </button>
              ))}
            </div>

            {/* Message Stream */}
            <div style={{ flex: 1, padding: "20px", overflowY: "auto", maxHeight: "420px", display: "flex", flexDirection: "column", gap: "16px", background: "#fafbff" }}>
              {messages.map((m, idx) => (
                <div
                  key={idx}
                  style={{
                    alignSelf: m.role === "user" ? "flex-end" : "flex-start",
                    maxWidth: "82%",
                    display: "flex",
                    flexDirection: "column",
                    alignItems: m.role === "user" ? "flex-end" : "flex-start"
                  }}
                >
                  {/* Meta tag */}
                  {m.role === "assistant" && (
                    <div style={{ display: "flex", alignItems: "center", gap: "6px", marginBottom: "4px", fontSize: "11px" }}>
                      <strong style={{ color: "#4f46e5" }}>⚡ LUTHAR AI</strong>
                      {m.lang && <span style={{ background: "#e0e7ff", color: "#4338ca", padding: "1px 6px", borderRadius: "4px", fontWeight: 700 }}>{m.lang}</span>}
                      {m.mode && <span style={{ background: "#fce7f3", color: "#be185d", padding: "1px 6px", borderRadius: "4px", fontWeight: 700 }}>{m.mode}</span>}
                    </div>
                  )}

                  <div
                    style={{
                      background: m.role === "user" ? "linear-gradient(135deg, #4f46e5, #7c3aed)" : "#fff",
                      color: m.role === "user" ? "#fff" : "#1e293b",
                      padding: "14px 18px",
                      borderRadius: m.role === "user" ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
                      boxShadow: "0 2px 8px rgba(0,0,0,0.06)",
                      border: m.role === "assistant" ? "1px solid #e2e8f0" : "none",
                      fontSize: "14.5px",
                      lineHeight: "1.7",
                      whiteSpace: "pre-line"
                    }}
                  >
                    {m.text}
                  </div>

                  <div style={{ display: "flex", alignItems: "center", gap: "8px", marginTop: "4px", fontSize: "11px", color: "#94a3b8" }}>
                    <span>{m.time}</span>
                    {m.role === "assistant" && (
                      <button
                        onClick={() => speakText(m.text)}
                        title="Listen in mother tongue audio"
                        style={{ background: "transparent", border: "none", color: "#5b5bea", cursor: "pointer", display: "flex", alignItems: "center", gap: "3px", fontWeight: 600 }}
                      >
                        <Volume2 size={13} /> Listen Audio
                      </button>
                    )}
                  </div>

                  {/* Follow-up suggestions */}
                  {m.suggestions && m.suggestions.length > 0 && (
                    <div style={{ display: "flex", flexWrap: "wrap", gap: "6px", marginTop: "10px" }}>
                      {m.suggestions.map((sug, sIdx) => (
                        <button
                          key={sIdx}
                          onClick={() => handleSendChat(sug)}
                          style={{ border: "1px solid #c7d2fe", background: "#f5f3ff", color: "#4f46e5", padding: "5px 12px", borderRadius: "14px", fontSize: "12px", fontWeight: 600, cursor: "pointer" }}
                        >
                          💬 {sug}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              ))}

              {chatLoading && (
                <div style={{ alignSelf: "flex-start", background: "#fff", border: "1px solid #e2e8f0", padding: "12px 18px", borderRadius: "18px", display: "flex", alignItems: "center", gap: "10px", color: "#5b5bea", fontSize: "14px" }}>
                  <div className="spinner" /> Vernacular AI பதில் எழுதுகிறது...
                </div>
              )}
              <div ref={chatBottomRef} />
            </div>

            {/* Input Bar */}
            <div style={{ padding: "16px 20px", borderTop: "1px solid #e2e8f0", background: "#fff", display: "flex", gap: "10px", alignItems: "center" }}>
              <button
                onClick={toggleSpeechMic}
                title="Speak question into microphone"
                style={{
                  width: "44px",
                  height: "44px",
                  borderRadius: "12px",
                  border: "1px solid #cbd5e1",
                  background: isListening ? "#ef4444" : "#f1f5f9",
                  color: isListening ? "#fff" : "#475569",
                  display: "grid",
                  placeItems: "center",
                  cursor: "pointer"
                }}
              >
                {isListening ? <MicOff size={20} /> : <Mic size={20} />}
              </button>

              <input
                type="text"
                value={chatInput}
                onChange={e => setChatInput(e.target.value)}
                onKeyDown={e => e.key === "Enter" && handleSendChat()}
                placeholder={`Ask any educational doubt in English, Tamil, or Tanglish... (e.g. "photosynthesis na enna?")`}
                style={{ flex: 1, padding: "12px 16px", borderRadius: "12px", border: "1px solid #cbd5e1", fontSize: "15px", outline: "none" }}
              />

              <button
                onClick={() => handleSendChat()}
                disabled={chatLoading || !chatInput.trim()}
                style={{
                  background: "linear-gradient(135deg, #5b5bea 0%, #8b5cf6 100%)",
                  color: "#fff",
                  border: "none",
                  borderRadius: "12px",
                  padding: "0 22px",
                  height: "44px",
                  fontWeight: 700,
                  fontSize: "14px",
                  display: "flex",
                  alignItems: "center",
                  gap: "6px",
                  cursor: chatLoading || !chatInput.trim() ? "not-allowed" : "pointer",
                  opacity: chatLoading || !chatInput.trim() ? 0.6 : 1
                }}
              >
                <Send size={16} /> Send
              </button>
            </div>
          </div>
        )}

        {/* TAB 2: LESSON TRANSLATOR */}
        {activeTab === "translate" && (
          <div>
            <section className="workspace">
              <div className="card">
                <div className="cardhead">
                  <span>English Lesson Content</span>
                  <small>{transText.length}/2000</small>
                </div>
                <textarea
                  maxLength="2000"
                  value={transText}
                  onChange={e => setTransText(e.target.value)}
                  placeholder="Type or paste an English lesson, concept, or question here..."
                />
                <div className="example">Try: “Plants need sunlight and water to produce food.”</div>
              </div>

              <div className="card result">
                <div className="cardhead">
                  <span>{targetLang} Vernacular Translation</span>
                  {transResult && (
                    <div style={{ display: "flex", gap: "6px" }}>
                      <button className="iconbtn" onClick={() => speakText(transResult)} title="Listen in audio">
                        <Volume2 size={16} />
                      </button>
                      <button className="iconbtn" onClick={copyResult}>
                        {copied ? <CheckCircle2 size={16} /> : <Copy size={16} />}
                      </button>
                    </div>
                  )}
                </div>
                <div className={"output " + (!transResult ? "empty" : "")}>
                  {transLoading ? (
                    <div className="loader"><div className="spinner" />Translating into {targetLang}...</div>
                  ) : (
                    transResult || `Your ${targetLang} translation will appear here.`
                  )}
                </div>
              </div>
            </section>

            {transError && <div className="error">{transError}</div>}

            <div className="actions">
              <button className="primary" onClick={handleTranslate} disabled={transLoading}>
                <Sparkles size={18} /> {transLoading ? "Translating..." : "Translate with AI"}
              </button>
              <button className="secondary" onClick={() => { setTransText(""); setTransResult(""); setTransError(""); }}>
                <Trash2 size={17} /> Clear
              </button>
            </div>
          </div>
        )}

        {/* Footer Feature Note */}
        <section className="feature" style={{ marginTop: "24px" }}>
          <div className="featureicon"><BookOpen size={21} /></div>
          <div>
            <b>Vernacular AI Pedagogical Engine</b>
            <p>Empowering children and students across rural and urban India to master science, mathematics, and world knowledge in their native mother tongue.</p>
          </div>
        </section>
      </main>
    </div>
  );
}
