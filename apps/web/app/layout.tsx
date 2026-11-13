import './globals.css';
import Link from 'next/link';
import type { ReactNode } from 'react';

export const metadata = { title: 'ChainTrust | Release & Risk Intelligence', description: 'Evidence-aware smart contract release and risk intelligence for Sepolia review workflows.' };

export default function RootLayout({ children }: { children: ReactNode }) {
  return <html lang="en"><body>
    <header className="mx-auto flex max-w-6xl items-center justify-between px-6 py-6">
      <Link href="/" className="flex items-center gap-3 font-bold tracking-tight"><span className="grid h-9 w-9 place-items-center rounded-xl bg-gradient-to-br from-electric to-violet text-lg">⌬</span><span>Chain<span className="text-electric">Trust</span></span></Link>
      <nav className="flex gap-5 text-sm text-slate-300"><Link href="/">Release brief</Link><Link href="/registry">Review records</Link><span className="rounded-full border border-violet/40 bg-violet/10 px-2 py-0.5 text-xs text-violet">Sepolia</span></nav>
    </header>
    {children}
    <footer className="mx-auto max-w-6xl px-6 py-10 text-xs text-slate-500">ChainTrust supports engineering review workflows. Findings are evidence-backed signals, not a security guarantee, and do not replace a professional security audit.</footer>
  </body></html>;
}
