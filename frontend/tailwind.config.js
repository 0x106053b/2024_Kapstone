/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}", // src 폴더 내의 모든 JSX/TSX 파일을 대상으로 Tailwind CSS를 적용
  ],
  theme: {
    extend: {
      colors: {
        skkuGreen: "#0E341B", // 커스텀 색상 추가
        skkuOrange: "#ff6c0f",
        skkuliteGreen: "#8dc63f",
      },
      fontFamily: {
        sans: ["Roboto", "sans-serif"],
      },
    },
  },
  plugins: [],
};
