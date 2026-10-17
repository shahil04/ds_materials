/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#111827',
        parchment: '#f8f3ec',
        sand: '#d7b98d',
        blush: '#f4e9df',
        accent: '#c58f4d',
        deep: '#1a1715'
      },
      fontFamily: {
        display: ['"Poppins"', 'sans-serif'],
        body: ['"Inter"', 'sans-serif']
      },
      boxShadow: {
        soft: '0 12px 30px rgba(17, 24, 39, 0.08)'
      }
    }
  },
  plugins: []
};
