import { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { FaPlane, FaHotel, FaHeartbeat, FaBlog } from 'react-icons/fa';

const baseUrl = 'http://localhost:8000/api';

const popularDestinations = [
  { name: 'Bali', price: 45000, image: 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80' },
  { name: 'Dubai', price: 60000, image: 'https://images.unsplash.com/photo-1542089363-d9e71a6a2d21?auto=format&fit=crop&w=1200&q=80' },
  { name: 'Maldives', price: 80000, image: 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80' },
  { name: 'Singapore', price: 55000, image: 'https://images.unsplash.com/photo-1549643136-fdc23d7f2440?auto=format&fit=crop&w=1200&q=80' },
  { name: 'Thailand', price: 40000, image: 'https://images.unsplash.com/photo-1496417263034-38ec4f0b665a?auto=format&fit=crop&w=1200&q=80' },
  { name: 'Vietnam', price: 50000, image: 'https://images.unsplash.com/photo-1533105042488-7c85f3cf6bf6?auto=format&fit=crop&w=1200&q=80' },
];

const dummyPackages = [
  { name: 'Bali Budget Trip', destination: 'Bali', days: 5, price: 45000 },
  { name: 'Dubai Luxury Trip', destination: 'Dubai', days: 6, price: 75000 },
  { name: 'Maldives Honeymoon', destination: 'Maldives', days: 4, price: 90000 },
];

const dummyBlogs = [
  { title: 'How to Plan Budget Travel in 2026', date: '2026-01-25', category: 'Budget' },
  { title: 'GST Rules for Travelers', date: '2026-02-10', category: 'Finance' },
  { title: 'Best Honeymoon Destinations', date: '2026-03-05', category: 'Honeymoon' },
];

const destinations = ['Bali','Dubai','Maldives','Singapore','Thailand','Vietnam','Europe','Japan'];

function App() {
  const [searchInput, setSearchInput] = useState('');
  const [duration, setDuration] = useState('5');
  const [budget, setBudget] = useState('60000');
  const [results, setResults] = useState<any[]>([]);
  const [chatOpen, setChatOpen] = useState(false);
  const [chatQuery, setChatQuery] = useState('');
  const [chatHistory, setChatHistory] = useState<{prompt:string, answer:string}[]>([]);
  const [itinerary, setItinerary] = useState<any>(null);
  const [planLoading, setPlanLoading] = useState(false);

  useEffect(() => {
    setResults(dummyPackages);
  }, []);

  const filtered = useMemo(() => {
    const minBudget = Number(budget);
    return results.filter((item) => item.price <= minBudget && Number(item.days) <= Number(duration) && (!searchInput || item.destination.toLowerCase().includes(searchInput.toLowerCase())));
  }, [results, searchInput, duration, budget]);

  const searchPackages = () => {
    setResults(dummyPackages);
  };

  const runItinerary = async () => {
    setPlanLoading(true);
    try {
      const response = await axios.post(`${baseUrl}/generate-itinerary`, {
        destination: searchInput || 'Bali',
        days: Number(duration),
        budget: Number(budget),
        people: 2,
      });
      setItinerary(response.data);
    } catch (e) {
      console.error(e);
      alert('Could not generate itinerary. Start backend and check logs.');
    } finally {
      setPlanLoading(false);
    }
  };

  const sendChat = async () => {
    if (!chatQuery.trim()) return;
    const q = chatQuery.trim();
    setChatHistory((prev) => [...prev, { prompt: q, answer: 'Thinking...' }]);
    setChatQuery('');
    try {
      const { data } = await axios.post(`${baseUrl}/chat`, { query: q });
      setChatHistory((prev) => {
        const copy = [...prev];
        copy[copy.length - 1].answer = data.answer;
        return copy;
      });
    } catch (err) {
      console.error(err);
      setChatHistory((prev) => {
        const copy = [...prev];
        copy[copy.length - 1].answer = 'Sorry, the AI chat is unavailable.';
        return copy;
      });
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 text-slate-800">
      <header className="bg-white shadow-sm">
        <div className="mx-auto flex max-w-7xl items-center justify-between p-3">
          <div className="text-2xl font-bold">PeaceTimeTravellers</div>
          <div className="hidden md:flex space-x-6 text-sm font-medium">
            <div className="relative group">
              <button className="hover:text-blue-600">International Packages</button>
              <div className="absolute left-0 top-full z-10 hidden w-48 rounded bg-white shadow-md group-hover:block">
                {destinations.map((d) => (<div key={d} className="px-3 py-2 hover:bg-slate-100">{d}</div>))}
              </div>
            </div>
            <span>Domestic Packages</span>
            <span>Honeymoon Packages</span>
            <span>Blogs</span>
            <span>Contact</span>
          </div>
          <div className="text-sm">📞 +91-9876543210 | ✉️ support@peacetimetravellers.com</div>
        </div>
      </header>

      <main className="relative">
        <section className="relative h-[660px] overflow-hidden bg-black text-white">
          <img
            src="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1600&q=80"
            alt="Travel bg"
            className="absolute inset-0 h-full w-full object-cover opacity-70"
          />
          <div className="relative mx-auto flex h-full max-w-7xl flex-col justify-center px-6 py-20">
            <h1 className="text-4xl font-extrabold sm:text-6xl">Holidays that fit you perfectly!</h1>
            <p className="mt-4 max-w-2xl text-lg sm:text-2xl">Your Pace • Your Budget • AI Travel Advisor • Custom Trips</p>
            <div className="mt-8 w-full max-w-4xl rounded-xl bg-white/90 p-6 text-slate-800 shadow-lg">
              <div className="flex flex-wrap gap-3">
                <input className="flex-1 rounded-md border p-3" placeholder="Destination: Bali" value={searchInput} onChange={(e) => setSearchInput(e.target.value)} />
                <select className="rounded-md border p-3" value={duration} onChange={(e) => setDuration(e.target.value)}>
                  {Array.from({ length: 8 }, (_, i) => i + 3).map((d) => (<option key={d}>{d}</option>))}
                </select>
                <select className="rounded-md border p-3" value={budget} onChange={(e) => setBudget(e.target.value)}>
                  {['20000','40000','60000','80000','100000'].map((b) => (<option key={b} value={b}>₹{b}</option>))}
                </select>
                <button onClick={searchPackages} className="rounded-md bg-blue-600 px-4 py-3 text-white">Search</button>
                <button onClick={runItinerary} className="rounded-md bg-emerald-600 px-4 py-3 text-white">Generate Itinerary</button>
              </div>
            </div>
            {itinerary && (
              <div className="mt-6 rounded-xl bg-white/95 p-5 shadow">
                <h2 className="text-xl font-bold">Generated Itinerary for {itinerary.destination}</h2>
                <p>Estimated Cost: {itinerary.estimated_cost}</p>
                <ul className="list-disc pl-5">
                  {itinerary.itinerary.map((x: any) => <li key={x.day}>{x.day}. {x.plan}</li>)}
                </ul>
              </div>
            )}
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-6 py-10">
          <h2 className="text-3xl font-bold">Popular Destinations</h2>
          <div className="mt-6 grid grid-cols-1 gap-6 md:grid-cols-3">
            {popularDestinations.map((dest) => (
              <div key={dest.name} className="overflow-hidden rounded-xl bg-white shadow hover:shadow-lg">
                <img className="h-52 w-full object-cover" src={dest.image} alt={dest.name} />
                <div className="p-4">
                  <h3 className="text-xl font-bold">{dest.name}</h3>
                  <p className="text-slate-600">Starting at ₹{dest.price.toLocaleString()}</p>
                  <button className="mt-3 rounded-xl bg-blue-600 px-4 py-2 text-white">View Package</button>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-6 py-10">
          <h2 className="flex items-center gap-2 text-3xl font-bold"><FaPlane /> Package Listing</h2>
          <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-3">
            {filtered.map((pkg) => (
              <div key={pkg.name} className="rounded-xl border p-4 shadow-sm">
                <h3 className="text-xl font-semibold">{pkg.name}</h3>
                <p>Destination: {pkg.destination}</p>
                <p>Duration: {pkg.days} Days</p>
                <p className="font-bold text-blue-600">₹{pkg.price.toLocaleString()}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-6 py-10">
          <h2 className="flex items-center gap-2 text-3xl font-bold"><FaBlog /> Travel Blog</h2>
          <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-3">
            {dummyBlogs.map((blog) => (
              <article key={blog.title} className="rounded-xl border p-4 shadow-sm">
                <h3 className="text-lg font-semibold">{blog.title}</h3>
                <p className="text-xs text-slate-500">{blog.category} · {blog.date}</p>
                <p className="mt-2">A quick summary for 2026-focused travel tips and budget strategies.</p>
                <button className="mt-3 rounded-lg bg-amber-500 px-3 py-1 text-sm text-white">Read More</button>
              </article>
            ))}
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-6 py-10">
          <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
            <div className="rounded-xl bg-white p-5 shadow"><h4><FaHotel /> Hotels</h4><p>Smart hotel suggestions from AI for all budgets.</p></div>
            <div className="rounded-xl bg-white p-5 shadow"><h4><FaHeartbeat /> Wellness</h4><p>Top peace retreats for calm travel.</p></div>
            <div className="rounded-xl bg-white p-5 shadow"><h4>⭐ Wishlist</h4><p>Save favorites and compare packages.</p></div>
            <div className="rounded-xl bg-white p-5 shadow"><h4>🗣 Voice Chat</h4><p>Voice-enabled chat soon (future upgrade).</p></div>
          </div>
        </section>
      </main>

      <div className="fixed bottom-5 right-5 z-50">
        <button onClick={() => setChatOpen((v) => !v)} className="rounded-full bg-blue-600 px-4 py-3 text-white shadow-lg">Traveller Buddy 🤖</button>
        {chatOpen && (
          <div className="mt-3 w-96 rounded-xl border bg-white p-4 shadow-xl">
            <div className="mb-2 flex justify-between text-sm font-semibold">AI Chat<p className="cursor-pointer text-red-500" onClick={() => setChatOpen(false)}>X</p></div>
            <div className="max-h-96 space-y-3 overflow-y-auto border-t pt-2">
              {chatHistory.map((entry, idx) => (
                <div key={idx} className="space-y-1">
                  <div className="text-xs text-slate-500">You: {entry.prompt}</div>
                  <div className="rounded-lg bg-slate-50 p-2 text-sm">{entry.answer}</div>
                </div>
              ))}
            </div>
            <div className="mt-2 flex gap-2">
              <input type="text" value={chatQuery} onChange={(e) => setChatQuery(e.target.value)} className="flex-1 rounded-md border p-2" placeholder="Ask Traveller Buddy" />
              <button onClick={sendChat} className="rounded-md bg-blue-600 px-3 text-white">Send</button>
            </div>
          </div>
        )}
      </div>

      <footer className="bg-slate-800 text-white">
        <div className="mx-auto flex max-w-7xl flex-wrap justify-between gap-4 p-6">
          <p>© 2026 PeaceTimeTravellers | Travel Smart. Travel Peacefully.</p>
          <p>Powered by FastAPI + React + RAG + OpenAI</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
