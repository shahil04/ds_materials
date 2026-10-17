import type { Product } from '../types';

export const products: Product[] = [
  {
    id: 'p1',
    slug: 'premium-cotton-shirt',
    name: 'Premium Cotton Shirt',
    gender: 'Men',
    category: 'Shirts',
    price: 999,
    originalPrice: 1499,
    rating: 4.7,
    badge: 'New',
    image:
      'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=900&q=80',
    gallery: [
      'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=900&q=80',
      'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?auto=format&fit=crop&w=900&q=80',
      'https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=900&q=80'
    ],
    colors: ['Black', 'White', 'Blue'],
    sizes: ['S', 'M', 'L', 'XL'],
    description:
      'Tailored for comfort and sharp styling, this premium cotton shirt balances polished cuts with breathable fabric for everyday premium wear.'
  },
  {
    id: 'p2',
    slug: 'satin-silk-dress',
    name: 'Satin Silhouette Dress',
    gender: 'Women',
    category: 'Dresses',
    price: 1899,
    originalPrice: 2499,
    rating: 4.8,
    badge: 'Trending',
    image:
      'https://images.unsplash.com/photo-1529139574466-a303027c1d8b?auto=format&fit=crop&w=900&q=80',
    gallery: [
      'https://images.unsplash.com/photo-1529139574466-a303027c1d8b?auto=format&fit=crop&w=900&q=80',
      'https://images.unsplash.com/photo-1496747611176-843222e1e57c?auto=format&fit=crop&w=900&q=80',
      'https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=900&q=80'
    ],
    colors: ['Beige', 'Red', 'Black'],
    sizes: ['XS', 'S', 'M', 'L'],
    description:
      'A fluid satin dress designed for graceful movement and elevated evenings. It brings luxury texture and clean lines to any occasion.'
  },
  {
    id: 'p3',
    slug: 'classic-denim-jeans',
    name: 'Classic Denim Jeans',
    gender: 'Men',
    category: 'Jeans',
    price: 1299,
    originalPrice: 1799,
    rating: 4.6,
    image:
      'https://images.unsplash.com/photo-1542272604-787c3835535d?auto=format&fit=crop&w=900&q=80',
    gallery: [
      'https://images.unsplash.com/photo-1542272604-787c3835535d?auto=format&fit=crop&w=900&q=80',
      'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=900&q=80',
      'https://images.unsplash.com/photo-1504593811423-6dd665756598?auto=format&fit=crop&w=900&q=80'
    ],
    colors: ['Blue', 'Black', 'Beige'],
    sizes: ['S', 'M', 'L', 'XL', 'XXL'],
    description:
      'A modern staple with stretch comfort and durable denim feel, giving you a sharp silhouette for every day of the week.'
  },
  {
    id: 'p4',
    slug: 'urban-zip-jacket',
    name: 'Urban Zip Jacket',
    gender: 'Women',
    category: 'Jackets',
    price: 2199,
    originalPrice: 3199,
    rating: 4.9,
    badge: 'Bestseller',
    image:
      'https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=900&q=80',
    gallery: [
      'https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=900&q=80',
      'https://images.unsplash.com/photo-1529139574466-a303027c1d8b?auto=format&fit=crop&w=900&q=80',
      'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?auto=format&fit=crop&w=900&q=80'
    ],
    colors: ['Black', 'White', 'Green'],
    sizes: ['XS', 'S', 'M', 'L'],
    description:
      'Command attention in a sleek zip jacket built with soft insulation, quality lining, and an effortlessly modern fit.'
  },
  {
    id: 'p5',
    slug: 'kids-graphic-hoodie',
    name: 'Kids Graphic Hoodie',
    gender: 'Kids',
    category: 'Hoodies',
    price: 799,
    originalPrice: 1199,
    rating: 4.5,
    image:
      'https://images.unsplash.com/photo-1519345182560-3f2917c472ef?auto=format&fit=crop&w=900&q=80',
    gallery: [
      'https://images.unsplash.com/photo-1519345182560-3f2917c472ef?auto=format&fit=crop&w=900&q=80',
      'https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=900&q=80',
      'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=900&q=80'
    ],
    colors: ['Blue', 'Green', 'White'],
    sizes: ['XS', 'S', 'M'],
    description:
      'Comfort-first hoodie for active kids, featuring a relaxed silhouette, soft fleece feel, and playful style details.'
  },
  {
    id: 'p6',
    slug: 'ethnic-embroidered-set',
    name: 'Ethnic Embroidered Set',
    gender: 'Women',
    category: 'Ethnic Wear',
    price: 2499,
    originalPrice: 3299,
    rating: 4.9,
    badge: 'Limited',
    image:
      'https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=900&q=80',
    gallery: [
      'https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=900&q=80',
      'https://images.unsplash.com/photo-1529139574466-a303027c1d8b?auto=format&fit=crop&w=900&q=80',
      'https://images.unsplash.com/photo-1496747611176-843222e1e57c?auto=format&fit=crop&w=900&q=80'
    ],
    colors: ['Beige', 'Red', 'Green'],
    sizes: ['S', 'M', 'L', 'XL'],
    description:
      'An artisanal festive set with detailed embroidery and elevated drape for celebrations, weddings, and special moments.'
  },
  {
    id: 'p7',
    slug: 'elevated-running-shoes',
    name: 'Elevated Running Shoes',
    gender: 'Men',
    category: 'Footwear',
    price: 1699,
    originalPrice: 2299,
    rating: 4.7,
    image:
      'https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80',
    gallery: [
      'https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80',
      'https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?auto=format&fit=crop&w=900&q=80',
      'https://images.unsplash.com/photo-1608231387042-66d1773070a5?auto=format&fit=crop&w=900&q=80'
    ],
    colors: ['Black', 'White', 'Red'],
    sizes: ['6', '7', '8', '9', '10'],
    description:
      'Lightweight and durable training shoes built with cushioning support and a sleek everyday street-ready profile.'
  },
  {
    id: 'p8',
    slug: 'everyday-crew-tee',
    name: 'Everyday Crew Tee',
    gender: 'Women',
    category: 'T-Shirts',
    price: 699,
    originalPrice: 999,
    rating: 4.4,
    image:
      'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?auto=format&fit=crop&w=900&q=80',
    gallery: [
      'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?auto=format&fit=crop&w=900&q=80',
      'https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=900&q=80',
      'https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=900&q=80'
    ],
    colors: ['White', 'Beige', 'Black'],
    sizes: ['XS', 'S', 'M', 'L', 'XL'],
    description:
      'An easy premium tee with a refined fit, breathable cotton, and styling versatility across casual, work, and travel moments.'
  }
];

export const categoryCards = [
  { name: 'Men', title: "Men's Fashion", image: 'https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=900&q=80' },
  { name: 'Women', title: "Women's Fashion", image: 'https://images.unsplash.com/photo-1496747611176-843222e1e57c?auto=format&fit=crop&w=900&q=80' },
  { name: 'Kids', title: 'Kids Fashion', image: 'https://images.unsplash.com/photo-1519345182560-3f2917c472ef?auto=format&fit=crop&w=900&q=80' },
  { name: 'Footwear', title: 'Footwear', image: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80' },
  { name: 'Accessories', title: 'Accessories', image: 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?auto=format&fit=crop&w=900&q=80' }
];
