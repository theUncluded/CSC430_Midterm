import React, { useEffect, useState } from 'react';
import './ProductGrid.css'; // Import the CSS file

// ProductGrid component to display a grid of products
const ProductGrid = ({ addToCart }) => {
  const [products, setProducts] = useState([]);

  // Fetch products from the Fake Store API
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await fetch('https://fakestoreapi.com/products');
        const data = await response.json();
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
      .slice(0, 8) // Limit to the first 8 products
      .filter(product => product.title.length <= 30) // Only include products with titles <= 30 characters
      .map(product => (
        <div key={product.id} className="product-card">
          <img src={product.image} alt={product.title} className="product-image" />
          <h3 className="product-title">{product.title}</h3>
          <p className="product-price"><strong>${product.price}</strong></p>
          <button className="add-to-cart" onClick={() => addToCart(product)}>Add to Cart</button>
        </div>
      ))}
    </div>
  );
};

export default ProductGrid;
