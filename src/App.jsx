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
    <section id = "sec1">
      <div>
        
        <div class = "login">
        <button type = "button" class = "login-btn" style = {{fontSize: "14px"}}>Login</button>
        </div>
        <div class = "signup">
        <button type = "button" class = "signup-btn"style = {{fontSize: "14px", color: "black"}}>Sign Up</button>
        </div>
        <h1 style = {{fontSize: "80px"}}>RepRight</h1>
        <p style = {{color: "rgba(255, 179, 64, 1)", fontSize: "25px"}}>Ai assissted gym form correction</p>
        <a href= "#sec2">
          <div class = "scroll_down"> 
        </div>
        </a>
       </div>
    </section>
    <section id = "sec2" >
      <div class = "container">
        <h1>Let's Get Started!  </h1>
        <ul>button1</ul>
        <ul>button2</ul>
      </div>
    </section>
      

              
    

      {/* <header className="App-header">
        <img src={viteLogo} className="App-logo" alt="logo" />
        <img src={reactLogo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
        <button onClick={handleRunScript}>Run Python Script</button>
        <p>Output from Python Script:</p>
        <pre>{output}</pre>
      </header> */}
    </div>
  );
}

export default App;
