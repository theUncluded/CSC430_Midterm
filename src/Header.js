import React, { useState, useEffect, useContext } from 'react';
import Cart from './Cart';
import Login from './Login';
import { useCart } from './CartContext';  // Import useCart here
import { UserContext } from './UserContext';
import './Header.css';

const Header = () => {
    const { cartItems, fetchCartFromDB } = useCart(); // Access fetchCartFromDB from CartContext
    const [cartOpen, setCartOpen] = useState(false);
    const [searchTerm, setSearchTerm] = useState("");
    const [suggestions, setSuggestions] = useState([]);
    const [products, setProducts] = useState([]);
    const [isLoginModalOpen, setLoginModalOpen] = useState(false);
    const { handleLogin, isLoggedIn, userName } = useContext(UserContext);

    const toggleLoginModal = () => {
        setLoginModalOpen(prev => !prev);
    };

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8080/');
                if (!response.ok) {
                    throw new Error(`Network response was not ok: ${response.statusText}`);
                }
                const data = await response.json();
                console.log("Fetched products:", data);
                setProducts(data);
            } catch (error) {
                console.error("Error fetching products:", error);
            }
        };

        fetchProducts();
    }, []);

    const toggleCart = () => {
        setCartOpen((prevCartOpen) => !prevCartOpen);
    };

    const handleLoginSuccess = (userId, name) => {
        handleLogin(userId);  // Update the user context upon successful login
        fetchCartFromDB();    // Fetch the cart from DB
        setLoginModalOpen(false);
    };

    const handleLogout = () => {
        handleLogin(null, '');
    };

    const handleSearchChange = (e) => {
        const term = e.target.value;
        setSearchTerm(term);

        if (term) {
            setSuggestions(products.filter(product =>
                product.product_name.toLowerCase().includes(term.toLowerCase())
            ));
        } else {
            setSuggestions([]);
        }
    };

    const handleSearchSubmit = () => {
        window.location.href = `/products?search=${encodeURIComponent(searchTerm)}`;
    };

    const handleSuggestionClick = (suggestion) => {
        setSearchTerm(suggestion.product_name);
        setSuggestions([]);
        handleSearchSubmit();
    };

    const handleKeyPress = (e) => {
        if (e.key === "Enter") {
            handleSearchSubmit();
        }
    };

    return (
        <header className="header">
            <a href="/" className="logo">😎</a>
            <nav className="nav-links">
                <a href="/products">Products</a>
            </nav>

            {/* Search bar */}
            <div className="search-bar-container">
                <input
                    type="text"
                    placeholder="Search for Products"
                    value={searchTerm}
                    onChange={handleSearchChange}
                    onKeyDown={handleKeyPress}
                />
                {suggestions.length > 0 && (
                    <div className="autocomplete-container">
                        {suggestions.map((suggestion) => (
                            <div
                                key={suggestion.id}
                                className="autocomplete-item"
                                onClick={() => handleSuggestionClick(suggestion)}
                            >
                                {suggestion.product_name}
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* Auth container with conditional rendering for login/logout */}
            <div className="auth-container">
                {isLoggedIn ? (
                    <div className="user-menu">
                        <button className="user-button">{userName}</button>
                        <div className="user-menu-content">
                            <button className="logout-button" onClick={handleLogout}>Logout</button>
                        </div>
                    </div>
                ) : (
                    <button onClick={toggleLoginModal} className="login-button">
                        Login
                    </button>
                )}
            </div>

            {/* Login modal */}
            <Login 
                isOpen={isLoginModalOpen} 
                onClose={toggleLoginModal} 
                onLoginSuccess={handleLoginSuccess}  
            />

            {/* Cart icon */}
            <div className="cart-icon" onClick={toggleCart}>
                Cart ({cartItems.reduce((count, item) => count + item.quantity, 0)})
            </div>
            {cartOpen && <Cart onClose={toggleCart} />}
        </header>
    );
};

export default Header;
