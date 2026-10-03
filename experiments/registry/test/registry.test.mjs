// Functional test of registry.compact and fallback.compact in the
// compact-runtime simulator (no proofs, no node, no network).
//
// Run through test/run.sh, which compiles the contracts with --skip-zk into a
// scratch directory and links a compact-runtime 0.20.0 node_modules there.
// Env: REG = path of the compiled registry contract/index.js,
//      FB  = path of the compiled fallback contract/index.js,
//      CO  = path of the compiled consume contract/index.js (optional).

import { createHash, randomBytes } from 'node:crypto';
import * as rt from '@midnight-ntwrk/compact-runtime';

const Reg = await import(process.env.REG);
const Fb = await import(process.env.FB);
const Co = process.env.CO ? await import(process.env.CO) : null;

const results = [];
function check(name, cond, detail = '') {
  results.push({ name, ok: !!cond, detail });
  console.log(`${cond ? 'PASS' : 'FAIL'} ${name}${detail ? ' :: ' + detail : ''}`);
}
async function expectFail(name, fn) {
  try { await fn(); check(name, false, 'call succeeded'); }
  catch (e) { check(name, true, String(e.message).split('\n')[0].slice(0, 100)); }
}

const PRIME = rt.maxField() + 1n;
const mod = (x) => ((x % PRIME) + PRIME) % PRIME;
const pad32 = (s) => { const b = new Uint8Array(32); b.set(Buffer.from(s)); return b; };
const hex = (u) => Buffer.from(u).toString('hex');

const addr = rt.sampleContractAddress();
const coinPk = '0'.repeat(64);

// ---------------------------------------------------------------------------
// Private state and witnesses

const ps = {
  stewardSk: randomBytes(32), relaySk: randomBytes(32), evidence: null, path: null,
};
const witnesses = {
  stewardSecret: ({ privateState }) => [privateState, privateState.stewardSk],
  relaySecret: ({ privateState }) => [privateState, privateState.relaySk],
  revocationEvidence: ({ privateState }) => [privateState, privateState.evidence],
  memberPath: ({ privateState }) => [privateState, privateState.path],
};
const reg = new Reg.Contract(witnesses);
const P = Reg.pureCircuits;

const params = {
  epochLength: 60n, membershipPeriod: 86400n, rootWindow: 3600n,
  quota: [64n, 16n, 4n, 1n], anchorWindow: 60n, anchorHistory: 176400n,
  shardCount: 1n, activationHeight: 0n, maxVersion: 1n, bootstrapHash: new Uint8Array(32),
};
const N = pad32('mpe-test-network');

const init = await reg.initialState(
  rt.createConstructorContext(ps, coinPk), P.stewardKeyOf(ps.stewardSk), N, 0n, params);
let state = init.currentContractState;

const T0 = 1_790_000_000;               // a fixed Unix time (2026-09)
const period = BigInt(Math.floor(T0 / 86400));

async function call(circuit, time, privateState, ...args) {
  const ctx = rt.createCircuitContext({
    circuitId: circuit, contractAddress: addr, coinPublicKeyOrZswapState: coinPk,
    contractState: state, privateState, time,
  });
  const res = await reg.circuits[circuit](ctx, ...args);
  state = res.context.queryContexts[addr].state;
  return res;
}
const L = () => Reg.ledger(state);

// ---------------------------------------------------------------------------
// 1. Steward-only relay list

const peer = createHash('sha256').update('peer-1').digest();
const entry = {
  operatorId: pad32('operator-A'),
  roles: { relay: true, store: true, bootstrapper: false, gateway: false, anchorer: true },
  keyCommitment: P.relayKeyOf(ps.relaySk),
};
await expectFail('addRelay refused for a non-steward secret', () =>
  call('addRelay', T0, { ...ps, stewardSk: randomBytes(32) }, peer, entry, 1n));
let r = await call('addRelay', T0, ps, peer, entry, 1n);
check('addRelay by steward', L().relays.member(peer));
check('addRelay emits one mpe/gov/v1 Misc', r.context.events.length === 1,
  JSON.stringify(r.context.events[0]).slice(0, 160));

// ---------------------------------------------------------------------------
// 2. Registration

const idc = createHash('sha256').update('member-1').digest();
r = await call('register', T0, ps, idc, period);
const leaf = P.memberLeafOf(idc, params.quota);
check('register inserts the leaf of the current period',
  L().members.lookup(period).findPathForLeaf(leaf) !== undefined);
await expectFail('register refused for a period that is not current', () =>
  call('register', T0, ps, randomBytes(32), period + 1n));
console.log('register gasCost', JSON.stringify(r.gasCost, (k, v) => typeof v === 'bigint' ? v.toString() : v));

// ---------------------------------------------------------------------------
// 3. Anchor post

