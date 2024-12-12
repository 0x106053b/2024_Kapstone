import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";
import { useState } from "react";
import AuthPage from "@/pages/auth.jsx";
import ChatInterface from "@/components/chat/ChatInterface.jsx";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route
          path="/login"
          element={<AuthPage setIsLoggedIn={setIsLoggedIn} />}
        />
        <Route
          path="/signup"
          element={<AuthPage setIsLoggedIn={setIsLoggedIn} />}
        />
        <Route
          path="/chatinterface"
          element={
            isLoggedIn ? <ChatInterface /> : <Navigate to="/login" replace />
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
