"""Archive primary Solana documentation through Scrapling; no TLS bypass."""
from scrapling.fetchers import Fetcher
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json, hashlib, datetime
ROOT=Path(__file__).parent
SOURCES=[
('rpc-http','https://solana.com/docs/rpc/http'),
('rpc-websocket','https://solana.com/docs/rpc/websocket'),
('rpc-structures','https://solana.com/docs/rpc/json-structures'),
('accounts','https://solana.com/docs/core/accounts'),
('transactions','https://solana.com/docs/core/transactions'),
('cpi','https://solana.com/docs/core/cpi'),
('confirmation','https://solana.com/developers/guides/advanced/confirmation'),
('durable-nonce','https://solana.com/developers/guides/advanced/introduction-to-durable-nonces'),
('tokens','https://www.solana-program.com/docs/token'),
('token-2022','https://www.solana-program.com/docs/token-2022'),
('token-extensions','https://www.solana-program.com/docs/token-2022/extensions'),
('associated-token','https://www.solana-program.com/docs/associated-token-account'),
('wallet-standard','https://raw.githubusercontent.com/wallet-standard/wallet-standard/master/extensions/solana.md'),
('wallet-signers','https://raw.githubusercontent.com/anza-xyz/wallet-adapter/master/packages/core/base/src/signer.ts'),
('nonce-runtime','https://solana.com/docs/core/transactions/durable-nonces'),
('versioned-transactions','https://solana.com/docs/core/transactions/versions'),
('account-structure','https://solana.com/docs/core/accounts/account-structure'),
('transaction-pipeline','https://solana.com/docs/core/transactions/transaction-pipeline'),
('wormhole-core-solana','https://docs.wormhole.com/products/messaging/reference/core-contract-solana/'),
('metaplex-core','https://developers.metaplex.com/core'),
('wormhole-solana','https://wormhole.com/docs/products/messaging/guides/solana-shim/'),
('jupiter-swap','https://dev.jup.ag/docs/swap-api'),
]
SOURCES += [(m,'https://solana.com/docs/rpc/http/'+m) for m in ['getaccountinfo','getprogramaccounts','getbalance','gettokenaccountbalance','gettokenaccountsbyowner','gettokensupply','gettransaction','getblock','getsignaturestatuses','getsignaturesforaddress','sendtransaction','simulatetransaction','getlatestblockhash','isblockhashvalid','getgenesishash','getversion','getepochinfo','getstakeactivation']]
SOURCES += [(m,'https://solana.com/docs/rpc/websocket/'+m) for m in ['accountsubscribe','programsubscribe','logssubscribe','signaturesubscribe','slotsubscribe','rootsubscribe','blocksubscribe','slotsupdatessubscribe','votesubscribe']]
def fetch(item):
 name,url=item
 try:
  r=Fetcher.get(url,timeout=35)
  body=bytes(r.body); txt=r.get_all_text()
  (ROOT/(name+'.raw')).write_bytes(body); (ROOT/(name+'.txt')).write_text(txt)
  m=dict(id=name,url=url,resolved_url=str(r.url),status=r.status,retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),fetcher='Scrapling Fetcher.get(timeout=35); TLS verification enabled',raw_path=name+'.raw',text_path=name+'.txt',raw_sha256=hashlib.sha256(body).hexdigest(),text_sha256=hashlib.sha256(txt.encode()).hexdigest(),text_chars=len(txt),evidence_usable=r.status==200)
 except Exception as e: m=dict(id=name,url=url,error=str(e),evidence_usable=False)
 (ROOT/(name+'.metadata.json')).write_text(json.dumps(m,indent=2)+'\n'); return m
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=6) as pool: records=list(pool.map(fetch,SOURCES))
 (ROOT/'manifest.json').write_text(json.dumps(records,indent=2)+'\n')
 for r in records: print(r['id'],r.get('status'),r.get('text_chars'),r.get('error',''))
