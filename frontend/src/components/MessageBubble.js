function MessageBubble({ sender, text }) {
  const isUser = sender === "user";

  return (
    <div className={`message-bubble ${isUser ? "user" : "agent"}`}>
      <div className={`bubble ${isUser ? "user" : "agent"}`}>
        {text}
      </div>
    </div>
  );
}

export default MessageBubble;