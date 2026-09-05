/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          bg: '#0a0a0f',
          card: '#12121a',
          border: '#1e1e2a',
          muted: '#6b6b80',
          accent: '#00d4aa',
          error: '#ff4756',
          warning: '#ffa502',
        },
        light: {
          bg: '#f8f9fa',
          card: '#ffffff',
          border: '#e0e0e0',
          muted: '#6c757d',
          accent: '#20c997',
          error: '#dc3545',
          warning: '#fd7e14',
        }
      }
    }
  },
  plugins: [],
}