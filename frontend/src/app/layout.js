import { geistSans, geistMono } from "@/assets/fonts";
import "@/assets/styles/globals.css";

export const metadata = {
  title: "iTap",
  description: "Tap in. Stay synced.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
        {children}
      </body>
    </html>
  );
}
