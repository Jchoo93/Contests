/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        'energy': {
          'solar': '#FFA500',
          'wind': '#87CEEB',
          'hydro': '#1E90FF',
          'fossil': '#696969',
          'nuclear': '#FFD700',
        }
      }
    },
  },
  plugins: [],
}
