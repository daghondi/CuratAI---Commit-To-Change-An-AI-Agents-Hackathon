module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
    './lib/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#a855f7',
        secondary: '#3b82f6',
      },
      animation: {
        slideInUp: 'slideInUp 0.3s ease-out',
      },
    },
  },
  plugins: [require('@tailwindcss/forms')],
};
