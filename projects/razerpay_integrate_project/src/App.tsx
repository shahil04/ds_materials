import { useMemo, useState } from 'react';
import {
  ArrowRight,
  ChevronRight,
  Heart,
  Menu,
  Minus,
  Plus,
  Search,
  ShoppingBag,
  ShoppingCart,
  Star,
  Trash2,
  User
} from 'lucide-react';
import { categoryCards, products } from './data/products';
import type { CartItem, Product } from './types';

const currency = (value: number) => `₹${value.toLocaleString('en-IN')}`;
const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:3001';

const priceRanges = [
  { label: 'Under ₹500', value: 'under500' },
  { label: '₹500–₹1,000', value: '500-1000' },
  { label: '₹1,000–₹2,000', value: '1000-2000' },
  { label: '₹2,000+', value: 'above2000' }
];

const sortOptions = [
  'Popular',
  'Newest',
  'Price Low to High',
  'Price High to Low',
  'Rating'
] as const;

const initialFilters = {
  gender: 'All',
  category: 'All',
  size: 'All',
  color: 'All',
  price: 'All',
  sort: 'Popular' as (typeof sortOptions)[number]
};

const getDiscountPercent = (price: number, originalPrice: number) =>
  Math.max(5, Math.round(((originalPrice - price) / originalPrice) * 100));

const getProductById = (id: string) => products.find((product) => product.id === id) || products[0];

