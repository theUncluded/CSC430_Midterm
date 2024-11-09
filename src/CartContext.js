import React, { createContext, useContext, useState, useEffect } from 'react';
import { UserContext } from './UserContext';

const CartContext = createContext();

export const useCart = () => useContext(CartContext);

export const CartProvider = ({ children }) => {
    const { currentUserId } = useContext(UserContext);  // Get currentUserId from UserContext
    const [cartItems, setCartItems] = useState([]);

    const addToCart = (product) => {
        setCartItems((prevItems) => {
            const existingItem = prevItems.find(item => item.product_id === product.product_id);
            if (existingItem) {
                return prevItems.map(item =>
                    item.product_id === product.product_id
                        ? { ...item, quantity: item.quantity + 1 }
                        : item
                );
            } else {
                return [...prevItems, { ...product, quantity: 1 }];
            }
        });
    };

    const updateItemQuantity = (productId, quantity) => {
        setCartItems((prevItems) =>
            prevItems.map((item) =>
                item.product_id === productId ? { ...item, quantity } : item
            )
        );
    };

    const removeFromCart = (productId) => {
        setCartItems((prevItems) => prevItems.filter((item) => item.product_id !== productId));
    };

    const saveCartToDB = async () => {
        if (!currentUserId) return;  // Ensure a user is logged in

        try {
            const response = await fetch('http://127.0.0.1:8080/cart/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: currentUserId, cart_items: cartItems })
            });

            if (!response.ok) {
                throw new Error(`Error saving cart: ${response.statusText}`);
            }
        } catch (error) {
            console.error("Error saving cart to database:", error);
        }
    };

    const fetchCartFromDB = async () => {
        if (!currentUserId) return;

        try {
            const response = await fetch(`http://127.0.0.1:8080/cart/${currentUserId}`);
            if (!response.ok) {
                throw new Error(`Error fetching cart: ${response.statusText}`);
            }
            const data = await response.json();
            setCartItems(data);  // Set cart items based on response
        } catch (error) {
            console.error("Error fetching cart from database:", error);
        }
    };

    useEffect(() => {
        if (currentUserId) {
            console.log("Saving cart to DB with cartItems:", cartItems, "and currentUserId:", currentUserId);
            saveCartToDB();
        } else {
            console.log("User is not logged in. Skipping saveCartToDB.");
        }
    }, [cartItems, currentUserId]);

    const handleLogin = (userId) => {
        fetchCartFromDB();  // Fetch the cart from the database upon login
    };

    return (
        <CartContext.Provider value={{ cartItems, addToCart, updateItemQuantity, removeFromCart, handleLogin }}>
            {children}
        </CartContext.Provider>
    );
};
