"use client"; // mark server & client component boundary
import { useState } from "react";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { jwtDecode } from "jwt-decode";
import Link from "next/link";

// primary function - personalized user dashboard
export default function Dashboard() {
  const router = useRouter();
  const [products, setProducts] = useState([]);

  useEffect(() => {
    // validate user token, redirect to login page in invalid
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
      return;
    }
    console.log("Logged in successfully");

    // decode user token to fetch related data
    const decode = jwtDecode<{ user_id: number }>(token);
    const user_id = decode.user_id;

    // fetch products associated with the user
    async function fetchProducts() {
      const fetchProd = await fetch(
        `http://localhost:8000/products/${user_id}/products`,
        { headers: { Authorization: `Bearer: ${token}` } },
      );
      const data = await fetchProd.json();
      setProducts(data.products);
    }
    fetchProducts();
  }, []);

  return (
    <main>
      <h1>Dashboard</h1>
    </main>
  );
}
