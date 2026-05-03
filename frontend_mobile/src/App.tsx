/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect } from 'react';
import { ArrowLeft, Eye, EyeOff, ShoppingBasket, ShoppingCart, Search, Home, User, Trash2, ChevronRight, Phone, MapPin, Pencil, LogOut } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

type Screen = 'splash' | 'login' | 'register' | 'home' | 'cart' | 'checkout' | 'order_details' | 'profile' | 'product_details';
type CartTab = 'current' | 'history';

interface Product {
  id: number;
  name: string;
  price: string;
  priceNum: number;
  image: string;
  category: string;
  description: string;
}

interface CartItem extends Product {
  quantity: number;
}

interface Order {
  id: string;
  total: string;
  date: string;
  itemCount: number;
  status: 'Kutilmoqda' | 'Yetkazildi' | 'Bekor qilindi';
  items: CartItem[];
}

const PRODUCTS: Product[] = [
  { id: 1, name: 'Elektronika Then', price: '180 196 so\'m', priceNum: 180196, image: 'https://picsum.photos/seed/elec1/300/200', category: 'Elektronika', description: 'One prove decision shake growth practice book.' },
  { id: 2, name: 'Elektronika Author', price: '121 151 so\'m', priceNum: 121151, image: 'https://picsum.photos/seed/elec2/300/200', category: 'Elektronika', description: 'High quality electronic device with advanced features.' },
  { id: 3, name: 'Elektronika Us', price: '177 593 so\'m', priceNum: 177593, image: 'https://picsum.photos/seed/elec3/300/200', category: 'Elektronika', description: 'Reliable and durable electronics for everyday use.' },
  { id: 4, name: 'Elektronika Physical', price: '67 071 so\'m', priceNum: 67071, image: 'https://picsum.photos/seed/elec4/300/200', category: 'Elektronika', description: 'Compact and powerful electronic solution.' },
  { id: 5, name: 'Oziq-ovqat Floor', price: '143 315 so\'m', priceNum: 143315, image: 'https://picsum.photos/seed/food1/300/200', category: 'Oziq-ovqat', description: 'Fresh and organic food products for your family.' },
  { id: 6, name: 'Oziq-ovqat Black', price: '42 411 so\'m', priceNum: 42411, image: 'https://picsum.photos/seed/food2/300/200', category: 'Oziq-ovqat', description: 'Premium quality ingredients for delicious meals.' },
  { id: 7, name: 'Kartoshka', price: '2 000 so\'m', priceNum: 2000, image: 'https://picsum.photos/seed/potato/300/200', category: 'Oziq-ovqat', description: 'Fresh local potatoes, perfect for any dish.' },
  { id: 8, name: 'Kitoblar Staff', price: '85 000 so\'m', priceNum: 85000, image: 'https://picsum.photos/seed/book1/300/200', category: 'Kitoblar', description: 'Educational and inspiring books for all ages.' },
  { id: 9, name: 'Kitoblar Machine', price: '92 000 so\'m', priceNum: 92000, image: 'https://picsum.photos/seed/book2/300/200', category: 'Kitoblar', description: 'Deep dive into technology and machinery.' },
  { id: 10, name: 'Kameralar h8c', price: '202 so\'m', priceNum: 202, image: 'https://picsum.photos/seed/cam1/300/200', category: 'Kameralar', description: 'Smart security camera with night vision.' },
  { id: 11, name: 'Kamera Pro', price: '1 200 000 so\'m', priceNum: 1200000, image: 'https://picsum.photos/seed/cam2/300/200', category: 'Kameralar', description: 'Professional grade camera for high-quality video.' },
  { id: 12, name: 'Futbolka', price: '50 000 so\'m', priceNum: 50000, image: 'https://picsum.photos/seed/shirt/300/200', category: 'Kiyim-kechak', description: 'Comfortable cotton t-shirt for daily wear.' },
  { id: 13, name: 'Shim', price: '120 000 so\'m', priceNum: 120000, image: 'https://picsum.photos/seed/pants/300/200', category: 'Kiyim-kechak', description: 'Stylish and durable pants for any occasion.' },
];

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

