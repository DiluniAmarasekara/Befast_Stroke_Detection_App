import './App.css';
import Landmarks from './pages/Landmarks';
import Lipsigns from './pages/Lipsigns';
import{
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<Landmarks/>} />
          <Route path="/lipsign" element={<Lipsigns/>} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
