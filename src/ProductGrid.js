import React, { useEffect, useState } from 'react';
import './ProductGrid.css';

const ProductGrid = ({ addToCart }) => {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/');
        if (!response.ok) {
          throw new Error(`Network response was not ok: ${response.statusText}`);
        }
        const data = await response.json();
        console.log("Fetched products:", data);  // Log the fetched data
        setProducts(data);
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    };

    fetchProducts();
  }, []);

  return (
    <div className="product-grid">
      {products
      .slice(0, 8)
      .filter(product => product.title && product.title.length <= 30)
      .map(product => (
        <div key={product.id} className="product-card">
          <img src={product.image} alt={product.title || "No Title"} className="product-image" />
          <h3 className="product-title">{product.title || "Untitled Product"}</h3>
          <p className="product-price"><strong>${product.price}</strong></p>
          <button className="add-to-cart" onClick={() => addToCart(product)}>Add to Cart</button>
        </div>
      ))}
    </div>
  );
};

export default ProductGrid;
