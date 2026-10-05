/* Bounded Moth adapter; verified against shieldedtech/moth-wallet d48206a.
 * Read-only describes our calls, not Moth's origin-wide permission grant. */
(function (root) {
  'use strict';
  const SUPPORTED_VERSION = '4.0.1';
  const NETWORKS = Object.freeze(['preprod', 'preview', 'undeployed']);
  function create(options = {}) {
    const networkId = options.networkId || 'preprod';
    if (!NETWORKS.includes(networkId)) throw new Error('Unsupported demonstration network.');
    let api = null, provider = null, epoch = 0;
    let state = Object.freeze({ status: 'disconnected', networkId, wallet: null, capabilities: [], error: null });
    const listeners = new Set();
    function update(patch) {
      state = Object.freeze({ ...state, ...patch });
      for (const listener of listeners) { try { listener(state); } catch (_) { /* observer isolation */ } }
      return state;
    }
    function fail(message, invalidate = true) {
      if (invalidate) ++epoch; // Invalidate outstanding calls when failure occurs outside their handler.
      api = null; provider = null;
      update({ status: 'error', wallet: null, capabilities: [], error: message });
      throw new Error(message);
    }
    function discover() {
      const candidate = root.midnight && root.midnight.moth;
      if (!candidate) return Object.freeze({ available: false, compatible: false, reason: 'Moth extension not detected.' });
      const compatible = candidate.rdns === 'io.shielded.moth' && candidate.apiVersion === SUPPORTED_VERSION && typeof candidate.connect === 'function';
      return Object.freeze({ available: true, compatible, name: 'Moth Wallet', apiVersion: typeof candidate.apiVersion === 'string' ? candidate.apiVersion : 'unknown', reason: compatible ? null : 'Unsupported Moth identity or API version; expected 4.0.1.' });
    }
    async function connect() {
      // Call synchronously from a trusted click to preserve the wallet popup's activation.
      if (!root.navigator || !root.navigator.userActivation || !root.navigator.userActivation.isActive) return fail('Connect requires an explicit user action.');
      if (state.status === 'connecting') throw new Error('Connection request already pending.');
      const found = discover();
      if (!found.compatible) return fail(found.reason);
      const token = ++epoch;
      const selected = root.midnight.moth;
      update({ status: 'connecting', error: null, wallet: null, capabilities: [] });
      try {
        const connected = await selected.connect(networkId);
        if (token !== epoch) return state;
        if (!connected || typeof connected.getConnectionStatus !== 'function') return fail('Wallet does not expose the required connection status capability.', false);
        const status = await connected.getConnectionStatus();
        if (token !== epoch) return state;
        if (!status || status.status !== 'connected' || status.networkId !== networkId) return fail('Wallet is disconnected or its network does not match.', false);
        if (root.midnight.moth !== selected || !discover().compatible) return fail('Wallet provider changed during connection.', false);
        api = connected; provider = selected;
        return update({ status: 'connected', wallet: 'Moth Wallet', capabilities: Object.freeze(['getConnectionStatus']), error: null });
      } catch (error) {
        if (token !== epoch) return state;
        return fail('Connection was rejected or failed. Review the wallet and retry explicitly.');
      }
    }
    function disconnect() {
      ++epoch; api = null; provider = null;
      return update({ status: 'disconnected', wallet: null, capabilities: [], error: null });
    }
    async function checkStatus() {
      if (!api) return state;
      const token = epoch;
      if (!discover().compatible || root.midnight.moth !== provider) { disconnect(); return update({ error: 'Wallet provider changed; reconnect explicitly.' }); }
      try {
        const status = await api.getConnectionStatus();
        if (token !== epoch) return state;
        if (!status || status.status !== 'connected' || status.networkId !== networkId) { disconnect(); return update({ error: 'Wallet locked, permission revoked, or network changed; reconnect explicitly.' }); }
        return state;
      } catch (_) {
        if (token === epoch) { disconnect(); update({ error: 'Wallet status unavailable; reconnect explicitly.' }); }
        return state;
      }
    }
    return Object.freeze({ discover, connect, disconnect, checkStatus, getState: () => state, subscribe(listener) {
      if (typeof listener !== 'function') throw new TypeError('Listener must be a function.');
      listeners.add(listener); listener(state); return () => listeners.delete(listener);
    } });
  }
  root.MothReadOnlyConnector = Object.freeze({ create, supportedVersion: SUPPORTED_VERSION, networks: NETWORKS });
})(globalThis);
