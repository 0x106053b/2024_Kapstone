import React from "react";
import { useLocation } from "react-router-dom";
import LeftSide from "@/components/init/leftside.jsx";
import LoginForm from "@/components/init/login.jsx";
import SignUpForm from "@/components/init/signup.jsx";

const AuthPage = ({ setIsLoggedIn }) => {
  const location = useLocation();
  const isLoginPage = location.pathname === "/login";

  return (
    <div className="container max-w-full min-h-screen flex flex-col lg:flex-row p-0">
      <LeftSide />
      <div className="w-full lg:w-2/5 min-h-screen bg-gray-100 flex flex-col items-center justify-center overflow-y-auto">
        {isLoginPage ? (
          <LoginForm setIsLoggedIn={setIsLoggedIn} />
        ) : (
          <SignUpForm />
        )}
      </div>
    </div>
  );
};

export default AuthPage;
