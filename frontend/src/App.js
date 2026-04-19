import { useEffect, useState, useRef, useCallback } from "react";
import ChatWindow from "./components/ChatWindow";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const hasStarted = useRef(false);
  const sessionIdRef = useRef(null);
  const handleResponseRef = useRef(null);

  const addMessage = useCallback((sender, text, options = null) => {
    setMessages((prev) => [
      ...prev,
      { sender, text, options }
    ]);
  }, []);

  const sendStep = useCallback(async (choice = null) => {
    const id = sessionIdRef.current;
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
    handleResponseRef.current?.(data.data);
  }, []);

  const handleResponse = useCallback((res) => {
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
  }, [sendStep, addMessage]);

  useEffect(() => {
    handleResponseRef.current = handleResponse;
  }, [handleResponse]);

  useEffect(() => {
    if (hasStarted.current) return;
    hasStarted.current = true;

    const startSession = async () => {
      const res = await fetch("https://dt-assignment-fqfo.onrender.com/start", {
        method: "POST",
      });

      const data = await res.json();

      sessionIdRef.current = data.session_id;
      handleResponseRef.current?.(data.data);
    };

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