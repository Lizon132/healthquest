import logo from './logo.svg';
import './App.css';
import startLogging from './eventlogger.js';
import stopLogging from './eventlogger.js';
import calculateDistance from './eventlogger.js';
import handlePositionChange from './eventlogger.js';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <startLogging />
        <stopLogging />
        <calculateDistance />
        <handlePositionChange />
        <p>
          Edit <code>src/App.js</code> and save to reload. THIS IS AWS
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
