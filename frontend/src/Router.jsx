import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";
import { useState, useEffect } from "react";
import AuthPage from "@/pages/auth.jsx";
import Cookies from "js-cookie";
import ChatInterface from "@/components/chat/ChatInterface.jsx";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = Cookies.get("access_token");
    if (token) {
      setIsLoggedIn(true);
    }
  }, []);

  // 보호된 라우트 컴포넌트
  const ProtectedRoute = ({ children }) => {
    const token = Cookies.get("access_token");
    if (!token) {
      return <Navigate to="/login" replace />;
    }
    return children;
  };

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            isLoggedIn ? (
              <Navigate to="/chatinterface" replace />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
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
            <ProtectedRoute>
              <ChatInterface />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
