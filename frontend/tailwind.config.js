/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        "autou-creme": "#F3F3E0",
        "autou-azul-escuro": "#27548A",
        "autou-azul-quase-preto": "#183B4E",
        "autou-amarelo-dourado": "#DDA853",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        chart: {
          1: "hsl(var(--chart-1))",
          2: "hsl(var(--chart-2))",
          3: "hsl(var(--chart-3))",
          4: "hsl(var(--chart-4))",
          5: "hsl(var(--chart-5))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      boxShadow: {
        "custom-sm": "0 1px 2px 0 rgba(var(--foreground-rgb), 0.05)",
        "custom-md":
          "0 4px 6px -1px rgba(var(--foreground-rgb), 0.1), 0 2px 4px -2px rgba(var(--foreground-rgb), 0.06)",
        "custom-lg":
          "0 10px 15px -3px rgba(var(--foreground-rgb), 0.1), 0 4px 6px -4px rgba(var(--foreground-rgb), 0.05)",
        "custom-xl":
          "0 20px 25px -5px rgba(var(--foreground-rgb), 0.1), 0 8px 10px -6px rgba(var(--foreground-rgb), 0.05)",
        "custom-inner": "inset 0 2px 4px 0 rgba(var(--foreground-rgb), 0.06)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};
