'use client';
import { useState } from 'react';
import AnalysisForm from '../components/AnalysisForm';
import RiskDashboard from '../components/RiskDashboard';
import { Analysis } from '../lib/api';
import Link from 'next/link';

export default function Home() {
  const [analysis, setAnalysis] = useState<Analysis>();
  return <main className="mx-auto max-w-6xl px-6 pb-12">
    <section className="mb-10 grid gap-6 lg:grid-cols-[1.05fr_.95fr]"><div className="pt-8">
      <p className="label text-electric">AI-powered · Sepolia review workspace</p>
      <h1 className="mt-3 text-5xl font-bold leading-tight tracking-tight">Release risk intelligence for <span className="bg-gradient-to-r from-electric to-violet bg-clip-text text-transparent">on-chain systems.</span></h1>
      <p className="mt-5 max-w-xl text-lg leading-8 text-slate-400">Build an evidence-aware review brief from source signals today, then extend the workflow with privilege, upgradeability, on-chain activity, and tamper-evident review records.</p>
      <div className="mt-7 flex flex-wrap items-center gap-6 text-sm text-slate-400"><span>◈ Source signals</span><span>◈ Review evidence</span><span>◈ Hash record</span><Link href="/profile" className="rounded-xl border border-violet/40 px-4 py-2 font-semibold text-violet">Open Sample Review</Link></div>
    </div><AnalysisForm onResult={setAnalysis} /></section>
    {analysis ? <RiskDashboard analysis={analysis} /> : <section className="panel grid place-items-center px-6 py-12 text-center"><div><p className="text-lg font-semibold">Your Release Risk Brief will appear here</p><p className="mt-2 text-sm text-slate-500">Submit candidate source code or a verified Sepolia contract address to begin an engineering review.</p></div></section>}
  </main>;
}
