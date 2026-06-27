"use client"; // login page state instance
import { useState } from "react";
import { useRouter } from "next/navigation";

// primary function - handle user login
export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  // call API upon button click
  async function handleLogin() {
    console.log("Login button clicked");

    const apicall = await fetch("http://localhost:8000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    const data = await apicall.json();

    // error handling, save token & redirect if login successful
    if (!data.token) {
      setError("Incorrect credentials");
    } else {
      localStorage.setItem("token", data.token);
      router.push("/dashboard");
    }
  }

  return (
    <main>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Enter email"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Enter password"
      />
      <button onClick={handleLogin}>Log In</button>
      {error && <p>{error}</p>}
    </main>
  );
}