export default function App() {
  const [screen, setScreen] = useState<Screen>('splash');
  const [activeCategory, setActiveCategory] = useState<string | number>('Barchasi');
  const [categories, setCategories] = useState<{ id: number, name: string }[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [showPassword, setShowPassword] = useState(false);
  const [cartTab, setCartTab] = useState<CartTab>('current');
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [dialogQty, setDialogQty] = useState(1);
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [productForDetails, setProductForDetails] = useState<Product | null>(null);
  const [currentUser, setCurrentUser] = useState<any>(null);

  // Cart and History states
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [orderHistory, setOrderHistory] = useState<Order[]>([]);

  // Form states
  const [formData, setFormData] = useState({
    fullName: '',
    phone: '',
    password: '',
    address: ''
  });

  // Fetch initial data
  useEffect(() => {
    fetchCategories();
    fetchProducts();
  }, []);

  const fetchCategories = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/categories`);
      if (response.ok) {
        const data = await response.json();
        setCategories(data);
      }
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const fetchProducts = async (catId?: number, search?: string) => {
    try {
      let url = `${API_BASE_URL}/products`;
      const params = new URLSearchParams();
      if (catId) params.append('category_id', catId.toString());
      if (search) params.append('search', search);
      if (params.toString()) url += `?${params.toString()}`;

      const response = await fetch(url);
      if (response.ok) {
        const data = await response.json();
        const formattedProducts = data.map((p: any) => ({
          ...p,
          price: p.price.toLocaleString('ru-RU').replace(/,/g, ' ') + " so'm",
          priceNum: p.price,
          image: p.image_url || 'https://picsum.photos/seed/product/300/200'
        }));
        setProducts(formattedProducts);
      }
    } catch (error) {
      console.error('Error fetching products:', error);
    }
  };

  useEffect(() => {
    if (activeCategory === 'Barchasi') {
      fetchProducts();
    } else {
      fetchProducts(activeCategory as number);
    }
  }, [activeCategory]);

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      if (searchQuery) {
        fetchProducts(undefined, searchQuery);
      } else if (activeCategory === 'Barchasi') {
        fetchProducts();
      }
    }, 500);

    return () => clearTimeout(delayDebounceFn);
  }, [searchQuery]);

  useEffect(() => {
    if (screen === 'splash') {
      const timer = setTimeout(() => {
        setScreen('register');
      }, 2500);
      return () => clearTimeout(timer);
    }
  }, [screen]);

  useEffect(() => {
    // Scroll to top when category changes
    const scrollContainer = document.querySelector('.overflow-y-auto');
    if (scrollContainer) {
      scrollContainer.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }, [activeCategory, screen]);

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleAuth = async () => {
    try {
      const endpoint = screen === 'login' ? '/customers/login' : '/customers';
      const body = screen === 'login'
        ? { phone: formData.phone, password: formData.password }
        : { full_name: formData.fullName, phone: formData.phone, password: formData.password, default_address: formData.address };

      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });

      if (response.ok) {
        const data = await response.json();
        const user = screen === 'login' ? data.customer : data;
        setCurrentUser(user);
        setFormData({
          fullName: user.full_name,
          phone: user.phone,
          password: '',
          address: user.default_address || ''
        });
        setScreen('home');
        fetchOrderHistory(user.id);
      } else {
        const errorData = await response.json();
        let errorMessage = 'Avtorizatsiyada xatolik';
        
        if (errorData.detail) {
          errorMessage = Array.isArray(errorData.detail) 
            ? errorData.detail[0] 
            : errorData.detail;
        } else if (typeof errorData === 'object') {
          // Handle field errors like {"phone": ["..."]}
          const firstKey = Object.keys(errorData)[0];
          if (firstKey && Array.isArray(errorData[firstKey])) {
            errorMessage = errorData[firstKey][0];
          }
        }
        
        alert(errorMessage);
      }
    } catch (error) {
      console.error('Auth error:', error);
      alert('Server bilan aloqa uzildi');
    }
  };

  const addToCart = (product: Product) => {
    setSelectedProduct(product);
    setDialogQty(1);
  };

  const confirmAddToCart = () => {
    if (!selectedProduct) return;

    setCartItems(prev => {
      const existing = prev.find(item => item.id === selectedProduct.id);
      if (existing) {
        return prev.map(item => item.id === selectedProduct.id ? { ...item, quantity: item.quantity + dialogQty } : item);
      }
      return [...prev, { ...selectedProduct, quantity: dialogQty }];
    });

    setSelectedProduct(null);
  };

  const removeFromCart = (id: number) => {
    setCartItems(prev => prev.filter(item => item.id !== id));
  };

  const calculateTotal = () => {
    const total = cartItems.reduce((sum, item) => sum + (item.priceNum * item.quantity), 0);
    return total.toLocaleString('ru-RU').replace(/,/g, ' ') + " so'm";
  };

  const placeOrder = async () => {
    if (!currentUser) {
      setScreen('login');
      return;
    }

    try {
      const body = {
        customer_id: currentUser.id,
        items: cartItems.map(item => ({
          product_id: item.id,
          quantity: item.quantity
        }))
      };

      const response = await fetch(`${API_BASE_URL}/orders`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });

      if (response.ok) {
        setCartItems([]);
        fetchOrderHistory(currentUser.id);
        setCartTab('history');
        setScreen('cart');
      } else {
        const error = await response.json();
        alert(error.detail || 'Buyurtma berishda xatolik');
      }
    } catch (error) {
      console.error('Order error:', error);
      alert('Server bilan aloqa uzildi');
    }
  };

  const fetchOrderHistory = async (customerId: number) => {
    try {
      const response = await fetch(`${API_BASE_URL}/orders/history?customer_id=${customerId}`);
      if (response.ok) {
        const data = await response.json();
        const formattedOrders = data.map((o: any) => ({
          ...o,
          total: o.total_price.toLocaleString('ru-RU').replace(/,/g, ' ') + " so'm",
          date: o.created_at.split('T')[0],
          itemCount: o.items.reduce((sum: number, i: any) => sum + i.quantity, 0),
          status: o.status === 'new' ? 'Kutilmoqda' : o.status,
          items: o.items.map((i: any) => ({
            ...i,
            name: i.product_name,
            price: i.unit_price.toLocaleString('ru-RU').replace(/,/g, ' ') + " so'm",
            priceNum: i.unit_price,
            image: i.image || 'https://picsum.photos/seed/item/300/200'
          }))
        }));
        setOrderHistory(formattedOrders);
      }
    } catch (error) {
      console.error('Error fetching history:', error);
    }
  };

  return (
    <div className="min-h-screen bg-[#f8f9fa] flex items-center justify-center font-sans overflow-hidden">
      <AnimatePresence mode="wait">
        {screen === 'splash' ? (
          <motion.div
            key="splash"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0, scale: 1.1 }}
            transition={{ duration: 0.5 }}
            className="fixed inset-0 bg-[#00964b] flex flex-col items-center justify-center p-6 text-white z-50"
          >
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.2, duration: 0.6 }}
              className="flex flex-col items-center"
            >
              <div className="relative mb-6">
                <div className="w-32 h-32 bg-white/20 rounded-full blur-2xl absolute -inset-4 animate-pulse" />
                <div className="relative bg-white p-6 rounded-3xl shadow-2xl transform -rotate-3">
                  <ShoppingBasket className="w-20 h-20 text-[#00964b]" strokeWidth={1.5} />
                  <div className="absolute -top-2 -right-2 bg-red-500 w-6 h-6 rounded-full border-2 border-white" />
                  <div className="absolute -bottom-1 -left-1 bg-yellow-400 w-8 h-4 rounded-lg border-2 border-white transform rotate-12" />
                </div>
              </div>

              <h1 className="text-8xl font-black italic tracking-tighter mb-8 drop-shadow-lg">
                Tez
              </h1>

              <div className="text-center max-w-[250px]">
                <p className="text-xl font-medium leading-tight opacity-90">
                  Tez va ishonchli
                </p>
                <p className="text-xl font-medium leading-tight opacity-90">
                  bozor yetkazib berish
                </p>
              </div>
            </motion.div>

            <motion.div
              initial={{ width: 0 }}
              animate={{ width: "100px" }}
              transition={{ duration: 2, ease: "linear" }}
              className="h-1 bg-white/30 rounded-full mt-12 overflow-hidden"
            >
              <div className="h-full bg-white w-full" />
            </motion.div>
          </motion.div>
        ) : screen === 'login' ? (
          <motion.div
            key="login"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            transition={{ duration: 0.3 }}
            className="w-full max-w-[400px] bg-white rounded-2xl shadow-2xl overflow-hidden flex flex-col min-h-[600px]"
          >
            <div className="p-6 pb-0">
              <button className="p-2 -ml-2 hover:bg-gray-100 rounded-full transition-colors cursor-pointer">
                <ArrowLeft className="w-6 h-6 text-gray-800" />
              </button>
            </div>

            <div className="p-8 flex-grow">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Dasturga kirish
              </h1>
              <p className="text-gray-500 text-sm mb-8">
                Davom etish uchun ma'lumotlaringizni kiriting
              </p>

              <div className="space-y-4">
                <input
                  type="tel"
                  placeholder="Telefon raqam"
                  value={formData.phone}
                  onChange={(e) => handleInputChange('phone', e.target.value)}
                  className="w-full bg-[#f4f6f9] border-none rounded-xl py-4 px-5 text-gray-800 placeholder-gray-400 focus:ring-2 focus:ring-emerald-500 outline-none transition-all"
                />

                <div className="relative">
                  <input
                    type={showPassword ? "text" : "password"}
                    placeholder="Parol"
                    value={formData.password}
                    onChange={(e) => handleInputChange('password', e.target.value)}
                    className="w-full bg-[#f4f6f9] border-none rounded-xl py-4 px-5 pr-12 text-gray-800 placeholder-gray-400 focus:ring-2 focus:ring-emerald-500 outline-none transition-all"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-4 top-1/2 -translate-y-1/2 text-emerald-600 hover:text-emerald-700 cursor-pointer"
                  >
                    {showPassword ? <EyeOff className="w-6 h-6" /> : <Eye className="w-6 h-6" />}
                  </button>
                </div>
              </div>
            </div>

            <div className="p-8 pt-0 space-y-4">
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={handleAuth}
                className="w-full bg-[#00964b] hover:bg-[#008542] text-white font-semibold py-4 rounded-xl transition-colors shadow-lg shadow-emerald-900/20 cursor-pointer"
              >
                Kirish
              </motion.button>
              <p className="text-center text-sm text-gray-500">
                Akkauntingiz yo'qmi?{' '}
                <button
                  onClick={() => setScreen('register')}
                  className="text-[#00964b] font-bold hover:underline cursor-pointer"
                >
                  Ro'yxatdan o'tish
                </button>
              </p>
            </div>
          </motion.div>
        ) : screen === 'register' ? (
          <motion.div
            key="register"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
            className="w-full max-w-[400px] bg-white rounded-2xl shadow-2xl overflow-hidden flex flex-col min-h-[600px]"
          >
            <div className="p-8 pt-12 flex-grow">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Xush kelibsiz!
              </h1>
              <p className="text-gray-500 text-sm mb-8">
                Davom etish uchun ma'lumotlaringizni kiriting
              </p>

              <div className="space-y-4">
                <input
                  type="text"
                  placeholder="To'liq ism"
                  value={formData.fullName}
                  onChange={(e) => handleInputChange('fullName', e.target.value)}
                  className="w-full bg-[#f4f6f9] border-none rounded-xl py-4 px-5 text-gray-800 placeholder-gray-400 focus:ring-2 focus:ring-emerald-500 outline-none transition-all"
                />

                <input
                  type="tel"
                  placeholder="Telefon raqam"
                  value={formData.phone}
                  onChange={(e) => handleInputChange('phone', e.target.value)}
                  className="w-full bg-[#f4f6f9] border-none rounded-xl py-4 px-5 text-gray-800 placeholder-gray-400 focus:ring-2 focus:ring-emerald-500 outline-none transition-all"
                />

                <div className="relative">
                  <input
                    type={showPassword ? "text" : "password"}
                    placeholder="Parol"
                    value={formData.password}
                    onChange={(e) => handleInputChange('password', e.target.value)}
                    className="w-full bg-[#f4f6f9] border-none rounded-xl py-4 px-5 pr-12 text-gray-800 placeholder-gray-400 focus:ring-2 focus:ring-emerald-500 outline-none transition-all"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-4 top-1/2 -translate-y-1/2 text-emerald-600 hover:text-emerald-700 cursor-pointer"
                  >
                    {showPassword ? <EyeOff className="w-6 h-6" /> : <Eye className="w-6 h-6" />}
                  </button>
                </div>

                <textarea
                  placeholder="Manzil"
                  value={formData.address}
                  onChange={(e) => handleInputChange('address', e.target.value)}
                  rows={4}
                  className="w-full bg-[#f4f6f9] border-none rounded-xl py-4 px-5 text-gray-800 placeholder-gray-400 focus:ring-2 focus:ring-emerald-500 outline-none transition-all resize-none"
                />
              </div>
            </div>

            <div className="p-8 pt-0 space-y-4">
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={handleAuth}
                className="w-full bg-[#00964b] hover:bg-[#008542] text-white font-semibold py-4 rounded-xl transition-colors shadow-lg shadow-emerald-900/20 cursor-pointer"
              >
                Ro'yxatdan o'tish
              </motion.button>
              <p className="text-center text-sm text-gray-500">
                Akkauntingiz bormi?{' '}
                <button
                  onClick={() => setScreen('login')}
                  className="text-[#00964b] font-bold hover:underline cursor-pointer"
                >
                  Kirish
                </button>
              </p>
            </div>
          </motion.div>
        ) : screen === 'home' ? (
          <motion.div
            key="home"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="w-full h-screen bg-white flex flex-col max-w-[500px] shadow-2xl relative"
          >
            {/* Home Header */}
            <div className="px-6 py-4 flex items-center justify-between bg-white sticky top-0 z-10">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 bg-[#00964b] rounded-lg flex items-center justify-center">
                  <ShoppingBasket className="w-5 h-5 text-white" />
                </div>
                <h2 className="text-xl font-bold text-[#1e252b]">Tez Bozor</h2>
              </div>
              <button
                onClick={() => setScreen('cart')}
                className="p-2 hover:bg-gray-100 rounded-full transition-colors relative"
              >
                <ShoppingCart className="w-6 h-6 text-[#00964b]" />
                {cartItems.length > 0 && (
                  <span className="absolute top-1 right-1 w-4 h-4 bg-red-500 rounded-full border border-white text-[10px] text-white flex items-center justify-center">
                    {cartItems.length}
                  </span>
                )}
              </button>
            </div>

            {/* Scrollable Content */}
            <div className="flex-grow overflow-y-auto pb-24">
              {/* Search Bar */}
              <div className="px-6 mb-6">
                <div className="relative">
                  <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Qidirish..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full bg-[#f4f6f9] border-none rounded-xl py-3 pl-12 pr-4 text-gray-800 placeholder-gray-400 focus:ring-2 focus:ring-emerald-500 outline-none"
                  />
                </div>
              </div>

              {/* Categories */}
              <div className="px-6 mb-8 overflow-x-auto flex gap-3 no-scrollbar">
                <button
                  onClick={() => setActiveCategory('Barchasi')}
                  className={`px-6 py-2 rounded-xl font-semibold whitespace-nowrap transition-all ${activeCategory === 'Barchasi'
                    ? 'bg-[#00964b] text-white'
                    : 'bg-[#f4f6f9] text-gray-600 hover:bg-gray-200'
                    }`}
                >
                  Barchasi
                </button>
                {categories.map((cat) => (
                  <button
                    key={cat.id}
                    onClick={() => setActiveCategory(cat.id)}
                    className={`px-6 py-2 rounded-xl font-semibold whitespace-nowrap transition-all ${activeCategory === cat.id
                      ? 'bg-[#00964b] text-white'
                      : 'bg-[#f4f6f9] text-gray-600 hover:bg-gray-200'
                      }`}
                  >
                    {cat.name}
                  </button>
                ))}
              </div>

              {searchQuery ? (
                <div className="px-6">
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="text-2xl font-bold text-gray-900">Qidiruv natijalari</h3>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    {products.map((product) => (
                      <div
                        key={product.id}
                        onClick={() => {
                          setProductForDetails(product);
                          setScreen('product_details');
                        }}
                        className="bg-white rounded-[24px] border border-gray-100 shadow-sm overflow-hidden flex flex-col cursor-pointer"
                      >
                        <div className="aspect-square overflow-hidden">
                          <img src={product.image} alt={product.name} className="w-full h-full object-cover" />
                        </div>
                        <div className="p-4 flex flex-col flex-grow">
                          <h4 className="font-bold text-gray-800 mb-1 text-sm line-clamp-2 min-h-[40px]">{product.name}</h4>
                          <p className="text-[#00964b] font-bold text-sm mb-4">{product.price}</p>
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              addToCart(product);
                            }}
                            className="w-full bg-[#00964b] text-white text-xs font-bold py-3 rounded-xl hover:bg-[#008542] transition-colors mt-auto"
                          >
                            + Savatga
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                  {products.length === 0 && (
                    <div className="text-center py-20">
                      <p className="text-gray-400 font-medium">Hech narsa topilmadi</p>
                    </div>
                  )}
                </div>
              ) : activeCategory === 'Barchasi' ? (
                <>
                  {/* Top Products Section */}
                  <div className="mb-8">
                    <div className="px-6 flex items-center justify-between mb-4">
                      <h3 className="text-xl font-bold text-gray-900">Top Mahsulotlar</h3>
                    </div>
                    <div className="px-6 overflow-x-auto flex gap-4 no-scrollbar pb-2">
                      {products.filter(p => (p as any).is_top).slice(0, 10).map((product) => (
                        <div
                          key={`top-${product.id}`}
                          onClick={() => {
                            setProductForDetails(product);
                            setScreen('product_details');
                          }}
                          className="min-w-[200px] bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden cursor-pointer"
                        >
                          <img src={product.image} alt={product.name} className="w-full h-32 object-cover" />
                          <div className="p-4">
                            <h4 className="font-semibold text-gray-800 mb-1 truncate">{product.name}</h4>
                            <p className="text-[#00964b] font-bold text-sm mb-3">{product.price}</p>
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                addToCart(product);
                              }}
                              className="w-full bg-[#00964b] text-white text-xs font-bold py-2 rounded-lg hover:bg-[#008542] transition-colors"
                            >
                              + Savatga
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Sections by Category */}
                  {categories.map((cat) => {
                    const categoryProducts = products.filter(p => (p as any).category?.id === cat.id);
                    if (categoryProducts.length === 0) return null;

                    return (
                      <div key={cat.id} className="mb-8">
                        <div className="px-6 flex items-center justify-between mb-4">
                          <h3 className="text-xl font-bold text-gray-900">{cat.name}</h3>
                          <button onClick={() => setActiveCategory(cat.id)} className="text-[#00964b] font-semibold text-sm">Barchasi</button>
                        </div>
                        <div className="px-6 overflow-x-auto flex gap-4 no-scrollbar pb-2">
                          {categoryProducts.slice(0, 3).map((product) => (
                            <div
                              key={`${cat.id}-${product.id}`}
                              onClick={() => {
                                setProductForDetails(product);
                                setScreen('product_details');
                              }}
                              className="min-w-[180px] bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden cursor-pointer"
                            >
                              <img src={product.image} alt={product.name} className="w-full h-32 object-cover" />
                              <div className="p-4">
                                <h4 className="font-semibold text-gray-800 mb-1 text-sm truncate">{product.name}</h4>
                                <p className="text-[#00964b] font-bold text-xs mb-3">{product.price}</p>
                                <button
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    addToCart(product);
                                  }}
                                  className="w-full bg-[#00964b] text-white text-xs font-bold py-2 rounded-lg hover:bg-[#008542] transition-colors"
                                >
                                  + Savatga
                                </button>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    );
                  })}
                </>
              ) : (
                <div className="px-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-xl font-bold text-gray-900">
                      {categories.find(c => c.id === activeCategory)?.name || activeCategory}
                    </h3>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    {products.map((product) => (
                      <div
                        key={product.id}
                        onClick={() => {
                          setProductForDetails(product);
                          setScreen('product_details');
                        }}
                        className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden cursor-pointer"
                      >
                        <img src={product.image} alt={product.name} className="w-full h-32 object-cover" />
                        <div className="p-4">
                          <h4 className="font-semibold text-gray-800 mb-1 text-sm truncate">{product.name}</h4>
                          <p className="text-[#00964b] font-bold text-xs mb-3">{product.price}</p>
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              addToCart(product);
                            }}
                            className="w-full bg-[#00964b] text-white text-xs font-bold py-2 rounded-lg hover:bg-[#008542] transition-colors"
                          >
                            + Savatga
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Bottom Navigation */}
            <div className="absolute bottom-0 left-0 right-0 bg-white border-t border-gray-100 px-8 py-3 flex items-center justify-between">
              <button className="flex flex-col items-center gap-1 text-[#00964b]">
                <div className="bg-emerald-50 p-2 rounded-xl">
                  <Home className="w-6 h-6" />
                </div>
                <span className="text-[10px] font-bold">Asosiy</span>
              </button>
              <button
                onClick={() => setScreen('cart')}
                className="flex flex-col items-center gap-1 text-gray-400 hover:text-[#00964b] transition-colors"
              >
                <ShoppingCart className="w-6 h-6" />
                <span className="text-[10px] font-bold">Savat</span>
              </button>
              <button
                onClick={() => setScreen('profile')}
                className="flex flex-col items-center gap-1 text-gray-400 hover:text-[#00964b] transition-colors"
              >
                <User className="w-6 h-6" />
                <span className="text-[10px] font-bold">Profil</span>
              </button>
            </div>
          </motion.div>
        ) : screen === 'cart' ? (
          <motion.div
            key="cart"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            className="w-full h-screen bg-[#f8f9fa] flex flex-col max-w-[500px] shadow-2xl relative"
          >
            {/* Cart Header */}
            <div className="px-6 py-4 flex items-center justify-between bg-white sticky top-0 z-10">
              <div className="flex items-center gap-4">
                <button
                  onClick={() => setScreen('home')}
                  className="p-2 -ml-2 hover:bg-gray-100 rounded-full transition-colors cursor-pointer"
                >
                  <ArrowLeft className="w-6 h-6 text-gray-800" />
                </button>
                <h2 className="text-xl font-bold text-gray-900">Savat va Tarix</h2>
              </div>
              <div className="relative">
                <ShoppingCart className="w-6 h-6 text-[#00964b]" />
                {cartItems.length > 0 && (
                  <span className="absolute -top-2 -right-2 w-5 h-5 bg-red-500 rounded-full border-2 border-white text-[10px] text-white flex items-center justify-center font-bold">
                    {cartItems.length}
                  </span>
                )}
              </div>
            </div>

            {/* Tab Switcher */}
            <div className="px-6 py-4">
              <div className="bg-white p-1 rounded-xl flex shadow-sm">
                <button
                  onClick={() => setCartTab('current')}
                  className={`flex-1 py-3 rounded-lg font-bold transition-all ${cartTab === 'current' ? 'bg-[#00964b] text-white shadow-md' : 'text-gray-400'
                    }`}
                >
                  Hozirgi
                </button>
                <button
                  onClick={() => setCartTab('history')}
                  className={`flex-1 py-3 rounded-lg font-bold transition-all ${cartTab === 'history' ? 'bg-[#00964b] text-white shadow-md' : 'text-gray-400'
                    }`}
                >
                  Tarix
                </button>
              </div>
            </div>

            {/* Tab Content */}
            <div className="flex-grow overflow-y-auto px-6 pb-40">
              {cartTab === 'current' ? (
                <div className="space-y-4">
                  {cartItems.length > 0 ? (
                    cartItems.map((item) => (
                      <div key={item.id} className="bg-white p-4 rounded-2xl shadow-sm border border-gray-100 flex gap-4 items-center">
                        <img src={item.image} alt={item.name} className="w-20 h-20 rounded-xl object-cover" />
                        <div className="flex-grow">
                          <div className="flex justify-between items-start mb-2">
                            <h4 className="font-bold text-gray-900">{item.name}</h4>
                            <button
                              onClick={() => removeFromCart(item.id)}
                              className="text-red-500 hover:bg-red-50 rounded-lg p-1 transition-colors"
                            >
                              <Trash2 className="w-5 h-5" />
                            </button>
                          </div>
                          <div className="flex justify-between items-center">
                            <span className="text-[#00964b] font-bold">{item.price}</span>
                            <span className="text-gray-400 font-bold">x{item.quantity}</span>
                          </div>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="text-center py-20">
                      <ShoppingBasket className="w-16 h-16 text-gray-200 mx-auto mb-4" />
                      <p className="text-gray-400 font-medium">Savatchangiz bo'sh</p>
                    </div>
                  )}
                </div>
              ) : (
                <div className="space-y-4">
                  {orderHistory.map((order) => (
                    <button
                      key={order.id}
                      onClick={() => {
                        setSelectedOrder(order);
                        setScreen('order_details');
                      }}
                      className="w-full text-left bg-white p-5 rounded-2xl shadow-sm border border-gray-100 relative hover:bg-gray-50 transition-colors"
                    >
                      <div className="flex justify-between items-start mb-4">
                        <span className="text-gray-400 font-bold">#{order.id}</span>
                        <span className="bg-orange-50 text-orange-500 px-3 py-1 rounded-lg text-xs font-bold">
                          {order.status}
                        </span>
                      </div>
                      <h4 className="text-xl font-bold text-gray-900 mb-2">{order.total}</h4>
                      <div className="flex justify-between items-center text-gray-400 text-sm font-medium">
                        <span>{order.date} · {order.itemCount} mahsulot</span>
                        <ChevronRight className="w-5 h-5" />
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Bottom Checkout Card (Only for Current Tab) */}
            {cartTab === 'current' && cartItems.length > 0 && (
              <div className="absolute bottom-24 left-6 right-6 bg-white p-6 rounded-3xl shadow-xl border border-gray-100">
                <div className="flex justify-between items-center mb-6">
                  <span className="text-gray-400 font-bold text-lg">Jami:</span>
                  <span className="text-[#00964b] font-black text-2xl">{calculateTotal()}</span>
                </div>
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => setScreen('checkout')}
                  className="w-full bg-[#00964b] text-white font-black py-4 rounded-2xl shadow-lg shadow-emerald-900/20 cursor-pointer text-lg"
                >
                  Buyurtma berish
                </motion.button>
              </div>
            )}

            {/* Bottom Navigation */}
            <div className="absolute bottom-0 left-0 right-0 bg-white border-t border-gray-100 px-8 py-3 flex items-center justify-between">
              <button
                onClick={() => setScreen('home')}
                className="flex flex-col items-center gap-1 text-gray-400 hover:text-[#00964b] transition-colors"
              >
                <Home className="w-6 h-6" />
                <span className="text-[10px] font-bold">Asosiy</span>
              </button>
              <button className="flex flex-col items-center gap-1 text-[#00964b]">
                <div className="bg-emerald-50 p-2 rounded-xl">
                  <ShoppingCart className="w-6 h-6" />
                </div>
                <span className="text-[10px] font-bold">Savat</span>
              </button>
              <button
                onClick={() => setScreen('profile')}
                className="flex flex-col items-center gap-1 text-gray-400 hover:text-[#00964b] transition-colors"
              >
                <User className="w-6 h-6" />
                <span className="text-[10px] font-bold">Profil</span>
              </button>
            </div>
          </motion.div>
        ) : screen === 'profile' ? (
          <motion.div
            key="profile"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="w-full h-screen bg-[#f8f9fa] flex flex-col max-w-[500px] shadow-2xl relative"
          >
            {/* Header */}
            <div className="px-6 py-4 flex items-center justify-between bg-white sticky top-0 z-10">
              <div className="flex items-center gap-4">
                <button
                  onClick={() => setScreen('home')}
                  className="p-2 -ml-2 hover:bg-gray-100 rounded-full transition-colors cursor-pointer"
                >
                  <ArrowLeft className="w-6 h-6 text-gray-800" />
                </button>
                <h2 className="text-xl font-bold text-gray-900">Shaxsiy kabinet</h2>
              </div>
              <button
                onClick={() => setScreen('cart')}
                className="p-2 hover:bg-gray-100 rounded-full transition-colors relative"
              >
                <ShoppingCart className="w-6 h-6 text-[#00964b]" />
                {cartItems.length > 0 && (
                  <span className="absolute top-1 right-1 w-4 h-4 bg-red-500 rounded-full border border-white text-[10px] text-white flex items-center justify-center">
                    {cartItems.length}
                  </span>
                )}
              </button>
            </div>

            {/* Content */}
            <div className="flex-grow overflow-y-auto px-6 py-8 pb-32">
              {/* Profile Header */}
              <div className="flex flex-col items-center mb-10">
                <div className="w-24 h-24 bg-white rounded-full shadow-lg flex items-center justify-center mb-4 border border-gray-50">
                  <div className="w-16 h-16 bg-[#00964b]/10 rounded-full flex items-center justify-center">
                    <User className="w-10 h-10 text-[#00964b]" />
                  </div>
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-1">
                  {formData.fullName || "Ruslan Joldasbaev"}
                </h3>
                <p className="text-gray-400 font-medium">
                  {formData.phone || "905762708"}
                </p>
              </div>

              {/* Info Card */}
              <div className="bg-white rounded-[32px] p-6 shadow-sm border border-gray-100 mb-8 space-y-6">
                <div className="flex items-center gap-4 bg-[#f4f6f9]/50 p-4 rounded-2xl">
                  <div className="w-10 h-10 bg-white rounded-xl flex items-center justify-center shadow-sm">
                    <User className="w-5 h-5 text-[#00964b]" />
                  </div>
                  <div>
                    <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest leading-none mb-1">
                      TO'LIQ ISM
                    </p>
                    <p className="text-lg font-bold text-gray-900">
                      {formData.fullName || "Ruslan Joldasbaev"}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-4 bg-[#f4f6f9]/50 p-4 rounded-2xl">
                  <div className="w-10 h-10 bg-white rounded-xl flex items-center justify-center shadow-sm">
                    <Phone className="w-5 h-5 text-[#00964b]" />
                  </div>
                  <div>
                    <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest leading-none mb-1">
                      TELEFON
                    </p>
                    <p className="text-lg font-bold text-gray-900">
                      {formData.phone || "905762708"}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-4 bg-[#f4f6f9]/50 p-4 rounded-2xl">
                  <div className="w-10 h-10 bg-white rounded-xl flex items-center justify-center shadow-sm">
                    <MapPin className="w-5 h-5 text-orange-500" />
                  </div>
                  <div>
                    <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest leading-none mb-1">
                      MANZIL
                    </p>
                    <p className="text-lg font-bold text-gray-900">
                      {formData.address || "Shimbay city"}
                    </p>
                  </div>
                </div>

                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full bg-[#00964b] text-white font-bold py-4 rounded-2xl shadow-lg shadow-emerald-900/10 cursor-pointer flex items-center justify-center gap-2"
                >
                  <Pencil className="w-5 h-5" />
                  Tahrirlash
                </motion.button>
              </div>

              {/* Logout */}
              <button
                onClick={() => setScreen('login')}
                className="w-full flex items-center justify-center gap-3 text-red-400 font-bold py-4 hover:bg-red-50 rounded-2xl transition-colors cursor-pointer"
              >
                <LogOut className="w-6 h-6" />
                <span className="text-lg">Tizimdan chiqish</span>
              </button>
            </div>

            {/* Bottom Navigation */}
            <div className="absolute bottom-0 left-0 right-0 bg-white border-t border-gray-100 px-8 py-3 flex items-center justify-between">
              <button
                onClick={() => setScreen('home')}
                className="flex flex-col items-center gap-1 text-gray-400 hover:text-[#00964b] transition-colors"
              >
                <Home className="w-6 h-6" />
                <span className="text-[10px] font-bold">Asosiy</span>
              </button>
              <button
                onClick={() => {
                  setScreen('cart');
                  setCartTab('current');
                }}
                className="flex flex-col items-center gap-1 text-gray-400 hover:text-[#00964b] transition-colors"
              >
                <ShoppingCart className="w-6 h-6" />
                <span className="text-[10px] font-bold">Savat</span>
              </button>
              <button className="flex flex-col items-center gap-1 text-[#00964b]">
                <div className="bg-emerald-50 p-2 rounded-xl">
                  <User className="w-6 h-6" />
                </div>
                <span className="text-[10px] font-bold">Profil</span>
              </button>
            </div>
          </motion.div>
        ) : screen === 'product_details' ? (
          <motion.div
            key="product_details"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="w-full h-screen bg-[#f8f9fa] flex flex-col max-w-[500px] shadow-2xl relative"
          >
            {/* Header */}
            <div className="px-6 py-4 flex items-center justify-between bg-white sticky top-0 z-10">
              <div className="flex items-center gap-4">
                <button
                  onClick={() => setScreen('home')}
                  className="p-2 -ml-2 hover:bg-gray-100 rounded-full transition-colors cursor-pointer"
                >
                  <ArrowLeft className="w-6 h-6 text-gray-800" />
                </button>
                <h2 className="text-xl font-bold text-gray-900">Tez Bozor</h2>
              </div>
              <button
                onClick={() => setScreen('cart')}
                className="p-2 hover:bg-gray-100 rounded-full transition-colors relative"
              >
                <ShoppingCart className="w-6 h-6 text-gray-800" />
                {cartItems.length > 0 && (
                  <span className="absolute top-1 right-1 w-4 h-4 bg-red-500 rounded-full border border-white text-[10px] text-white flex items-center justify-center">
                    {cartItems.length}
                  </span>
                )}
              </button>
            </div>

            {/* Content */}
            <div className="flex-grow overflow-y-auto">
              <div className="w-full aspect-square overflow-hidden">
                <img
                  src={productForDetails?.image}
                  alt={productForDetails?.name}
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="bg-white rounded-t-[40px] -mt-10 relative z-10 p-8 min-h-full shadow-[0_-10px_40px_rgba(0,0,0,0.05)]">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">{productForDetails?.name}</h1>
                <p className="text-[#00964b] text-2xl font-bold mb-6">{productForDetails?.price}</p>

                <div className="w-full h-[1px] bg-gray-100 mb-6" />

                <h3 className="text-xl font-bold text-gray-900 mb-4">Mahsulot haqida</h3>
                <p className="text-gray-400 leading-relaxed text-lg">
                  {productForDetails?.description}
                </p>
              </div>
            </div>

            {/* Bottom Action */}
            <div className="p-6 bg-[#f8f9fa] pb-24">
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => productForDetails && addToCart(productForDetails)}
                className="w-full bg-[#00964b] text-white font-bold py-5 rounded-2xl shadow-lg shadow-emerald-900/20 cursor-pointer text-xl"
              >
                Savatga qo'shish
              </motion.button>
            </div>

            {/* Bottom Navigation */}
            <div className="absolute bottom-0 left-0 right-0 bg-white border-t border-gray-100 px-8 py-3 flex items-center justify-between">
              <button
                onClick={() => setScreen('home')}
                className="flex flex-col items-center gap-1 text-[#00964b]"
              >
                <div className="bg-emerald-50 p-2 rounded-xl">
                  <Home className="w-6 h-6" />
                </div>
                <span className="text-[10px] font-bold">Asosiy</span>
              </button>
              <button
                onClick={() => {
                  setScreen('cart');
                  setCartTab('current');
                }}
                className="flex flex-col items-center gap-1 text-gray-400 hover:text-[#00964b] transition-colors"
              >
                <ShoppingCart className="w-6 h-6" />
                <span className="text-[10px] font-bold">Savat</span>
              </button>
              <button
                onClick={() => setScreen('profile')}
                className="flex flex-col items-center gap-1 text-gray-400 hover:text-[#00964b] transition-colors"
              >
                <User className="w-6 h-6" />
                <span className="text-[10px] font-bold">Profil</span>
              </button>
            </div>
          </motion.div>
        ) : screen === 'order_details' ? (
          <motion.div
            key="order_details"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="w-full h-screen bg-[#f8f9fa] flex flex-col max-w-[500px] shadow-2xl relative"
          >
            {/* Header */}
            <div className="px-6 py-4 flex items-center justify-between bg-white sticky top-0 z-10">
              <div className="flex items-center gap-4">
                <button
                  onClick={() => setScreen('cart')}
                  className="p-2 -ml-2 hover:bg-gray-100 rounded-full transition-colors cursor-pointer"
                >
                  <ArrowLeft className="w-6 h-6 text-gray-800" />
                </button>
                <h2 className="text-xl font-bold text-gray-900">Buyurtma #{selectedOrder?.id}</h2>
              </div>
              <div className="bg-orange-50 text-orange-500 px-3 py-1 rounded-lg text-xs font-bold">
                {selectedOrder?.status}
              </div>
            </div>

            {/* Content */}
            <div className="flex-grow overflow-y-auto px-6 py-6 pb-24">
              <div className="bg-white rounded-[32px] p-6 shadow-sm border border-gray-100 mb-6">
                <div className="flex justify-between items-center mb-4">
                  <span className="text-gray-400 font-bold">Sana:</span>
                  <span className="text-gray-900 font-bold">{selectedOrder?.date}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 font-bold">Jami summa:</span>
                  <span className="text-[#00964b] font-black text-xl">{selectedOrder?.total}</span>
                </div>
              </div>

              <h3 className="text-lg font-bold text-gray-900 mb-4 px-2">Mahsulotlar</h3>
              <div className="space-y-4">
                {selectedOrder?.items.map((item) => (
                  <div key={item.id} className="bg-white p-4 rounded-2xl shadow-sm border border-gray-100 flex gap-4 items-center">
                    <img src={item.image} alt={item.name} className="w-16 h-16 rounded-xl object-cover" />
                    <div className="flex-grow">
                      <h4 className="font-bold text-gray-900 text-sm mb-1">{item.name}</h4>
                      <div className="flex justify-between items-center">
                        <span className="text-[#00964b] font-bold text-sm">{item.price}</span>
                        <span className="text-gray-400 font-bold text-sm">x{item.quantity}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Bottom Navigation */}
            <div className="absolute bottom-0 left-0 right-0 bg-white border-t border-gray-100 px-8 py-3 flex items-center justify-between">
              <button
                onClick={() => setScreen('home')}
                className="flex flex-col items-center gap-1 text-gray-400 hover:text-[#00964b] transition-colors"
              >
                <Home className="w-6 h-6" />
                <span className="text-[10px] font-bold">Asosiy</span>
              </button>
              <button
                onClick={() => {
                  setScreen('cart');
                  setCartTab('history');
                }}
                className="flex flex-col items-center gap-1 text-[#00964b]"
              >
                <div className="bg-emerald-50 p-2 rounded-xl">
                  <ShoppingCart className="w-6 h-6" />
                </div>
                <span className="text-[10px] font-bold">Savat</span>
              </button>
              <button
                onClick={() => setScreen('profile')}
                className="flex flex-col items-center gap-1 text-gray-400 hover:text-[#00964b] transition-colors"
              >
                <User className="w-6 h-6" />
                <span className="text-[10px] font-bold">Profil</span>
              </button>
            </div>
          </motion.div>
        ) : (
          <motion.div
            key="checkout"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="w-full h-screen bg-[#f8f9fa] flex flex-col max-w-[500px] shadow-2xl relative"
          >
            {/* Checkout Header */}
            <div className="px-6 py-4 flex items-center justify-between bg-white sticky top-0 z-10">
              <div className="flex items-center gap-4">
                <button
                  onClick={() => setScreen('cart')}
                  className="p-2 -ml-2 hover:bg-gray-100 rounded-full transition-colors cursor-pointer"
                >
                  <ArrowLeft className="w-6 h-6 text-gray-800" />
                </button>
                <h2 className="text-xl font-bold text-gray-900">UZ-SHOP</h2>
              </div>
              <div className="relative">
                <ShoppingCart className="w-6 h-6 text-gray-800" />
                {cartItems.length > 0 && (
                  <span className="absolute -top-2 -right-2 w-5 h-5 bg-red-500 rounded-full border-2 border-white text-[10px] text-white flex items-center justify-center font-bold">
                    {cartItems.length}
                  </span>
                )}
              </div>
            </div>

            <div className="p-8 flex-grow">
              <h1 className="text-4xl font-bold text-gray-900 mb-10">Tasdiqlash</h1>

              <div className="bg-white rounded-[32px] p-8 shadow-sm border border-gray-100 space-y-8">
                <div>
                  <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-2">
                    QABUL QILUVCHI
                  </p>
                  <p className="text-xl font-bold text-gray-900">
                    {formData.fullName || "Joldasbaev Ruslan"}
                  </p>
                </div>

                <div>
                  <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-2">
                    TELEFON
                  </p>
                  <p className="text-xl font-bold text-gray-900">
                    {formData.phone || "905762708"}
                  </p>
                </div>

                <div>
                  <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-2">
                    MANZIL
                  </p>
                  <p className="text-xl font-bold text-gray-900">
                    {formData.address || "Shimbay city"}
                  </p>
                </div>
              </div>
            </div>

            <div className="p-8 pt-0 pb-24">
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={placeOrder}
                className="w-full bg-[#00964b] text-white font-bold py-5 rounded-2xl shadow-lg shadow-emerald-900/20 cursor-pointer text-xl"
              >
                Tasdiqlash
              </motion.button>
            </div>

            {/* Bottom Navigation */}
            <div className="absolute bottom-0 left-0 right-0 bg-white border-t border-gray-100 px-8 py-3 flex items-center justify-between">
              <button
                onClick={() => setScreen('home')}
                className="flex flex-col items-center gap-1 text-gray-400 hover:text-[#00964b] transition-colors"
              >
                <Home className="w-6 h-6" />
                <span className="text-[10px] font-bold">Asosiy</span>
              </button>
              <button
                onClick={() => {
                  setScreen('cart');
                  setCartTab('current');
                }}
                className="flex flex-col items-center gap-1 text-gray-400 hover:text-[#00964b] transition-colors"
              >
                <ShoppingCart className="w-6 h-6" />
                <span className="text-[10px] font-bold">Savat</span>
              </button>
              <button
                onClick={() => setScreen('profile')}
                className="flex flex-col items-center gap-1 text-gray-400 hover:text-[#00964b] transition-colors"
              >
                <User className="w-6 h-6" />
                <span className="text-[10px] font-bold">Profil</span>
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Add to Cart Dialog */}
      <AnimatePresence>
        {selectedProduct && (
          <div className="fixed inset-0 z-[100] flex items-end justify-center sm:items-center p-0 sm:p-4">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setSelectedProduct(null)}
              className="absolute inset-0 bg-black/40 backdrop-blur-sm"
            />
            <motion.div
              initial={{ y: "100%" }}
              animate={{ y: 0 }}
              exit={{ y: "100%" }}
              transition={{ type: "spring", damping: 25, stiffness: 300 }}
              className="relative w-full max-w-[500px] bg-white rounded-t-[32px] sm:rounded-[32px] p-8 shadow-2xl overflow-hidden"
            >
              <div className="flex gap-6 items-start mb-8">
                <img
                  src={selectedProduct.image}
                  alt={selectedProduct.name}
                  className="w-24 h-24 rounded-2xl object-cover shadow-md"
                />
                <div className="flex-grow">
                  <h3 className="text-xl font-bold text-gray-900 mb-4 leading-tight">
                    {selectedProduct.name}
                  </h3>
                  <div className="flex items-center bg-[#f4f6f9] rounded-xl p-1 w-fit">
                    <button
                      onClick={() => setDialogQty(Math.max(1, dialogQty - 1))}
                      className="w-10 h-10 flex items-center justify-center text-gray-500 hover:text-gray-800 transition-colors"
                    >
                      <span className="text-2xl font-medium">−</span>
                    </button>
                    <span className="w-10 text-center font-bold text-gray-900">{dialogQty}</span>
                    <button
                      onClick={() => setDialogQty(dialogQty + 1)}
                      className="w-10 h-10 flex items-center justify-center text-gray-500 hover:text-gray-800 transition-colors"
                    >
                      <span className="text-2xl font-medium">+</span>
                    </button>
                  </div>
                </div>
              </div>

              <div className="space-y-6">
                <div>
                  <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-4">
                    MA'LUMOTLARNI TEKSHIRING
                  </p>
                  <div className="space-y-3">
                    <div className="bg-[#f4f6f9] rounded-xl py-4 px-5 text-gray-800 font-medium">
                      {formData.fullName || "Joldasbaev Ruslan"}
                    </div>
                    <div className="bg-[#f4f6f9] rounded-xl py-4 px-5 text-gray-800 font-medium">
                      {formData.phone || "905762708"}
                    </div>
                    <div className="bg-[#f4f6f9] rounded-xl py-4 px-5 text-gray-800 font-medium">
                      {formData.address || "Shimbay city"}
                    </div>
                  </div>
                </div>

                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={confirmAddToCart}
                  className="w-full bg-[#00964b] text-white font-bold py-5 rounded-2xl shadow-lg shadow-emerald-900/20 cursor-pointer text-lg"
                >
                  Tasdiqlash va Savatga qo'shish
                </motion.button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}
