import { useEffect, useState, useRef } from "react";
import ChatWindow from "./components/ChatWindow";
import "./App.css";

function App() {
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const hasStarted = useRef(false);
  const sessionIdRef = useRef(null);

  const addMessage = (sender, text, options = null) => {
    setMessages((prev) => [
      ...prev,
      { sender, text, options }
    ]);
  };

  const handleResponse = (res) => {
    if (!res) return;

    if (res.type === "message") {
      addMessage("agent", res.text);
      sendStep();
    } else if (res.type === "question") {
      addMessage("agent", res.text, res.options);
    } else if (res.type === "summary") {
      addMessage("agent", res.text);
      sendStep();
    } else if (res.type === "end") {
      addMessage("agent", res.text);
    }
  };

  const sendStep = async (choice = null) => {
    const id = sessionIdRef.current || sessionId;
    if (!id) return;

    const res = await fetch("https://dt-assignment-fqfo.onrender.com/step", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        session_id: id,
        choice: choice,
      }),
    });

    const data = await res.json();
    handleResponse(data.data);
  };

  const startSession = async () => {
    const res = await fetch("https://dt-assignment-fqfo.onrender.com/start", {
      method: "POST",
    });

    const data = await res.json();

    setSessionId(data.session_id);
    sessionIdRef.current = data.session_id;
    handleResponse(data.data);
  };

  useEffect(() => {
    if (hasStarted.current) return;
    hasStarted.current = true;
    startSession();
  }, []);

  const handleOptionClick = (optionIndex, optionText) => {
    addMessage("user", optionText);
    sendStep(optionIndex);
  };

  return (
    <div className="app-container">
      <div className="app-header">
        <h2> Reflection Agent</h2>
      </div>

      <ChatWindow
        messages={messages}
        onOptionClick={handleOptionClick}
      />
    </div>
  );
}

export default App;