"""Archive primary Ethereum application sources with Scrapling, not runtime fetching."""
from scrapling.fetchers import Fetcher
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json, hashlib, datetime
ROOT=Path(__file__).parent
SOURCES=[
('json-rpc','https://ethereum.org/developers/docs/apis/json-rpc/'),
('execution-api','https://raw.githubusercontent.com/ethereum/execution-apis/main/src/eth/transaction.yaml'),
('pubsub','https://geth.ethereum.org/docs/interacting-with-geth/rpc/pubsub'),
('eip1474','https://eips.ethereum.org/EIPS/eip-1474'),
('eip1898','https://eips.ethereum.org/EIPS/eip-1898'),
('eip1193','https://eips.ethereum.org/EIPS/eip-1193'),
('eip2255','https://eips.ethereum.org/EIPS/eip-2255'),
('eip712','https://eips.ethereum.org/EIPS/eip-712'),
('eip3085','https://eips.ethereum.org/EIPS/eip-3085'),
('eip3326','https://eips.ethereum.org/EIPS/eip-3326'),
('erc20','https://eips.ethereum.org/EIPS/eip-20'),
('erc721','https://eips.ethereum.org/EIPS/eip-721'),
('erc1155','https://eips.ethereum.org/EIPS/eip-1155'),
('abi','https://docs.soliditylang.org/en/latest/abi-spec.html'),
('abi-source','https://raw.githubusercontent.com/ethereum/solidity/develop/docs/abi-spec.rst'),
('finality','https://ethereum.org/developers/docs/consensus-mechanisms/pos/'),
('uniswap-v3-events','https://raw.githubusercontent.com/Uniswap/v3-core/main/contracts/interfaces/pool/IUniswapV3PoolEvents.sol'),
('optimism-bridge','https://docs.optimism.io/app-developers/bridging/standard-bridge'),
('eip4844','https://eips.ethereum.org/EIPS/eip-4844'),
('eip7702','https://eips.ethereum.org/EIPS/eip-7702'),
('erc4337','https://ercs.ethereum.org/ERCS/erc-4337'),
('erc7769','https://ercs.ethereum.org/ERCS/erc-7769'),
('eip5792','https://eips.ethereum.org/EIPS/eip-5792'),
]
def fetch(item):
 name,url=item
 try:
  r=Fetcher.get(url,timeout=35)
  body=bytes(r.body); txt=r.get_all_text()
  (ROOT/(name+'.raw')).write_bytes(body); (ROOT/(name+'.txt')).write_text(txt)
  m={'id':name,'url':url,'resolved_url':str(r.url),'status':r.status,'retrieved_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fetcher':'Scrapling Fetcher.get(timeout=35); TLS verification enabled','raw_path':name+'.raw','text_path':name+'.txt','raw_sha256':hashlib.sha256(body).hexdigest(),'text_sha256':hashlib.sha256(txt.encode()).hexdigest(),'text_chars':len(txt)}
 except Exception as e: m={'id':name,'url':url,'error':str(e),'retrieved_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 (ROOT/(name+'.metadata.json')).write_text(json.dumps(m,indent=2)+'\n'); return m
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=4) as pool: records=list(pool.map(fetch,SOURCES))
 (ROOT/'manifest.json').write_text(json.dumps(records,indent=2)+'\n')
 for r in records: print(r['id'],r.get('status'),r.get('text_chars'),r.get('error',''))
