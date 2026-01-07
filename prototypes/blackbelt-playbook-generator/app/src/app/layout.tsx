import type { Metadata } from "next";
import { Montserrat } from "next/font/google";
import "./globals.css";

const montserrat = Montserrat({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800", "900"],
  variable: "--font-montserrat",
});

export const metadata: Metadata = {
  title: "Playbook Generator | BlackBelt",
  description: "Generate professional onboarding playbooks for any role in 30 seconds. Fill out a simple form, get a customized playbook ready to download as DOCX or Markdown.",
  metadataBase: new URL('https://app-eight-indol-52.vercel.app'),
  openGraph: {
    title: "Playbook Generator | BlackBelt",
    description: "Generate professional onboarding playbooks for any role in 30 seconds.",
    type: "website",
    siteName: "BlackBelt Playbook Generator",
  },
  twitter: {
    card: "summary_large_image",
    title: "Playbook Generator | BlackBelt",
    description: "Generate professional onboarding playbooks for any role in 30 seconds.",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${montserrat.className} antialiased`}>
        {children}
      </body>
    </html>
  );
}
