"""Bounded, read-only transfer projections. RPC/branch/metadata context is fixture evidence,
not authenticated consensus. No requests, signing, broadcasting or economic effects.
"""
from pathlib import Path
import hashlib,json,re,sqlite3
from jsonschema import Draft202012Validator
ALPHABET='123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
TOKEN2022='TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb'
TOKEN='TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'
TRANSFER='0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
HERE=Path(__file__).parent

def sha(raw):return 'sha256:'+hashlib.sha256(raw).hexdigest()
def bytes_json(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def b58decode(s,length=None):
    if not isinstance(s,str) or not s or len(s)>128:raise ValueError('base58 bound')
    n=0
    for c in s:
        if c not in ALPHABET:raise ValueError('base58 alphabet')
        n=n*58+ALPHABET.index(c)
    raw=b'\0'*(len(s)-len(s.lstrip('1')))+(n.to_bytes((n.bit_length()+7)//8,'big') if n else b'')
    if length is not None and len(raw)!=length:raise ValueError('base58 length')
    return raw

def b58encode(raw):
    n=int.from_bytes(raw,'big');out=''
    while n:n,d=divmod(n,58);out=ALPHABET[d]+out
    return '1'*(len(raw)-len(raw.lstrip(b'\0')))+out

def hx(s,length):
    if not isinstance(s,str) or not re.fullmatch('0x[0-9a-fA-F]{'+str(length*2)+'}',s):raise ValueError('hex data')
    return s.lower()

def quantity(s):
    if not isinstance(s,str) or not re.fullmatch(r'0x(?:0|[1-9a-fA-F][0-9a-fA-F]*)',s) or len(s)>66:raise ValueError('hex quantity')
    return int(s,16)

def trust(c):
    if c.get('fixtureTrust')!='trusted-test-fixture-only':raise ValueError('source context is not a trusted fixture')

def fact(chain,network,location,asset,amount,sender,receiver,decoder,raw,parent=None,context=None):
    key=sha(bytes_json({'chain':chain,'network':network,'location':location}))
    result={'chain':chain,'network':network,'factId':key,'location':location,'asset':asset,'rawAmount':str(amount),'sender':sender,'receiver':receiver,'decoder':decoder,'sourceDigest':sha(bytes_json(parent if parent is not None else raw)),'fragmentDigest':sha(bytes_json(raw)),'contextDigest':sha(bytes_json(context)),'execution':'Succeeded','effectAuthority':False}
    validate_fact(result)
    return result

def validate_fact(f):
    Draft202012Validator(json.loads((HERE/'transfer.schema.json').read_text())).validate(f)
    n=int(f['rawAmount'])
    if not 0<=n<=(2**256-1 if f['chain']=='ethereum' else 2**64-1):raise ValueError('raw amount range')
    expected=sha(bytes_json({'chain':f['chain'],'network':f['network'],'location':f['location']}))
    if expected!=f['factId']:raise ValueError('physical fact ID')
    if f['chain']=='ethereum':
        hx(f['asset'],20);hx(f['sender'],20);hx(f['receiver'],20);hx(f['network']['genesis'],32)
        hx(f['location']['blockHash'],32);hx(f['location']['transactionHash'],32)
    else:
        for key in [f['asset'],f['sender'],f['receiver'],f['network']['genesis'],f['location']['branchHash']]:b58decode(key,32)
        b58decode(f['location']['signature'],64)

def ethereum(receipt,c):
    trust(c)
    if len(bytes_json(receipt))>1048576:raise ValueError('source body bound')
    network={'chainId':str(quantity(c['chainId'])),'genesis':hx(c['genesis'],32)}
    block=hx(receipt['blockHash'],32);tx=hx(receipt['transactionHash'],32);height=str(quantity(receipt['blockNumber']))
    if c['blockHash'].lower()!=block:raise ValueError('wrong branch context')
    status=receipt['status']
    if status not in ('0x0','0x1'):raise ValueError('unsupported receipt status')
    if len(receipt['logs'])>64:raise ValueError('log bound')
    if status=='0x0':return []  # diagnostics/fees remain in source evidence, not transfer effects.
    out=[];indices=set();allowed=hx(c['contract'],20)
    for log in receipt['logs']:
        if hx(log['blockHash'],32)!=block or hx(log['transactionHash'],32)!=tx:raise ValueError('inclusion mismatch')
        if log.get('removed',False):raise ValueError('removed evidence requires explicit journal invalidation')
        if hx(log['address'],20)!=allowed:continue
        topics=log['topics']
        if not topics or topics[0].lower()!=TRANSFER:continue
        # ERC721 Transfer uses four topics; never coerce it into ERC20 economics.
        if len(topics)!=3:raise ValueError('not reviewed ERC20 Transfer')
        a=hx(topics[1],32);b=hx(topics[2],32)
        if a[2:26]!='0'*24 or b[2:26]!='0'*24:raise ValueError('address padding')
        amount=int(hx(log['data'],32)[2:],16);index=str(quantity(log['logIndex']))
        if index in indices:raise ValueError('duplicate physical log index')
        indices.add(index)
        out.append(fact('ethereum',network,{'blockHash':block,'blockNumber':height,'transactionHash':tx,'logIndex':index},allowed,amount,'0x'+a[26:],'0x'+b[26:],'erc20-transfer-v0.1',log,receipt,c))
    return out

def solana(result,c):
    trust(c)
    if len(bytes_json(result))>1048576:raise ValueError('source body bound')
    if result['version']!='legacy':raise ValueError('transaction version outside this slice')
    b58decode(c['genesis'],32);b58decode(c['branchHash'],32)
    sig=result['transaction']['signatures'][0];b58decode(sig,64)
    if result['meta']['err'] is not None:return []  # fees/durable nonce may persist; not ordinary transfers.
    slot=result['slot']
    if type(slot) is not int or not 0<=slot<=2**64-1:raise ValueError('slot range')
    message=result['transaction']['message'];keys=message['accountKeys']
    if len(keys)>64:raise ValueError('key bound')
    for key in keys:b58decode(key,32)
    instructions=[]
    if len(message['instructions'])>16 or len(result['meta'].get('innerInstructions',[]))>16:raise ValueError('instruction bound')
    for i,ins in enumerate(message['instructions']):instructions.append((f'outer:{i}',ins))
    seen=set()
    for group in result['meta'].get('innerInstructions',[]):
        i=group['index']
        if type(i) is not int or i<0 or i>=len(message['instructions']) or i in seen:raise ValueError('inner group')
        seen.add(i)
        if len(group['instructions'])>16:raise ValueError('CPI bound')
        for j,ins in enumerate(group['instructions']):instructions.append((f'outer:{i}/inner:{j}',ins))
    balances=result['meta']['preTokenBalances'];out=[]
    for path,ins in instructions:
        p=ins['programIdIndex']
        if type(p) is not int or not 0<=p<len(keys):raise ValueError('program index')
        if keys[p]==TOKEN2022:raise ValueError('Token-2022 is outside this slice')
        if keys[p]!=TOKEN:continue  # other programs/extensions are unreviewed, not base-token effects.
        if '/inner:' in path:
            outcome=c.get('instructionOutcomes',{}).get(path)
            if outcome is None:raise ValueError('CPI success is unresolved; overall transaction success is insufficient')
            if outcome=='Failed':continue
            if outcome!='Succeeded' or c.get('instructionOutcomeSource')!='fixture-program-trace-v1':raise ValueError('unsupported CPI outcome evidence')
        data=b58decode(ins['data'])
        if len(data)!=10 or data[0]!=12:raise ValueError('only TransferChecked is admitted')
        indices=ins['accounts']
        if len(indices)<4 or any(type(k)is not int or not 0<=k<len(keys) for k in indices):raise ValueError('account index')
        source,mint,destination=indices[:3]
        entries=[x for x in balances if x['accountIndex']==source]
        if len(entries)!=1:raise ValueError('missing/ambiguous mint evidence')
        meta=entries[0]
        if meta['mint']!=keys[mint] or type(meta['uiTokenAmount']['decimals'])is not int or meta['uiTokenAmount']['decimals']!=data[9]:raise ValueError('mint/decimal evidence')
        amount=int.from_bytes(data[1:9],'little')
        out.append(fact('solana',{'genesis':c['genesis']},{'branchHash':c['branchHash'],'slot':str(slot),'signature':sig,'instructionPath':path},keys[mint],amount,keys[source],keys[destination],'spl-transferchecked-legacy-v0.1',ins,result,c))
    return out

class Journal:
    """Append-only source facts, observer deliveries and invalidations; SQLite projection only."""
    def __init__(self,path):
        self.db=sqlite3.connect(path);self.db.execute('PRAGMA journal_mode=WAL');self.db.execute('PRAGMA synchronous=FULL')
        self.db.execute('CREATE TABLE IF NOT EXISTS entries(seq INTEGER PRIMARY KEY, delivery TEXT UNIQUE, observed TEXT NOT NULL, kind TEXT NOT NULL, fact TEXT NOT NULL, body TEXT NOT NULL)');self.db.commit()
    def append(self,delivery,when,kind,fact_id,body):
        from validator import instant
        instant(when)
        if kind not in ('fact','invalidate','finality','gap'):raise ValueError('journal kind')
        if kind=='fact':
            validate_fact(body)
            if body['factId']!=fact_id:raise ValueError('fact identity')
        if kind=='finality' and body.get('commitment') not in ('ethereum:unsafe','ethereum:safe','ethereum:finalized','solana:processed','solana:confirmed','solana:finalized'):raise ValueError('native commitment')
        encoded=json.dumps(body,sort_keys=True,separators=(',',':'))
        with self.db:
            prior=self.db.execute('SELECT observed,kind,fact,body FROM entries WHERE delivery=?',(delivery,)).fetchone()
            current=(when,kind,fact_id,encoded)
            if prior:
                if prior!=current:raise ValueError('delivery identity conflict')
                return 'duplicate-delivery'
            if kind=='fact':
                rows=self.db.execute("SELECT body FROM entries WHERE fact=? AND kind='fact'",(fact_id,)).fetchall()
                # Source captures/decoder attestations can differ; economic physical fact cannot.
                economic=lambda x:{k:v for k,v in x.items() if k not in ('sourceDigest','fragmentDigest','contextDigest','decoder')}
                if any(economic(json.loads(row[0]))!=economic(body) for row in rows):raise ValueError('physical fact conflict')
            latest=self.db.execute('SELECT max(observed) FROM entries').fetchone()[0]
            if latest is not None and when<latest:raise ValueError('known-at clock regression')
            self.db.execute('INSERT INTO entries(delivery,observed,kind,fact,body) VALUES(?,?,?,?,?)',(delivery,*current))
        return 'recorded'
    def totals(self,as_of,required_commitment):
        from validator import instant
        instant(as_of)
        if required_commitment not in ('ethereum:unsafe','ethereum:safe','ethereum:finalized','solana:processed','solana:confirmed','solana:finalized'):raise ValueError('native commitment policy')
        facts={};invalid=set();finality={};gaps=[]
        for kind,fid,raw in self.db.execute('SELECT kind,fact,body FROM entries WHERE observed<=? ORDER BY seq',(as_of,)):
            body=json.loads(raw)
            if kind=='fact':facts[fid]=body
            elif kind=='invalidate':invalid.add(fid)
            elif kind=='finality':finality.setdefault(fid,{})[body['source']]=body['commitment']
            elif kind=='gap':gaps.append(body)
        totals={};contributors=[]
        for fid,f in facts.items():
            reports=finality.get(fid,{})
            if len(set(reports.values()))>1:
                gaps.append({'scope':fid,'missing':'contradictory-native-commitment','sources':reports});continue
            if fid in invalid or set(reports.values())!={required_commitment}:continue
            if not required_commitment.startswith(f['chain']+':'):raise ValueError('cross-chain finality')
            asset=json.dumps([f['chain'],f['network'],f['asset']],sort_keys=True)
            totals[asset]=str(int(totals.get(asset,'0'))+int(f['rawAmount']));contributors.append(fid)
        return {'rawTotals':totals,'factIds':sorted(contributors),'gaps':gaps,'coverage':'not-established-by-this-journal','effectAuthority':False}
    def close(self):self.db.close()
