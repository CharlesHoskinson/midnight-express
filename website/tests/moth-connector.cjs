'use strict';
// Synthetic provider contracts only. No live extension or signing test is claimed.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '../dist/moth-connector.js'), 'utf8');
const tests = [];
const test = (name, run) => tests.push({ name, run });
function deferred() { let resolve, reject; const promise = new Promise((yes, no) => { resolve = yes; reject = no; }); return { promise, resolve, reject }; }
function fixture(options = {}) {
  const calls = [];
  let status = { status: 'connected', networkId: options.networkId || 'preprod' };
  const connected = new Proxy({ getConnectionStatus: async () => { calls.push('getConnectionStatus'); return status; } }, {
    get(target, key) { if (key in target || key === 'then') return target[key]; throw new Error(`Forbidden wallet capability accessed: ${String(key)}`); }
  });
  const provider = { rdns: 'io.shielded.moth', apiVersion: '4.0.1', connect: async (network) => { calls.push(['connect', network]); return connected; } };
  const context = { navigator: { userActivation: { isActive: true } }, midnight: { moth: provider } };
  vm.createContext(context); vm.runInContext(source, context);
  const adapter = context.MothReadOnlyConnector.create(options);
  return { adapter, context, provider, connected, calls, setStatus: value => { status = value; } };
}
function cleared(adapter, status) {
  const state = adapter.getState(); assert.equal(state.status, status); assert.equal(state.wallet, null); assert.equal(state.capabilities.length, 0);
  assert.equal('api' in state, false);
}
test('loading, creating, discovering, observing, and disconnected status never call wallet RPC', async () => {
  const f = fixture(); const seen = []; const unsubscribe = f.adapter.subscribe(s => seen.push(s.status));
  assert.equal(f.adapter.discover().compatible, true); await f.adapter.checkStatus(); unsubscribe();
  assert.deepEqual(f.calls, []); assert.deepEqual(seen, ['disconnected']); cleared(f.adapter, 'disconnected');
  assert.deepEqual(Object.keys(f.adapter).sort(), ['checkStatus', 'connect', 'disconnect', 'discover', 'getState', 'subscribe']);
});
test('inactive or absent browser activation refuses before any provider call', async () => {
  for (const setup of [f => { f.context.navigator.userActivation.isActive = false; }, f => { delete f.context.navigator.userActivation; }, f => { delete f.context.navigator; }]) {
    const f = fixture(); setup(f); await assert.rejects(f.adapter.connect(), /explicit user action/); assert.deepEqual(f.calls, []); cleared(f.adapter, 'error');
  }
});
test('only genuine namespace, reverse domain, exact version, and connect capability are accepted', async () => {
  for (const setup of [f => { f.context.moth = f.provider; delete f.context.midnight; }, f => { f.provider.rdns = 'other.wallet'; }, f => { f.provider.apiVersion = '4.1.0-beta.1'; }, f => { f.provider.apiVersion = '4.0.2'; }, f => { delete f.provider.connect; }]) {
    const f = fixture(); setup(f); assert.equal(f.adapter.discover().compatible, false); await assert.rejects(f.adapter.connect()); assert.deepEqual(f.calls, []); cleared(f.adapter, 'error');
  }
});
test('active connection invokes only connect and status and passes exact requested network', async () => {
  for (const networkId of ['preprod', 'preview', 'undeployed']) {
    const f = fixture({ networkId }); const pending = f.adapter.connect(); assert.deepEqual(f.calls, [['connect', networkId]]); await pending;
    assert.equal(f.adapter.getState().status, 'connected'); assert.equal(f.adapter.getState().networkId, networkId);
    await f.adapter.checkStatus(); assert.deepEqual(f.calls, [['connect', networkId], 'getConnectionStatus', 'getConnectionStatus']);
    f.adapter.disconnect(); cleared(f.adapter, 'disconnected'); assert.equal(f.adapter.getState().error, null);
    await f.adapter.checkStatus(); assert.equal(f.calls.length, 3);
  }
  const f = fixture(); assert.throws(() => f.context.MothReadOnlyConnector.create({ networkId: 'mainnet' }), /Unsupported/);
});
test('mismatched network, disconnected status, and missing status capability fail closed', async () => {
  for (const status of [{ status: 'connected', networkId: 'preview' }, { status: 'disconnected' }, null]) {
    const f = fixture(); f.setStatus(status); await assert.rejects(f.adapter.connect()); cleared(f.adapter, 'error');
  }
  const f = fixture(); f.provider.connect = async () => ({}); await assert.rejects(f.adapter.connect()); cleared(f.adapter, 'error');
});
test('wallet refusal clears state without reconnect or additional RPC', async () => {
  const f = fixture(); f.provider.connect = async () => { f.calls.push('refused'); throw new Error('Rejected'); };
  await assert.rejects(f.adapter.connect(), /rejected or failed/); cleared(f.adapter, 'error'); await f.adapter.checkStatus(); assert.deepEqual(f.calls, ['refused']);
});
test('provider removal or replacement clears session without asking stale provider for status', async () => {
  for (const setup of [f => { delete f.context.midnight; }, f => { delete f.context.midnight.moth; }, f => { f.context.midnight.moth = { ...f.provider }; }, f => { f.provider.apiVersion = '5.0.0'; }]) {
    const f = fixture(); await f.adapter.connect(); const count = f.calls.length; setup(f); await f.adapter.checkStatus(); cleared(f.adapter, 'disconnected'); assert.equal(f.calls.length, count);
  }
});
test('lock, changed network, and status refusal clear an established session', async () => {
  for (const status of [{ status: 'disconnected' }, { status: 'connected', networkId: 'preview' }]) {
    const f = fixture(); await f.adapter.connect(); f.setStatus(status); await f.adapter.checkStatus(); cleared(f.adapter, 'disconnected');
  }
  const f = fixture(); await f.adapter.connect(); f.connected.getConnectionStatus = async () => { throw new Error('Disconnected'); }; await f.adapter.checkStatus(); cleared(f.adapter, 'disconnected');
});
test('local disconnect invalidates pending connect and status completion, including late rejection', async () => {
  for (const reject of [false, true]) {
    const f = fixture(); const d = deferred(); f.provider.connect = () => d.promise;
    const pending = f.adapter.connect(); f.adapter.disconnect(); if (reject) d.reject(new Error('Rejected')); else d.resolve(f.connected);
    await pending; cleared(f.adapter, 'disconnected'); assert.deepEqual(f.calls, []);
  }
  const f = fixture(); await f.adapter.connect(); const d = deferred(); f.connected.getConnectionStatus = () => d.promise;
  const pending = f.adapter.checkStatus(); f.adapter.disconnect(); d.resolve({ status: 'connected', networkId: 'preprod' }); await pending; cleared(f.adapter, 'disconnected');
});
test('a second pending request never produces a second wallet connect', async () => {
  const f = fixture(); const d = deferred(); f.provider.connect = () => { f.calls.push('connect'); return d.promise; };
  const pending = f.adapter.connect(); await assert.rejects(f.adapter.connect(), /already pending/); d.resolve(f.connected); await pending; assert.deepEqual(f.calls, ['connect', 'getConnectionStatus']);
});
test('a failed new request cannot resurrect an older pending session', async () => {
  const f = fixture(); const d = deferred(); f.provider.connect = () => d.promise;
  const pending = f.adapter.connect(); f.context.navigator.userActivation.isActive = false; await assert.rejects(f.adapter.connect());
  d.resolve(f.connected); await pending; cleared(f.adapter, 'error'); assert.deepEqual(f.calls, []);
});
(async () => { for (const { name, run } of tests) { await run(); console.log(`PASS ${name}`); } console.log(`${tests.length} connector contract tests passed.`); })().catch(error => { console.error(error); process.exitCode = 1; });
