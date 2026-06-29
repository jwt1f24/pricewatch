"use client"; // page state instance
import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

// primary function - handle user account sign up
export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  // validate credentials upon button click
  async function handleRegister() {
    console.log("Register button clicked");
    const email_format = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;

    // input form validation
    if (email === "" || password === "") {
      setError("Credentials must not be empty");
      return;
    }
    if (password.length < 8) {
      setError("Password must have at least 8 characters");
      return;
    }
    if (!email_format.test(email)) {
      setError("Invalid email format");
      return;
    }

    try {
      const apicall = await fetch("http://localhost:8000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      // error handling, redirect to login page if registration is successful
      if (apicall.ok) {
        router.push("/login");
      } else {
        setError("Invalid! Account already exists");
      }
    } catch {
      console.log("Error: ", error);
    }
  }

  // page structure
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
      <button onClick={handleRegister}>Sign Up</button>
      <Link href="/login">Already have an account?</Link>
      {error && <p>{error}</p>}
    </main>
  );
}
