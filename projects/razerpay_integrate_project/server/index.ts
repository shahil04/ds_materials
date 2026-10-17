import cors from 'cors';
import dotenv from 'dotenv';
import express, { type Request, type Response } from 'express';
import Razorpay from 'razorpay';

dotenv.config();

const app = express();
const port = Number(process.env.PORT) || 3001;

const razorpay = process.env.RAZORPAY_KEY_ID && process.env.RAZORPAY_KEY_SECRET
  ? new Razorpay({
      key_id: process.env.RAZORPAY_KEY_ID,
      key_secret: process.env.RAZORPAY_KEY_SECRET
    })
  : null;

const dummyProducts = [
  {
    id: 'p1',
    name: 'Premium Cotton Shirt',
    category: 'Shirts',
    gender: 'Men',
    price: 999,
    originalPrice: 1499,
    rating: 4.7,
    image: 'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=900&q=80'
  },
  {
    id: 'p2',
    name: 'Satin Silhouette Dress',
    category: 'Dresses',
    gender: 'Women',
    price: 1899,
    originalPrice: 2499,
    rating: 4.8,
    image: 'https://images.unsplash.com/photo-1529139574466-a303027c1d8b?auto=format&fit=crop&w=900&q=80'
  },
  {
    id: 'p3',
    name: 'Classic Denim Jeans',
    category: 'Jeans',
    gender: 'Men',
    price: 1299,
    originalPrice: 1799,
    rating: 4.6,
    image: 'https://images.unsplash.com/photo-1542272604-787c3835535d?auto=format&fit=crop&w=900&q=80'
  }
];

app.use(cors());
app.use(express.json());

app.get('/api/health', (_req: Request, res: Response) => {
  res.json({ status: 'ok', message: 'STYLEHUB API is running' });
});

app.get('/api/products', (_req: Request, res: Response) => {
  res.json({ products: dummyProducts });
});

app.get('/api/products/:id', (req: Request, res: Response) => {
  const product = dummyProducts.find((item) => item.id === req.params.id);
  if (!product) {
    return res.status(404).json({ message: 'Product not found' });
  }
  return res.json({ product });
});

app.post('/api/create-order', async (req: Request, res: Response) => {
  const { amount, currency = 'INR', receipt = 'stylehub-order' } = req.body;

  if (!amount || Number(amount) <= 0) {
    return res.status(400).json({ message: 'Invalid amount.' });
  }

  if (!razorpay) {
    return res.json({
      id: `order_demo_${Date.now()}`,
      amount: Number(amount),
      currency,
      receipt,
      status: 'created',
      notes: { demoMode: true }
    });
  }

  try {
    const order = await razorpay.orders.create({
      amount: Number(amount),
      currency,
      receipt
    });
    return res.json(order);
  } catch (error) {
    console.error('Razorpay order creation failed', error);
    return res.status(500).json({ message: 'Failed to create Razorpay order.' });
  }
});

app.post('/api/verify-payment', async (req: Request, res: Response) => {
  const { razorpay_order_id, razorpay_payment_id, razorpay_signature, amount } = req.body;

  if (!razorpay_order_id || !razorpay_payment_id || !razorpay_signature || !amount) {
    return res.status(400).json({ success: false, message: 'Missing payment verification data.' });
  }

  if (!process.env.RAZORPAY_KEY_SECRET) {
    return res.json({ success: true, message: 'Demo verification succeeded.' });
  }

  const crypto = await import('node:crypto');
  const body = `${razorpay_order_id}|${razorpay_payment_id}`;
  const expectedSignature = crypto
    .createHmac('sha256', process.env.RAZORPAY_KEY_SECRET)
    .update(body)
    .digest('hex');

  if (expectedSignature === razorpay_signature) {
    return res.json({ success: true, message: 'Payment verified' });
  }

  return res.status(400).json({ success: false, message: 'Invalid signature' });
});

app.listen(port, () => {
  console.log(`STYLEHUB API listening on http://localhost:${port}`);
});