const window = BigInt(Math.floor(T0 / 60)) - 1n;   // the minute that closed most recently
const q = window / 2940n, slot = window % 2940n;
const root = createHash('sha256').update('window-root').digest();
const counts = [600n, 0n, 0n, 0n, 0n, 0n, 0n, 0n];
const tPost = Number((window + 1n) * 60n + 25n);

await expectFail('postAnchor refused before window close + 20 s', () =>
  call('postAnchor', Number((window + 1n) * 60n + 5n), ps, peer, window, q, slot, root, counts));
await expectFail('postAnchor refused for a wrong anchorer secret', () =>
  call('postAnchor', tPost, { ...ps, relaySk: randomBytes(32) }, peer, window, q, slot, root, counts));
await expectFail('postAnchor refused for a wrong slot', () =>
  call('postAnchor', tPost, ps, peer, window, q, (slot + 1n) % 2940n, root, counts));
await expectFail('postAnchor refused for an empty window', () =>
  call('postAnchor', tPost, ps, peer, window, q, slot, root, [0n, 0n, 0n, 0n, 0n, 0n, 0n, 0n]));
await expectFail('postAnchor refused for a count on an inactive Shard', () =>
  call('postAnchor', tPost, ps, peer, window, q, slot, root, [1n, 1n, 0n, 0n, 0n, 0n, 0n, 0n]));

r = await call('postAnchor', tPost, ps, peer, window, q, slot, root, counts);
check('postAnchor stores the record', L().anchors.member(slot) && hex(L().anchors.lookup(slot).root) === hex(root));
check('postAnchor emits exactly one event', r.context.events.length === 1);
console.log('anchor event', JSON.stringify(r.context.events[0], (k, v) =>
  v instanceof Uint8Array ? hex(v) : typeof v === 'bigint' ? v.toString() : v).slice(0, 600));
console.log('postAnchor gasCost', JSON.stringify(r.gasCost, (k, v) => typeof v === 'bigint' ? v.toString() : v));
await expectFail('second Anchor for the same window refused', () =>
  call('postAnchor', tPost + 5, ps, peer, window, q, slot, root, counts));

const aLeaf = P.anchorLeafOf(window, root);
const aPath = L().anchorTree.findPathForLeaf(aLeaf);
const valid = await call('anchorRootValid', tPost, ps, L().anchorTree.root());
check('anchorRootValid accepts the current Anchor-tree root', valid.result === true);
const invalid = await call('anchorRootValid', tPost, ps, { field: 12345n });
check('anchorRootValid rejects an unknown root', invalid.result === false);
check('Anchor-tree path exists for (window, root)', aPath !== undefined);

// A later Anchor keeps the earlier root valid (historic check, MPE-VER-031).
const oldRoot = L().anchorTree.root();
const w2 = window + 1n;
await call('postAnchor', tPost + 60, ps, peer, w2, w2 / 2940n, w2 % 2940n, randomBytes(32), counts);
check('earlier Anchor-tree root still valid after a later Anchor',
  (await call('anchorRootValid', tPost + 60, ps, oldRoot)).result === true);

// ---------------------------------------------------------------------------
// 4. Revocation on equivocation evidence

const a0 = mod(BigInt('0x' + randomBytes(31).toString('hex')));
const idc2 = P.idcOf(a0);
await call('register', T0, ps, idc2, period);
const epoch = BigInt(Math.floor(T0 / 60)), sizeClass = 1n, credit = 3n;
const a1 = P.rlnA1(a0, epoch, sizeClass, credit);
const eid1 = randomBytes(32), eid2 = randomBytes(32);
const share = (eid) => ({ eid, y: mod(a0 + a1 * P.rlnX(eid)) });
const leaf2 = P.memberLeafOf(idc2, params.quota);
const path2 = L().members.lookup(period).findPathForLeaf(leaf2);
const goodEv = { a0, epoch, sizeClass, credit, quota: params.quota, s1: share(eid1), s2: share(eid2) };

await expectFail('revoke refused when one share is off the member line', () =>
  call('revoke', T0 + 100, { ...ps, evidence: { ...goodEv, s2: { eid: eid2, y: mod(goodEv.s2.y + 1n) } }, path: path2 }, period, 9n));
await expectFail('revoke refused for a single repeated share', () =>
  call('revoke', T0 + 100, { ...ps, evidence: { ...goodEv, s2: goodEv.s1 }, path: path2 }, period, 9n));
r = await call('revoke', T0 + 100, { ...ps, evidence: goodEv, path: path2 }, period, 9n);
check('revoke removes the member leaf', L().members.lookup(period).findPathForLeaf(leaf2) === undefined);
check('revoke records the commitment as revoked', L().revoked.member(idc2));
check('revoke emits one mpe/gov/v1 Misc', r.context.events.length === 1);
check('first member unaffected', L().members.lookup(period).findPathForLeaf(leaf) !== undefined);
await expectFail('re-registration of a revoked commitment refused', () =>
  call('register', T0 + 200, ps, idc2, period));

