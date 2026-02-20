import { geistSans, geistMono } from "@/assets/fonts";
import "@/assets/styles/globals.css";

export const metadata = {
  title: "iTap",
  description: "Tap in. Stay synced.",
  icons: {
    icon: [{ url: "/images/meta_logo.svg" }],
    shortcut: ["/images/meta_logo.svg"],
    apple: [{ url: "/images/meta_logo.svg" }],
  },
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
