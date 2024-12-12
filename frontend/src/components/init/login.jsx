import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { EyeIcon, EyeOffIcon } from "lucide-react";

import { postLogin } from "@/api/authAPI";

const LoginForm = ({ setIsLoggedIn }) => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      const response = await postLogin(email, password);
      console.log("Login successful:", response);
      setIsLoggedIn(true);
      navigate("/chatinterface");
    } catch (error) {
      console.error("Login failed:", error);
      setError("Login failed. Please check your email and password.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-8 w-full max-w-md">
      <h1 className="mb-6 text-2xl font-bold text-center">
        Welcome to Perfect Studymate
      </h1>
      {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="email">Email</Label>
          <Input
            id="email"
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="password">Password</Label>
          <div className="relative">
            <Input
              id="password"
              type={showPassword ? "text" : "password"}
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button
              type="button"
              className="absolute inset-y-0 right-0 pr-4 flex items-center justify-center bg-transparent focus:outline-none"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? (
                <EyeOffIcon className="h-4 w-4 text-gray-500" />
              ) : (
                <EyeIcon className="h-4 w-4 text-gray-500" />
              )}
            </button>
          </div>
        </div>
        <Button
          type="submit"
          className="w-full bg-black text-white hover:bg-gray-500"
          disabled={isLoading}
        >
          {isLoading ? "Signing in..." : "Sign In"}
        </Button>
      </form>
      <div className="mt-4 text-sm text-center space-y-2">
        <Link
          to="/forgot-password"
          className="text-[#8dc63f] hover:underline block"
          aria-label="Forgot password"
        >
          Forgot Password?
        </Link>
        <p className="text-gray-600">
          Don&apos;t have an account?{" "}
          <Link to="/signup" className="text-[#8dc63f] hover:underline">
            Sign up
          </Link>
        </p>
      </div>
    </div>
  );
};

export default LoginForm;
