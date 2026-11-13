'use client';
import { useState, type FormEvent } from 'react';
import { analyze, Analysis } from '../lib/api';

export default function AnalysisForm({ onResult }: { onResult: (analysis: Analysis) => void }) {
  const [mode, setMode] = useState<'code' | 'sepolia_address'>('code');
  const [value, setValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  async function submit(event: FormEvent) {
    event.preventDefault(); setLoading(true); setError('');
    try { onResult(await analyze(mode, value)); }
    catch (cause) { setError(cause instanceof Error ? cause.message : 'The review request could not be completed.'); }
    finally { setLoading(false); }
  }
  return <form onSubmit={submit} className="panel p-5">
    <div className="mb-5 flex gap-2">
      <button type="button" onClick={() => setMode('code')} className={`rounded-lg px-3 py-2 text-sm ${mode === 'code' ? 'bg-indigo-500/20 text-indigo-200' : 'text-slate-400'}`}>Source code</button>
      <button type="button" onClick={() => { setMode('sepolia_address'); setValue(''); }} className={`rounded-lg px-3 py-2 text-sm ${mode === 'sepolia_address' ? 'bg-indigo-500/20 text-indigo-200' : 'text-slate-400'}`}>Sepolia address</button>
    </div>
    {mode === 'code'
      ? <textarea aria-label="Solidity source" value={value} onChange={event => setValue(event.target.value)} rows={15} className="input font-mono text-xs leading-6" placeholder="Paste Solidity source code for release review…" />
      : <input aria-label="Sepolia contract address" value={value} onChange={event => setValue(event.target.value)} className="input" placeholder="0x…" />}
    <p className="mt-3 text-xs text-slate-500">{mode === 'code' ? 'Submit candidate source code to generate evidence-backed review signals.' : 'Address review is limited to verified Sepolia source and available chain data.'}</p>
    {error && <p className="mt-3 rounded-lg bg-rose-500/10 p-3 text-sm text-rose-200">{error}</p>}
    <button disabled={loading || !value.trim()} className="btn mt-5 w-full">{loading ? 'Building Release Risk Brief…' : 'Build Release Risk Brief'}</button>
  </form>;
}
