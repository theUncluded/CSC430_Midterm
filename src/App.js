import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './Header';
import ProductList from './ProductList';
import ProductGrid from './ProductGrid';
import AdminPage from './AdminPage';
import Checkout from './Checkout';
import { ProductProvider } from './ProductContext';
import { CartProvider } from './CartContext'; // Import CartProvider
import './App.css';

function App() {
    return (
        <ProductProvider>
            <CartProvider> {/* Wrap with CartProvider to share cart state globally */}
                <Router>
                    <div className="App">
                        <Header />
                        <Routes>
                            <Route path="/" element={<ProductGrid />} /> {/* Home page as ProductGrid */}
                            <Route path="/products" element={<ProductList />} />
                            <Route path="/admin" element={<AdminPage />} />
                            <Route path="/checkout" element={<Checkout />} />
                        </Routes>
                    </div>
                </Router>
            </CartProvider>
        </ProductProvider>
    );
}

export default App;
