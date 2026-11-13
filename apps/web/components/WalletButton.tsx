'use client';
import { useState } from 'react';
import { BrowserProvider, Contract } from 'ethers';
import { registryAbi, registryAddress } from '../lib/contracts';

declare global { interface Window { ethereum?: unknown } }

export default function WalletButton({ sourceHash, reportHash }: { sourceHash: string; reportHash: string }) {
  const [status, setStatus] = useState('');
  async function record() {
    if (registryAddress === '[TO CONFIGURE]') { setStatus('Registry address is [TO CONFIGURE]. Deploy the contract and update NEXT_PUBLIC_REGISTRY_ADDRESS.'); return; }
    if (!window.ethereum) { setStatus('No injected wallet detected. Install or open a Sepolia-compatible wallet.'); return; }
    try {
      const provider = new BrowserProvider(window.ethereum as any);
      await provider.send('eth_requestAccounts', []);
      if ((await provider.getNetwork()).chainId !== 11155111n) throw new Error('Switch your wallet to Sepolia before submitting.');
      const contract = new Contract(registryAddress, registryAbi, await provider.getSigner());
      const transaction = await contract.recordAnalysis(sourceHash, reportHash);
      setStatus(`Submitted: ${transaction.hash}. Waiting for confirmation…`);
      await transaction.wait();
      setStatus(`Recorded on Sepolia: ${transaction.hash}`);
    } catch (error) { setStatus(error instanceof Error ? error.message : 'Wallet action failed.'); }
  }
  return <div><button className="btn" onClick={record}>Connect wallet & record hash</button>{status && <p className="mt-2 text-xs text-slate-400">{status}</p>}</div>;
}