// ---------------------------------------------------------------------------
// 5. Pause gates registration and Anchors

await call('pause', T0 + 300, ps, 2n);
await expectFail('register refused while paused', () => call('register', T0 + 300, ps, randomBytes(32), period));
await call('unpause', T0 + 400, ps, 3n);
await call('register', T0 + 400, ps, randomBytes(32), period);
check('register works after unpause', true);

// ---------------------------------------------------------------------------
// 6. Hash encoding: is persistentHash<Bytes<k>> plain SHA-256 of the k bytes?
// (Decides whether the RFC 6962 leaf and node hashes of consume.compact match
// the anchorer's off-chain SHA-256, MPE-NET-051.)

const b33 = new Uint8Array(33); b33.set(randomBytes(32), 1);
const ph = rt.persistentHash(new rt.CompactTypeBytes(33), b33);
const sh = createHash('sha256').update(b33).digest();
check('persistentHash<Bytes<33>> equals SHA-256 of the raw 33 bytes', hex(ph) === hex(sh),
  `${hex(ph).slice(0, 16)} vs ${hex(sh).slice(0, 16)}`);

if (Co) {
  const e = randomBytes(32), l = randomBytes(32), rr = randomBytes(32);
  const sha = (b) => createHash('sha256').update(b).digest('hex');
  check('consume rfcLeaf equals SHA-256(0x00 || EID)',
    hex(Co.pureCircuits.rfcLeaf(e)) === sha(Buffer.concat([Buffer.from([0]), e])));
  check('consume rfcNode equals SHA-256(0x01 || left || right)',
    hex(Co.pureCircuits.rfcNode(l, rr)) === sha(Buffer.concat([Buffer.from([1]), l, rr])));
  check('consume anchorLeafOf equals the Registry anchorLeafOf',
    hex(Co.pureCircuits.anchorLeafOf(window, root)) === hex(P.anchorLeafOf(window, root)));
}

// ---------------------------------------------------------------------------
// 7. Fallback: one call emits 16 parts in order

const fb = new Fb.Contract({});
const fbInit = await fb.initialState(rt.createConstructorContext({}, coinPk));
const parts = Array.from({ length: 16 }, (_, i) => { const b = new Uint8Array(256); b.fill(i); return b; });
const fbCtx = rt.createCircuitContext({
  circuitId: 'publishClass2', contractAddress: addr, coinPublicKeyOrZswapState: coinPk,
  contractState: fbInit.currentContractState, privateState: {}, time: T0,
});
const fr = await fb.circuits.publishClass2(fbCtx, parts);
check('publishClass2 emits 16 events', fr.context.events.length === 16);
const order = fr.context.events.map((e) => JSON.stringify(e, (k, v) => v instanceof Uint8Array ? hex(v) : typeof v === 'bigint' ? v.toString() : v));
// The runtime's Value encoding drops trailing zero bytes, so part 0 (all zero)
// shows only the name; parts 1..15 must carry their fill byte in order.
check('parts appear in emission order',
  order.slice(1).every((s, j) => s.includes((j + 1).toString(16).padStart(2, '0').repeat(8))) &&
  !order[0].includes('01'.repeat(8)));
console.log('publishClass2 gasCost', JSON.stringify(fr.gasCost, (k, v) => typeof v === 'bigint' ? v.toString() : v));
const fbCtx2 = rt.createCircuitContext({
  circuitId: 'publishPart', contractAddress: addr, coinPublicKeyOrZswapState: coinPk,
  contractState: fbInit.currentContractState, privateState: {}, time: T0,
});
const fbCtx0 = rt.createCircuitContext({
  circuitId: 'publishClass0', contractAddress: addr, coinPublicKeyOrZswapState: coinPk,
  contractState: fbInit.currentContractState, privateState: {}, time: T0,
});
const f0 = await fb.circuits.publishClass0(fbCtx0, parts[0]);
console.log('publishClass0 gasCost', JSON.stringify(f0.gasCost, (k, v) => typeof v === 'bigint' ? v.toString() : v));
const perEvent = (f, n) => Number(f.gasCost.bytesWritten) / n;
console.log('simulator per-event bytesWritten: class0', perEvent(f0, 1), 'class2', perEvent(fr, 16),
  'marginal', (Number(fr.gasCost.bytesWritten) - Number(f0.gasCost.bytesWritten)) / 15,
  'marginal compute ps', (Number(fr.gasCost.computeTime) - Number(f0.gasCost.computeTime)) / 15);
await expectFail('publishPart refuses a non-MPE name', () => fb.circuits.publishPart(fbCtx2, pad32('other'), parts[0]));

const failed = results.filter((x) => !x.ok);
console.log(`\n${results.length - failed.length}/${results.length} checks passed`);
if (failed.length) process.exitCode = 1;
