import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { EyeIcon, EyeOffIcon } from "lucide-react";

import { postRegister } from "@/api/userAPI";

const SignUpForm = () => {
  const navigate = useNavigate();
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);

    try {
      await postRegister(firstName, lastName, email, password);
      //console.log("Registration successful:", response);
      alert("Registration successful");
      // 성공 시 로그인 페이지로 이동
      navigate("/login");
    } catch (error) {
      console.error("Registration failed:", error);
      // 에러 처리 (예: 사용자에게 에러 메시지 표시)
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-8 w-full max-w-md">
      <h1 className="mb-1 text-2xl font-bold text-center">Sign up</h1>
      <p className="text-center text-sm mb-3 text-gray-600">
        Start your journey with us today
      </p>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="firstName">First Name</Label>
            <Input
              id="firstName"
              type="text"
              placeholder="Enter your first name"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              required
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="lastName">Last Name</Label>
            <Input
              id="lastName"
              type="text"
              placeholder="Enter your last name"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              required
            />
          </div>
        </div>
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
          {isLoading ? "Signing up..." : "Sign Up"}
        </Button>
      </form>
      <div className="mt-4 text-sm text-center">
        <p className="text-gray-600">
          Already have an account?{" "}
          <Link to="/login" className="text-[#8dc63f] hover:underline">
            Log in
          </Link>
        </p>
      </div>
    </div>
  );
};

export default SignUpForm;
