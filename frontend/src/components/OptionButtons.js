function OptionButtons({ options, onClick }) {
  return (
    <div className="option-buttons">
      {options.map((opt, i) => (
        <button
          key={i}
          onClick={() => onClick(i, opt)}
          className="option-button"
        >
          {opt}
        </button>
      ))}
    </div>
  );
}

export default OptionButtons;