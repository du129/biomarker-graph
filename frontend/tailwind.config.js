import animate from 'tailwindcss-animate';

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#09090b", // zinc-950
        surface: "#18181b", // zinc-900
        primary: "#10b981", // emerald-500
        secondary: "#3b82f6", // blue-500
        danger: "#ef4444", // red-500
        muted: "#71717a", // zinc-500
      }
    },
  },
  plugins: [
    animate
  ],
}
