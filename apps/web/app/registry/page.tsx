import { registryAddress } from '../../lib/contracts';

export default function Registry() {
  return <main className="mx-auto max-w-3xl px-6 py-12"><p className="label text-electric">Sepolia review records</p><h1 className="mt-2 text-4xl font-bold">Tamper-evident review registry</h1><div className="panel mt-8 p-6"><p className="text-sm text-slate-400">The registry stores only source and Release Risk Brief hashes, timestamp, and submitting wallet. Review content remains off-chain and is not published by this contract.</p><div className="mt-6 rounded-xl border border-white/10 bg-black/20 p-4"><p className="label">Configured registry</p><code className="mt-2 block text-sm text-electric">{registryAddress}</code></div><p className="mt-6 text-sm text-slate-500">Historical lookup becomes available after <code>NEXT_PUBLIC_REGISTRY_ADDRESS</code> is configured. Submit a completed brief to create a Sepolia review record.</p></div></main>;
}
