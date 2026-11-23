import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = {
  title: "TRADE VISION | Trader Console",
  description: "Public trading journal and performance platform",
};
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
