"use client"; // mark server & client component boundary
import { useState } from "react";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { jwtDecode } from "jwt-decode";
import Link from "next/link";

// blueprint for product object
type Product = {
  product_id: number;
  user_id: number;
  name: string;
  url: string;
  current_price: number;
  target_price: number;
  stock: number;
};

// primary function - personalized user dashboard
export default function Dashboard() {
  const router = useRouter();
  const [products, setProducts] = useState<Product[]>([]);

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
        { headers: { Authorization: `Bearer ${token}` } },
      );
      const data = await fetchProd.json();
      setProducts(data.products);
    }
    fetchProducts();
  }, []);

  return (
    <main>
      <h1>Dashboard</h1>

      {products.map((product) => (
        <div key={product.product_id}>
          <h1>{product.name}</h1>
          <h1>{product.current_price}</h1>
          <a href={`/dashboard/${product.product_id}`}>View</a>
          <a href={product.url} target="_blank">
            Buy
          </a>
        </div>
      ))}
    </main>
  );
}
