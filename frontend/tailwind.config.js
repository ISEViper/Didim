/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',

  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
theme: {
    extend: {
      colors: {
        main: 'var(--bg-main)',      
        primary: 'var(--text-main)',  
        
        'grad-start': 'var(--gradient-start)',
        'grad-end': 'var(--gradient-end)',
      },
      fontFamily: {
        pretendard: ["Pretendard", "sans-serif"],
      }
    },
  },
  plugins: [],
}