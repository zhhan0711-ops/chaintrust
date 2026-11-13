import httpx
from datetime import datetime, timezone
from app.core.config import settings
from app.schemas.chain_data import ContractProfile, Deployment, ProxyAnalysis, Interaction
EIP1967_IMPLEMENTATION_SLOT='0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc'
EXPLORER_URL='https://api.etherscan.io/v2/api'
class SepoliaRpcProvider:
    def __init__(self): self.url=settings.sepolia_rpc_url
    async def _rpc(self, method, params):
        if not self.url or self.url=='[TO CONFIGURE]': return None
        async with httpx.AsyncClient(timeout=12) as client:
            r=await client.post(self.url,json={'jsonrpc':'2.0','id':1,'method':method,'params':params}); r.raise_for_status(); payload=r.json()
        if payload.get('error'): raise ValueError(f'RPC error: {payload["error"].get("message","unknown")}')
        return payload.get('result')
    async def _explorer(self, action, **params):
        if not settings.etherscan_api_key or settings.etherscan_api_key=='[TO CONFIGURE]': return None
        query={'chainid':'11155111','module':'contract' if action in ('getsourcecode','getcontractcreation') else 'account','action':action,'apikey':settings.etherscan_api_key,**params}
        async with httpx.AsyncClient(timeout=12) as client: r=await client.get(EXPLORER_URL,params=query); r.raise_for_status(); data=r.json()
        return data.get('result') if data.get('status')=='1' else None
    async def get_contract_profile(self,address,activity_limit):
        collected=datetime.now(timezone.utc).isoformat(); chain=await self._rpc('eth_chainId',[])
        if chain is None: return ContractProfile(address=address,has_code=False,collected_at=collected,deployment=Deployment(data_status='unavailable'),proxy_analysis=ProxyAnalysis(classification='unavailable',confidence='unavailable'),data_mode='live')
        if int(chain,16)!=11155111: raise ValueError('Configured RPC is not Sepolia (11155111).')
        code,balance,block,slot=await self._rpc('eth_getCode',[address,'latest']),await self._rpc('eth_getBalance',[address,'latest']),await self._rpc('eth_blockNumber',[]),await self._rpc('eth_getStorageAt',[address,EIP1967_IMPLEMENTATION_SLOT,'latest'])
        creation=await self._explorer('getcontractcreation',contractaddresses=address); txs=await self._explorer('txlist',address=address,sort='desc',page='1',offset=str(activity_limit)); source=await self._explorer('getsourcecode',address=address)
        item=creation[0] if isinstance(creation,list) and creation else {}; deployment=Deployment(transaction_hash=item.get('txHash'),deployer=item.get('contractCreator'),block_number=int(item['blockNumber']) if item.get('blockNumber','').isdigit() else None,timestamp=None,data_status='confirmed' if item else 'unavailable')
        interactions=[Interaction(transaction_hash=t.get('hash',''),timestamp=datetime.fromtimestamp(int(t['timeStamp']),timezone.utc).isoformat() if t.get('timeStamp','').isdigit() else None,block_number=int(t['blockNumber']) if t.get('blockNumber','').isdigit() else None,status='failed' if t.get('isError')=='1' else 'success',source='onchain_data') for t in (txs or []) if t.get('hash')]
        implementation=None if not slot or int(slot,16)==0 else '0x'+slot[-40:]
        return ContractProfile(address=address,has_code=code!='0x',balance_wei=str(int(balance,16)),current_block_number=int(block,16),collected_at=collected,rpc_status='confirmed',explorer_status='confirmed' if creation or txs or source else 'unavailable',deployment=deployment,interactions=interactions,interaction_count=len(interactions) if txs is not None else None,failed_transaction_count=sum(x.status=='failed' for x in interactions) if txs is not None else None,proxy_analysis=ProxyAnalysis(classification='eip1967_proxy' if implementation else 'not_detected',confidence='confirmed' if implementation else 'unavailable',evidence=[f'EIP-1967 implementation: {implementation}'] if implementation else [],implementation_address=implementation,evidence_type='onchain_data' if implementation else 'unavailable'),data_mode='live',source_link_status='unavailable')