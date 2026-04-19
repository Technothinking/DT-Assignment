import MessageBubble from "./MessageBubble";
import OptionButtons from "./OptionButtons";

function ChatWindow({ messages, onOptionClick }) {
  return (
    <div className="chat-window">
      {messages.map((msg, index) => (
        <div key={index} className="message-container">
          <MessageBubble sender={msg.sender} text={msg.text} />

          {msg.options && (
            <OptionButtons
              options={msg.options}
              onClick={onOptionClick}
            />
          )}
        </div>
      ))}
    </div>
  );
}

export default ChatWindow;