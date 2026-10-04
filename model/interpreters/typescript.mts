/** Independent RFQ interpreter. No Python/Rust calls or generated semantic engine. */
import {readFileSync,realpathSync,lstatSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {createInterface} from 'node:readline';
import {resolve} from 'node:path';
const root=resolve(process.argv[2]||'model');
function fail(message:string):never {throw new Error(message)}
export function parse(raw:string):any {
 if(Buffer.byteLength(raw)>3926)fail('body-bound');let i=0;
 function ws(){while(/[ \t\r\n]/.test(raw[i]||'x'))i++}
 function str(){let start=i++;while(i<raw.length){if(raw[i]==='\\'){i+=2;continue}if(raw[i++]==='"'){
  let s=JSON.parse(raw.slice(start,i));if([...s].length>512)fail('string-bound');
  for(let k=0;k<s.length;k++){let c=s.charCodeAt(k);if(c>=0xd800&&c<=0xdbff){let d=s.charCodeAt(++k);if(!(d>=0xdc00&&d<=0xdfff))fail('surrogate')}else if(c>=0xdc00&&c<=0xdfff)fail('surrogate')}return s;
 }}fail('string')}
 function value(depth:number):any {if(depth>12)fail('depth');ws();let c=raw[i];
  if(c==='"')return str();
  if(c==='{'){i++;let o:any=Object.create(null);ws();if(raw[i]==='}'){i++;return o}while(true){ws();if(raw[i]!=='"')fail('key');let k=str();if(Object.hasOwn(o,k))fail('duplicate-key');ws();if(raw[i++]!==':')fail('colon');o[k]=value(depth+1);ws();let d=raw[i++];if(d==='}')return o;if(d!==',')fail('object')}}
  if(c==='['){i++;let a:any[]=[];ws();if(raw[i]===']'){i++;return a}while(true){a.push(value(depth+1));if(a.length>16)fail('array');ws();let d=raw[i++];if(d===']')return a;if(d!==',')fail('array')}}
  for(const [t,v] of [['true',true],['false',false],['null',null]] as const){if(raw.startsWith(t,i)){i+=t.length;return v}}
  let match=/^(0|[1-9][0-9]*)/.exec(raw.slice(i));if(!match)fail('integer-token');let token=match[0];i+=token.length;
  if(/[.eE0-9]/.test(raw[i]||'x')||token.length>16||!Number.isSafeInteger(Number(token)))fail('integer-token');return Number(token);
 }
 let v=value(0);ws();if(i!==raw.length)fail('trailing');return v;
}
function canonical(v:any):string {if(v===null||typeof v!=='object')return JSON.stringify(v);if(Array.isArray(v))return '['+v.map(canonical).join(',')+']';return '{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+canonical(v[k])).join(',')+'}'}
function hash(raw:string|Buffer){return 'sha256:'+createHash('sha256').update(raw).digest('hex')}
function refs(v:any){if(v&&typeof v==='object'){for(let k of Object.keys(v)){if(['$ref','$dynamicRef','$recursiveRef'].includes(k))fail('references');refs(v[k])}}}
function schema(s:any,v:any):void {
 if(Object.hasOwn(s,'const')&&canonical(s.const)!==canonical(v))fail('const');
 if(s.enum&&!s.enum.some((x:any)=>canonical(x)===canonical(v)))fail('enum');
 if(s.type==='object'){if(!v||Array.isArray(v)||typeof v!=='object')fail('object');for(let k of s.required||[])if(!Object.hasOwn(v,k))fail('required');for(let k of Object.keys(v)){if(!Object.hasOwn(s.properties,k))fail('unknown');schema(s.properties[k],v[k])}}
 if(s.type==='string'){if(typeof v!=='string')fail('string');if(s.maxLength&&[...v].length>s.maxLength)fail('length');if(s.pattern){let m=new RegExp(s.pattern).exec(v);if(!m||m.index!==0||m[0].length!==v.length)fail('grammar')}}
}
function load(e:any){const installed=JSON.parse(readFileSync(root+'/profiles/installed.json','utf8')),entry=installed[e.mpecontract];
 if(!entry||entry.profile!==e.mpeprofile||entry.mode!=='conformance'||e.mpeprofile!=='rfq.v0.2')fail('unsupported');
 const folder=root+'/bundles/'+e.mpecontract.slice(7);if(entry.directory!=='bundles/'+e.mpecontract.slice(7)||lstatSync(folder).isSymbolicLink()||realpathSync(folder)!==folder)fail('bundle-path');
 const manifest=JSON.parse(readFileSync(folder+'/manifest.json','utf8'));if(Object.keys(manifest).sort().join(',')!=='bundleVersion,profile,resources,role,schema,signatures,status,version'||manifest.bundleVersion!==1||manifest.version!=='0.2'||manifest.status!=='experimental-model-only'||manifest.signatures!=='unsigned-fixture-only'||hash(canonical(manifest))!==e.mpecontract||manifest.profile!==e.mpeprofile)fail('manifest');
 if(Object.keys(manifest.resources).sort().join(',')!=='core.json,rules.json,schema.json')fail('closure');let capture:any={};
 for(let name of Object.keys(manifest.resources)){let p=folder+'/'+name;if(lstatSync(p).isSymbolicLink())fail('symlink');let raw=readFileSync(p);if(hash(raw)!==manifest.resources[name])fail('integrity');capture[name]=JSON.parse(raw.toString())}
 refs(capture['schema.json']);if(capture['rules.json'].profile!==e.mpeprofile||capture['rules.json'].role!==manifest.role||capture['core.json'].version!=='0.2'||capture['schema.json'].$id!=='urn:mpe:model:'+e.mpeprofile)fail('metadata');return capture['schema.json'];
}
function instant(s:any){if(typeof s!=='string'||!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.000Z$/.test(s)||Number(s.slice(0,4))<1)fail('time');let d=new Date(s);if(!Number.isFinite(d.getTime())||d.toISOString()!==s)fail('calendar');return d.getTime()}
function equal(a:any,b:any){return canonical(a)===canonical(b)}
function interpret(raw:string,c:any):any {let e=parse(raw);schema(load(e),e);if(c.fixtureTrust!=='trusted-test-fixture-only')fail('trust');const d=e.data,now=instant(c.now),ref=c.rfqs[d.rfqId],source=c.sources[e.source];
 if(!source||source.role!=='dealer'||source.principal!==d.dealer||!ref||ref.state!=='open')fail('source-state');
 for(let k of ['requester','dealer','requesterSide','asset','quantity','currency'])if(!equal(d[k],ref[k]))fail('terms');
 const [buyer,seller]=d.requesterSide==='BuyAsset'?[d.requester,d.dealer]:[d.dealer,d.requester];if(buyer===seller||d.buyer!==buyer||d.seller!==seller)fail('roles');
 if(d.price.assetRef!==d.asset||d.price.unit!==d.quantity.unit||d.price.currency!==d.currency)fail('basis');
 if(!(instant(e.time)<=instant(d.validFrom)&&instant(d.validFrom)<=now&&now<instant(d.validUntil)))fail('expiry');
 const cash=BigInt(d.quantity.coefficient)*BigInt(d.price.value.coefficient);if(cash>999999999999999999n||cash!==BigInt(d.cash.coefficient))fail('cash');
 const intent={domain:'mpe.model.intent.v0.2',source:e.source,type:e.type,profile:e.mpeprofile,contract:e.mpecontract,data:d};
 return {status:'offchain-quote-valid',businessDigest:hash(canonical(intent)),canonicalEvent:canonical(e),canonicalIntent:canonical(intent),executes:false};
}
/** Adapter A: dollar price per share, requester perspective. Exact closed source. */
function adaptA(input:any,template:any):any {let keys=['format','quantity','unitPriceDollars','currency','basisShares','perspective','fees'];if(Object.keys(input).sort().join()!==keys.sort().join()||input.format!=='dealer-a.usd-share.v1'||input.currency!=='USD'||input.basisShares!=='1'||input.perspective!=='RequesterBuy'||input.fees!=='None')fail('adapter-contract');if(!/^[1-9][0-9]{0,17}$/.test(input.quantity)||!/^(0|[1-9][0-9]*)\.[0-9]{2}$/.test(input.unitPriceDollars))fail('adapter-amount');let cents=BigInt(input.unitPriceDollars.replace('.',''));if(cents<=0n||cents>999999999999999999n)fail('adapter-price');let e=structuredClone(template);e.data.quantity.coefficient=input.quantity;e.data.price.value.coefficient=cents.toString();e.data.cash.coefficient=(BigInt(input.quantity)*cents).toString();if(BigInt(e.data.cash.coefficient)>999999999999999999n)fail('adapter-overflow');return e;}
const occurrences=new Map<string,string>();
const lines=createInterface({input:process.stdin});for await(const line of lines){try{let q=JSON.parse(line);let result=q.kind==='adapter-a'?{event:adaptA(q.input,q.template),executes:false}:interpret(q.raw,q.context);if(q.kind==='process'&&result.status==='offchain-quote-valid'){let e=parse(q.raw),key=e.source+'|'+e.id,old=occurrences.get(key);if(old&&old!==result.canonicalEvent)fail('event conflict');if(old)result.status='duplicate-event';occurrences.set(key,result.canonicalEvent)}console.log(JSON.stringify(result))}catch(e){console.log(JSON.stringify({status:'reject',executes:false}))}}
