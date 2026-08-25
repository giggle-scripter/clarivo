import type { Metadata } from "next";

import { AppHeader } from "@/components/ui/AppHeader";

import "./globals.css";


export const metadata: Metadata = {
  title: "Clarivo — Nói rõ điều bạn nghĩ",
  description:
    "Luyện cách trình bày rõ ràng, mạch lạc và có cấu trúc bằng tiếng Việt.",
};


export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="vi">
      <body>
        <div className="page-shell">
          <AppHeader />
          {children}
        </div>
      </body>
    </html>
  );
}
