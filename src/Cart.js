import React from 'react';
import { useCart } from './CartContext';
import './Cart.css';

const Cart = ({ onClose }) => {
    const { cartItems, updateItemQuantity, removeFromCart } = useCart();
    const subtotal = cartItems.reduce((total, item) => total + item.price * item.quantity, 0);

    const handleQuantityChange = (itemId, quantity) => {
        updateItemQuantity(itemId, Number(quantity));
    };

    return (
        <div className="cart-sidebar open">
            <div className="cart-header">
                <h2>Your Cart</h2>
                <button className="close-btn" onClick={onClose}>Close</button>
            </div>
            <div className="cart-items">
                {cartItems.length === 0 ? (
                    <p>No items in your cart</p>
                ) : (
                    cartItems.map((item) => (
                        <div key={item.id} className="cart-item">
                            <img src={`/Images/p${item.product_id}.jpg`} alt={item.title} className="cart-item-image" onError={(e) => e.target.src = '/images/default.jpg'}/>
                            <div className="cart-item-details">
                                <p className="cart-item-title" title={item.title}>{item.title}</p>
                                <p className="cart-item-price">
                                    ${item.price.toFixed(2)} x {item.quantity} = ${(item.price * item.quantity).toFixed(2)}
                                </p>
                                <div className="cart-item-controls">
                                    <label>
                                        Quantity:
                                        <select
                                            value={item.quantity}
                                            onChange={(e) => handleQuantityChange(item.id, e.target.value)}
                                            className="quantity-dropdown"
                                        >
                                            {[...Array(10)].map((_, i) => (
                                                <option key={i + 1} value={i + 1}>
                                                    {i + 1}
                                                </option>
                                            ))}
                                        </select>
                                    </label>
                                    <button
                                        className="remove-btn"
                                        onClick={() => removeFromCart(item.product_id)}
                                    >
                                        X
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))
                )}
            </div>
            <div className="cart-footer">
                <p className="subtotal">Subtotal: ${subtotal.toFixed(2)}</p>
                <button className="checkout-btn">Checkout</button>
            </div>
        </div>
    );
};

export default Cart;
