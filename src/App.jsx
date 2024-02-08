import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";

function App() {
  const [output, setOutput] = useState("");

  const handleRunScript = () => {
    // Replace this URL with your Flask server's endpoint
    fetch("http://localhost:5000/run-script")
      .then((response) => response.json())
      .then((data) => setOutput(data.message))
      .catch((error) => console.error("Error:", error));
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={viteLogo} className="App-logo" alt="logo" />
        <img src={reactLogo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
        <button onClick={handleRunScript}>Run Python Script</button>
        <p>Output from Python Script:</p>
        <pre>{output}</pre>
      </header>
    </div>
  );
}

export default App;
