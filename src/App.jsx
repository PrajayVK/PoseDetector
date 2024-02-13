import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import bg from "./assets/bg.png"
import squat from "./assets/squat_website.jpg"
import pushup from "./assets/pushup_website.jpg"
import barbellrow from "./assets/barbellrow_website.jpg"
import "./App.css"


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
    <section id = "sec1">
      <div>
        
        
        <h1 style = {{fontSize: "80px"}}>RepRight</h1>
        <p style = {{color: "rgba(255, 179, 64, 1)", fontSize: "25px"}}>Ai assissted gym form correction</p>
        <a href= "#sec2">
          <div class = "scroll_down"> 
        </div>
        </a>
       </div>
    </section>
    <section id = "sec2">
      <div class = "container">
        <h1 style = {{padding: "2px", fontSize:"40px"}}>CHOOSE EXERCISE</h1>
        <div class = "squats">
          <div class = "sq-overlay">
            <button onClick={() => handleRunScript("test")} class = "sq-button">Squats</button>
          </div> 
          <img class = "sq-image" src = {squat} alt = "squat image"/>   
        </div> 
        <div class = "planks">
          <div class="sq-overlay">
            <button onClick={() => handleRunScript("pushups")} class = "sq-button">Push Up</button>
          </div>
          <img class = "sq-image" src = {pushup} alt = "push up image"/>
        </div>
        <div class = "pushups">
          <div class="sq-overlay">
            <button onClick={() => handleRunScript("barbellrow")} class = "sq-button">Barbell Row</button>
          </div>
          <img class = "sq-image" src = {barbellrow} alt = "barbellrow image"/>
        </div>
        {/* <pre>{output}</pre> */}
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