function App() {
  const [selectedGender, setSelectedGender] = useState<string>('All');
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [selectedSize, setSelectedSize] = useState<string>('All');
  const [selectedColor, setSelectedColor] = useState<string>('All');
  const [selectedPrice, setSelectedPrice] = useState<string>('All');
  const [sortMode, setSortMode] = useState<(typeof sortOptions)[number]>('Popular');
  const [query, setQuery] = useState('');
  const [selectedProductId, setSelectedProductId] = useState<string>(products[0].id);
  const [cart, setCart] = useState<CartItem[]>([
    {
      id: products[0].id,
      name: products[0].name,
      image: products[0].image,
      price: products[0].price,
      size: 'M',
      color: 'Black',
      quantity: 1
    }
  ]);
  const [checkoutOpen, setCheckoutOpen] = useState(false);
  const [address, setAddress] = useState({
    fullName: 'Aarav Sharma',
    phone: '9876543210',
    address: '24, Rosewood Lane, Andheri East',
    city: 'Mumbai',
    state: 'Maharashtra',
    pincode: '400069'
  });
  const [paymentState, setPaymentState] = useState<string>('');

  const filteredProducts = useMemo(() => {
    const searchTerms = query.trim().toLowerCase();
    const nextProducts = products.filter((product) => {
      const matchesQuery =
        !searchTerms ||
        product.name.toLowerCase().includes(searchTerms) ||
        product.category.toLowerCase().includes(searchTerms) ||
        product.description.toLowerCase().includes(searchTerms);
      const matchesGender = selectedGender === 'All' || product.gender === selectedGender;
      const matchesCategory = selectedCategory === 'All' || product.category === selectedCategory;
      const matchesSize = selectedSize === 'All' || product.sizes.includes(selectedSize);
      const matchesColor = selectedColor === 'All' || product.colors.includes(selectedColor);
      const matchesPrice =
        selectedPrice === 'All' ||
        (selectedPrice === 'under500' && product.price < 500) ||
        (selectedPrice === '500-1000' && product.price >= 500 && product.price <= 1000) ||
        (selectedPrice === '1000-2000' && product.price > 1000 && product.price <= 2000) ||
        (selectedPrice === 'above2000' && product.price > 2000);

      return matchesQuery && matchesGender && matchesCategory && matchesSize && matchesColor && matchesPrice;
    });

    return [...nextProducts].sort((a, b) => {
      switch (sortMode) {
        case 'Newest':
          return b.rating - a.rating;
        case 'Price Low to High':
          return a.price - b.price;
        case 'Price High to Low':
          return b.price - a.price;
        case 'Rating':
          return b.rating - a.rating;
        default:
          return b.rating * 10 + b.price - (a.rating * 10 + a.price);
      }
    });
  }, [query, selectedGender, selectedCategory, selectedSize, selectedColor, selectedPrice, sortMode]);

  const selectedProduct = getProductById(selectedProductId);

  const subtotal = cart.reduce((total, item) => total + item.price * item.quantity, 0);
  const discount = subtotal > 0 ? Math.min(Math.round(subtotal * 0.12), 650) : 0;
  const shipping = subtotal > 0 ? 150 : 0;
  const total = subtotal - discount + shipping;

  const addToCart = (product: Product, size = 'M', color = product.colors[0]) => {
    setCart((current) => {
      const existing = current.find(
        (item) => item.id === product.id && item.size === size && item.color === color
      );

      if (existing) {
        return current.map((item) =>
          item.id === product.id && item.size === size && item.color === color
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      }

      return [
        ...current,
        {
          id: product.id,
          name: product.name,
          image: product.image,
          price: product.price,
          size,
          color,
          quantity: 1
        }
      ];
    });
    setCheckoutOpen(true);
  };

  const updateQuantity = (itemId: string, size: string, color: string, change: number) => {
    setCart((current) =>
      current
        .map((item) =>
          item.id === itemId && item.size === size && item.color === color
            ? { ...item, quantity: Math.max(0, item.quantity + change) }
            : item
        )
        .filter((item) => item.quantity > 0)
    );
  };

  const clearCart = () => setCart([]);

  const placeOrder = async () => {
    const payload = {
      amount: total * 100,
      currency: 'INR',
      receipt: `stylehub-${Date.now()}`
    };

    try {
      setPaymentState('Creating secure payment request...');
      const response = await fetch(`${apiBase}/api/create-order`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const order = await response.json();
      const keyId = import.meta.env.VITE_RAZORPAY_KEY_ID || 'rzp_test_123456';
      const RazorpayCtor = (window as any).Razorpay;

      if (!RazorpayCtor) {
        setPaymentState('Demo checkout approved. Razorpay script is not loaded, but the order flow is simulated successfully.');
        return;
      }

      const razorpay = new RazorpayCtor({
        key: keyId,
        amount: order.amount,
        currency: order.currency,
        name: 'STYLEHUB',
        description: 'Premium fashion order',
        order_id: order.id,
        handler: async function (paymentResponse: any) {
          const verifyResponse = await fetch(`${apiBase}/api/verify-payment`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              razorpay_order_id: paymentResponse.razorpay_order_id,
              razorpay_payment_id: paymentResponse.razorpay_payment_id,
              razorpay_signature: paymentResponse.razorpay_signature,
              amount: total * 100,
              currency: 'INR'
            })
          });

          const verifyResult = await verifyResponse.json();
          if (verifyResult.success) {
            setPaymentState('Payment successful! Your order has been placed.');
            clearCart();
            setCheckoutOpen(false);
          } else {
            setPaymentState('Payment verification failed. Please try again.');
          }
        },
        prefill: {
          name: address.fullName,
          contact: address.phone,
          email: 'customer@example.com'
        },
        theme: {
          color: '#c58f4d'
        }
      });

      razorpay.open();
    } catch (error) {
      console.error(error);
      setPaymentState('Something went wrong while creating the payment. Please try again.');
    }
  };

  return (
    <div className="min-h-screen bg-[#f8f3ec] text-slate-900">
      <header className="sticky top-0 z-50 border-b border-slate-200/80 bg-[#f8f3ec]/90 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3">
            <button className="rounded-full border border-slate-300 p-2 md:hidden">
              <Menu className="h-5 w-5" />
            </button>
            <div className="flex items-center gap-2">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-900 text-sm font-bold text-white">
                S
              </div>
              <div>
                <p className="text-lg font-semibold tracking-[0.35rem] text-slate-900">STYLEHUB</p>
              </div>
            </div>
          </div>

          <nav className="hidden items-center gap-7 text-sm font-medium text-slate-700 md:flex">
            <a href="#">Home</a>
            <a href="#">Men</a>
            <a href="#">Women</a>
            <a href="#">Kids</a>
            <a href="#">New Arrivals</a>
            <a href="#">Offers</a>
          </nav>

          <div className="flex items-center gap-3">
            <div className="hidden items-center gap-2 rounded-full border border-slate-300 bg-white px-3 py-2 text-sm text-slate-500 md:flex">
              <Search className="h-4 w-4" />
              <input
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Search products"
                className="w-32 border-none bg-transparent outline-none placeholder:text-slate-400"
              />
            </div>
            <button className="rounded-full border border-slate-300 bg-white p-2.5">
              <Heart className="h-4 w-4" />
            </button>
            <button className="relative rounded-full border border-slate-300 bg-white p-2.5" onClick={() => setCheckoutOpen(true)}>
              <ShoppingCart className="h-4 w-4" />
              <span className="absolute -right-1 -top-1 flex h-5 w-5 items-center justify-center rounded-full bg-[#c58f4d] text-[10px] font-semibold text-white">
                {cart.reduce((sum, item) => sum + item.quantity, 0)}
              </span>
            </button>
            <button className="rounded-full border border-slate-300 bg-white p-2.5">
              <User className="h-4 w-4" />
            </button>
          </div>
        </div>
      </header>

      <main>
        <section className="mx-auto max-w-7xl px-4 pb-14 pt-8 sm:px-6 lg:px-8">
          <div className="grid items-center gap-10 lg:grid-cols-[1.1fr_0.9fr]">
            <div>
              <p className="mb-4 inline-flex items-center gap-2 rounded-full bg-[#f4e9df] px-4 py-2 text-xs font-semibold uppercase tracking-[0.2em] text-slate-700">
                Curated essentials
              </p>
              <h1 className="max-w-xl text-5xl font-black leading-[1.05] tracking-tight text-slate-900">
                Elevate Your Everyday Style
              </h1>
              <p className="mt-5 max-w-lg text-lg text-slate-600">
                Discover premium fashion designed for every moment.
              </p>
              <div className="mt-8 flex flex-wrap gap-4">
                <button className="rounded-full bg-slate-900 px-6 py-3 text-sm font-semibold text-white transition hover:bg-slate-800">
                  Shop Men
                </button>
                <button className="rounded-full border border-slate-300 bg-white px-6 py-3 text-sm font-semibold text-slate-900 transition hover:border-slate-400">
                  Shop Women
                </button>
              </div>
              <div className="mt-10 flex flex-wrap gap-10 text-sm text-slate-600">
                <div>
                  <p className="text-3xl font-bold text-slate-900">12k+</p>
                  <span>happy shoppers</span>
                </div>
                <div>
                  <p className="text-3xl font-bold text-slate-900">4.9/5</p>
                  <span>average rating</span>
                </div>
                <div>
                  <p className="text-3xl font-bold text-slate-900">24h</p>
                  <span>dispatch</span>
                </div>
              </div>
            </div>

            <div className="relative">
              <div className="absolute -left-12 top-10 h-28 w-28 rounded-full bg-[#f4e9df] blur-2xl" />
              <div className="absolute -right-12 bottom-10 h-28 w-28 rounded-full bg-[#e2d0b6] blur-2xl" />
              <div className="relative overflow-hidden rounded-[2rem] border border-slate-200 bg-white p-3 shadow-soft">
                <img
                  src="https://images.unsplash.com/photo-1529139574466-a303027c1d8b?auto=format&fit=crop&w=1200&q=80"
                  alt="Fashion hero"
                  className="h-[520px] w-full rounded-[1.5rem] object-cover"
                />
                <div className="absolute bottom-8 left-8 right-8 rounded-2xl bg-white/80 p-4 shadow-lg backdrop-blur-md">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-xs uppercase tracking-[0.2em] text-slate-500">Weekend edit</p>
                      <p className="mt-1 text-xl font-bold text-slate-900">New season essentials</p>
                    </div>
                    <button className="rounded-full bg-[#c58f4d] p-3 text-white">
                      <ArrowRight className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-4 pb-16 sm:px-6 lg:px-8">
          <div className="mb-8 flex items-center justify-between">
            <h2 className="text-3xl font-bold tracking-tight text-slate-900">Shop by category</h2>
            <button className="text-sm font-semibold text-slate-700">Explore all</button>
          </div>
          <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-5">
            {categoryCards.map((category) => (
              <div key={category.name} className="group overflow-hidden rounded-[1.75rem] border border-slate-200 bg-white shadow-soft">
                <div className="relative h-64 overflow-hidden">
                  <img src={category.image} alt={category.title} className="h-full w-full object-cover transition duration-500 group-hover:scale-105" />
                  <div className="absolute inset-0 bg-gradient-to-t from-[#111827]/70 via-[#111827]/10 to-transparent" />
                  <div className="absolute left-5 top-5 z-10 text-white">
                    <p className="text-2xl font-bold uppercase tracking-wide">{category.name}</p>
                  </div>
                </div>
                <div className="flex items-center justify-between p-4">
                  <p className="text-sm font-medium text-slate-700">Explore Collection</p>
                  <ArrowRight className="h-4 w-4 text-slate-600" />
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-4 pb-16 sm:px-6 lg:px-8">
          <div className="mb-8 flex items-center justify-between">
            <h2 className="text-3xl font-bold tracking-tight text-slate-900">New arrivals</h2>
            <button className="rounded-full border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-700">
              View all
            </button>
          </div>
          <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
            {products.slice(0, 4).map((product) => (
              <div key={product.id} className="group overflow-hidden rounded-[1.75rem] border border-slate-200 bg-white shadow-soft">
                <div className="relative overflow-hidden">
                  <img src={product.image} alt={product.name} className="h-80 w-full object-cover transition duration-500 group-hover:scale-105" />
                  <button className="absolute right-4 top-4 rounded-full bg-white/90 p-2 text-slate-700 shadow-sm">
                    <Heart className="h-4 w-4" />
                  </button>
                  {product.badge && (
                    <span className="absolute left-4 top-4 rounded-full bg-[#c58f4d] px-2.5 py-1 text-[10px] font-bold uppercase tracking-[0.15em] text-white">
                      {product.badge}
                    </span>
                  )}
                </div>
                <div className="p-5">
                  <div className="mb-2 flex items-center justify-between gap-4">
                    <h3 className="text-lg font-semibold text-slate-800">{product.name}</h3>
                    <button
                      className="rounded-full bg-slate-900 px-2.5 py-1.5 text-[11px] font-semibold text-white"
                      onClick={() => addToCart(product)}
                    >
                      Add
                    </button>
                  </div>
                  <div className="mb-3 flex items-center gap-1 text-sm text-amber-500">
                    <Star className="h-4 w-4 fill-current" />
                    <span className="font-medium text-slate-700">{product.rating}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xl font-bold text-slate-900">{currency(product.price)}</span>
                    <span className="text-sm text-slate-400 line-through">{currency(product.originalPrice)}</span>
                  </div>
                  <div className="mt-3 flex items-center justify-between text-xs font-semibold uppercase tracking-wide text-[#c58f4d]">
                    <span>{getDiscountPercent(product.price, product.originalPrice)}% OFF</span>
                    <button onClick={() => setSelectedProductId(product.id)} className="text-slate-700 hover:text-slate-900">
                      Quick view
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-4 pb-16 sm:px-6 lg:px-8">
          <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft lg:p-8">
            <div className="mb-8 flex items-center justify-between gap-4">
              <div>
                <p className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">Fashion collection</p>
                <h2 className="mt-2 text-3xl font-bold tracking-tight text-slate-900">Browse premium styles</h2>
              </div>
              <button className="rounded-full border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700">
                Filters
              </button>
            </div>

            <div className="grid gap-8 lg:grid-cols-[260px_1fr]">
              <aside className="space-y-8 rounded-[1.5rem] bg-[#f8f3ec] p-5">
                <div>
                  <h3 className="mb-4 text-lg font-semibold text-slate-900">Gender</h3>
                  <div className="flex flex-wrap gap-2">
                    {['All', 'Men', 'Women', 'Kids'].map((option) => (
                      <button
                        key={option}
                        onClick={() => setSelectedGender(option)}
                        className={`rounded-full px-3 py-2 text-sm ${selectedGender === option ? 'bg-slate-900 text-white' : 'bg-white text-slate-700'}`}
                      >
                        {option}
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <h3 className="mb-4 text-lg font-semibold text-slate-900">Category</h3>
                  <div className="space-y-2 text-sm text-slate-700">
                    {['All', 'Shirts', 'T-Shirts', 'Jeans', 'Dresses', 'Jackets', 'Hoodies', 'Ethnic Wear', 'Footwear'].map((option) => (
                      <button
                        key={option}
                        onClick={() => setSelectedCategory(option)}
                        className={`block w-full rounded-full px-3 py-2 text-left ${selectedCategory === option ? 'bg-slate-900 text-white' : 'bg-white'}`}
                      >
                        {option}
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <h3 className="mb-4 text-lg font-semibold text-slate-900">Size</h3>
                  <div className="flex flex-wrap gap-2">
                    {['All', 'XS', 'S', 'M', 'L', 'XL', 'XXL'].map((option) => (
                      <button
                        key={option}
                        onClick={() => setSelectedSize(option)}
                        className={`rounded-full px-3 py-2 text-sm ${selectedSize === option ? 'bg-slate-900 text-white' : 'bg-white text-slate-700'}`}
                      >
                        {option}
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <h3 className="mb-4 text-lg font-semibold text-slate-900">Price</h3>
                  <div className="space-y-2 text-sm text-slate-700">
                    {['All', ...priceRanges.map((range) => range.label)].map((option) => {
                      const matchingValue = priceRanges.find((range) => range.label === option)?.value ?? 'All';
                      return (
                        <button
                          key={option}
                          onClick={() => setSelectedPrice(matchingValue)}
                          className={`block w-full rounded-full px-3 py-2 text-left ${selectedPrice === matchingValue ? 'bg-slate-900 text-white' : 'bg-white'}`}
                        >
                          {option}
                        </button>
                      );
                    })}
                  </div>
                </div>

                <div>
                  <h3 className="mb-4 text-lg font-semibold text-slate-900">Color</h3>
                  <div className="flex flex-wrap gap-2">
                    {['All', 'Black', 'White', 'Blue', 'Red', 'Green', 'Beige'].map((option) => (
                      <button
                        key={option}
                        onClick={() => setSelectedColor(option)}
                        className={`rounded-full px-3 py-2 text-sm ${selectedColor === option ? 'bg-slate-900 text-white' : 'bg-white text-slate-700'}`}
                      >
                        {option}
                      </button>
                    ))}
                  </div>
                </div>
              </aside>

              <div>
                <div className="mb-6 flex flex-col gap-4 rounded-[1.5rem] border border-slate-200 bg-[#f9f5f0] p-4 sm:flex-row sm:items-center sm:justify-between">
                  <div>
                    <p className="text-sm text-slate-500">Showing {filteredProducts.length} products</p>
                  </div>
                  <div className="flex items-center gap-3">
                    <label className="text-sm font-medium text-slate-600">Sort by</label>
                    <select
                      value={sortMode}
                      onChange={(event) => setSortMode(event.target.value as (typeof sortOptions)[number])}
                      className="rounded-full border border-slate-300 bg-white px-3 py-2 text-sm outline-none"
                    >
                      {sortOptions.map((option) => (
                        <option key={option} value={option}>
                          {option}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
                  {filteredProducts.map((product) => (
                    <div key={product.id} className="group overflow-hidden rounded-[1.5rem] border border-slate-200 bg-white shadow-soft">
                      <div className="relative overflow-hidden">
                        <img src={product.image} alt={product.name} className="h-72 w-full object-cover transition duration-500 group-hover:scale-105" />
                        {product.badge && (
                          <span className="absolute left-4 top-4 rounded-full bg-[#c58f4d] px-2.5 py-1 text-[10px] font-bold uppercase tracking-[0.15em] text-white">
                            {product.badge}
                          </span>
                        )}
                        <button className="absolute right-4 top-4 rounded-full bg-white/90 p-2 text-slate-700 shadow-sm">
                          <Heart className="h-4 w-4" />
                        </button>
                      </div>
                      <div className="p-4">
                        <div className="mb-2 flex items-center justify-between">
                          <p className="text-xs uppercase tracking-[0.18em] text-slate-500">{product.category}</p>
                          <div className="flex items-center gap-1 text-sm text-amber-500">
                            <Star className="h-4 w-4 fill-current" />
                            <span className="text-slate-700">{product.rating}</span>
                          </div>
                        </div>
                        <h3 className="text-lg font-semibold text-slate-900">{product.name}</h3>
                        <div className="mt-3 flex items-center gap-2">
                          <span className="text-xl font-bold text-slate-900">{currency(product.price)}</span>
                          <span className="text-sm text-slate-400 line-through">{currency(product.originalPrice)}</span>
                        </div>
                        <div className="mt-3 flex items-center justify-between">
                          <span className="text-xs font-semibold uppercase tracking-wide text-[#c58f4d]">
                            {getDiscountPercent(product.price, product.originalPrice)}% OFF
                          </span>
                          <button
                            className="rounded-full bg-slate-900 px-3 py-2 text-xs font-semibold text-white"
                            onClick={() => addToCart(product)}
                          >
                            Add to Cart
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-4 pb-20 sm:px-6 lg:px-8">
          <div className="rounded-[2rem] border border-slate-200 bg-[#1d1a17] p-6 text-white shadow-soft lg:p-8">
            <div className="grid gap-8 lg:grid-cols-[1fr_1.1fr] lg:items-center">
              <div>
                <p className="text-sm font-semibold uppercase tracking-[0.2em] text-[#d9b98a]">Style spotlight</p>
                <h2 className="mt-3 text-3xl font-bold tracking-tight">Curated fits that move with you.</h2>
                <p className="mt-4 max-w-md text-slate-300">
                  Discover layered silhouettes and elevated essentials built for the everyday rhythm of your life.
                </p>
                <button className="mt-6 rounded-full bg-white px-5 py-3 text-sm font-semibold text-slate-900">
                  Shop the edit
                </button>
              </div>
              <div className="grid gap-4 sm:grid-cols-2">
                {products.slice(0, 4).map((product) => (
                  <div key={product.id} className="rounded-[1.5rem] bg-white/5 p-3">
                    <img src={product.image} alt={product.name} className="h-52 w-full rounded-[1.1rem] object-cover" />
                    <div className="mt-3 flex items-center justify-between">
                      <div>
                        <h3 className="text-base font-semibold text-white">{product.name}</h3>
                        <p className="text-sm text-slate-300">{currency(product.price)}</p>
                      </div>
                      <button className="rounded-full bg-[#c58f4d] p-2 text-white">
                        <ChevronRight className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-4 pb-24 sm:px-6 lg:px-8">
          <div className="grid gap-8 lg:grid-cols-[1.2fr_0.8fr]">
            <div className="overflow-hidden rounded-[2rem] border border-slate-200 bg-white shadow-soft">
              <div className="grid gap-8 p-6 lg:grid-cols-2 lg:p-8">
                <div>
                  <img src={selectedProduct.image} alt={selectedProduct.name} className="h-[430px] w-full rounded-[1.4rem] object-cover" />
                  <div className="mt-4 grid grid-cols-3 gap-3">
                    {selectedProduct.gallery.map((image) => (
                      <img key={image} src={image} alt={selectedProduct.name} className="h-24 w-full rounded-xl object-cover" />
                    ))}
                  </div>
                </div>
                <div className="flex flex-col justify-center">
                  <p className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">{selectedProduct.category}</p>
                  <h2 className="mt-3 text-3xl font-bold tracking-tight text-slate-900">{selectedProduct.name}</h2>
                  <div className="mt-4 flex items-center gap-2 text-amber-500">
                    <Star className="h-5 w-5 fill-current" />
                    <span className="font-medium text-slate-700">{selectedProduct.rating} • 1,284 reviews</span>
                  </div>
                  <div className="mt-5 flex items-end gap-3">
                    <span className="text-3xl font-bold text-slate-900">{currency(selectedProduct.price)}</span>
                    <span className="mb-1 text-lg text-slate-400 line-through">{currency(selectedProduct.originalPrice)}</span>
                    <span className="mb-1 rounded-full bg-[#f4e9df] px-2 py-1 text-xs font-bold uppercase text-[#c58f4d]">
                      {getDiscountPercent(selectedProduct.price, selectedProduct.originalPrice)}% OFF
                    </span>
                  </div>
                  <p className="mt-5 text-slate-600">{selectedProduct.description}</p>

                  <div className="mt-6">
                    <p className="mb-3 text-sm font-semibold uppercase tracking-[0.12em] text-slate-500">Colors</p>
                    <div className="flex flex-wrap gap-2">
                      {selectedProduct.colors.map((color) => (
                        <button
                          key={color}
                          className="rounded-full border border-slate-300 bg-white px-3 py-2 text-sm text-slate-700"
                        >
                          {color}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="mt-6">
                    <p className="mb-3 text-sm font-semibold uppercase tracking-[0.12em] text-slate-500">Sizes</p>
                    <div className="flex flex-wrap gap-2">
                      {selectedProduct.sizes.map((size) => (
                        <button
                          key={size}
                          className="rounded-full border border-slate-300 bg-white px-3 py-2 text-sm text-slate-700"
                        >
                          {size}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="mt-8 flex flex-wrap gap-4">
                    <button
                      onClick={() => addToCart(selectedProduct, selectedProduct.sizes[0], selectedProduct.colors[0])}
                      className="rounded-full bg-slate-900 px-6 py-3 text-sm font-semibold text-white"
                    >
                      Add to Cart
                    </button>
                    <button className="rounded-full border border-slate-300 bg-white px-6 py-3 text-sm font-semibold text-slate-900">
                      Add to Wishlist
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <div className="rounded-[2rem] border border-slate-200 bg-[#f9f5f0] p-5 shadow-soft">
              <div className="flex items-center justify-between gap-4 border-b border-slate-200 pb-4">
                <div>
                  <p className="text-sm uppercase tracking-[0.18em] text-slate-500">Cart summary</p>
                  <h3 className="mt-1 text-2xl font-bold text-slate-900">{cart.reduce((sum, item) => sum + item.quantity, 0)} items</h3>
                </div>
                <button onClick={() => setCheckoutOpen(true)} className="rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white">
                  Checkout
                </button>
              </div>

              <div className="mt-5 space-y-4">
                {cart.length === 0 ? (
                  <p className="py-8 text-center text-sm text-slate-500">Your cart is empty. Add products to continue.</p>
                ) : (
                  cart.map((item) => (
                    <div key={`${item.id}-${item.size}-${item.color}`} className="flex gap-3 rounded-[1.25rem] bg-white p-3 shadow-sm">
                      <img src={item.image} alt={item.name} className="h-20 w-16 rounded-xl object-cover" />
                      <div className="flex-1">
                        <div className="flex items-start justify-between gap-4">
                          <div>
                            <p className="font-semibold text-slate-900">{item.name}</p>
                            <p className="text-xs text-slate-500">{item.color} • {item.size}</p>
                          </div>
                          <button onClick={() => updateQuantity(item.id, item.size, item.color, -item.quantity)}>
                            <Trash2 className="h-4 w-4 text-slate-400" />
                          </button>
                        </div>
                        <div className="mt-3 flex items-center justify-between">
                          <div className="flex items-center gap-2 rounded-full border border-slate-200 px-2 py-1">
                            <button onClick={() => updateQuantity(item.id, item.size, item.color, -1)} className="p-1">
                              <Minus className="h-3 w-3" />
                            </button>
                            <span className="min-w-5 text-center text-sm font-semibold">{item.quantity}</span>
                            <button onClick={() => updateQuantity(item.id, item.size, item.color, 1)} className="p-1">
                              <Plus className="h-3 w-3" />
                            </button>
                          </div>
                          <span className="font-semibold text-slate-900">{currency(item.price * item.quantity)}</span>
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>

              <div className="mt-6 rounded-[1.25rem] bg-white p-4 shadow-sm">
                <div className="space-y-3 text-sm text-slate-600">
                  <div className="flex justify-between">
                    <span>Subtotal</span>
                    <span>{currency(subtotal)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Discount</span>
                    <span>-{currency(discount)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Shipping</span>
                    <span>{currency(shipping)}</span>
                  </div>
                  <div className="flex justify-between border-t border-slate-200 pt-3 text-base font-bold text-slate-900">
                    <span>Total</span>
                    <span>{currency(total)}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>

      {checkoutOpen && (
        <div className="fixed inset-0 z-50 flex items-end justify-center bg-slate-900/40 p-3 sm:items-center">
          <div className="max-h-[90vh] w-full max-w-4xl overflow-y-auto rounded-[2rem] bg-white p-6 shadow-2xl">
            <div className="mb-5 flex items-center justify-between">
              <div>
                <p className="text-sm uppercase tracking-[0.18em] text-slate-500">Checkout</p>
                <h3 className="mt-2 text-2xl font-bold text-slate-900">Place your order</h3>
              </div>
              <button onClick={() => setCheckoutOpen(false)} className="rounded-full bg-slate-100 px-3 py-2 text-sm font-medium text-slate-700">
                Close
              </button>
            </div>

            <div className="grid gap-8 lg:grid-cols-[1.1fr_0.9fr]">
              <div className="space-y-5">
                <div className="grid gap-4 sm:grid-cols-2">
                  <label className="text-sm text-slate-700">
                    Full name
                    <input value={address.fullName} onChange={(e) => setAddress({ ...address, fullName: e.target.value })} className="mt-2 w-full rounded-2xl border border-slate-200 bg-[#f8f3ec] px-4 py-3 outline-none" />
                  </label>
                  <label className="text-sm text-slate-700">
                    Phone
                    <input value={address.phone} onChange={(e) => setAddress({ ...address, phone: e.target.value })} className="mt-2 w-full rounded-2xl border border-slate-200 bg-[#f8f3ec] px-4 py-3 outline-none" />
                  </label>
                </div>
                <label className="block text-sm text-slate-700">
                  Delivery address
                  <input value={address.address} onChange={(e) => setAddress({ ...address, address: e.target.value })} className="mt-2 w-full rounded-2xl border border-slate-200 bg-[#f8f3ec] px-4 py-3 outline-none" />
                </label>
                <div className="grid gap-4 sm:grid-cols-3">
                  <label className="text-sm text-slate-700">
                    City
                    <input value={address.city} onChange={(e) => setAddress({ ...address, city: e.target.value })} className="mt-2 w-full rounded-2xl border border-slate-200 bg-[#f8f3ec] px-4 py-3 outline-none" />
                  </label>
                  <label className="text-sm text-slate-700">
                    State
                    <input value={address.state} onChange={(e) => setAddress({ ...address, state: e.target.value })} className="mt-2 w-full rounded-2xl border border-slate-200 bg-[#f8f3ec] px-4 py-3 outline-none" />
                  </label>
                  <label className="text-sm text-slate-700">
                    Pincode
                    <input value={address.pincode} onChange={(e) => setAddress({ ...address, pincode: e.target.value })} className="mt-2 w-full rounded-2xl border border-slate-200 bg-[#f8f3ec] px-4 py-3 outline-none" />
                  </label>
                </div>
                <div className="rounded-[1.5rem] bg-[#f8f3ec] p-4">
                  <p className="mb-3 text-sm font-semibold uppercase tracking-[0.16em] text-slate-500">Payment method</p>
                  <div className="flex items-center gap-3 rounded-2xl bg-white p-3 shadow-sm">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-[#f4e9df] text-[#c58f4d]">
                      <ShoppingBag className="h-4 w-4" />
                    </div>
                    <div>
                      <p className="font-semibold text-slate-900">Razorpay secure checkout</p>
                      <p className="text-sm text-slate-500">Cards, UPI, wallets, and net banking</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="rounded-[1.5rem] bg-[#f8f3ec] p-5">
                <p className="mb-4 text-sm font-semibold uppercase tracking-[0.16em] text-slate-500">Order summary</p>
                <div className="space-y-3">
                  {cart.map((item) => (
                    <div key={`${item.id}-${item.size}-${item.color}`} className="flex items-center justify-between rounded-2xl bg-white p-3 shadow-sm">
                      <div className="flex items-center gap-3">
                        <img src={item.image} alt={item.name} className="h-14 w-12 rounded-xl object-cover" />
                        <div>
                          <p className="font-medium text-slate-900">{item.name}</p>
                          <p className="text-xs text-slate-500">{item.color} • {item.size} • Qty {item.quantity}</p>
                        </div>
                      </div>
                      <p className="font-semibold text-slate-900">{currency(item.price * item.quantity)}</p>
                    </div>
                  ))}
                </div>

                <div className="mt-5 space-y-3 text-sm text-slate-600">
                  <div className="flex justify-between">
                    <span>Subtotal</span>
                    <span>{currency(subtotal)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Discount</span>
                    <span>-{currency(discount)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Shipping</span>
                    <span>{currency(shipping)}</span>
                  </div>
                  <div className="flex justify-between border-t border-slate-200 pt-3 text-base font-bold text-slate-900">
                    <span>Total</span>
                    <span>{currency(total)}</span>
                  </div>
                </div>

                <button
                  onClick={placeOrder}
                  className="mt-6 w-full rounded-full bg-[#c58f4d] px-5 py-3 text-sm font-semibold text-white"
                >
                  Pay {currency(total)}
                </button>
                {paymentState && (
                  <p className="mt-4 rounded-2xl bg-[#f4e9df] px-4 py-3 text-sm text-slate-700">
                    {paymentState}
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
