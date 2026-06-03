/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0e1016",
        panel: "#171b24",
        "panel-lighter": "#202635",
        border: "#353c4d",
        text: "#f5f7fb",
        muted: "#a9b2c7",
        accent: "#ff7a3d",
        blue: "#6bd6ff",
      },
    },
  },
  plugins: [],
}
