import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";

function App() {
  const [output, setOutput] = useState("");

  const handleRunScript = (scriptName) => {
    fetch(`http://localhost:5000/run-script?script=${scriptName}`)
      .then((response) => response.json())
      .then((data) => setOutput(data.message))
      .catch((error) => console.error("Error:", error));
  };

  return (
    <div className="App">
      <header className="App-header">
        <title>RepRight</title>  {/* Added website title in the title tag */}
        <img src={viteLogo} className="App-logo" alt="logo" />
        <img src={reactLogo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
        <button onClick={() => handleRunScript("squats")}>Squats</button>
        <button onClick={() => handleRunScript("pushup")}>Push Up</button>
        <button onClick={() => handleRunScript("plank")}>Plank</button>
        <p>Output from Python Script:</p>
        <pre>{output}</pre>
      </header>
    </div>
  );
}

export default App;