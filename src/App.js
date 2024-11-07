import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './Navbar';
import ProductGrid from './ProductGrid';
import AdminPage from './AdminPage';
import Checkout from './Checkout'; // Import the Checkout component
import './App.css';

// Main App component
function App() {
  // State to keep track of cart items count and products in the cart
  const [cartItems, setCartItems] = useState(0);
  const [cartProducts, setCartProducts] = useState([]);

  // Function to add a product to the cart
  const addToCart = (product) => {
    setCartItems(prevItems => prevItems + 1); // Increment cart items count
    setCartProducts(prevProducts => [...prevProducts, product]); // Add product to the cart
  };

  return (
    <Router>
      <div className="App">
        {/* Navbar component with cart items and products as props */}
        <Navbar cartItems={cartItems} cartProducts={cartProducts} />
        {/* Define routes for the app */}
        <Routes>
          <Route path="/" element={<ProductGrid addToCart={addToCart} />} /> {/* Home page */}
          <Route path="/Admin" element={<AdminPage />} /> {/* Admin page */}
          <Route path="/Checkout" element={<Checkout />} /> {/* Checkout page */}
        </Routes>
      </div>
    </Router>
  );
}

// Export the App component
export default App;
