import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './Header';
import ProductList from './ProductList';
import ProductGrid from './ProductGrid';
import AdminPage from './AdminPage';
import Checkout from './Checkout';
import { ProductProvider } from './ProductContext';
import { CartProvider } from './CartContext'; // Import CartProvider
import { UserProvider } from './UserContext'; // Import UserProvider

import './App.css';

function App() {
    return (
        <ProductProvider>
                            <UserProvider> {/* Wrap with UserProvider */}
            <CartProvider>

                    <Router>
                        <div className="App">
                            <Header />
                            <Routes>
                                <Route path="/" element={<ProductGrid />} />
                                <Route path="/products" element={<ProductList />} />
                                <Route path="/admin" element={<AdminPage />} />
                                <Route path="/checkout" element={<Checkout />} />
                            </Routes>
                        </div>
                    </Router>
                    </CartProvider>
                </UserProvider>

        </ProductProvider>
    );
}

export default App;
