"use client"; // login page state instance
import { useState } from "react";

// primary function - handle user login
export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

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
      <input type="button" onClick={HandleLogin} value={"submit"}>
        Log In
      </input>
    </main>
  );
}

function HandleLogin() {}
