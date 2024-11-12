"use client"
import { useState } from "react";
import { useRouter } from "next/navigation";
import Login from "../../components/Login";
import Signup from "../../components/Signup";

export default function Home() {
   const [isLogin, setIsLogin] = useState(true);
  const router = useRouter();

  const handleAuthSuccess = () => {
    alert(isLogin ? "Login successful!" : "Registration successful!");
    // Redirect to main app page or dashboard after alert
    router.push("/dashboard"); // Replace with your main app route
  };

  return (
    <div>
      <h1>Welcome to Our App</h1>
      <div>
        <button onClick={() => setIsLogin(true)}>Login</button>
        <button onClick={() => setIsLogin(false)}>Sign Up</button>
      </div>
      {isLogin ? <Login onSuccess={handleAuthSuccess} /> : <Signup onSuccess={handleAuthSuccess} />}
    </div>
  )
}
