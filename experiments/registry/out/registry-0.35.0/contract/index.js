import * as __compactRuntime from '@midnight-ntwrk/compact-runtime';
__compactRuntime.checkRuntimeVersion('0.20.0');

const _descriptor_0 = new __compactRuntime.CompactTypeBytes(32);

const _descriptor_1 = __compactRuntime.CompactTypeField;

class _MerkleTreeDigest_0 {
  alignment() {
    return _descriptor_1.alignment();
  }
  fromValue(value_0) {
    return {
      field: _descriptor_1.fromValue(value_0)
    }
  }
  toValue(value_0) {
    return _descriptor_1.toValue(value_0.field);
  }
}

const _descriptor_2 = new _MerkleTreeDigest_0();

const _descriptor_3 = __compactRuntime.CompactTypeBoolean;

class _Roles_0 {
  alignment() {
    return _descriptor_3.alignment().concat(_descriptor_3.alignment().concat(_descriptor_3.alignment().concat(_descriptor_3.alignment().concat(_descriptor_3.alignment()))));
  }
  fromValue(value_0) {
    return {
      relay: _descriptor_3.fromValue(value_0),
      store: _descriptor_3.fromValue(value_0),
      bootstrapper: _descriptor_3.fromValue(value_0),
      gateway: _descriptor_3.fromValue(value_0),
      anchorer: _descriptor_3.fromValue(value_0)
    }
  }
  toValue(value_0) {
    return _descriptor_3.toValue(value_0.relay).concat(_descriptor_3.toValue(value_0.store).concat(_descriptor_3.toValue(value_0.bootstrapper).concat(_descriptor_3.toValue(value_0.gateway).concat(_descriptor_3.toValue(value_0.anchorer)))));
  }
}

const _descriptor_4 = new _Roles_0();

class _RelayEntry_0 {
  alignment() {
    return _descriptor_0.alignment().concat(_descriptor_4.alignment().concat(_descriptor_0.alignment()));
  }
  fromValue(value_0) {
    return {
      operatorId: _descriptor_0.fromValue(value_0),
      roles: _descriptor_4.fromValue(value_0),
      keyCommitment: _descriptor_0.fromValue(value_0)
    }
  }
  toValue(value_0) {
    return _descriptor_0.toValue(value_0.operatorId).concat(_descriptor_4.toValue(value_0.roles).concat(_descriptor_0.toValue(value_0.keyCommitment)));
  }
}

const _descriptor_5 = new _RelayEntry_0();

const _descriptor_6 = new __compactRuntime.CompactTypeUnsignedInteger(4294967295n, 4);

const _descriptor_7 = new __compactRuntime.CompactTypeUnsignedInteger(65535n, 2);

const _descriptor_8 = new __compactRuntime.CompactTypeVector(4, _descriptor_7);

const _descriptor_9 = new __compactRuntime.CompactTypeUnsignedInteger(255n, 1);

const _descriptor_10 = new __compactRuntime.CompactTypeUnsignedInteger(18446744073709551615n, 8);

class _Params_0 {
  alignment() {
    return _descriptor_6.alignment().concat(_descriptor_6.alignment().concat(_descriptor_6.alignment().concat(_descriptor_8.alignment().concat(_descriptor_6.alignment().concat(_descriptor_6.alignment().concat(_descriptor_9.alignment().concat(_descriptor_10.alignment().concat(_descriptor_9.alignment().concat(_descriptor_0.alignment())))))))));
  }
  fromValue(value_0) {
    return {
      epochLength: _descriptor_6.fromValue(value_0),
      membershipPeriod: _descriptor_6.fromValue(value_0),
      rootWindow: _descriptor_6.fromValue(value_0),
      quota: _descriptor_8.fromValue(value_0),
      anchorWindow: _descriptor_6.fromValue(value_0),
      anchorHistory: _descriptor_6.fromValue(value_0),
      shardCount: _descriptor_9.fromValue(value_0),
      activationHeight: _descriptor_10.fromValue(value_0),
      maxVersion: _descriptor_9.fromValue(value_0),
      bootstrapHash: _descriptor_0.fromValue(value_0)
    }
  }
  toValue(value_0) {
    return _descriptor_6.toValue(value_0.epochLength).concat(_descriptor_6.toValue(value_0.membershipPeriod).concat(_descriptor_6.toValue(value_0.rootWindow).concat(_descriptor_8.toValue(value_0.quota).concat(_descriptor_6.toValue(value_0.anchorWindow).concat(_descriptor_6.toValue(value_0.anchorHistory).concat(_descriptor_9.toValue(value_0.shardCount).concat(_descriptor_10.toValue(value_0.activationHeight).concat(_descriptor_9.toValue(value_0.maxVersion).concat(_descriptor_0.toValue(value_0.bootstrapHash))))))))));
  }
}

const _descriptor_11 = new _Params_0();

const _descriptor_12 = new __compactRuntime.CompactTypeVector(8, _descriptor_6);

class _AnchorRecord_0 {
  alignment() {
    return _descriptor_10.alignment().concat(_descriptor_0.alignment().concat(_descriptor_12.alignment()));
  }
  fromValue(value_0) {
    return {
      window: _descriptor_10.fromValue(value_0),
      root: _descriptor_0.fromValue(value_0),
      counts: _descriptor_12.fromValue(value_0)
    }
  }
  toValue(value_0) {
    return _descriptor_10.toValue(value_0.window).concat(_descriptor_0.toValue(value_0.root).concat(_descriptor_12.toValue(value_0.counts)));
  }
}

const _descriptor_13 = new _AnchorRecord_0();

const _descriptor_14 = new __compactRuntime.CompactTypeBytes(288);

class _PendingParams_0 {
  alignment() {
    return _descriptor_11.alignment().concat(_descriptor_10.alignment());
  }
  fromValue(value_0) {
    return {
      params: _descriptor_11.fromValue(value_0),
      effectiveAt: _descriptor_10.fromValue(value_0)
    }
  }
  toValue(value_0) {
    return _descriptor_11.toValue(value_0.params).concat(_descriptor_10.toValue(value_0.effectiveAt));
  }
}

const _descriptor_15 = new _PendingParams_0();

class _Maybe_0 {
  alignment() {
    return _descriptor_3.alignment().concat(_descriptor_15.alignment());
  }
  fromValue(value_0) {
    return {
      is_some: _descriptor_3.fromValue(value_0),
      value: _descriptor_15.fromValue(value_0)
    }
  }
  toValue(value_0) {
    return _descriptor_3.toValue(value_0.is_some).concat(_descriptor_15.toValue(value_0.value));
  }
}

const _descriptor_16 = new _Maybe_0();

const _descriptor_17 = new __compactRuntime.CompactTypeBytes(256);

const _descriptor_18 = new __compactRuntime.CompactTypeBytes(2);

const _descriptor_19 = new __compactRuntime.CompactTypeBytes(8);

const _descriptor_20 = new __compactRuntime.CompactTypeBytes(4);

class _MerkleTreePathEntry_0 {
  alignment() {
    return _descriptor_2.alignment().concat(_descriptor_3.alignment());
  }
  fromValue(value_0) {
    return {
      sibling: _descriptor_2.fromValue(value_0),
      goes_left: _descriptor_3.fromValue(value_0)
    }
  }
  toValue(value_0) {
    return _descriptor_2.toValue(value_0.sibling).concat(_descriptor_3.toValue(value_0.goes_left));
  }
}

const _descriptor_21 = new _MerkleTreePathEntry_0();

const _descriptor_22 = new __compactRuntime.CompactTypeVector(20, _descriptor_21);

class _MerkleTreePath_0 {
  alignment() {
    return _descriptor_0.alignment().concat(_descriptor_22.alignment());
  }
  fromValue(value_0) {
    return {
      leaf: _descriptor_0.fromValue(value_0),
      path: _descriptor_22.fromValue(value_0)
    }
  }
  toValue(value_0) {
    return _descriptor_0.toValue(value_0.leaf).concat(_descriptor_22.toValue(value_0.path));
  }
}

const _descriptor_23 = new _MerkleTreePath_0();

class _Share_0 {
  alignment() {
    return _descriptor_0.alignment().concat(_descriptor_1.alignment());
  }
  fromValue(value_0) {
    return {
      eid: _descriptor_0.fromValue(value_0),
      y: _descriptor_1.fromValue(value_0)
    }
  }
  toValue(value_0) {
    return _descriptor_0.toValue(value_0.eid).concat(_descriptor_1.toValue(value_0.y));
  }
}

const _descriptor_24 = new _Share_0();

class _Evidence_0 {
  alignment() {
    return _descriptor_1.alignment().concat(_descriptor_10.alignment().concat(_descriptor_9.alignment().concat(_descriptor_7.alignment().concat(_descriptor_8.alignment().concat(_descriptor_24.alignment().concat(_descriptor_24.alignment()))))));
  }
  fromValue(value_0) {
    return {
      a0: _descriptor_1.fromValue(value_0),
      epoch: _descriptor_10.fromValue(value_0),
      sizeClass: _descriptor_9.fromValue(value_0),
      credit: _descriptor_7.fromValue(value_0),
      quota: _descriptor_8.fromValue(value_0),
      s1: _descriptor_24.fromValue(value_0),
      s2: _descriptor_24.fromValue(value_0)
    }
  }
  toValue(value_0) {
    return _descriptor_1.toValue(value_0.a0).concat(_descriptor_10.toValue(value_0.epoch).concat(_descriptor_9.toValue(value_0.sizeClass).concat(_descriptor_7.toValue(value_0.credit).concat(_descriptor_8.toValue(value_0.quota).concat(_descriptor_24.toValue(value_0.s1).concat(_descriptor_24.toValue(value_0.s2)))))));
  }
}

const _descriptor_25 = new _Evidence_0();

const _descriptor_26 = new __compactRuntime.CompactTypeBytes(6);

class _LeafPreimage_0 {
  alignment() {
    return _descriptor_26.alignment().concat(_descriptor_0.alignment());
  }
  fromValue(value_0) {
    return {
      domain_sep: _descriptor_26.fromValue(value_0),
      data: _descriptor_0.fromValue(value_0)
    }
  }
  toValue(value_0) {
    return _descriptor_26.toValue(value_0.domain_sep).concat(_descriptor_0.toValue(value_0.data));
  }
}

const _descriptor_27 = new _LeafPreimage_0();

const _descriptor_28 = new __compactRuntime.CompactTypeVector(2, _descriptor_0);

class _AnchorLeaf_0 {
  alignment() {
    return _descriptor_0.alignment().concat(_descriptor_10.alignment().concat(_descriptor_0.alignment()));
  }
  fromValue(value_0) {
    return {
      domain: _descriptor_0.fromValue(value_0),
      window: _descriptor_10.fromValue(value_0),
      root: _descriptor_0.fromValue(value_0)
    }
  }
  toValue(value_0) {
    return _descriptor_0.toValue(value_0.domain).concat(_descriptor_10.toValue(value_0.window).concat(_descriptor_0.toValue(value_0.root)));
  }
}

const _descriptor_29 = new _AnchorLeaf_0();

const _descriptor_30 = new __compactRuntime.CompactTypeVector(2, _descriptor_1);

class _MemberLeaf_0 {
  alignment() {
    return _descriptor_0.alignment().concat(_descriptor_0.alignment().concat(_descriptor_8.alignment()));
  }
  fromValue(value_0) {
    return {
      domain: _descriptor_0.fromValue(value_0),
      idc: _descriptor_0.fromValue(value_0),
      quota: _descriptor_8.fromValue(value_0)
    }
  }
  toValue(value_0) {
    return _descriptor_0.toValue(value_0.domain).concat(_descriptor_0.toValue(value_0.idc).concat(_descriptor_8.toValue(value_0.quota)));
  }
}

const _descriptor_31 = new _MemberLeaf_0();

const _descriptor_32 = new __compactRuntime.CompactTypeVector(5, _descriptor_1);

class _Either_0 {
  alignment() {
    return _descriptor_3.alignment().concat(_descriptor_0.alignment().concat(_descriptor_0.alignment()));
  }
  fromValue(value_0) {
    return {
      is_left: _descriptor_3.fromValue(value_0),
      left: _descriptor_0.fromValue(value_0),
      right: _descriptor_0.fromValue(value_0)
    }
  }
  toValue(value_0) {
    return _descriptor_3.toValue(value_0.is_left).concat(_descriptor_0.toValue(value_0.left).concat(_descriptor_0.toValue(value_0.right)));
  }
}

const _descriptor_33 = new _Either_0();

const _descriptor_34 = new __compactRuntime.CompactTypeUnsignedInteger(340282366920938463463374607431768211455n, 16);

class _ContractAddress_0 {
  alignment() {
    return _descriptor_0.alignment();
  }
  fromValue(value_0) {
    return {
      bytes: _descriptor_0.fromValue(value_0)
    }
  }
  toValue(value_0) {
    return _descriptor_0.toValue(value_0.bytes);
  }
}

const _descriptor_35 = new _ContractAddress_0();

class _UserAddress_0 {
  alignment() {
    return _descriptor_0.alignment();
  }
  fromValue(value_0) {
    return {
      bytes: _descriptor_0.fromValue(value_0)
    }
  }
  toValue(value_0) {
    return _descriptor_0.toValue(value_0.bytes);
  }
}

const _descriptor_36 = new _UserAddress_0();

class _Either_1 {
  alignment() {
    return _descriptor_3.alignment().concat(_descriptor_35.alignment().concat(_descriptor_36.alignment()));
  }
  fromValue(value_0) {
    return {
      is_left: _descriptor_3.fromValue(value_0),
      left: _descriptor_35.fromValue(value_0),
      right: _descriptor_36.fromValue(value_0)
    }
  }
  toValue(value_0) {
    return _descriptor_3.toValue(value_0.is_left).concat(_descriptor_35.toValue(value_0.left).concat(_descriptor_36.toValue(value_0.right)));
  }
}

const _descriptor_37 = new _Either_1();

class _Maybe_1 {
  alignment() {
    return _descriptor_3.alignment().concat(_descriptor_37.alignment());
  }
  fromValue(value_0) {
    return {
      is_some: _descriptor_3.fromValue(value_0),
      value: _descriptor_37.fromValue(value_0)
    }
  }
  toValue(value_0) {
    return _descriptor_3.toValue(value_0.is_some).concat(_descriptor_37.toValue(value_0.value));
  }
}

const _descriptor_38 = new _Maybe_1();

export class Contract {
  witnesses;
  constructor(...args_0) {
    if (args_0.length !== 1) {
      throw new __compactRuntime.CompactError(`Contract constructor: expected 1 argument, received ${args_0.length}`);
    }
    const witnesses_0 = args_0[0];
    if (typeof(witnesses_0) !== 'object') {
      throw new __compactRuntime.CompactError('first (witnesses) argument to Contract constructor is not an object');
    }
    if (typeof(witnesses_0.stewardSecret) !== 'function') {
      throw new __compactRuntime.CompactError('first (witnesses) argument to Contract constructor does not contain a function-valued field named stewardSecret');
    }
    if (typeof(witnesses_0.relaySecret) !== 'function') {
      throw new __compactRuntime.CompactError('first (witnesses) argument to Contract constructor does not contain a function-valued field named relaySecret');
    }
    if (typeof(witnesses_0.revocationEvidence) !== 'function') {
      throw new __compactRuntime.CompactError('first (witnesses) argument to Contract constructor does not contain a function-valued field named revocationEvidence');
    }
    if (typeof(witnesses_0.memberPath) !== 'function') {
      throw new __compactRuntime.CompactError('first (witnesses) argument to Contract constructor does not contain a function-valued field named memberPath');
    }
    this.witnesses = witnesses_0;
    this.circuits = {
      async stewardKeyOf(context, ...args_1) {
        return { result: pureCircuits.stewardKeyOf(...args_1), context };
      },
      async relayKeyOf(context, ...args_1) {
        return { result: pureCircuits.relayKeyOf(...args_1), context };
      },
      async memberLeafOf(context, ...args_1) {
        return { result: pureCircuits.memberLeafOf(...args_1), context };
      },
      async idcOf(context, ...args_1) {
        return { result: pureCircuits.idcOf(...args_1), context };
      },
      async anchorLeafOf(context, ...args_1) {
        return { result: pureCircuits.anchorLeafOf(...args_1), context };
      },
      async rlnA1(context, ...args_1) {
        return { result: pureCircuits.rlnA1(...args_1), context };
      },
      async rlnX(context, ...args_1) {
        return { result: pureCircuits.rlnX(...args_1), context };
      },
      register: async (...args_1) => {
        if (args_1.length !== 3) {
          throw new __compactRuntime.CompactError(`register: expected 3 arguments (as invoked from Typescript), received ${args_1.length}`);
        }
        const contextOrig_0 = args_1[0];
        const idc_0 = args_1[1];
        const period_0 = args_1[2];
        if (!(typeof(contextOrig_0) === 'object' && contextOrig_0.callContext.currentQueryContext != undefined)) {
          __compactRuntime.typeError('register',
                                     'argument 1 (as invoked from Typescript)',
                                     'registry.compact line 281 char 1',
                                     'CircuitContext',
                                     contextOrig_0)
        }
        if (!(idc_0.buffer instanceof ArrayBuffer && idc_0.BYTES_PER_ELEMENT === 1 && idc_0.length === 32)) {
          __compactRuntime.typeError('register',
                                     'argument 1 (argument 2 as invoked from Typescript)',
                                     'registry.compact line 281 char 1',
                                     'Bytes<32>',
                                     idc_0)
        }
        if (!(typeof(period_0) === 'bigint' && period_0 >= 0n && period_0 <= 4294967295n)) {
          __compactRuntime.typeError('register',
                                     'argument 2 (argument 3 as invoked from Typescript)',
                                     'registry.compact line 281 char 1',
                                     'Uint<0..4294967296>',
                                     period_0)
        }
        const context = __compactRuntime.copyCircuitContext(contextOrig_0);
        const partialProofData = {
          input: {
            value: _descriptor_0.toValue(idc_0).concat(_descriptor_6.toValue(period_0)),
            alignment: _descriptor_0.alignment().concat(_descriptor_6.alignment())
          },
          output: undefined,
          publicTranscript: [],
          privateTranscriptOutputs: []
        };
        const result_0 = await this._register_0(context,
                                                partialProofData,
                                                idc_0,
                                                period_0);
        partialProofData.output = { value: [], alignment: [] };
        __compactRuntime.finalizeCallProofData(context, partialProofData);
        return { result: result_0, context: context, gasCost: context.callContext.currentGasCost };
      },
      revoke: async (...args_1) => {
        if (args_1.length !== 3) {
          throw new __compactRuntime.CompactError(`revoke: expected 3 arguments (as invoked from Typescript), received ${args_1.length}`);
        }
        const contextOrig_0 = args_1[0];
        const period_0 = args_1[1];
        const reason_0 = args_1[2];
        if (!(typeof(contextOrig_0) === 'object' && contextOrig_0.callContext.currentQueryContext != undefined)) {
          __compactRuntime.typeError('revoke',
                                     'argument 1 (as invoked from Typescript)',
                                     'registry.compact line 302 char 1',
                                     'CircuitContext',
                                     contextOrig_0)
        }
        if (!(typeof(period_0) === 'bigint' && period_0 >= 0n && period_0 <= 4294967295n)) {
          __compactRuntime.typeError('revoke',
                                     'argument 1 (argument 2 as invoked from Typescript)',
                                     'registry.compact line 302 char 1',
                                     'Uint<0..4294967296>',
                                     period_0)
        }
        if (!(typeof(reason_0) === 'bigint' && reason_0 >= 0n && reason_0 <= 65535n)) {
          __compactRuntime.typeError('revoke',
                                     'argument 2 (argument 3 as invoked from Typescript)',
                                     'registry.compact line 302 char 1',
                                     'Uint<0..65536>',
                                     reason_0)
        }
        const context = __compactRuntime.copyCircuitContext(contextOrig_0);
        const partialProofData = {
          input: {
            value: _descriptor_6.toValue(period_0).concat(_descriptor_7.toValue(reason_0)),
            alignment: _descriptor_6.alignment().concat(_descriptor_7.alignment())
          },
          output: undefined,
          publicTranscript: [],
          privateTranscriptOutputs: []
        };
        const result_0 = await this._revoke_0(context,
                                              partialProofData,
                                              period_0,
                                              reason_0);
        partialProofData.output = { value: [], alignment: [] };
        __compactRuntime.finalizeCallProofData(context, partialProofData);
        return { result: result_0, context: context, gasCost: context.callContext.currentGasCost };
      },
      prunePeriod: async (...args_1) => {
        if (args_1.length !== 2) {
          throw new __compactRuntime.CompactError(`prunePeriod: expected 2 arguments (as invoked from Typescript), received ${args_1.length}`);
        }
        const contextOrig_0 = args_1[0];
        const period_0 = args_1[1];
        if (!(typeof(contextOrig_0) === 'object' && contextOrig_0.callContext.currentQueryContext != undefined)) {
          __compactRuntime.typeError('prunePeriod',
                                     'argument 1 (as invoked from Typescript)',
                                     'registry.compact line 325 char 1',
                                     'CircuitContext',
                                     contextOrig_0)
        }
        if (!(typeof(period_0) === 'bigint' && period_0 >= 0n && period_0 <= 4294967295n)) {
          __compactRuntime.typeError('prunePeriod',
                                     'argument 1 (argument 2 as invoked from Typescript)',
                                     'registry.compact line 325 char 1',
                                     'Uint<0..4294967296>',
                                     period_0)
        }
        const context = __compactRuntime.copyCircuitContext(contextOrig_0);
        const partialProofData = {
          input: {
            value: _descriptor_6.toValue(period_0),
            alignment: _descriptor_6.alignment()
          },
          output: undefined,
          publicTranscript: [],
          privateTranscriptOutputs: []
        };
        const result_0 = await this._prunePeriod_0(context,
                                                   partialProofData,
                                                   period_0);
        partialProofData.output = { value: [], alignment: [] };
        __compactRuntime.finalizeCallProofData(context, partialProofData);
        return { result: result_0, context: context, gasCost: context.callContext.currentGasCost };
      },
      addRelay: async (...args_1) => {
        if (args_1.length !== 4) {
          throw new __compactRuntime.CompactError(`addRelay: expected 4 arguments (as invoked from Typescript), received ${args_1.length}`);
        }
        const contextOrig_0 = args_1[0];
        const peer_0 = args_1[1];
        const entry_0 = args_1[2];
        const reason_0 = args_1[3];
        if (!(typeof(contextOrig_0) === 'object' && contextOrig_0.callContext.currentQueryContext != undefined)) {
          __compactRuntime.typeError('addRelay',
                                     'argument 1 (as invoked from Typescript)',
                                     'registry.compact line 335 char 1',
                                     'CircuitContext',
                                     contextOrig_0)
        }
        if (!(peer_0.buffer instanceof ArrayBuffer && peer_0.BYTES_PER_ELEMENT === 1 && peer_0.length === 32)) {
          __compactRuntime.typeError('addRelay',
                                     'argument 1 (argument 2 as invoked from Typescript)',
                                     'registry.compact line 335 char 1',
                                     'Bytes<32>',
                                     peer_0)
        }
        if (!(typeof(entry_0) === 'object' && entry_0.operatorId.buffer instanceof ArrayBuffer && entry_0.operatorId.BYTES_PER_ELEMENT === 1 && entry_0.operatorId.length === 32 && typeof(entry_0.roles) === 'object' && typeof(entry_0.roles.relay) === 'boolean' && typeof(entry_0.roles.store) === 'boolean' && typeof(entry_0.roles.bootstrapper) === 'boolean' && typeof(entry_0.roles.gateway) === 'boolean' && typeof(entry_0.roles.anchorer) === 'boolean' && entry_0.keyCommitment.buffer instanceof ArrayBuffer && entry_0.keyCommitment.BYTES_PER_ELEMENT === 1 && entry_0.keyCommitment.length === 32)) {
          __compactRuntime.typeError('addRelay',
                                     'argument 2 (argument 3 as invoked from Typescript)',
                                     'registry.compact line 335 char 1',
                                     'struct RelayEntry<operatorId: Bytes<32>, roles: struct Roles<relay: Boolean, store: Boolean, bootstrapper: Boolean, gateway: Boolean, anchorer: Boolean>, keyCommitment: Bytes<32>>',
                                     entry_0)
        }
        if (!(typeof(reason_0) === 'bigint' && reason_0 >= 0n && reason_0 <= 65535n)) {
          __compactRuntime.typeError('addRelay',
                                     'argument 3 (argument 4 as invoked from Typescript)',
                                     'registry.compact line 335 char 1',
                                     'Uint<0..65536>',
                                     reason_0)
        }
        const context = __compactRuntime.copyCircuitContext(contextOrig_0);
        const partialProofData = {
          input: {
            value: _descriptor_0.toValue(peer_0).concat(_descriptor_5.toValue(entry_0).concat(_descriptor_7.toValue(reason_0))),
            alignment: _descriptor_0.alignment().concat(_descriptor_5.alignment().concat(_descriptor_7.alignment()))
          },
          output: undefined,
          publicTranscript: [],
          privateTranscriptOutputs: []
        };
        const result_0 = await this._addRelay_0(context,
                                                partialProofData,
                                                peer_0,
                                                entry_0,
                                                reason_0);
        partialProofData.output = { value: [], alignment: [] };
        __compactRuntime.finalizeCallProofData(context, partialProofData);
        return { result: result_0, context: context, gasCost: context.callContext.currentGasCost };
      },
      removeRelay: async (...args_1) => {
        if (args_1.length !== 3) {
          throw new __compactRuntime.CompactError(`removeRelay: expected 3 arguments (as invoked from Typescript), received ${args_1.length}`);
        }
        const contextOrig_0 = args_1[0];
        const peer_0 = args_1[1];
        const reason_0 = args_1[2];
        if (!(typeof(contextOrig_0) === 'object' && contextOrig_0.callContext.currentQueryContext != undefined)) {
          __compactRuntime.typeError('removeRelay',
                                     'argument 1 (as invoked from Typescript)',
                                     'registry.compact line 342 char 1',
                                     'CircuitContext',
                                     contextOrig_0)
        }
        if (!(peer_0.buffer instanceof ArrayBuffer && peer_0.BYTES_PER_ELEMENT === 1 && peer_0.length === 32)) {
          __compactRuntime.typeError('removeRelay',
                                     'argument 1 (argument 2 as invoked from Typescript)',
                                     'registry.compact line 342 char 1',
                                     'Bytes<32>',
                                     peer_0)
        }
        if (!(typeof(reason_0) === 'bigint' && reason_0 >= 0n && reason_0 <= 65535n)) {
          __compactRuntime.typeError('removeRelay',
                                     'argument 2 (argument 3 as invoked from Typescript)',
                                     'registry.compact line 342 char 1',
                                     'Uint<0..65536>',
                                     reason_0)
        }
        const context = __compactRuntime.copyCircuitContext(contextOrig_0);
        const partialProofData = {
          input: {
            value: _descriptor_0.toValue(peer_0).concat(_descriptor_7.toValue(reason_0)),
            alignment: _descriptor_0.alignment().concat(_descriptor_7.alignment())
          },
          output: undefined,
          publicTranscript: [],
          privateTranscriptOutputs: []
        };
        const result_0 = await this._removeRelay_0(context,
                                                   partialProofData,
                                                   peer_0,
                                                   reason_0);
        partialProofData.output = { value: [], alignment: [] };
        __compactRuntime.finalizeCallProofData(context, partialProofData);
        return { result: result_0, context: context, gasCost: context.callContext.currentGasCost };
      },
      proposeParams: async (...args_1) => {
        if (args_1.length !== 4) {
          throw new __compactRuntime.CompactError(`proposeParams: expected 4 arguments (as invoked from Typescript), received ${args_1.length}`);
        }
        const contextOrig_0 = args_1[0];
        const p_0 = args_1[1];
        const now_0 = args_1[2];
        const reason_0 = args_1[3];
        if (!(typeof(contextOrig_0) === 'object' && contextOrig_0.callContext.currentQueryContext != undefined)) {
          __compactRuntime.typeError('proposeParams',
                                     'argument 1 (as invoked from Typescript)',
                                     'registry.compact line 353 char 1',
                                     'CircuitContext',
                                     contextOrig_0)
        }
        if (!(typeof(p_0) === 'object' && typeof(p_0.epochLength) === 'bigint' && p_0.epochLength >= 0n && p_0.epochLength <= 4294967295n && typeof(p_0.membershipPeriod) === 'bigint' && p_0.membershipPeriod >= 0n && p_0.membershipPeriod <= 4294967295n && typeof(p_0.rootWindow) === 'bigint' && p_0.rootWindow >= 0n && p_0.rootWindow <= 4294967295n && Array.isArray(p_0.quota) && p_0.quota.length === 4 && p_0.quota.every((t) => typeof(t) === 'bigint' && t >= 0n && t <= 65535n) && typeof(p_0.anchorWindow) === 'bigint' && p_0.anchorWindow >= 0n && p_0.anchorWindow <= 4294967295n && typeof(p_0.anchorHistory) === 'bigint' && p_0.anchorHistory >= 0n && p_0.anchorHistory <= 4294967295n && typeof(p_0.shardCount) === 'bigint' && p_0.shardCount >= 0n && p_0.shardCount <= 255n && typeof(p_0.activationHeight) === 'bigint' && p_0.activationHeight >= 0n && p_0.activationHeight <= 18446744073709551615n && typeof(p_0.maxVersion) === 'bigint' && p_0.maxVersion >= 0n && p_0.maxVersion <= 255n && p_0.bootstrapHash.buffer instanceof ArrayBuffer && p_0.bootstrapHash.BYTES_PER_ELEMENT === 1 && p_0.bootstrapHash.length === 32)) {
          __compactRuntime.typeError('proposeParams',
                                     'argument 1 (argument 2 as invoked from Typescript)',
                                     'registry.compact line 353 char 1',
                                     'struct Params<epochLength: Uint<0..4294967296>, membershipPeriod: Uint<0..4294967296>, rootWindow: Uint<0..4294967296>, quota: Vector<4, Uint<0..65536>>, anchorWindow: Uint<0..4294967296>, anchorHistory: Uint<0..4294967296>, shardCount: Uint<0..256>, activationHeight: Uint<0..18446744073709551616>, maxVersion: Uint<0..256>, bootstrapHash: Bytes<32>>',
                                     p_0)
        }
        if (!(typeof(now_0) === 'bigint' && now_0 >= 0n && now_0 <= 18446744073709551615n)) {
          __compactRuntime.typeError('proposeParams',
                                     'argument 2 (argument 3 as invoked from Typescript)',
                                     'registry.compact line 353 char 1',
                                     'Uint<0..18446744073709551616>',
                                     now_0)
        }
        if (!(typeof(reason_0) === 'bigint' && reason_0 >= 0n && reason_0 <= 65535n)) {
          __compactRuntime.typeError('proposeParams',
                                     'argument 3 (argument 4 as invoked from Typescript)',
                                     'registry.compact line 353 char 1',
                                     'Uint<0..65536>',
                                     reason_0)
        }
        const context = __compactRuntime.copyCircuitContext(contextOrig_0);
        const partialProofData = {
          input: {
            value: _descriptor_11.toValue(p_0).concat(_descriptor_10.toValue(now_0).concat(_descriptor_7.toValue(reason_0))),
            alignment: _descriptor_11.alignment().concat(_descriptor_10.alignment().concat(_descriptor_7.alignment()))
          },
          output: undefined,
          publicTranscript: [],
          privateTranscriptOutputs: []
        };
        const result_0 = await this._proposeParams_0(context,
                                                     partialProofData,
                                                     p_0,
                                                     now_0,
                                                     reason_0);
        partialProofData.output = { value: [], alignment: [] };
        __compactRuntime.finalizeCallProofData(context, partialProofData);
        return { result: result_0, context: context, gasCost: context.callContext.currentGasCost };
      },
      activateParams: async (...args_1) => {
        if (args_1.length !== 1) {
          throw new __compactRuntime.CompactError(`activateParams: expected 1 argument (as invoked from Typescript), received ${args_1.length}`);
        }
        const contextOrig_0 = args_1[0];
        if (!(typeof(contextOrig_0) === 'object' && contextOrig_0.callContext.currentQueryContext != undefined)) {
          __compactRuntime.typeError('activateParams',
                                     'argument 1 (as invoked from Typescript)',
                                     'registry.compact line 362 char 1',
                                     'CircuitContext',
                                     contextOrig_0)
        }
        const context = __compactRuntime.copyCircuitContext(contextOrig_0);
        const partialProofData = {
          input: { value: [], alignment: [] },
          output: undefined,
          publicTranscript: [],
          privateTranscriptOutputs: []
        };
        const result_0 = await this._activateParams_0(context, partialProofData);
        partialProofData.output = { value: [], alignment: [] };
        __compactRuntime.finalizeCallProofData(context, partialProofData);
        return { result: result_0, context: context, gasCost: context.callContext.currentGasCost };
      },
      pause: async (...args_1) => {
        if (args_1.length !== 2) {
          throw new __compactRuntime.CompactError(`pause: expected 2 arguments (as invoked from Typescript), received ${args_1.length}`);
        }
        const contextOrig_0 = args_1[0];
        const reason_0 = args_1[1];
        if (!(typeof(contextOrig_0) === 'object' && contextOrig_0.callContext.currentQueryContext != undefined)) {
          __compactRuntime.typeError('pause',
                                     'argument 1 (as invoked from Typescript)',
                                     'registry.compact line 370 char 1',
                                     'CircuitContext',
                                     contextOrig_0)
        }
        if (!(typeof(reason_0) === 'bigint' && reason_0 >= 0n && reason_0 <= 65535n)) {
          __compactRuntime.typeError('pause',
                                     'argument 1 (argument 2 as invoked from Typescript)',
                                     'registry.compact line 370 char 1',
                                     'Uint<0..65536>',
                                     reason_0)
        }
        const context = __compactRuntime.copyCircuitContext(contextOrig_0);
        const partialProofData = {
          input: {
            value: _descriptor_7.toValue(reason_0),
            alignment: _descriptor_7.alignment()
          },
          output: undefined,
          publicTranscript: [],
          privateTranscriptOutputs: []
        };
        const result_0 = await this._pause_0(context, partialProofData, reason_0);
        partialProofData.output = { value: [], alignment: [] };
        __compactRuntime.finalizeCallProofData(context, partialProofData);
        return { result: result_0, context: context, gasCost: context.callContext.currentGasCost };
      },
      unpause: async (...args_1) => {
        if (args_1.length !== 2) {
          throw new __compactRuntime.CompactError(`unpause: expected 2 arguments (as invoked from Typescript), received ${args_1.length}`);
        }
        const contextOrig_0 = args_1[0];
        const reason_0 = args_1[1];
        if (!(typeof(contextOrig_0) === 'object' && contextOrig_0.callContext.currentQueryContext != undefined)) {
          __compactRuntime.typeError('unpause',
                                     'argument 1 (as invoked from Typescript)',
                                     'registry.compact line 376 char 1',
                                     'CircuitContext',
                                     contextOrig_0)
        }
        if (!(typeof(reason_0) === 'bigint' && reason_0 >= 0n && reason_0 <= 65535n)) {
          __compactRuntime.typeError('unpause',
                                     'argument 1 (argument 2 as invoked from Typescript)',
                                     'registry.compact line 376 char 1',
                                     'Uint<0..65536>',
                                     reason_0)
        }
        const context = __compactRuntime.copyCircuitContext(contextOrig_0);
        const partialProofData = {
          input: {
            value: _descriptor_7.toValue(reason_0),
            alignment: _descriptor_7.alignment()
          },
          output: undefined,
          publicTranscript: [],
          privateTranscriptOutputs: []
        };
        const result_0 = await this._unpause_0(context,
                                               partialProofData,
                                               reason_0);
        partialProofData.output = { value: [], alignment: [] };
        __compactRuntime.finalizeCallProofData(context, partialProofData);
        return { result: result_0, context: context, gasCost: context.callContext.currentGasCost };
      },
      setSteward: async (...args_1) => {
        if (args_1.length !== 3) {
          throw new __compactRuntime.CompactError(`setSteward: expected 3 arguments (as invoked from Typescript), received ${args_1.length}`);
        }
        const contextOrig_0 = args_1[0];
        const newKey_0 = args_1[1];
        const reason_0 = args_1[2];
        if (!(typeof(contextOrig_0) === 'object' && contextOrig_0.callContext.currentQueryContext != undefined)) {
          __compactRuntime.typeError('setSteward',
                                     'argument 1 (as invoked from Typescript)',
                                     'registry.compact line 382 char 1',
                                     'CircuitContext',
                                     contextOrig_0)
        }
        if (!(newKey_0.buffer instanceof ArrayBuffer && newKey_0.BYTES_PER_ELEMENT === 1 && newKey_0.length === 32)) {
          __compactRuntime.typeError('setSteward',
                                     'argument 1 (argument 2 as invoked from Typescript)',
                                     'registry.compact line 382 char 1',
                                     'Bytes<32>',
                                     newKey_0)
        }
        if (!(typeof(reason_0) === 'bigint' && reason_0 >= 0n && reason_0 <= 65535n)) {
          __compactRuntime.typeError('setSteward',
                                     'argument 2 (argument 3 as invoked from Typescript)',
                                     'registry.compact line 382 char 1',
                                     'Uint<0..65536>',
                                     reason_0)
        }
        const context = __compactRuntime.copyCircuitContext(contextOrig_0);
        const partialProofData = {
          input: {
            value: _descriptor_0.toValue(newKey_0).concat(_descriptor_7.toValue(reason_0)),
            alignment: _descriptor_0.alignment().concat(_descriptor_7.alignment())
          },
          output: undefined,
          publicTranscript: [],
          privateTranscriptOutputs: []
        };
        const result_0 = await this._setSteward_0(context,
                                                  partialProofData,
                                                  newKey_0,
                                                  reason_0);
        partialProofData.output = { value: [], alignment: [] };
        __compactRuntime.finalizeCallProofData(context, partialProofData);
        return { result: result_0, context: context, gasCost: context.callContext.currentGasCost };
      },
      postAnchor: async (...args_1) => {
        if (args_1.length !== 7) {
          throw new __compactRuntime.CompactError(`postAnchor: expected 7 arguments (as invoked from Typescript), received ${args_1.length}`);
        }
        const contextOrig_0 = args_1[0];
        const peer_0 = args_1[1];
        const window_0 = args_1[2];
        const q_0 = args_1[3];
        const slot_0 = args_1[4];
        const root_0 = args_1[5];
        const counts_0 = args_1[6];
        if (!(typeof(contextOrig_0) === 'object' && contextOrig_0.callContext.currentQueryContext != undefined)) {
          __compactRuntime.typeError('postAnchor',
                                     'argument 1 (as invoked from Typescript)',
                                     'registry.compact line 394 char 1',
                                     'CircuitContext',
                                     contextOrig_0)
        }
        if (!(peer_0.buffer instanceof ArrayBuffer && peer_0.BYTES_PER_ELEMENT === 1 && peer_0.length === 32)) {
          __compactRuntime.typeError('postAnchor',
                                     'argument 1 (argument 2 as invoked from Typescript)',
                                     'registry.compact line 394 char 1',
                                     'Bytes<32>',
                                     peer_0)
        }
        if (!(typeof(window_0) === 'bigint' && window_0 >= 0n && window_0 <= 18446744073709551615n)) {
          __compactRuntime.typeError('postAnchor',
                                     'argument 2 (argument 3 as invoked from Typescript)',
                                     'registry.compact line 394 char 1',
                                     'Uint<0..18446744073709551616>',
                                     window_0)
        }
        if (!(typeof(q_0) === 'bigint' && q_0 >= 0n && q_0 <= 18446744073709551615n)) {
          __compactRuntime.typeError('postAnchor',
                                     'argument 3 (argument 4 as invoked from Typescript)',
                                     'registry.compact line 394 char 1',
                                     'Uint<0..18446744073709551616>',
                                     q_0)
        }
        if (!(typeof(slot_0) === 'bigint' && slot_0 >= 0n && slot_0 <= 65535n)) {
          __compactRuntime.typeError('postAnchor',
                                     'argument 4 (argument 5 as invoked from Typescript)',
                                     'registry.compact line 394 char 1',
                                     'Uint<0..65536>',
                                     slot_0)
        }
        if (!(root_0.buffer instanceof ArrayBuffer && root_0.BYTES_PER_ELEMENT === 1 && root_0.length === 32)) {
          __compactRuntime.typeError('postAnchor',
                                     'argument 5 (argument 6 as invoked from Typescript)',
                                     'registry.compact line 394 char 1',
                                     'Bytes<32>',
                                     root_0)
        }
        if (!(Array.isArray(counts_0) && counts_0.length === 8 && counts_0.every((t) => typeof(t) === 'bigint' && t >= 0n && t <= 4294967295n))) {
          __compactRuntime.typeError('postAnchor',
                                     'argument 6 (argument 7 as invoked from Typescript)',
                                     'registry.compact line 394 char 1',
                                     'Vector<8, Uint<0..4294967296>>',
                                     counts_0)
        }
        const context = __compactRuntime.copyCircuitContext(contextOrig_0);
        const partialProofData = {
          input: {
            value: _descriptor_0.toValue(peer_0).concat(_descriptor_10.toValue(window_0).concat(_descriptor_10.toValue(q_0).concat(_descriptor_7.toValue(slot_0).concat(_descriptor_0.toValue(root_0).concat(_descriptor_12.toValue(counts_0)))))),
            alignment: _descriptor_0.alignment().concat(_descriptor_10.alignment().concat(_descriptor_10.alignment().concat(_descriptor_7.alignment().concat(_descriptor_0.alignment().concat(_descriptor_12.alignment())))))
          },
          output: undefined,
          publicTranscript: [],
          privateTranscriptOutputs: []
        };
        const result_0 = await this._postAnchor_0(context,
                                                  partialProofData,
                                                  peer_0,
                                                  window_0,
                                                  q_0,
                                                  slot_0,
                                                  root_0,
                                                  counts_0);
        partialProofData.output = { value: [], alignment: [] };
        __compactRuntime.finalizeCallProofData(context, partialProofData);
        return { result: result_0, context: context, gasCost: context.callContext.currentGasCost };
      },
      pruneAnchor: async (...args_1) => {
        if (args_1.length !== 2) {
          throw new __compactRuntime.CompactError(`pruneAnchor: expected 2 arguments (as invoked from Typescript), received ${args_1.length}`);
        }
        const contextOrig_0 = args_1[0];
        const slot_0 = args_1[1];
        if (!(typeof(contextOrig_0) === 'object' && contextOrig_0.callContext.currentQueryContext != undefined)) {
          __compactRuntime.typeError('pruneAnchor',
                                     'argument 1 (as invoked from Typescript)',
                                     'registry.compact line 430 char 1',
                                     'CircuitContext',
                                     contextOrig_0)
        }
        if (!(typeof(slot_0) === 'bigint' && slot_0 >= 0n && slot_0 <= 65535n)) {
          __compactRuntime.typeError('pruneAnchor',
                                     'argument 1 (argument 2 as invoked from Typescript)',
                                     'registry.compact line 430 char 1',
                                     'Uint<0..65536>',
                                     slot_0)
        }
        const context = __compactRuntime.copyCircuitContext(contextOrig_0);
        const partialProofData = {
          input: {
            value: _descriptor_7.toValue(slot_0),
            alignment: _descriptor_7.alignment()
          },
          output: undefined,
          publicTranscript: [],
          privateTranscriptOutputs: []
        };
        const result_0 = await this._pruneAnchor_0(context,
                                                   partialProofData,
                                                   slot_0);
        partialProofData.output = { value: [], alignment: [] };
        __compactRuntime.finalizeCallProofData(context, partialProofData);
        return { result: result_0, context: context, gasCost: context.callContext.currentGasCost };
      },
      anchorRootValid: async (...args_1) => {
        if (args_1.length !== 2) {
          throw new __compactRuntime.CompactError(`anchorRootValid: expected 2 arguments (as invoked from Typescript), received ${args_1.length}`);
        }
        const contextOrig_0 = args_1[0];
        const rt_0 = args_1[1];
        if (!(typeof(contextOrig_0) === 'object' && contextOrig_0.callContext.currentQueryContext != undefined)) {
          __compactRuntime.typeError('anchorRootValid',
                                     'argument 1 (as invoked from Typescript)',
                                     'registry.compact line 441 char 1',
                                     'CircuitContext',
                                     contextOrig_0)
        }
        if (!(typeof(rt_0) === 'object' && typeof(rt_0.field) === 'bigint' && rt_0.field >= 0 && rt_0.field <= __compactRuntime.MAX_FIELD)) {
          __compactRuntime.typeError('anchorRootValid',
                                     'argument 1 (argument 2 as invoked from Typescript)',
                                     'registry.compact line 441 char 1',
                                     'struct MerkleTreeDigest<field: Field>',
                                     rt_0)
        }
        const context = __compactRuntime.copyCircuitContext(contextOrig_0);
        const partialProofData = {
          input: {
            value: _descriptor_2.toValue(rt_0),
            alignment: _descriptor_2.alignment()
          },
          output: undefined,
          publicTranscript: [],
          privateTranscriptOutputs: []
        };
        const result_0 = await this._anchorRootValid_0(context,
                                                       partialProofData,
                                                       rt_0);
        partialProofData.output = { value: _descriptor_3.toValue(result_0), alignment: _descriptor_3.alignment() };
        __compactRuntime.finalizeCallProofData(context, partialProofData);
        return { result: result_0, context: context, gasCost: context.callContext.currentGasCost };
      }
    };
    this.impureCircuits = {
      register: this.circuits.register,
      revoke: this.circuits.revoke,
      prunePeriod: this.circuits.prunePeriod,
      addRelay: this.circuits.addRelay,
      removeRelay: this.circuits.removeRelay,
      proposeParams: this.circuits.proposeParams,
      activateParams: this.circuits.activateParams,
      pause: this.circuits.pause,
      unpause: this.circuits.unpause,
      setSteward: this.circuits.setSteward,
      postAnchor: this.circuits.postAnchor,
      pruneAnchor: this.circuits.pruneAnchor,
      anchorRootValid: this.circuits.anchorRootValid
    };
    this.provableCircuits = {
      register: this.circuits.register,
      revoke: this.circuits.revoke,
      prunePeriod: this.circuits.prunePeriod,
      addRelay: this.circuits.addRelay,
      removeRelay: this.circuits.removeRelay,
      proposeParams: this.circuits.proposeParams,
      activateParams: this.circuits.activateParams,
      pause: this.circuits.pause,
      unpause: this.circuits.unpause,
      setSteward: this.circuits.setSteward,
      postAnchor: this.circuits.postAnchor,
      pruneAnchor: this.circuits.pruneAnchor,
      anchorRootValid: this.circuits.anchorRootValid
    };
  }
  async initialState(...args_0) {
    if (args_0.length !== 5) {
      throw new __compactRuntime.CompactError(`Contract state constructor: expected 5 arguments (as invoked from Typescript), received ${args_0.length}`);
    }
    const constructorContext_0 = args_0[0];
    const stewardKey_0 = args_0[1];
    const n_0 = args_0[2];
    const delay_0 = args_0[3];
    const p_0 = args_0[4];
    if (typeof(constructorContext_0) !== 'object') {
      throw new __compactRuntime.CompactError(`Contract state constructor: expected 'constructorContext' in argument 1 (as invoked from Typescript) to be an object`);
    }
    if (!('initialPrivateState' in constructorContext_0)) {
      throw new __compactRuntime.CompactError(`Contract state constructor: expected 'initialPrivateState' in argument 1 (as invoked from Typescript)`);
    }
    if (!('initialZswapLocalState' in constructorContext_0)) {
      throw new __compactRuntime.CompactError(`Contract state constructor: expected 'initialZswapLocalState' in argument 1 (as invoked from Typescript)`);
    }
    if (typeof(constructorContext_0.initialZswapLocalState) !== 'object') {
      throw new __compactRuntime.CompactError(`Contract state constructor: expected 'initialZswapLocalState' in argument 1 (as invoked from Typescript) to be an object`);
    }
    if (!(stewardKey_0.buffer instanceof ArrayBuffer && stewardKey_0.BYTES_PER_ELEMENT === 1 && stewardKey_0.length === 32)) {
      __compactRuntime.typeError('Contract state constructor',
                                 'argument 1 (argument 2 as invoked from Typescript)',
                                 'registry.compact line 164 char 1',
                                 'Bytes<32>',
                                 stewardKey_0)
    }
    if (!(n_0.buffer instanceof ArrayBuffer && n_0.BYTES_PER_ELEMENT === 1 && n_0.length === 32)) {
      __compactRuntime.typeError('Contract state constructor',
                                 'argument 2 (argument 3 as invoked from Typescript)',
                                 'registry.compact line 164 char 1',
                                 'Bytes<32>',
                                 n_0)
    }
    if (!(typeof(delay_0) === 'bigint' && delay_0 >= 0n && delay_0 <= 4294967295n)) {
      __compactRuntime.typeError('Contract state constructor',
                                 'argument 3 (argument 4 as invoked from Typescript)',
                                 'registry.compact line 164 char 1',
                                 'Uint<0..4294967296>',
                                 delay_0)
    }
    if (!(typeof(p_0) === 'object' && typeof(p_0.epochLength) === 'bigint' && p_0.epochLength >= 0n && p_0.epochLength <= 4294967295n && typeof(p_0.membershipPeriod) === 'bigint' && p_0.membershipPeriod >= 0n && p_0.membershipPeriod <= 4294967295n && typeof(p_0.rootWindow) === 'bigint' && p_0.rootWindow >= 0n && p_0.rootWindow <= 4294967295n && Array.isArray(p_0.quota) && p_0.quota.length === 4 && p_0.quota.every((t) => typeof(t) === 'bigint' && t >= 0n && t <= 65535n) && typeof(p_0.anchorWindow) === 'bigint' && p_0.anchorWindow >= 0n && p_0.anchorWindow <= 4294967295n && typeof(p_0.anchorHistory) === 'bigint' && p_0.anchorHistory >= 0n && p_0.anchorHistory <= 4294967295n && typeof(p_0.shardCount) === 'bigint' && p_0.shardCount >= 0n && p_0.shardCount <= 255n && typeof(p_0.activationHeight) === 'bigint' && p_0.activationHeight >= 0n && p_0.activationHeight <= 18446744073709551615n && typeof(p_0.maxVersion) === 'bigint' && p_0.maxVersion >= 0n && p_0.maxVersion <= 255n && p_0.bootstrapHash.buffer instanceof ArrayBuffer && p_0.bootstrapHash.BYTES_PER_ELEMENT === 1 && p_0.bootstrapHash.length === 32)) {
      __compactRuntime.typeError('Contract state constructor',
                                 'argument 4 (argument 5 as invoked from Typescript)',
                                 'registry.compact line 164 char 1',
                                 'struct Params<epochLength: Uint<0..4294967296>, membershipPeriod: Uint<0..4294967296>, rootWindow: Uint<0..4294967296>, quota: Vector<4, Uint<0..65536>>, anchorWindow: Uint<0..4294967296>, anchorHistory: Uint<0..4294967296>, shardCount: Uint<0..256>, activationHeight: Uint<0..18446744073709551616>, maxVersion: Uint<0..256>, bootstrapHash: Bytes<32>>',
                                 p_0)
    }
    const state_0 = new __compactRuntime.ContractState();
    let stateValue_0 = __compactRuntime.StateValue.newArray();
    stateValue_0 = stateValue_0.arrayPush(__compactRuntime.StateValue.newNull());
    stateValue_0 = stateValue_0.arrayPush(__compactRuntime.StateValue.newNull());
    stateValue_0 = stateValue_0.arrayPush(__compactRuntime.StateValue.newNull());
    stateValue_0 = stateValue_0.arrayPush(__compactRuntime.StateValue.newNull());
    stateValue_0 = stateValue_0.arrayPush(__compactRuntime.StateValue.newNull());
    stateValue_0 = stateValue_0.arrayPush(__compactRuntime.StateValue.newNull());
    stateValue_0 = stateValue_0.arrayPush(__compactRuntime.StateValue.newNull());
    stateValue_0 = stateValue_0.arrayPush(__compactRuntime.StateValue.newNull());
    stateValue_0 = stateValue_0.arrayPush(__compactRuntime.StateValue.newNull());
    stateValue_0 = stateValue_0.arrayPush(__compactRuntime.StateValue.newNull());
    stateValue_0 = stateValue_0.arrayPush(__compactRuntime.StateValue.newNull());
    state_0.data = new __compactRuntime.ChargedState(stateValue_0);
    state_0.setOperation('register', new __compactRuntime.ContractOperation());
    state_0.setOperation('revoke', new __compactRuntime.ContractOperation());
    state_0.setOperation('prunePeriod', new __compactRuntime.ContractOperation());
    state_0.setOperation('addRelay', new __compactRuntime.ContractOperation());
    state_0.setOperation('removeRelay', new __compactRuntime.ContractOperation());
    state_0.setOperation('proposeParams', new __compactRuntime.ContractOperation());
    state_0.setOperation('activateParams', new __compactRuntime.ContractOperation());
    state_0.setOperation('pause', new __compactRuntime.ContractOperation());
    state_0.setOperation('unpause', new __compactRuntime.ContractOperation());
    state_0.setOperation('setSteward', new __compactRuntime.ContractOperation());
    state_0.setOperation('postAnchor', new __compactRuntime.ContractOperation());
    state_0.setOperation('pruneAnchor', new __compactRuntime.ContractOperation());
    state_0.setOperation('anchorRootValid', new __compactRuntime.ContractOperation());
    const context = __compactRuntime.createCircuitContext({circuitId: 'constructor', contractAddress: __compactRuntime.dummyContractAddress(), coinPublicKeyOrZswapState: constructorContext_0.initialZswapLocalState.coinPublicKey, contractState: state_0.data, privateState: constructorContext_0.initialPrivateState});
    const partialProofData = {
      input: { value: [], alignment: [] },
      output: undefined,
      publicTranscript: [],
      privateTranscriptOutputs: []
    };
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_9.toValue(0n),
                                                                                              alignment: _descriptor_9.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_0.toValue(new Uint8Array(32)),
                                                                                              alignment: _descriptor_0.alignment() }).encode() } },
                                       { ins: { cached: false, n: 1 } }]);
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_9.toValue(1n),
                                                                                              alignment: _descriptor_9.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_6.toValue(0n),
                                                                                              alignment: _descriptor_6.alignment() }).encode() } },
                                       { ins: { cached: false, n: 1 } }]);
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_9.toValue(2n),
                                                                                              alignment: _descriptor_9.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_0.toValue(new Uint8Array(32)),
                                                                                              alignment: _descriptor_0.alignment() }).encode() } },
                                       { ins: { cached: false, n: 1 } }]);
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_9.toValue(3n),
                                                                                              alignment: _descriptor_9.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_3.toValue(false),
                                                                                              alignment: _descriptor_3.alignment() }).encode() } },
                                       { ins: { cached: false, n: 1 } }]);
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_9.toValue(4n),
                                                                                              alignment: _descriptor_9.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_11.toValue({ epochLength: 0n, membershipPeriod: 0n, rootWindow: 0n, quota: new Array(4).fill(0n), anchorWindow: 0n, anchorHistory: 0n, shardCount: 0n, activationHeight: 0n, maxVersion: 0n, bootstrapHash: new Uint8Array(32) }),
                                                                                              alignment: _descriptor_11.alignment() }).encode() } },
                                       { ins: { cached: false, n: 1 } }]);
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_9.toValue(5n),
                                                                                              alignment: _descriptor_9.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_16.toValue({ is_some: false, value: { params: { epochLength: 0n, membershipPeriod: 0n, rootWindow: 0n, quota: new Array(4).fill(0n), anchorWindow: 0n, anchorHistory: 0n, shardCount: 0n, activationHeight: 0n, maxVersion: 0n, bootstrapHash: new Uint8Array(32) }, effectiveAt: 0n } }),
                                                                                              alignment: _descriptor_16.alignment() }).encode() } },
                                       { ins: { cached: false, n: 1 } }]);
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_9.toValue(6n),
                                                                                              alignment: _descriptor_9.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newMap(
                                                          new __compactRuntime.StateMap()
                                                        ).encode() } },
                                       { ins: { cached: false, n: 1 } }]);
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_9.toValue(7n),
                                                                                              alignment: _descriptor_9.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newMap(
                                                          new __compactRuntime.StateMap()
                                                        ).encode() } },
                                       { ins: { cached: false, n: 1 } }]);
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_9.toValue(8n),
                                                                                              alignment: _descriptor_9.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newMap(
                                                          new __compactRuntime.StateMap()
                                                        ).encode() } },
                                       { ins: { cached: false, n: 1 } }]);
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_9.toValue(9n),
                                                                                              alignment: _descriptor_9.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newMap(
                                                          new __compactRuntime.StateMap()
                                                        ).encode() } },
                                       { ins: { cached: false, n: 1 } }]);
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_9.toValue(10n),
                                                                                              alignment: _descriptor_9.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newArray()
                                                          .arrayPush(__compactRuntime.StateValue.newBoundedMerkleTree(
                                                                       new __compactRuntime.StateBoundedMerkleTree(12)
                                                                     )).arrayPush(__compactRuntime.StateValue.newCell({ value: _descriptor_10.toValue(0n),
                                                                                                                        alignment: _descriptor_10.alignment() })).arrayPush(__compactRuntime.StateValue.newMap(
                                                                                                                                                                              new __compactRuntime.StateMap()
                                                                                                                                                                            ))
                                                          .encode() } },
                                       { idx: { cached: false,
                                                pushPath: true,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(2n),
                                                                  alignment: _descriptor_9.alignment() } }] } },
                                       { dup: { n: 2 } },
                                       { idx: { cached: false,
                                                pushPath: false,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(0n),
                                                                  alignment: _descriptor_9.alignment() } }] } },
                                       'root',
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newNull().encode() } },
                                       { ins: { cached: true, n: 2 } },
                                       { ins: { cached: false, n: 1 } }]);
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_9.toValue(2n),
                                                                                              alignment: _descriptor_9.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_0.toValue(stewardKey_0),
                                                                                              alignment: _descriptor_0.alignment() }).encode() } },
                                       { ins: { cached: false, n: 1 } }]);
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_9.toValue(0n),
                                                                                              alignment: _descriptor_9.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_0.toValue(n_0),
                                                                                              alignment: _descriptor_0.alignment() }).encode() } },
                                       { ins: { cached: false, n: 1 } }]);
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_9.toValue(1n),
                                                                                              alignment: _descriptor_9.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_6.toValue(delay_0),
                                                                                              alignment: _descriptor_6.alignment() }).encode() } },
                                       { ins: { cached: false, n: 1 } }]);
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_9.toValue(4n),
                                                                                              alignment: _descriptor_9.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_11.toValue(p_0),
                                                                                              alignment: _descriptor_11.alignment() }).encode() } },
                                       { ins: { cached: false, n: 1 } }]);
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_9.toValue(3n),
                                                                                              alignment: _descriptor_9.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_3.toValue(false),
                                                                                              alignment: _descriptor_3.alignment() }).encode() } },
                                       { ins: { cached: false, n: 1 } }]);
    const tmp_0 = this._none_0();
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_9.toValue(5n),
                                                                                              alignment: _descriptor_9.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_16.toValue(tmp_0),
                                                                                              alignment: _descriptor_16.alignment() }).encode() } },
                                       { ins: { cached: false, n: 1 } }]);
    state_0.data = new __compactRuntime.ChargedState(context.callContext.currentQueryContext.state.state);
    return {
      currentContractState: state_0,
      currentPrivateState: context.callContext.currentPrivateState,
      currentZswapLocalState: context.callContext.currentZswapLocalState
    }
  }
  _some_0(value_0) { return { is_some: true, value: value_0 }; }
  _none_0() {
    return { is_some: false,
             value:
               { params: { epochLength: 0n, membershipPeriod: 0n, rootWindow: 0n, quota: new Array(4).fill(0n), anchorWindow: 0n, anchorHistory: 0n, shardCount: 0n, activationHeight: 0n, maxVersion: 0n, bootstrapHash: new Uint8Array(32) }, effectiveAt: 0n } };
  }
  _merkleTreePathRoot_0(path_0) {
    return { field:
               this._folder_0((...args_0) =>
                                this._merkleTreePathEntryRoot_0(...args_0),
                              this._degradeToTransient_0(this._persistentHash_3({ domain_sep:
                                                                                    new Uint8Array([109, 100, 110, 58, 108, 104]),
                                                                                  data:
                                                                                    path_0.leaf })),
                              path_0.path) };
  }
  _merkleTreePathEntryRoot_0(recursiveDigest_0, entry_0) {
    const left_0 = entry_0.goes_left ? recursiveDigest_0 : entry_0.sibling.field;
    const right_0 = entry_0.goes_left ?
                    entry_0.sibling.field :
                    recursiveDigest_0;
    return this._transientHash_1([left_0, right_0]);
  }
  async _blockTimeLt_0(context, partialProofData, time_0) {
    return _descriptor_3.fromValue(__compactRuntime.queryLedgerState(context,
                                                                     partialProofData,
                                                                     [
                                                                      { dup: { n: 2 } },
                                                                      { idx: { cached: true,
                                                                               pushPath: false,
                                                                               path: [
                                                                                      { tag: 'value',
                                                                                        value: { value: _descriptor_9.toValue(2n),
                                                                                                 alignment: _descriptor_9.alignment() } }] } },
                                                                      { push: { storage: false,
                                                                                value: __compactRuntime.StateValue.newCell({ value: _descriptor_10.toValue(time_0),
                                                                                                                             alignment: _descriptor_10.alignment() }).encode() } },
                                                                      'lt',
                                                                      { popeq: { cached: true,
                                                                                 result: undefined } }]).value);
  }
  async _blockTimeGte_0(context, partialProofData, time_0) {
    return !await this._blockTimeLt_0(context, partialProofData, time_0);
  }
  _transientHash_0(value_0) {
    const result_0 = __compactRuntime.transientHash(_descriptor_32, value_0);
    return result_0;
  }
  _transientHash_1(value_0) {
    const result_0 = __compactRuntime.transientHash(_descriptor_30, value_0);
    return result_0;
  }
  _persistentHash_0(value_0) {
    const result_0 = __compactRuntime.persistentHash(_descriptor_31, value_0);
    return result_0;
  }
  _persistentHash_1(value_0) {
    const result_0 = __compactRuntime.persistentHash(_descriptor_28, value_0);
    return result_0;
  }
  _persistentHash_2(value_0) {
    const result_0 = __compactRuntime.persistentHash(_descriptor_29, value_0);
    return result_0;
  }
  _persistentHash_3(value_0) {
    const result_0 = __compactRuntime.persistentHash(_descriptor_27, value_0);
    return result_0;
  }
  _degradeToTransient_0(x_0) {
    const result_0 = __compactRuntime.degradeToTransient(x_0);
    return result_0;
  }
  _anchorName_0() {
    return new Uint8Array([109, 112, 101, 47, 97, 110, 99, 104, 111, 114, 47, 118, 49, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]);
  }
  _govName_0() {
    return new Uint8Array([109, 112, 101, 47, 103, 111, 118, 47, 118, 49, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]);
  }
  _actParams_0() { return 1n; }
  _actParamsActive_0() { return 2n; }
  _actPause_0() { return 3n; }
  _actUnpause_0() { return 4n; }
  _actRelayAdd_0() { return 5n; }
  _actRelayRemove_0() { return 6n; }
  _actRevoke_0() { return 7n; }
  _actSteward_0() { return 8n; }
  _anchorSlots_0() { return 2940n; }
  _clockTolerance_0() { return 900n; }
  _anchorDelay_0() { return 20n; }
  _stewardSecret_0(context, partialProofData) {
    const witnessContext_0 = __compactRuntime.createWitnessContext(ledger(context.callContext.currentQueryContext.state), context.callContext.currentPrivateState, context.callContext.currentQueryContext.address);
    const [nextPrivateState_0, result_0] = this.witnesses.stewardSecret(witnessContext_0);
    context.callContext.currentPrivateState = nextPrivateState_0;
    if (!(result_0.buffer instanceof ArrayBuffer && result_0.BYTES_PER_ELEMENT === 1 && result_0.length === 32)) {
      __compactRuntime.typeError('stewardSecret',
                                 'return value',
                                 'registry.compact line 156 char 1',
                                 'Bytes<32>',
                                 result_0)
    }
    partialProofData.privateTranscriptOutputs.push({
      value: _descriptor_0.toValue(result_0),
      alignment: _descriptor_0.alignment()
    });
    return result_0;
  }
  _relaySecret_0(context, partialProofData) {
    const witnessContext_0 = __compactRuntime.createWitnessContext(ledger(context.callContext.currentQueryContext.state), context.callContext.currentPrivateState, context.callContext.currentQueryContext.address);
    const [nextPrivateState_0, result_0] = this.witnesses.relaySecret(witnessContext_0);
    context.callContext.currentPrivateState = nextPrivateState_0;
    if (!(result_0.buffer instanceof ArrayBuffer && result_0.BYTES_PER_ELEMENT === 1 && result_0.length === 32)) {
      __compactRuntime.typeError('relaySecret',
                                 'return value',
                                 'registry.compact line 157 char 1',
                                 'Bytes<32>',
                                 result_0)
    }
    partialProofData.privateTranscriptOutputs.push({
      value: _descriptor_0.toValue(result_0),
      alignment: _descriptor_0.alignment()
    });
    return result_0;
  }
  _revocationEvidence_0(context, partialProofData) {
    const witnessContext_0 = __compactRuntime.createWitnessContext(ledger(context.callContext.currentQueryContext.state), context.callContext.currentPrivateState, context.callContext.currentQueryContext.address);
    const [nextPrivateState_0, result_0] = this.witnesses.revocationEvidence(witnessContext_0);
    context.callContext.currentPrivateState = nextPrivateState_0;
    if (!(typeof(result_0) === 'object' && typeof(result_0.a0) === 'bigint' && result_0.a0 >= 0 && result_0.a0 <= __compactRuntime.MAX_FIELD && typeof(result_0.epoch) === 'bigint' && result_0.epoch >= 0n && result_0.epoch <= 18446744073709551615n && typeof(result_0.sizeClass) === 'bigint' && result_0.sizeClass >= 0n && result_0.sizeClass <= 255n && typeof(result_0.credit) === 'bigint' && result_0.credit >= 0n && result_0.credit <= 65535n && Array.isArray(result_0.quota) && result_0.quota.length === 4 && result_0.quota.every((t) => typeof(t) === 'bigint' && t >= 0n && t <= 65535n) && typeof(result_0.s1) === 'object' && result_0.s1.eid.buffer instanceof ArrayBuffer && result_0.s1.eid.BYTES_PER_ELEMENT === 1 && result_0.s1.eid.length === 32 && typeof(result_0.s1.y) === 'bigint' && result_0.s1.y >= 0 && result_0.s1.y <= __compactRuntime.MAX_FIELD && typeof(result_0.s2) === 'object' && result_0.s2.eid.buffer instanceof ArrayBuffer && result_0.s2.eid.BYTES_PER_ELEMENT === 1 && result_0.s2.eid.length === 32 && typeof(result_0.s2.y) === 'bigint' && result_0.s2.y >= 0 && result_0.s2.y <= __compactRuntime.MAX_FIELD)) {
      __compactRuntime.typeError('revocationEvidence',
                                 'return value',
                                 'registry.compact line 158 char 1',
                                 'struct Evidence<a0: Field, epoch: Uint<0..18446744073709551616>, sizeClass: Uint<0..256>, credit: Uint<0..65536>, quota: Vector<4, Uint<0..65536>>, s1: struct Share<eid: Bytes<32>, y: Field>, s2: struct Share<eid: Bytes<32>, y: Field>>',
                                 result_0)
    }
    partialProofData.privateTranscriptOutputs.push({
      value: _descriptor_25.toValue(result_0),
      alignment: _descriptor_25.alignment()
    });
    return result_0;
  }
  _memberPath_0(context, partialProofData) {
    const witnessContext_0 = __compactRuntime.createWitnessContext(ledger(context.callContext.currentQueryContext.state), context.callContext.currentPrivateState, context.callContext.currentQueryContext.address);
    const [nextPrivateState_0, result_0] = this.witnesses.memberPath(witnessContext_0);
    context.callContext.currentPrivateState = nextPrivateState_0;
    if (!(typeof(result_0) === 'object' && result_0.leaf.buffer instanceof ArrayBuffer && result_0.leaf.BYTES_PER_ELEMENT === 1 && result_0.leaf.length === 32 && Array.isArray(result_0.path) && result_0.path.length === 20 && result_0.path.every((t) => typeof(t) === 'object' && typeof(t.sibling) === 'object' && typeof(t.sibling.field) === 'bigint' && t.sibling.field >= 0 && t.sibling.field <= __compactRuntime.MAX_FIELD && typeof(t.goes_left) === 'boolean'))) {
      __compactRuntime.typeError('memberPath',
                                 'return value',
                                 'registry.compact line 159 char 1',
                                 'struct MerkleTreePath<leaf: Bytes<32>, path: Vector<20, struct MerkleTreePathEntry<sibling: struct MerkleTreeDigest<field: Field>, goes_left: Boolean>>>',
                                 result_0)
    }
    partialProofData.privateTranscriptOutputs.push({
      value: _descriptor_23.toValue(result_0),
      alignment: _descriptor_23.alignment()
    });
    return result_0;
  }
  _stewardKeyOf_0(sk_0) {
    return this._persistentHash_1([new Uint8Array([109, 112, 101, 47, 118, 49, 47, 115, 116, 101, 119, 97, 114, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   sk_0]);
  }
  _relayKeyOf_0(sk_0) {
    return this._persistentHash_1([new Uint8Array([109, 112, 101, 47, 118, 49, 47, 114, 101, 108, 97, 121, 107, 101, 121, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   sk_0]);
  }
  _memberLeafOf_0(idc_0, quota_0) {
    return this._persistentHash_0({ domain:
                                      new Uint8Array([109, 112, 101, 47, 118, 49, 47, 108, 101, 97, 102, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                    idc: idc_0,
                                    quota: quota_0 });
  }
  _idcOf_0(a0_0) {
    return this._persistentHash_1([new Uint8Array([109, 112, 101, 47, 118, 49, 47, 105, 100, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   __compactRuntime.convertBigintToBytes(32,
                                                                         a0_0,
                                                                         'registry.compact line 189 char 71')]);
  }
  _anchorLeafOf_0(window_0, root_0) {
    return this._persistentHash_2({ domain:
                                      new Uint8Array([109, 112, 101, 47, 118, 49, 47, 97, 110, 99, 104, 111, 114, 108, 101, 97, 102, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                    window: window_0,
                                    root: root_0 });
  }
  _rlnA1_0(a0_0, epoch_0, sizeClass_0, credit_0) {
    return this._transientHash_0([1n, a0_0, epoch_0, sizeClass_0, credit_0]);
  }
  _rlnX_0(eid_0) {
    return this._transientHash_1([3n, this._degradeToTransient_0(eid_0)]);
  }
  _pathBit_0(acc_0, e_0, w_0) {
    return ((t1) => {
             if (t1 > 18446744073709551615n) {
               throw new __compactRuntime.CompactError('registry.compact line 209 char 10: cast from Field or Uint value to smaller Uint value failed: ' + t1 + ' is greater than 18446744073709551615');
             }
             return t1;
           })(e_0.goes_left ? acc_0 : acc_0 + w_0);
  }
  _pathIndex_0(path_0) {
    return this._folder_1((...args_0) => this._pathBit_0(...args_0),
                          0n,
                          path_0.path,
                          [1n,
                           2n,
                           4n,
                           8n,
                           16n,
                           32n,
                           64n,
                           128n,
                           256n,
                           512n,
                           1024n,
                           2048n,
                           4096n,
                           8192n,
                           16384n,
                           32768n,
                           65536n,
                           131072n,
                           262144n,
                           524288n]);
  }
  _be64_0(x_0) {
    const b_0 = __compactRuntime.convertBigintToBytes(8,
                                                      x_0,
                                                      'registry.compact line 220 char 13');
    return Uint8Array.from([BigInt(b_0[7n]),
                            BigInt(b_0[6n]),
                            BigInt(b_0[5n]),
                            BigInt(b_0[4n]),
                            BigInt(b_0[3n]),
                            BigInt(b_0[2n]),
                            BigInt(b_0[1n]),
                            BigInt(b_0[0n])],
                           Number);
  }
  _be32_0(x_0) {
    const b_0 = __compactRuntime.convertBigintToBytes(4,
                                                      x_0,
                                                      'registry.compact line 225 char 13');
    return Uint8Array.from([BigInt(b_0[3n]),
                            BigInt(b_0[2n]),
                            BigInt(b_0[1n]),
                            BigInt(b_0[0n])],
                           Number);
  }
  _be16_0(x_0) {
    const b_0 = __compactRuntime.convertBigintToBytes(2,
                                                      x_0,
                                                      'registry.compact line 230 char 13');
    return Uint8Array.from([BigInt(b_0[1n]), BigInt(b_0[0n])], Number);
  }
  _anchorPayload_0(window_0, root_0, c_0) {
    return Uint8Array.from([...Array.from(this._be64_0(window_0), BigInt),
                            ...Array.from(root_0, BigInt),
                            ...Array.from(this._be32_0(c_0[0]), BigInt),
                            ...Array.from(this._be32_0(c_0[1]), BigInt),
                            ...Array.from(this._be32_0(c_0[2]), BigInt),
                            ...Array.from(this._be32_0(c_0[3]), BigInt),
                            ...Array.from(this._be32_0(c_0[4]), BigInt),
                            ...Array.from(this._be32_0(c_0[5]), BigInt),
                            ...Array.from(this._be32_0(c_0[6]), BigInt),
                            ...Array.from(this._be32_0(c_0[7]), BigInt),
                            ...Array.from(new Uint8Array(184), BigInt)],
                           Number);
  }
  _govPayload_0(action_0, reason_0, subject_0) {
    return Uint8Array.from([action_0,
                            ...Array.from(this._be16_0(reason_0), BigInt),
                            ...Array.from(subject_0, BigInt),
                            ...Array.from(new Uint8Array(221), BigInt)],
                           Number);
  }
  async _emitGov_0(context, partialProofData, action_0, reason_0, subject_0) {
    let t_0;
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newArray()
                                                          .arrayPush(__compactRuntime.StateValue.newCell({ value: _descriptor_6.toValue(1n),
                                                                                                           alignment: _descriptor_6.alignment() })).arrayPush(__compactRuntime.StateValue.newCell({ value: _descriptor_9.toValue(10n),
                                                                                                                                                                                                    alignment: _descriptor_9.alignment() })).arrayPush(__compactRuntime.StateValue.newCell({ value: _descriptor_14.toValue((t_0 = { name:
                                                                                                                                                                                                                                                                                                                                      this._govName_0(),
                                                                                                                                                                                                                                                                                                                                    payload:
                                                                                                                                                                                                                                                                                                                                      this._govPayload_0(action_0,
                                                                                                                                                                                                                                                                                                                                                         reason_0,
                                                                                                                                                                                                                                                                                                                                                         subject_0) },
                                                                                                                                                                                                                                                                                                                            Uint8Array.from([...Array.from(t_0.name,
                                                                                                                                                                                                                                                                                                                                                           BigInt),
                                                                                                                                                                                                                                                                                                                                             ...Array.from(t_0.payload,
                                                                                                                                                                                                                                                                                                                                                           BigInt)],
                                                                                                                                                                                                                                                                                                                                            Number))),
                                                                                                                                                                                                                                                                                             alignment: _descriptor_14.alignment() }))
                                                          .encode() } },
                                       'log']);
    return [];
  }
  async _assertSteward_0(context, partialProofData) {
    __compactRuntime.assert(this._equal_0(_descriptor_0.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                                    partialProofData,
                                                                                                    [
                                                                                                     { dup: { n: 0 } },
                                                                                                     { idx: { cached: false,
                                                                                                              pushPath: false,
                                                                                                              path: [
                                                                                                                     { tag: 'value',
                                                                                                                       value: { value: _descriptor_9.toValue(2n),
                                                                                                                                alignment: _descriptor_9.alignment() } }] } },
                                                                                                     { popeq: { cached: false,
                                                                                                                result: undefined } }]).value),
                                          this._stewardKeyOf_0(this._stewardSecret_0(context,
                                                                                     partialProofData))),
                            'not the steward');
    return [];
  }
  async _assertClock_0(context, partialProofData, t_0) {
    __compactRuntime.assert(await this._blockTimeGte_0(context,
                                                       partialProofData,
                                                       t_0),
                            'clock ahead of block time');
    __compactRuntime.assert(await this._blockTimeLt_0(context,
                                                      partialProofData,
                                                      ((t1) => {
                                                        if (t1 > 18446744073709551615n) {
                                                          throw new __compactRuntime.CompactError('registry.compact line 261 char 22: cast from Field or Uint value to smaller Uint value failed: ' + t1 + ' is greater than 18446744073709551615');
                                                        }
                                                        return t1;
                                                      })(t_0
                                                         +
                                                         this._clockTolerance_0())),
                            'clock behind block time');
    return [];
  }
  _countOk_0(acc_0, c_0, i_0, shards_0) {
    return acc_0 && (i_0 < shards_0 || c_0 === 0n);
  }
  _countAny_0(acc_0, c_0) { return acc_0 || c_0 !== 0n; }
  async _register_0(context, partialProofData, idc_0, period_0) {
    __compactRuntime.assert(!_descriptor_3.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                       partialProofData,
                                                                                       [
                                                                                        { dup: { n: 0 } },
                                                                                        { idx: { cached: false,
                                                                                                 pushPath: false,
                                                                                                 path: [
                                                                                                        { tag: 'value',
                                                                                                          value: { value: _descriptor_9.toValue(3n),
                                                                                                                   alignment: _descriptor_9.alignment() } }] } },
                                                                                        { popeq: { cached: false,
                                                                                                   result: undefined } }]).value),
                            'bus paused');
    const p_0 = period_0;
    const len_0 = _descriptor_11.fromValue(__compactRuntime.queryLedgerState(context,
                                                                             partialProofData,
                                                                             [
                                                                              { dup: { n: 0 } },
                                                                              { idx: { cached: false,
                                                                                       pushPath: false,
                                                                                       path: [
                                                                                              { tag: 'value',
                                                                                                value: { value: _descriptor_9.toValue(4n),
                                                                                                         alignment: _descriptor_9.alignment() } }] } },
                                                                              { popeq: { cached: false,
                                                                                         result: undefined } }]).value).membershipPeriod;
    __compactRuntime.assert(await this._blockTimeGte_0(context,
                                                       partialProofData,
                                                       p_0 * len_0),
                            'period not started');
    __compactRuntime.assert(await this._blockTimeLt_0(context,
                                                      partialProofData,
                                                      (p_0 + 1n) * len_0),
                            'period ended');
    const id_0 = idc_0;
    __compactRuntime.assert(!_descriptor_3.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                       partialProofData,
                                                                                       [
                                                                                        { dup: { n: 0 } },
                                                                                        { idx: { cached: false,
                                                                                                 pushPath: false,
                                                                                                 path: [
                                                                                                        { tag: 'value',
                                                                                                          value: { value: _descriptor_9.toValue(7n),
                                                                                                                   alignment: _descriptor_9.alignment() } }] } },
                                                                                        { push: { storage: false,
                                                                                                  value: __compactRuntime.StateValue.newCell({ value: _descriptor_0.toValue(id_0),
                                                                                                                                               alignment: _descriptor_0.alignment() }).encode() } },
                                                                                        'member',
                                                                                        { popeq: { cached: true,
                                                                                                   result: undefined } }]).value),
                            'commitment revoked');
    if (!_descriptor_3.fromValue(__compactRuntime.queryLedgerState(context,
                                                                   partialProofData,
                                                                   [
                                                                    { dup: { n: 0 } },
                                                                    { idx: { cached: false,
                                                                             pushPath: false,
                                                                             path: [
                                                                                    { tag: 'value',
                                                                                      value: { value: _descriptor_9.toValue(6n),
                                                                                               alignment: _descriptor_9.alignment() } }] } },
                                                                    { push: { storage: false,
                                                                              value: __compactRuntime.StateValue.newCell({ value: _descriptor_6.toValue(p_0),
                                                                                                                           alignment: _descriptor_6.alignment() }).encode() } },
                                                                    'member',
                                                                    { popeq: { cached: true,
                                                                               result: undefined } }]).value))
    {
      __compactRuntime.queryLedgerState(context,
                                        partialProofData,
                                        [
                                         { idx: { cached: false,
                                                  pushPath: true,
                                                  path: [
                                                         { tag: 'value',
                                                           value: { value: _descriptor_9.toValue(6n),
                                                                    alignment: _descriptor_9.alignment() } }] } },
                                         { push: { storage: false,
                                                   value: __compactRuntime.StateValue.newCell({ value: _descriptor_6.toValue(p_0),
                                                                                                alignment: _descriptor_6.alignment() }).encode() } },
                                         { push: { storage: true,
                                                   value: __compactRuntime.StateValue.newArray()
                                                            .arrayPush(__compactRuntime.StateValue.newBoundedMerkleTree(
                                                                         new __compactRuntime.StateBoundedMerkleTree(20)
                                                                       )).arrayPush(__compactRuntime.StateValue.newCell({ value: _descriptor_10.toValue(0n),
                                                                                                                          alignment: _descriptor_10.alignment() })).arrayPush(__compactRuntime.StateValue.newMap(
                                                                                                                                                                                new __compactRuntime.StateMap()
                                                                                                                                                                              ))
                                                            .encode() } },
                                         { ins: { cached: false, n: 1 } },
                                         { ins: { cached: true, n: 1 } }]);
    }
    __compactRuntime.assert(!_descriptor_3.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                       partialProofData,
                                                                                       [
                                                                                        { dup: { n: 0 } },
                                                                                        { idx: { cached: false,
                                                                                                 pushPath: false,
                                                                                                 path: [
                                                                                                        { tag: 'value',
                                                                                                          value: { value: _descriptor_9.toValue(6n),
                                                                                                                   alignment: _descriptor_9.alignment() } },
                                                                                                        { tag: 'value',
                                                                                                          value: { value: _descriptor_6.toValue(p_0),
                                                                                                                   alignment: _descriptor_6.alignment() } }] } },
                                                                                        { idx: { cached: false,
                                                                                                 pushPath: false,
                                                                                                 path: [
                                                                                                        { tag: 'value',
                                                                                                          value: { value: _descriptor_9.toValue(1n),
                                                                                                                   alignment: _descriptor_9.alignment() } }] } },
                                                                                        { push: { storage: false,
                                                                                                  value: __compactRuntime.StateValue.newCell({ value: _descriptor_10.toValue(1048576n),
                                                                                                                                               alignment: _descriptor_10.alignment() }).encode() } },
                                                                                        'lt',
                                                                                        'neg',
                                                                                        { popeq: { cached: true,
                                                                                                   result: undefined } }]).value),
                            'membership tree full');
    const tmp_0 = this._memberLeafOf_0(id_0,
                                       _descriptor_11.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                                  partialProofData,
                                                                                                  [
                                                                                                   { dup: { n: 0 } },
                                                                                                   { idx: { cached: false,
                                                                                                            pushPath: false,
                                                                                                            path: [
                                                                                                                   { tag: 'value',
                                                                                                                     value: { value: _descriptor_9.toValue(4n),
                                                                                                                              alignment: _descriptor_9.alignment() } }] } },
                                                                                                   { popeq: { cached: false,
                                                                                                              result: undefined } }]).value).quota);
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { idx: { cached: false,
                                                pushPath: true,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(6n),
                                                                  alignment: _descriptor_9.alignment() } },
                                                       { tag: 'value',
                                                         value: { value: _descriptor_6.toValue(p_0),
                                                                  alignment: _descriptor_6.alignment() } }] } },
                                       { idx: { cached: false,
                                                pushPath: true,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(0n),
                                                                  alignment: _descriptor_9.alignment() } }] } },
                                       { dup: { n: 2 } },
                                       { idx: { cached: false,
                                                pushPath: false,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(1n),
                                                                  alignment: _descriptor_9.alignment() } }] } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newCell(__compactRuntime.leafHash(
                                                                                              { value: _descriptor_0.toValue(tmp_0),
                                                                                                alignment: _descriptor_0.alignment() }
                                                                                            )).encode() } },
                                       { ins: { cached: false, n: 1 } },
                                       { ins: { cached: true, n: 1 } },
                                       { idx: { cached: false,
                                                pushPath: true,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(1n),
                                                                  alignment: _descriptor_9.alignment() } }] } },
                                       { addi: { immediate: 1 } },
                                       { ins: { cached: true, n: 1 } },
                                       { idx: { cached: false,
                                                pushPath: true,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(2n),
                                                                  alignment: _descriptor_9.alignment() } }] } },
                                       { dup: { n: 2 } },
                                       { idx: { cached: false,
                                                pushPath: false,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(0n),
                                                                  alignment: _descriptor_9.alignment() } }] } },
                                       'root',
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newNull().encode() } },
                                       { ins: { cached: false, n: 1 } },
                                       { ins: { cached: true, n: 3 } }]);
    return [];
  }
  async _revoke_0(context, partialProofData, period_0, reason_0) {
    const ev_0 = this._revocationEvidence_0(context, partialProofData);
    const path_0 = this._memberPath_0(context, partialProofData);
    __compactRuntime.assert(!this._equal_1(ev_0.s1.eid, ev_0.s2.eid),
                            'evidence needs two Envelope Identifiers');
    const a1_0 = this._rlnA1_0(ev_0.a0, ev_0.epoch, ev_0.sizeClass, ev_0.credit);
    const x1_0 = this._rlnX_0(ev_0.s1.eid);
    const x2_0 = this._rlnX_0(ev_0.s2.eid);
    __compactRuntime.assert(ev_0.s1.y
                            ===
                            __compactRuntime.addField(ev_0.a0,
                                                      __compactRuntime.mulField(a1_0,
                                                                                x1_0)),
                            'share 1 not on the member line');
    __compactRuntime.assert(ev_0.s2.y
                            ===
                            __compactRuntime.addField(ev_0.a0,
                                                      __compactRuntime.mulField(a1_0,
                                                                                x2_0)),
                            'share 2 not on the member line');
    let t_0;
    __compactRuntime.assert((t_0 = ev_0.sizeClass, t_0 < 4n), 'bad size class');
    const idc_0 = this._idcOf_0(ev_0.a0);
    __compactRuntime.assert(this._equal_2(path_0.leaf,
                                          this._memberLeafOf_0(idc_0, ev_0.quota)),
                            'path is not for this member');
    const p_0 = period_0;
    __compactRuntime.assert(_descriptor_3.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                      partialProofData,
                                                                                      [
                                                                                       { dup: { n: 0 } },
                                                                                       { idx: { cached: false,
                                                                                                pushPath: false,
                                                                                                path: [
                                                                                                       { tag: 'value',
                                                                                                         value: { value: _descriptor_9.toValue(6n),
                                                                                                                  alignment: _descriptor_9.alignment() } }] } },
                                                                                       { push: { storage: false,
                                                                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_6.toValue(p_0),
                                                                                                                                              alignment: _descriptor_6.alignment() }).encode() } },
                                                                                       'member',
                                                                                       { popeq: { cached: true,
                                                                                                  result: undefined } }]).value),
                            'no such period');
    let tmp_0;
    __compactRuntime.assert((tmp_0 = this._merkleTreePathRoot_0(path_0),
                             _descriptor_3.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                       partialProofData,
                                                                                       [
                                                                                        { dup: { n: 0 } },
                                                                                        { idx: { cached: false,
                                                                                                 pushPath: false,
                                                                                                 path: [
                                                                                                        { tag: 'value',
                                                                                                          value: { value: _descriptor_9.toValue(6n),
                                                                                                                   alignment: _descriptor_9.alignment() } },
                                                                                                        { tag: 'value',
                                                                                                          value: { value: _descriptor_6.toValue(p_0),
                                                                                                                   alignment: _descriptor_6.alignment() } }] } },
                                                                                        { idx: { cached: false,
                                                                                                 pushPath: false,
                                                                                                 path: [
                                                                                                        { tag: 'value',
                                                                                                          value: { value: _descriptor_9.toValue(2n),
                                                                                                                   alignment: _descriptor_9.alignment() } }] } },
                                                                                        { push: { storage: false,
                                                                                                  value: __compactRuntime.StateValue.newCell({ value: _descriptor_2.toValue(tmp_0),
                                                                                                                                               alignment: _descriptor_2.alignment() }).encode() } },
                                                                                        'member',
                                                                                        { popeq: { cached: true,
                                                                                                   result: undefined } }]).value)),
                            'unknown root');
    const tmp_1 = this._pathIndex_0(path_0);
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { idx: { cached: false,
                                                pushPath: true,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(6n),
                                                                  alignment: _descriptor_9.alignment() } },
                                                       { tag: 'value',
                                                         value: { value: _descriptor_6.toValue(p_0),
                                                                  alignment: _descriptor_6.alignment() } }] } },
                                       { idx: { cached: false,
                                                pushPath: true,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(0n),
                                                                  alignment: _descriptor_9.alignment() } }] } },
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_10.toValue(tmp_1),
                                                                                              alignment: _descriptor_10.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newCell(__compactRuntime.leafHash(
                                                                                              { value: _descriptor_0.toValue(new Uint8Array(32)),
                                                                                                alignment: _descriptor_0.alignment() }
                                                                                            )).encode() } },
                                       { ins: { cached: false, n: 2 } },
                                       { idx: { cached: false,
                                                pushPath: true,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(1n),
                                                                  alignment: _descriptor_9.alignment() } }] } },
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_10.toValue(tmp_1),
                                                                                              alignment: _descriptor_10.alignment() }).encode() } },
                                       { addi: { immediate: 1 } },
                                       { dup: { n: 1 } },
                                       { dup: { n: 1 } },
                                       'lt',
                                       { branch: { skip: 2 } },
                                       'pop',
                                       { jmp: { skip: 2 } },
                                       { swap: { n: 0 } },
                                       'pop',
                                       { ins: { cached: false, n: 1 } },
                                       { idx: { cached: false,
                                                pushPath: true,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(2n),
                                                                  alignment: _descriptor_9.alignment() } }] } },
                                       { dup: { n: 2 } },
                                       { idx: { cached: false,
                                                pushPath: false,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(0n),
                                                                  alignment: _descriptor_9.alignment() } }] } },
                                       'root',
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newNull().encode() } },
                                       { ins: { cached: false, n: 1 } },
                                       { ins: { cached: true, n: 3 } }]);
    const id_0 = idc_0;
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { idx: { cached: false,
                                                pushPath: true,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(7n),
                                                                  alignment: _descriptor_9.alignment() } }] } },
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_0.toValue(id_0),
                                                                                              alignment: _descriptor_0.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newNull().encode() } },
                                       { ins: { cached: false, n: 1 } },
                                       { ins: { cached: true, n: 1 } }]);
    await this._emitGov_0(context,
                          partialProofData,
                          this._actRevoke_0(),
                          reason_0,
                          id_0);
    return [];
  }
  async _prunePeriod_0(context, partialProofData, period_0) {
    const p_0 = period_0;
    __compactRuntime.assert(_descriptor_3.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                      partialProofData,
                                                                                      [
                                                                                       { dup: { n: 0 } },
                                                                                       { idx: { cached: false,
                                                                                                pushPath: false,
                                                                                                path: [
                                                                                                       { tag: 'value',
                                                                                                         value: { value: _descriptor_9.toValue(6n),
                                                                                                                  alignment: _descriptor_9.alignment() } }] } },
                                                                                       { push: { storage: false,
                                                                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_6.toValue(p_0),
                                                                                                                                              alignment: _descriptor_6.alignment() }).encode() } },
                                                                                       'member',
                                                                                       { popeq: { cached: true,
                                                                                                  result: undefined } }]).value),
                            'no such period');
    __compactRuntime.assert(await this._blockTimeGte_0(context,
                                                       partialProofData,
                                                       (p_0 + 1n)
                                                       *
                                                       _descriptor_11.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                                                  partialProofData,
                                                                                                                  [
                                                                                                                   { dup: { n: 0 } },
                                                                                                                   { idx: { cached: false,
                                                                                                                            pushPath: false,
                                                                                                                            path: [
                                                                                                                                   { tag: 'value',
                                                                                                                                     value: { value: _descriptor_9.toValue(4n),
                                                                                                                                              alignment: _descriptor_9.alignment() } }] } },
                                                                                                                   { popeq: { cached: false,
                                                                                                                              result: undefined } }]).value).membershipPeriod
                                                       +
                                                       _descriptor_11.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                                                  partialProofData,
                                                                                                                  [
                                                                                                                   { dup: { n: 0 } },
                                                                                                                   { idx: { cached: false,
                                                                                                                            pushPath: false,
                                                                                                                            path: [
                                                                                                                                   { tag: 'value',
                                                                                                                                     value: { value: _descriptor_9.toValue(4n),
                                                                                                                                              alignment: _descriptor_9.alignment() } }] } },
                                                                                                                   { popeq: { cached: false,
                                                                                                                              result: undefined } }]).value).rootWindow),
                            'period still eligible');
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { idx: { cached: false,
                                                pushPath: true,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(6n),
                                                                  alignment: _descriptor_9.alignment() } }] } },
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_6.toValue(p_0),
                                                                                              alignment: _descriptor_6.alignment() }).encode() } },
                                       { rem: { cached: false } },
                                       { ins: { cached: true, n: 1 } }]);
    return [];
  }
  async _addRelay_0(context, partialProofData, peer_0, entry_0, reason_0) {
    await this._assertSteward_0(context, partialProofData);
    const k_0 = peer_0;
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { idx: { cached: false,
                                                pushPath: true,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(8n),
                                                                  alignment: _descriptor_9.alignment() } }] } },
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_0.toValue(k_0),
                                                                                              alignment: _descriptor_0.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_5.toValue(entry_0),
                                                                                              alignment: _descriptor_5.alignment() }).encode() } },
                                       { ins: { cached: false, n: 1 } },
                                       { ins: { cached: true, n: 1 } }]);
    await this._emitGov_0(context,
                          partialProofData,
                          this._actRelayAdd_0(),
                          reason_0,
                          k_0);
    return [];
  }
  async _removeRelay_0(context, partialProofData, peer_0, reason_0) {
    await this._assertSteward_0(context, partialProofData);
    const k_0 = peer_0;
    __compactRuntime.assert(_descriptor_3.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                      partialProofData,
                                                                                      [
                                                                                       { dup: { n: 0 } },
                                                                                       { idx: { cached: false,
                                                                                                pushPath: false,
                                                                                                path: [
                                                                                                       { tag: 'value',
                                                                                                         value: { value: _descriptor_9.toValue(8n),
                                                                                                                  alignment: _descriptor_9.alignment() } }] } },
                                                                                       { push: { storage: false,
                                                                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_0.toValue(k_0),
                                                                                                                                              alignment: _descriptor_0.alignment() }).encode() } },
                                                                                       'member',
                                                                                       { popeq: { cached: true,
                                                                                                  result: undefined } }]).value),
                            'no such relay');
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { idx: { cached: false,
                                                pushPath: true,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(8n),
                                                                  alignment: _descriptor_9.alignment() } }] } },
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_0.toValue(k_0),
                                                                                              alignment: _descriptor_0.alignment() }).encode() } },
                                       { rem: { cached: false } },
                                       { ins: { cached: true, n: 1 } }]);
    await this._emitGov_0(context,
                          partialProofData,
                          this._actRelayRemove_0(),
                          reason_0,
                          k_0);
    return [];
  }
  async _proposeParams_0(context, partialProofData, p_0, now_0, reason_0) {
    await this._assertSteward_0(context, partialProofData);
    const t_0 = now_0;
    await this._assertClock_0(context, partialProofData, t_0);
    const tmp_0 = this._some_0({ params: p_0,
                                 effectiveAt:
                                   ((t1) => {
                                     if (t1 > 18446744073709551615n) {
                                       throw new __compactRuntime.CompactError('registry.compact line 357 char 83: cast from Field or Uint value to smaller Uint value failed: ' + t1 + ' is greater than 18446744073709551615');
                                     }
                                     return t1;
                                   })(t_0
                                      +
                                      _descriptor_6.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                                partialProofData,
                                                                                                [
                                                                                                 { dup: { n: 0 } },
                                                                                                 { idx: { cached: false,
                                                                                                          pushPath: false,
                                                                                                          path: [
                                                                                                                 { tag: 'value',
                                                                                                                   value: { value: _descriptor_9.toValue(1n),
                                                                                                                            alignment: _descriptor_9.alignment() } }] } },
                                                                                                 { popeq: { cached: false,
                                                                                                            result: undefined } }]).value)) });
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_9.toValue(5n),
                                                                                              alignment: _descriptor_9.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_16.toValue(tmp_0),
                                                                                              alignment: _descriptor_16.alignment() }).encode() } },
                                       { ins: { cached: false, n: 1 } }]);
    await this._emitGov_0(context,
                          partialProofData,
                          this._actParams_0(),
                          reason_0,
                          new Uint8Array(32));
    return [];
  }
  async _activateParams_0(context, partialProofData) {
    __compactRuntime.assert(_descriptor_16.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                       partialProofData,
                                                                                       [
                                                                                        { dup: { n: 0 } },
                                                                                        { idx: { cached: false,
                                                                                                 pushPath: false,
                                                                                                 path: [
                                                                                                        { tag: 'value',
                                                                                                          value: { value: _descriptor_9.toValue(5n),
                                                                                                                   alignment: _descriptor_9.alignment() } }] } },
                                                                                        { popeq: { cached: false,
                                                                                                   result: undefined } }]).value).is_some,
                            'nothing pending');
    __compactRuntime.assert(await this._blockTimeGte_0(context,
                                                       partialProofData,
                                                       _descriptor_16.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                                                  partialProofData,
                                                                                                                  [
                                                                                                                   { dup: { n: 0 } },
                                                                                                                   { idx: { cached: false,
                                                                                                                            pushPath: false,
                                                                                                                            path: [
                                                                                                                                   { tag: 'value',
                                                                                                                                     value: { value: _descriptor_9.toValue(5n),
                                                                                                                                              alignment: _descriptor_9.alignment() } }] } },
                                                                                                                   { popeq: { cached: false,
                                                                                                                              result: undefined } }]).value).value.effectiveAt),
                            'time-lock running');
    const tmp_0 = _descriptor_16.fromValue(__compactRuntime.queryLedgerState(context,
                                                                             partialProofData,
                                                                             [
                                                                              { dup: { n: 0 } },
                                                                              { idx: { cached: false,
                                                                                       pushPath: false,
                                                                                       path: [
                                                                                              { tag: 'value',
                                                                                                value: { value: _descriptor_9.toValue(5n),
                                                                                                         alignment: _descriptor_9.alignment() } }] } },
                                                                              { popeq: { cached: false,
                                                                                         result: undefined } }]).value).value.params;
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_9.toValue(4n),
                                                                                              alignment: _descriptor_9.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_11.toValue(tmp_0),
                                                                                              alignment: _descriptor_11.alignment() }).encode() } },
                                       { ins: { cached: false, n: 1 } }]);
    const tmp_1 = this._none_0();
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_9.toValue(5n),
                                                                                              alignment: _descriptor_9.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_16.toValue(tmp_1),
                                                                                              alignment: _descriptor_16.alignment() }).encode() } },
                                       { ins: { cached: false, n: 1 } }]);
    await this._emitGov_0(context,
                          partialProofData,
                          this._actParamsActive_0(),
                          0n,
                          new Uint8Array(32));
    return [];
  }
  async _pause_0(context, partialProofData, reason_0) {
    await this._assertSteward_0(context, partialProofData);
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_9.toValue(3n),
                                                                                              alignment: _descriptor_9.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_3.toValue(true),
                                                                                              alignment: _descriptor_3.alignment() }).encode() } },
                                       { ins: { cached: false, n: 1 } }]);
    await this._emitGov_0(context,
                          partialProofData,
                          this._actPause_0(),
                          reason_0,
                          new Uint8Array(32));
    return [];
  }
  async _unpause_0(context, partialProofData, reason_0) {
    await this._assertSteward_0(context, partialProofData);
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_9.toValue(3n),
                                                                                              alignment: _descriptor_9.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_3.toValue(false),
                                                                                              alignment: _descriptor_3.alignment() }).encode() } },
                                       { ins: { cached: false, n: 1 } }]);
    await this._emitGov_0(context,
                          partialProofData,
                          this._actUnpause_0(),
                          reason_0,
                          new Uint8Array(32));
    return [];
  }
  async _setSteward_0(context, partialProofData, newKey_0, reason_0) {
    await this._assertSteward_0(context, partialProofData);
    const k_0 = newKey_0;
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_9.toValue(2n),
                                                                                              alignment: _descriptor_9.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_0.toValue(k_0),
                                                                                              alignment: _descriptor_0.alignment() }).encode() } },
                                       { ins: { cached: false, n: 1 } }]);
    await this._emitGov_0(context,
                          partialProofData,
                          this._actSteward_0(),
                          reason_0,
                          k_0);
    return [];
  }
  async _postAnchor_0(context,
                      partialProofData,
                      peer_0,
                      window_0,
                      q_0,
                      slot_0,
                      root_0,
                      counts_0)
  {
    __compactRuntime.assert(!_descriptor_3.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                       partialProofData,
                                                                                       [
                                                                                        { dup: { n: 0 } },
                                                                                        { idx: { cached: false,
                                                                                                 pushPath: false,
                                                                                                 path: [
                                                                                                        { tag: 'value',
                                                                                                          value: { value: _descriptor_9.toValue(3n),
                                                                                                                   alignment: _descriptor_9.alignment() } }] } },
                                                                                        { popeq: { cached: false,
                                                                                                   result: undefined } }]).value),
                            'bus paused');
    const k_0 = peer_0;
    __compactRuntime.assert(_descriptor_3.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                      partialProofData,
                                                                                      [
                                                                                       { dup: { n: 0 } },
                                                                                       { idx: { cached: false,
                                                                                                pushPath: false,
                                                                                                path: [
                                                                                                       { tag: 'value',
                                                                                                         value: { value: _descriptor_9.toValue(8n),
                                                                                                                  alignment: _descriptor_9.alignment() } }] } },
                                                                                       { push: { storage: false,
                                                                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_0.toValue(k_0),
                                                                                                                                              alignment: _descriptor_0.alignment() }).encode() } },
                                                                                       'member',
                                                                                       { popeq: { cached: true,
                                                                                                  result: undefined } }]).value),
                            'not a listed relay');
    const e_0 = _descriptor_5.fromValue(__compactRuntime.queryLedgerState(context,
                                                                          partialProofData,
                                                                          [
                                                                           { dup: { n: 0 } },
                                                                           { idx: { cached: false,
                                                                                    pushPath: false,
                                                                                    path: [
                                                                                           { tag: 'value',
                                                                                             value: { value: _descriptor_9.toValue(8n),
                                                                                                      alignment: _descriptor_9.alignment() } }] } },
                                                                           { idx: { cached: false,
                                                                                    pushPath: false,
                                                                                    path: [
                                                                                           { tag: 'value',
                                                                                             value: { value: _descriptor_0.toValue(k_0),
                                                                                                      alignment: _descriptor_0.alignment() } }] } },
                                                                           { popeq: { cached: false,
                                                                                      result: undefined } }]).value);
    __compactRuntime.assert(e_0.roles.anchorer, 'relay lacks the anchorer role');
    __compactRuntime.assert(this._equal_3(e_0.keyCommitment,
                                          this._relayKeyOf_0(this._relaySecret_0(context,
                                                                                 partialProofData))),
                            'not the anchorer key');
    const w_0 = window_0;
    const s_0 = slot_0;
    __compactRuntime.assert(s_0 < this._anchorSlots_0(), 'slot out of range');
    __compactRuntime.assert(q_0 * this._anchorSlots_0() + s_0 === w_0,
                            'slot is not window mod 2940');
    const closeAt_0 = (w_0 + 1n)
                      *
                      _descriptor_11.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                 partialProofData,
                                                                                 [
                                                                                  { dup: { n: 0 } },
                                                                                  { idx: { cached: false,
                                                                                           pushPath: false,
                                                                                           path: [
                                                                                                  { tag: 'value',
                                                                                                    value: { value: _descriptor_9.toValue(4n),
                                                                                                             alignment: _descriptor_9.alignment() } }] } },
                                                                                  { popeq: { cached: false,
                                                                                             result: undefined } }]).value).anchorWindow;
    __compactRuntime.assert(await this._blockTimeGte_0(context,
                                                       partialProofData,
                                                       ((t1) => {
                                                         if (t1 > 18446744073709551615n) {
                                                           throw new __compactRuntime.CompactError('registry.compact line 410 char 23: cast from Field or Uint value to smaller Uint value failed: ' + t1 + ' is greater than 18446744073709551615');
                                                         }
                                                         return t1;
                                                       })(closeAt_0
                                                          +
                                                          this._anchorDelay_0())),
                            'window not closed');
    __compactRuntime.assert(await this._blockTimeLt_0(context,
                                                      partialProofData,
                                                      ((t1) => {
                                                        if (t1 > 18446744073709551615n) {
                                                          throw new __compactRuntime.CompactError('registry.compact line 411 char 22: cast from Field or Uint value to smaller Uint value failed: ' + t1 + ' is greater than 18446744073709551615');
                                                        }
                                                        return t1;
                                                      })(closeAt_0
                                                         +
                                                         _descriptor_11.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                                                    partialProofData,
                                                                                                                    [
                                                                                                                     { dup: { n: 0 } },
                                                                                                                     { idx: { cached: false,
                                                                                                                              pushPath: false,
                                                                                                                              path: [
                                                                                                                                     { tag: 'value',
                                                                                                                                       value: { value: _descriptor_9.toValue(4n),
                                                                                                                                                alignment: _descriptor_9.alignment() } }] } },
                                                                                                                     { popeq: { cached: false,
                                                                                                                                result: undefined } }]).value).anchorHistory)),
                            'window too old');
    const c_0 = counts_0;
    __compactRuntime.assert(this._folder_2((...args_0) =>
                                             this._countAny_0(...args_0),
                                           false,
                                           c_0),
                            'empty window: no Anchor');
    __compactRuntime.assert(this._folder_3((...args_1) =>
                                             this._countOk_0(...args_1),
                                           true,
                                           c_0,
                                           [0n, 1n, 2n, 3n, 4n, 5n, 6n, 7n],
                                           [_descriptor_11.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                                       partialProofData,
                                                                                                       [
                                                                                                        { dup: { n: 0 } },
                                                                                                        { idx: { cached: false,
                                                                                                                 pushPath: false,
                                                                                                                 path: [
                                                                                                                        { tag: 'value',
                                                                                                                          value: { value: _descriptor_9.toValue(4n),
                                                                                                                                   alignment: _descriptor_9.alignment() } }] } },
                                                                                                        { popeq: { cached: false,
                                                                                                                   result: undefined } }]).value).shardCount,
                                            _descriptor_11.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                                       partialProofData,
                                                                                                       [
                                                                                                        { dup: { n: 0 } },
                                                                                                        { idx: { cached: false,
                                                                                                                 pushPath: false,
                                                                                                                 path: [
                                                                                                                        { tag: 'value',
                                                                                                                          value: { value: _descriptor_9.toValue(4n),
                                                                                                                                   alignment: _descriptor_9.alignment() } }] } },
                                                                                                        { popeq: { cached: false,
                                                                                                                   result: undefined } }]).value).shardCount,
                                            _descriptor_11.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                                       partialProofData,
                                                                                                       [
                                                                                                        { dup: { n: 0 } },
                                                                                                        { idx: { cached: false,
                                                                                                                 pushPath: false,
                                                                                                                 path: [
                                                                                                                        { tag: 'value',
                                                                                                                          value: { value: _descriptor_9.toValue(4n),
                                                                                                                                   alignment: _descriptor_9.alignment() } }] } },
                                                                                                        { popeq: { cached: false,
                                                                                                                   result: undefined } }]).value).shardCount,
                                            _descriptor_11.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                                       partialProofData,
                                                                                                       [
                                                                                                        { dup: { n: 0 } },
                                                                                                        { idx: { cached: false,
                                                                                                                 pushPath: false,
                                                                                                                 path: [
                                                                                                                        { tag: 'value',
                                                                                                                          value: { value: _descriptor_9.toValue(4n),
                                                                                                                                   alignment: _descriptor_9.alignment() } }] } },
                                                                                                        { popeq: { cached: false,
                                                                                                                   result: undefined } }]).value).shardCount,
                                            _descriptor_11.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                                       partialProofData,
                                                                                                       [
                                                                                                        { dup: { n: 0 } },
                                                                                                        { idx: { cached: false,
                                                                                                                 pushPath: false,
                                                                                                                 path: [
                                                                                                                        { tag: 'value',
                                                                                                                          value: { value: _descriptor_9.toValue(4n),
                                                                                                                                   alignment: _descriptor_9.alignment() } }] } },
                                                                                                        { popeq: { cached: false,
                                                                                                                   result: undefined } }]).value).shardCount,
                                            _descriptor_11.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                                       partialProofData,
                                                                                                       [
                                                                                                        { dup: { n: 0 } },
                                                                                                        { idx: { cached: false,
                                                                                                                 pushPath: false,
                                                                                                                 path: [
                                                                                                                        { tag: 'value',
                                                                                                                          value: { value: _descriptor_9.toValue(4n),
                                                                                                                                   alignment: _descriptor_9.alignment() } }] } },
                                                                                                        { popeq: { cached: false,
                                                                                                                   result: undefined } }]).value).shardCount,
                                            _descriptor_11.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                                       partialProofData,
                                                                                                       [
                                                                                                        { dup: { n: 0 } },
                                                                                                        { idx: { cached: false,
                                                                                                                 pushPath: false,
                                                                                                                 path: [
                                                                                                                        { tag: 'value',
                                                                                                                          value: { value: _descriptor_9.toValue(4n),
                                                                                                                                   alignment: _descriptor_9.alignment() } }] } },
                                                                                                        { popeq: { cached: false,
                                                                                                                   result: undefined } }]).value).shardCount,
                                            _descriptor_11.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                                       partialProofData,
                                                                                                       [
                                                                                                        { dup: { n: 0 } },
                                                                                                        { idx: { cached: false,
                                                                                                                 pushPath: false,
                                                                                                                 path: [
                                                                                                                        { tag: 'value',
                                                                                                                          value: { value: _descriptor_9.toValue(4n),
                                                                                                                                   alignment: _descriptor_9.alignment() } }] } },
                                                                                                        { popeq: { cached: false,
                                                                                                                   result: undefined } }]).value).shardCount]),
                            'count for an inactive Shard');
    if (_descriptor_3.fromValue(__compactRuntime.queryLedgerState(context,
                                                                  partialProofData,
                                                                  [
                                                                   { dup: { n: 0 } },
                                                                   { idx: { cached: false,
                                                                            pushPath: false,
                                                                            path: [
                                                                                   { tag: 'value',
                                                                                     value: { value: _descriptor_9.toValue(9n),
                                                                                              alignment: _descriptor_9.alignment() } }] } },
                                                                   { push: { storage: false,
                                                                             value: __compactRuntime.StateValue.newCell({ value: _descriptor_7.toValue(s_0),
                                                                                                                          alignment: _descriptor_7.alignment() }).encode() } },
                                                                   'member',
                                                                   { popeq: { cached: true,
                                                                              result: undefined } }]).value))
    {
      let t_0;
      __compactRuntime.assert((t_0 = _descriptor_13.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                                partialProofData,
                                                                                                [
                                                                                                 { dup: { n: 0 } },
                                                                                                 { idx: { cached: false,
                                                                                                          pushPath: false,
                                                                                                          path: [
                                                                                                                 { tag: 'value',
                                                                                                                   value: { value: _descriptor_9.toValue(9n),
                                                                                                                            alignment: _descriptor_9.alignment() } }] } },
                                                                                                 { idx: { cached: false,
                                                                                                          pushPath: false,
                                                                                                          path: [
                                                                                                                 { tag: 'value',
                                                                                                                   value: { value: _descriptor_7.toValue(s_0),
                                                                                                                            alignment: _descriptor_7.alignment() } }] } },
                                                                                                 { popeq: { cached: false,
                                                                                                            result: undefined } }]).value).window,
                               t_0 < w_0),
                              'window already anchored');
    }
    const r_0 = root_0;
    const tmp_0 = { window: w_0, root: r_0, counts: c_0 };
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { idx: { cached: false,
                                                pushPath: true,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(9n),
                                                                  alignment: _descriptor_9.alignment() } }] } },
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_7.toValue(s_0),
                                                                                              alignment: _descriptor_7.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_13.toValue(tmp_0),
                                                                                              alignment: _descriptor_13.alignment() }).encode() } },
                                       { ins: { cached: false, n: 1 } },
                                       { ins: { cached: true, n: 1 } }]);
    const tmp_1 = this._anchorLeafOf_0(w_0, r_0);
    const tmp_2 = s_0;
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { idx: { cached: false,
                                                pushPath: true,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(10n),
                                                                  alignment: _descriptor_9.alignment() } }] } },
                                       { idx: { cached: false,
                                                pushPath: true,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(0n),
                                                                  alignment: _descriptor_9.alignment() } }] } },
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_10.toValue(tmp_2),
                                                                                              alignment: _descriptor_10.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newCell(__compactRuntime.leafHash(
                                                                                              { value: _descriptor_0.toValue(tmp_1),
                                                                                                alignment: _descriptor_0.alignment() }
                                                                                            )).encode() } },
                                       { ins: { cached: false, n: 2 } },
                                       { idx: { cached: false,
                                                pushPath: true,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(1n),
                                                                  alignment: _descriptor_9.alignment() } }] } },
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_10.toValue(tmp_2),
                                                                                              alignment: _descriptor_10.alignment() }).encode() } },
                                       { addi: { immediate: 1 } },
                                       { dup: { n: 1 } },
                                       { dup: { n: 1 } },
                                       'lt',
                                       { branch: { skip: 2 } },
                                       'pop',
                                       { jmp: { skip: 2 } },
                                       { swap: { n: 0 } },
                                       'pop',
                                       { ins: { cached: false, n: 1 } },
                                       { idx: { cached: false,
                                                pushPath: true,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(2n),
                                                                  alignment: _descriptor_9.alignment() } }] } },
                                       { dup: { n: 2 } },
                                       { idx: { cached: false,
                                                pushPath: false,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(0n),
                                                                  alignment: _descriptor_9.alignment() } }] } },
                                       'root',
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newNull().encode() } },
                                       { ins: { cached: false, n: 1 } },
                                       { ins: { cached: true, n: 2 } }]);
    let t_1;
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newArray()
                                                          .arrayPush(__compactRuntime.StateValue.newCell({ value: _descriptor_6.toValue(1n),
                                                                                                           alignment: _descriptor_6.alignment() })).arrayPush(__compactRuntime.StateValue.newCell({ value: _descriptor_9.toValue(10n),
                                                                                                                                                                                                    alignment: _descriptor_9.alignment() })).arrayPush(__compactRuntime.StateValue.newCell({ value: _descriptor_14.toValue((t_1 = { name:
                                                                                                                                                                                                                                                                                                                                      this._anchorName_0(),
                                                                                                                                                                                                                                                                                                                                    payload:
                                                                                                                                                                                                                                                                                                                                      this._anchorPayload_0(w_0,
                                                                                                                                                                                                                                                                                                                                                            r_0,
                                                                                                                                                                                                                                                                                                                                                            c_0) },
                                                                                                                                                                                                                                                                                                                            Uint8Array.from([...Array.from(t_1.name,
                                                                                                                                                                                                                                                                                                                                                           BigInt),
                                                                                                                                                                                                                                                                                                                                             ...Array.from(t_1.payload,
                                                                                                                                                                                                                                                                                                                                                           BigInt)],
                                                                                                                                                                                                                                                                                                                                            Number))),
                                                                                                                                                                                                                                                                                             alignment: _descriptor_14.alignment() }))
                                                          .encode() } },
                                       'log']);
    return [];
  }
  async _pruneAnchor_0(context, partialProofData, slot_0) {
    const s_0 = slot_0;
    __compactRuntime.assert(_descriptor_3.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                      partialProofData,
                                                                                      [
                                                                                       { dup: { n: 0 } },
                                                                                       { idx: { cached: false,
                                                                                                pushPath: false,
                                                                                                path: [
                                                                                                       { tag: 'value',
                                                                                                         value: { value: _descriptor_9.toValue(9n),
                                                                                                                  alignment: _descriptor_9.alignment() } }] } },
                                                                                       { push: { storage: false,
                                                                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_7.toValue(s_0),
                                                                                                                                              alignment: _descriptor_7.alignment() }).encode() } },
                                                                                       'member',
                                                                                       { popeq: { cached: true,
                                                                                                  result: undefined } }]).value),
                            'empty slot');
    const w_0 = _descriptor_13.fromValue(__compactRuntime.queryLedgerState(context,
                                                                           partialProofData,
                                                                           [
                                                                            { dup: { n: 0 } },
                                                                            { idx: { cached: false,
                                                                                     pushPath: false,
                                                                                     path: [
                                                                                            { tag: 'value',
                                                                                              value: { value: _descriptor_9.toValue(9n),
                                                                                                       alignment: _descriptor_9.alignment() } }] } },
                                                                            { idx: { cached: false,
                                                                                     pushPath: false,
                                                                                     path: [
                                                                                            { tag: 'value',
                                                                                              value: { value: _descriptor_7.toValue(s_0),
                                                                                                       alignment: _descriptor_7.alignment() } }] } },
                                                                            { popeq: { cached: false,
                                                                                       result: undefined } }]).value).window;
    __compactRuntime.assert(await this._blockTimeGte_0(context,
                                                       partialProofData,
                                                       ((t1) => {
                                                         if (t1 > 18446744073709551615n) {
                                                           throw new __compactRuntime.CompactError('registry.compact line 434 char 23: cast from Field or Uint value to smaller Uint value failed: ' + t1 + ' is greater than 18446744073709551615');
                                                         }
                                                         return t1;
                                                       })((w_0 + 1n)
                                                          *
                                                          _descriptor_11.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                                                     partialProofData,
                                                                                                                     [
                                                                                                                      { dup: { n: 0 } },
                                                                                                                      { idx: { cached: false,
                                                                                                                               pushPath: false,
                                                                                                                               path: [
                                                                                                                                      { tag: 'value',
                                                                                                                                        value: { value: _descriptor_9.toValue(4n),
                                                                                                                                                 alignment: _descriptor_9.alignment() } }] } },
                                                                                                                      { popeq: { cached: false,
                                                                                                                                 result: undefined } }]).value).anchorWindow
                                                          +
                                                          _descriptor_11.fromValue(__compactRuntime.queryLedgerState(context,
                                                                                                                     partialProofData,
                                                                                                                     [
                                                                                                                      { dup: { n: 0 } },
                                                                                                                      { idx: { cached: false,
                                                                                                                               pushPath: false,
                                                                                                                               path: [
                                                                                                                                      { tag: 'value',
                                                                                                                                        value: { value: _descriptor_9.toValue(4n),
                                                                                                                                                 alignment: _descriptor_9.alignment() } }] } },
                                                                                                                      { popeq: { cached: false,
                                                                                                                                 result: undefined } }]).value).anchorHistory)),
                            'record still live');
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { idx: { cached: false,
                                                pushPath: true,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(9n),
                                                                  alignment: _descriptor_9.alignment() } }] } },
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_7.toValue(s_0),
                                                                                              alignment: _descriptor_7.alignment() }).encode() } },
                                       { rem: { cached: false } },
                                       { ins: { cached: true, n: 1 } }]);
    const tmp_0 = s_0;
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { idx: { cached: false,
                                                pushPath: true,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(10n),
                                                                  alignment: _descriptor_9.alignment() } }] } },
                                       { idx: { cached: false,
                                                pushPath: true,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(0n),
                                                                  alignment: _descriptor_9.alignment() } }] } },
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_10.toValue(tmp_0),
                                                                                              alignment: _descriptor_10.alignment() }).encode() } },
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newCell(__compactRuntime.leafHash(
                                                                                              { value: _descriptor_0.toValue(new Uint8Array(32)),
                                                                                                alignment: _descriptor_0.alignment() }
                                                                                            )).encode() } },
                                       { ins: { cached: false, n: 2 } },
                                       { idx: { cached: false,
                                                pushPath: true,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(1n),
                                                                  alignment: _descriptor_9.alignment() } }] } },
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newCell({ value: _descriptor_10.toValue(tmp_0),
                                                                                              alignment: _descriptor_10.alignment() }).encode() } },
                                       { addi: { immediate: 1 } },
                                       { dup: { n: 1 } },
                                       { dup: { n: 1 } },
                                       'lt',
                                       { branch: { skip: 2 } },
                                       'pop',
                                       { jmp: { skip: 2 } },
                                       { swap: { n: 0 } },
                                       'pop',
                                       { ins: { cached: false, n: 1 } },
                                       { idx: { cached: false,
                                                pushPath: true,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(2n),
                                                                  alignment: _descriptor_9.alignment() } }] } },
                                       { dup: { n: 2 } },
                                       { idx: { cached: false,
                                                pushPath: false,
                                                path: [
                                                       { tag: 'value',
                                                         value: { value: _descriptor_9.toValue(0n),
                                                                  alignment: _descriptor_9.alignment() } }] } },
                                       'root',
                                       { push: { storage: true,
                                                 value: __compactRuntime.StateValue.newNull().encode() } },
                                       { ins: { cached: false, n: 1 } },
                                       { ins: { cached: true, n: 2 } }]);
    return [];
  }
  async _anchorRootValid_0(context, partialProofData, rt_0) {
    return _descriptor_3.fromValue(__compactRuntime.queryLedgerState(context,
                                                                     partialProofData,
                                                                     [
                                                                      { dup: { n: 0 } },
                                                                      { idx: { cached: false,
                                                                               pushPath: false,
                                                                               path: [
                                                                                      { tag: 'value',
                                                                                        value: { value: _descriptor_9.toValue(10n),
                                                                                                 alignment: _descriptor_9.alignment() } }] } },
                                                                      { idx: { cached: false,
                                                                               pushPath: false,
                                                                               path: [
                                                                                      { tag: 'value',
                                                                                        value: { value: _descriptor_9.toValue(2n),
                                                                                                 alignment: _descriptor_9.alignment() } }] } },
                                                                      { push: { storage: false,
                                                                                value: __compactRuntime.StateValue.newCell({ value: _descriptor_2.toValue(rt_0),
                                                                                                                             alignment: _descriptor_2.alignment() }).encode() } },
                                                                      'member',
                                                                      { popeq: { cached: true,
                                                                                 result: undefined } }]).value);
  }
  _folder_0(f, x, a0) {
    for (let i = 0; i < 20; i++) { x = f(x, a0[i]); }
    return x;
  }
  _folder_1(f, x, a0, a1) {
    for (let i = 0; i < 20; i++) { x = f(x, a0[i], a1[i]); }
    return x;
  }
  _equal_0(x0, y0) {
    if (!x0.every((x, i) => y0[i] === x)) { return false; }
    return true;
  }
  _equal_1(x0, y0) {
    if (!x0.every((x, i) => y0[i] === x)) { return false; }
    return true;
  }
  _equal_2(x0, y0) {
    if (!x0.every((x, i) => y0[i] === x)) { return false; }
    return true;
  }
  _equal_3(x0, y0) {
    if (!x0.every((x, i) => y0[i] === x)) { return false; }
    return true;
  }
  _folder_2(f, x, a0) {
    for (let i = 0; i < 8; i++) { x = f(x, a0[i]); }
    return x;
  }
  _folder_3(f, x, a0, a1, a2) {
    for (let i = 0; i < 8; i++) { x = f(x, a0[i], a1[i], a2[i]); }
    return x;
  }
}
export function ledger(stateOrChargedState) {
  const state = stateOrChargedState instanceof __compactRuntime.StateValue ? stateOrChargedState : stateOrChargedState.state;
  const chargedState = stateOrChargedState instanceof __compactRuntime.StateValue ? new __compactRuntime.ChargedState(stateOrChargedState) : stateOrChargedState;
  const context = {
    callContext: { currentQueryContext: new __compactRuntime.QueryContext(chargedState, __compactRuntime.dummyContractAddress()), currentGasCost: __compactRuntime.emptyRunningCost() },
    costModel: __compactRuntime.CostModel.initialCostModel()
  };
  const partialProofData = {
    input: { value: [], alignment: [] },
    output: undefined,
    publicTranscript: [],
    privateTranscriptOutputs: []
  };
  return {
    get networkId() {
      return _descriptor_0.fromValue(__compactRuntime.queryLedgerState(context,
                                                                       partialProofData,
                                                                       [
                                                                        { dup: { n: 0 } },
                                                                        { idx: { cached: false,
                                                                                 pushPath: false,
                                                                                 path: [
                                                                                        { tag: 'value',
                                                                                          value: { value: _descriptor_9.toValue(0n),
                                                                                                   alignment: _descriptor_9.alignment() } }] } },
                                                                        { popeq: { cached: false,
                                                                                   result: undefined } }]).value);
    },
    get paramsDelay() {
      return _descriptor_6.fromValue(__compactRuntime.queryLedgerState(context,
                                                                       partialProofData,
                                                                       [
                                                                        { dup: { n: 0 } },
                                                                        { idx: { cached: false,
                                                                                 pushPath: false,
                                                                                 path: [
                                                                                        { tag: 'value',
                                                                                          value: { value: _descriptor_9.toValue(1n),
                                                                                                   alignment: _descriptor_9.alignment() } }] } },
                                                                        { popeq: { cached: false,
                                                                                   result: undefined } }]).value);
    },
    get steward() {
      return _descriptor_0.fromValue(__compactRuntime.queryLedgerState(context,
                                                                       partialProofData,
                                                                       [
                                                                        { dup: { n: 0 } },
                                                                        { idx: { cached: false,
                                                                                 pushPath: false,
                                                                                 path: [
                                                                                        { tag: 'value',
                                                                                          value: { value: _descriptor_9.toValue(2n),
                                                                                                   alignment: _descriptor_9.alignment() } }] } },
                                                                        { popeq: { cached: false,
                                                                                   result: undefined } }]).value);
    },
    get paused() {
      return _descriptor_3.fromValue(__compactRuntime.queryLedgerState(context,
                                                                       partialProofData,
                                                                       [
                                                                        { dup: { n: 0 } },
                                                                        { idx: { cached: false,
                                                                                 pushPath: false,
                                                                                 path: [
                                                                                        { tag: 'value',
                                                                                          value: { value: _descriptor_9.toValue(3n),
                                                                                                   alignment: _descriptor_9.alignment() } }] } },
                                                                        { popeq: { cached: false,
                                                                                   result: undefined } }]).value);
    },
    get params() {
      return _descriptor_11.fromValue(__compactRuntime.queryLedgerState(context,
                                                                        partialProofData,
                                                                        [
                                                                         { dup: { n: 0 } },
                                                                         { idx: { cached: false,
                                                                                  pushPath: false,
                                                                                  path: [
                                                                                         { tag: 'value',
                                                                                           value: { value: _descriptor_9.toValue(4n),
                                                                                                    alignment: _descriptor_9.alignment() } }] } },
                                                                         { popeq: { cached: false,
                                                                                    result: undefined } }]).value);
    },
    get pending() {
      return _descriptor_16.fromValue(__compactRuntime.queryLedgerState(context,
                                                                        partialProofData,
                                                                        [
                                                                         { dup: { n: 0 } },
                                                                         { idx: { cached: false,
                                                                                  pushPath: false,
                                                                                  path: [
                                                                                         { tag: 'value',
                                                                                           value: { value: _descriptor_9.toValue(5n),
                                                                                                    alignment: _descriptor_9.alignment() } }] } },
                                                                         { popeq: { cached: false,
                                                                                    result: undefined } }]).value);
    },
    members: {
      isEmpty(...args_0) {
        if (args_0.length !== 0) {
          throw new __compactRuntime.CompactError(`isEmpty: expected 0 arguments, received ${args_0.length}`);
        }
        return _descriptor_3.fromValue(__compactRuntime.queryLedgerState(context,
                                                                         partialProofData,
                                                                         [
                                                                          { dup: { n: 0 } },
                                                                          { idx: { cached: false,
                                                                                   pushPath: false,
                                                                                   path: [
                                                                                          { tag: 'value',
                                                                                            value: { value: _descriptor_9.toValue(6n),
                                                                                                     alignment: _descriptor_9.alignment() } }] } },
                                                                          'size',
                                                                          { push: { storage: false,
                                                                                    value: __compactRuntime.StateValue.newCell({ value: _descriptor_10.toValue(0n),
                                                                                                                                 alignment: _descriptor_10.alignment() }).encode() } },
                                                                          'eq',
                                                                          { popeq: { cached: true,
                                                                                     result: undefined } }]).value);
      },
      size(...args_0) {
        if (args_0.length !== 0) {
          throw new __compactRuntime.CompactError(`size: expected 0 arguments, received ${args_0.length}`);
        }
        return _descriptor_10.fromValue(__compactRuntime.queryLedgerState(context,
                                                                          partialProofData,
                                                                          [
                                                                           { dup: { n: 0 } },
                                                                           { idx: { cached: false,
                                                                                    pushPath: false,
                                                                                    path: [
                                                                                           { tag: 'value',
                                                                                             value: { value: _descriptor_9.toValue(6n),
                                                                                                      alignment: _descriptor_9.alignment() } }] } },
                                                                           'size',
                                                                           { popeq: { cached: true,
                                                                                      result: undefined } }]).value);
      },
      member(...args_0) {
        if (args_0.length !== 1) {
          throw new __compactRuntime.CompactError(`member: expected 1 argument, received ${args_0.length}`);
        }
        const key_0 = args_0[0];
        if (!(typeof(key_0) === 'bigint' && key_0 >= 0n && key_0 <= 4294967295n)) {
          __compactRuntime.typeError('member',
                                     'argument 1',
                                     'registry.compact line 145 char 1',
                                     'Uint<0..4294967296>',
                                     key_0)
        }
        return _descriptor_3.fromValue(__compactRuntime.queryLedgerState(context,
                                                                         partialProofData,
                                                                         [
                                                                          { dup: { n: 0 } },
                                                                          { idx: { cached: false,
                                                                                   pushPath: false,
                                                                                   path: [
                                                                                          { tag: 'value',
                                                                                            value: { value: _descriptor_9.toValue(6n),
                                                                                                     alignment: _descriptor_9.alignment() } }] } },
                                                                          { push: { storage: false,
                                                                                    value: __compactRuntime.StateValue.newCell({ value: _descriptor_6.toValue(key_0),
                                                                                                                                 alignment: _descriptor_6.alignment() }).encode() } },
                                                                          'member',
                                                                          { popeq: { cached: true,
                                                                                     result: undefined } }]).value);
      },
      lookup(...args_0) {
        if (args_0.length !== 1) {
          throw new __compactRuntime.CompactError(`lookup: expected 1 argument, received ${args_0.length}`);
        }
        const key_0 = args_0[0];
        if (!(typeof(key_0) === 'bigint' && key_0 >= 0n && key_0 <= 4294967295n)) {
          __compactRuntime.typeError('lookup',
                                     'argument 1',
                                     'registry.compact line 145 char 1',
                                     'Uint<0..4294967296>',
                                     key_0)
        }
        if (state.asArray()[6].asMap().get({ value: _descriptor_6.toValue(key_0),
                                             alignment: _descriptor_6.alignment() }) === undefined) {
          throw new __compactRuntime.CompactError(`Map value undefined for ${key_0}`);
        }
        return {
          isFull(...args_1) {
            if (args_1.length !== 0) {
              throw new __compactRuntime.CompactError(`isFull: expected 0 arguments, received ${args_1.length}`);
            }
            return _descriptor_3.fromValue(__compactRuntime.queryLedgerState(context,
                                                                             partialProofData,
                                                                             [
                                                                              { dup: { n: 0 } },
                                                                              { idx: { cached: false,
                                                                                       pushPath: false,
                                                                                       path: [
                                                                                              { tag: 'value',
                                                                                                value: { value: _descriptor_9.toValue(6n),
                                                                                                         alignment: _descriptor_9.alignment() } },
                                                                                              { tag: 'value',
                                                                                                value: { value: _descriptor_6.toValue(key_0),
                                                                                                         alignment: _descriptor_6.alignment() } }] } },
                                                                              { idx: { cached: false,
                                                                                       pushPath: false,
                                                                                       path: [
                                                                                              { tag: 'value',
                                                                                                value: { value: _descriptor_9.toValue(1n),
                                                                                                         alignment: _descriptor_9.alignment() } }] } },
                                                                              { push: { storage: false,
                                                                                        value: __compactRuntime.StateValue.newCell({ value: _descriptor_10.toValue(1048576n),
                                                                                                                                     alignment: _descriptor_10.alignment() }).encode() } },
                                                                              'lt',
                                                                              'neg',
                                                                              { popeq: { cached: true,
                                                                                         result: undefined } }]).value);
          },
          checkRoot(...args_1) {
            if (args_1.length !== 1) {
              throw new __compactRuntime.CompactError(`checkRoot: expected 1 argument, received ${args_1.length}`);
            }
            const rt_0 = args_1[0];
            if (!(typeof(rt_0) === 'object' && typeof(rt_0.field) === 'bigint' && rt_0.field >= 0 && rt_0.field <= __compactRuntime.MAX_FIELD)) {
              __compactRuntime.typeError('checkRoot',
                                         'argument 1',
                                         'registry.compact line 145 char 38',
                                         'struct MerkleTreeDigest<field: Field>',
                                         rt_0)
            }
            return _descriptor_3.fromValue(__compactRuntime.queryLedgerState(context,
                                                                             partialProofData,
                                                                             [
                                                                              { dup: { n: 0 } },
                                                                              { idx: { cached: false,
                                                                                       pushPath: false,
                                                                                       path: [
                                                                                              { tag: 'value',
                                                                                                value: { value: _descriptor_9.toValue(6n),
                                                                                                         alignment: _descriptor_9.alignment() } },
                                                                                              { tag: 'value',
                                                                                                value: { value: _descriptor_6.toValue(key_0),
                                                                                                         alignment: _descriptor_6.alignment() } }] } },
                                                                              { idx: { cached: false,
                                                                                       pushPath: false,
                                                                                       path: [
                                                                                              { tag: 'value',
                                                                                                value: { value: _descriptor_9.toValue(2n),
                                                                                                         alignment: _descriptor_9.alignment() } }] } },
                                                                              { push: { storage: false,
                                                                                        value: __compactRuntime.StateValue.newCell({ value: _descriptor_2.toValue(rt_0),
                                                                                                                                     alignment: _descriptor_2.alignment() }).encode() } },
                                                                              'member',
                                                                              { popeq: { cached: true,
                                                                                         result: undefined } }]).value);
          },
          root(...args_1) {
            if (args_1.length !== 0) {
              throw new __compactRuntime.CompactError(`root: expected 0 arguments, received ${args_1.length}`);
            }
            const self_0 = state.asArray()[6].asMap().get({ value: _descriptor_6.toValue(key_0),
                                                            alignment: _descriptor_6.alignment() });
            return ((result) => result             ? __compactRuntime.CompactTypeMerkleTreeDigest.fromValue(result)             : undefined)(self_0.asArray()[0].asBoundedMerkleTree().rehash().root()?.value);
          },
          firstFree(...args_1) {
            if (args_1.length !== 0) {
              throw new __compactRuntime.CompactError(`first_free: expected 0 arguments, received ${args_1.length}`);
            }
            const self_0 = state.asArray()[6].asMap().get({ value: _descriptor_6.toValue(key_0),
                                                            alignment: _descriptor_6.alignment() });
            return __compactRuntime.CompactTypeField.fromValue(self_0.asArray()[1].asCell().value);
          },
          pathForLeaf(...args_1) {
            if (args_1.length !== 2) {
              throw new __compactRuntime.CompactError(`path_for_leaf: expected 2 arguments, received ${args_1.length}`);
            }
            const index_0 = args_1[0];
            const leaf_0 = args_1[1];
            if (!(typeof(index_0) === 'bigint' && index_0 >= 0 && index_0 <= __compactRuntime.MAX_FIELD)) {
              __compactRuntime.typeError('path_for_leaf',
                                         'argument 1',
                                         'registry.compact line 145 char 38',
                                         'Field',
                                         index_0)
            }
            if (!(leaf_0.buffer instanceof ArrayBuffer && leaf_0.BYTES_PER_ELEMENT === 1 && leaf_0.length === 32)) {
              __compactRuntime.typeError('path_for_leaf',
                                         'argument 2',
                                         'registry.compact line 145 char 38',
                                         'Bytes<32>',
                                         leaf_0)
            }
            const self_0 = state.asArray()[6].asMap().get({ value: _descriptor_6.toValue(key_0),
                                                            alignment: _descriptor_6.alignment() });
            return ((result) => result             ? new __compactRuntime.CompactTypeMerkleTreePath(20, _descriptor_0).fromValue(result)             : undefined)(  self_0.asArray()[0].asBoundedMerkleTree().rehash().pathForLeaf(    index_0,    {      value: _descriptor_0.toValue(leaf_0),      alignment: _descriptor_0.alignment()    }  )?.value);
          },
          findPathForLeaf(...args_1) {
            if (args_1.length !== 1) {
              throw new __compactRuntime.CompactError(`find_path_for_leaf: expected 1 argument, received ${args_1.length}`);
            }
            const leaf_0 = args_1[0];
            if (!(leaf_0.buffer instanceof ArrayBuffer && leaf_0.BYTES_PER_ELEMENT === 1 && leaf_0.length === 32)) {
              __compactRuntime.typeError('find_path_for_leaf',
                                         'argument 1',
                                         'registry.compact line 145 char 38',
                                         'Bytes<32>',
                                         leaf_0)
            }
            const self_0 = state.asArray()[6].asMap().get({ value: _descriptor_6.toValue(key_0),
                                                            alignment: _descriptor_6.alignment() });
            return ((result) => result             ? new __compactRuntime.CompactTypeMerkleTreePath(20, _descriptor_0).fromValue(result)             : undefined)(  self_0.asArray()[0].asBoundedMerkleTree().rehash().findPathForLeaf(    {      value: _descriptor_0.toValue(leaf_0),      alignment: _descriptor_0.alignment()    }  )?.value);
          },
          history(...args_1) {
            if (args_1.length !== 0) {
              throw new __compactRuntime.CompactError(`history: expected 0 arguments, received ${args_1.length}`);
            }
            const self_0 = state.asArray()[6].asMap().get({ value: _descriptor_6.toValue(key_0),
                                                            alignment: _descriptor_6.alignment() });
            return self_0.asArray()[2].asMap().keys().map(  (elem) => __compactRuntime.CompactTypeMerkleTreeDigest.fromValue(elem.value))[Symbol.iterator]();
          }
        }
      }
    },
    revoked: {
      isEmpty(...args_0) {
        if (args_0.length !== 0) {
          throw new __compactRuntime.CompactError(`isEmpty: expected 0 arguments, received ${args_0.length}`);
        }
        return _descriptor_3.fromValue(__compactRuntime.queryLedgerState(context,
                                                                         partialProofData,
                                                                         [
                                                                          { dup: { n: 0 } },
                                                                          { idx: { cached: false,
                                                                                   pushPath: false,
                                                                                   path: [
                                                                                          { tag: 'value',
                                                                                            value: { value: _descriptor_9.toValue(7n),
                                                                                                     alignment: _descriptor_9.alignment() } }] } },
                                                                          'size',
                                                                          { push: { storage: false,
                                                                                    value: __compactRuntime.StateValue.newCell({ value: _descriptor_10.toValue(0n),
                                                                                                                                 alignment: _descriptor_10.alignment() }).encode() } },
                                                                          'eq',
                                                                          { popeq: { cached: true,
                                                                                     result: undefined } }]).value);
      },
      size(...args_0) {
        if (args_0.length !== 0) {
          throw new __compactRuntime.CompactError(`size: expected 0 arguments, received ${args_0.length}`);
        }
        return _descriptor_10.fromValue(__compactRuntime.queryLedgerState(context,
                                                                          partialProofData,
                                                                          [
                                                                           { dup: { n: 0 } },
                                                                           { idx: { cached: false,
                                                                                    pushPath: false,
                                                                                    path: [
                                                                                           { tag: 'value',
                                                                                             value: { value: _descriptor_9.toValue(7n),
                                                                                                      alignment: _descriptor_9.alignment() } }] } },
                                                                           'size',
                                                                           { popeq: { cached: true,
                                                                                      result: undefined } }]).value);
      },
      member(...args_0) {
        if (args_0.length !== 1) {
          throw new __compactRuntime.CompactError(`member: expected 1 argument, received ${args_0.length}`);
        }
        const elem_0 = args_0[0];
        if (!(elem_0.buffer instanceof ArrayBuffer && elem_0.BYTES_PER_ELEMENT === 1 && elem_0.length === 32)) {
          __compactRuntime.typeError('member',
                                     'argument 1',
                                     'registry.compact line 146 char 1',
                                     'Bytes<32>',
                                     elem_0)
        }
        return _descriptor_3.fromValue(__compactRuntime.queryLedgerState(context,
                                                                         partialProofData,
                                                                         [
                                                                          { dup: { n: 0 } },
                                                                          { idx: { cached: false,
                                                                                   pushPath: false,
                                                                                   path: [
                                                                                          { tag: 'value',
                                                                                            value: { value: _descriptor_9.toValue(7n),
                                                                                                     alignment: _descriptor_9.alignment() } }] } },
                                                                          { push: { storage: false,
                                                                                    value: __compactRuntime.StateValue.newCell({ value: _descriptor_0.toValue(elem_0),
                                                                                                                                 alignment: _descriptor_0.alignment() }).encode() } },
                                                                          'member',
                                                                          { popeq: { cached: true,
                                                                                     result: undefined } }]).value);
      },
      [Symbol.iterator](...args_0) {
        if (args_0.length !== 0) {
          throw new __compactRuntime.CompactError(`iter: expected 0 arguments, received ${args_0.length}`);
        }
        const self_0 = state.asArray()[7];
        return self_0.asMap().keys().map((elem) => _descriptor_0.fromValue(elem.value))[Symbol.iterator]();
      }
    },
    relays: {
      isEmpty(...args_0) {
        if (args_0.length !== 0) {
          throw new __compactRuntime.CompactError(`isEmpty: expected 0 arguments, received ${args_0.length}`);
        }
        return _descriptor_3.fromValue(__compactRuntime.queryLedgerState(context,
                                                                         partialProofData,
                                                                         [
                                                                          { dup: { n: 0 } },
                                                                          { idx: { cached: false,
                                                                                   pushPath: false,
                                                                                   path: [
                                                                                          { tag: 'value',
                                                                                            value: { value: _descriptor_9.toValue(8n),
                                                                                                     alignment: _descriptor_9.alignment() } }] } },
                                                                          'size',
                                                                          { push: { storage: false,
                                                                                    value: __compactRuntime.StateValue.newCell({ value: _descriptor_10.toValue(0n),
                                                                                                                                 alignment: _descriptor_10.alignment() }).encode() } },
                                                                          'eq',
                                                                          { popeq: { cached: true,
                                                                                     result: undefined } }]).value);
      },
      size(...args_0) {
        if (args_0.length !== 0) {
          throw new __compactRuntime.CompactError(`size: expected 0 arguments, received ${args_0.length}`);
        }
        return _descriptor_10.fromValue(__compactRuntime.queryLedgerState(context,
                                                                          partialProofData,
                                                                          [
                                                                           { dup: { n: 0 } },
                                                                           { idx: { cached: false,
                                                                                    pushPath: false,
                                                                                    path: [
                                                                                           { tag: 'value',
                                                                                             value: { value: _descriptor_9.toValue(8n),
                                                                                                      alignment: _descriptor_9.alignment() } }] } },
                                                                           'size',
                                                                           { popeq: { cached: true,
                                                                                      result: undefined } }]).value);
      },
      member(...args_0) {
        if (args_0.length !== 1) {
          throw new __compactRuntime.CompactError(`member: expected 1 argument, received ${args_0.length}`);
        }
        const key_0 = args_0[0];
        if (!(key_0.buffer instanceof ArrayBuffer && key_0.BYTES_PER_ELEMENT === 1 && key_0.length === 32)) {
          __compactRuntime.typeError('member',
                                     'argument 1',
                                     'registry.compact line 148 char 1',
                                     'Bytes<32>',
                                     key_0)
        }
        return _descriptor_3.fromValue(__compactRuntime.queryLedgerState(context,
                                                                         partialProofData,
                                                                         [
                                                                          { dup: { n: 0 } },
                                                                          { idx: { cached: false,
                                                                                   pushPath: false,
                                                                                   path: [
                                                                                          { tag: 'value',
                                                                                            value: { value: _descriptor_9.toValue(8n),
                                                                                                     alignment: _descriptor_9.alignment() } }] } },
                                                                          { push: { storage: false,
                                                                                    value: __compactRuntime.StateValue.newCell({ value: _descriptor_0.toValue(key_0),
                                                                                                                                 alignment: _descriptor_0.alignment() }).encode() } },
                                                                          'member',
                                                                          { popeq: { cached: true,
                                                                                     result: undefined } }]).value);
      },
      lookup(...args_0) {
        if (args_0.length !== 1) {
          throw new __compactRuntime.CompactError(`lookup: expected 1 argument, received ${args_0.length}`);
        }
        const key_0 = args_0[0];
        if (!(key_0.buffer instanceof ArrayBuffer && key_0.BYTES_PER_ELEMENT === 1 && key_0.length === 32)) {
          __compactRuntime.typeError('lookup',
                                     'argument 1',
                                     'registry.compact line 148 char 1',
                                     'Bytes<32>',
                                     key_0)
        }
        return _descriptor_5.fromValue(__compactRuntime.queryLedgerState(context,
                                                                         partialProofData,
                                                                         [
                                                                          { dup: { n: 0 } },
                                                                          { idx: { cached: false,
                                                                                   pushPath: false,
                                                                                   path: [
                                                                                          { tag: 'value',
                                                                                            value: { value: _descriptor_9.toValue(8n),
                                                                                                     alignment: _descriptor_9.alignment() } }] } },
                                                                          { idx: { cached: false,
                                                                                   pushPath: false,
                                                                                   path: [
                                                                                          { tag: 'value',
                                                                                            value: { value: _descriptor_0.toValue(key_0),
                                                                                                     alignment: _descriptor_0.alignment() } }] } },
                                                                          { popeq: { cached: false,
                                                                                     result: undefined } }]).value);
      },
      [Symbol.iterator](...args_0) {
        if (args_0.length !== 0) {
          throw new __compactRuntime.CompactError(`iter: expected 0 arguments, received ${args_0.length}`);
        }
        const self_0 = state.asArray()[8];
        return self_0.asMap().keys().map(  (key) => {    const value = self_0.asMap().get(key).asCell();    return [      _descriptor_0.fromValue(key.value),      _descriptor_5.fromValue(value.value)    ];  })[Symbol.iterator]();
      }
    },
    anchors: {
      isEmpty(...args_0) {
        if (args_0.length !== 0) {
          throw new __compactRuntime.CompactError(`isEmpty: expected 0 arguments, received ${args_0.length}`);
        }
        return _descriptor_3.fromValue(__compactRuntime.queryLedgerState(context,
                                                                         partialProofData,
                                                                         [
                                                                          { dup: { n: 0 } },
                                                                          { idx: { cached: false,
                                                                                   pushPath: false,
                                                                                   path: [
                                                                                          { tag: 'value',
                                                                                            value: { value: _descriptor_9.toValue(9n),
                                                                                                     alignment: _descriptor_9.alignment() } }] } },
                                                                          'size',
                                                                          { push: { storage: false,
                                                                                    value: __compactRuntime.StateValue.newCell({ value: _descriptor_10.toValue(0n),
                                                                                                                                 alignment: _descriptor_10.alignment() }).encode() } },
                                                                          'eq',
                                                                          { popeq: { cached: true,
                                                                                     result: undefined } }]).value);
      },
      size(...args_0) {
        if (args_0.length !== 0) {
          throw new __compactRuntime.CompactError(`size: expected 0 arguments, received ${args_0.length}`);
        }
        return _descriptor_10.fromValue(__compactRuntime.queryLedgerState(context,
                                                                          partialProofData,
                                                                          [
                                                                           { dup: { n: 0 } },
                                                                           { idx: { cached: false,
                                                                                    pushPath: false,
                                                                                    path: [
                                                                                           { tag: 'value',
                                                                                             value: { value: _descriptor_9.toValue(9n),
                                                                                                      alignment: _descriptor_9.alignment() } }] } },
                                                                           'size',
                                                                           { popeq: { cached: true,
                                                                                      result: undefined } }]).value);
      },
      member(...args_0) {
        if (args_0.length !== 1) {
          throw new __compactRuntime.CompactError(`member: expected 1 argument, received ${args_0.length}`);
        }
        const key_0 = args_0[0];
        if (!(typeof(key_0) === 'bigint' && key_0 >= 0n && key_0 <= 65535n)) {
          __compactRuntime.typeError('member',
                                     'argument 1',
                                     'registry.compact line 150 char 1',
                                     'Uint<0..65536>',
                                     key_0)
        }
        return _descriptor_3.fromValue(__compactRuntime.queryLedgerState(context,
                                                                         partialProofData,
                                                                         [
                                                                          { dup: { n: 0 } },
                                                                          { idx: { cached: false,
                                                                                   pushPath: false,
                                                                                   path: [
                                                                                          { tag: 'value',
                                                                                            value: { value: _descriptor_9.toValue(9n),
                                                                                                     alignment: _descriptor_9.alignment() } }] } },
                                                                          { push: { storage: false,
                                                                                    value: __compactRuntime.StateValue.newCell({ value: _descriptor_7.toValue(key_0),
                                                                                                                                 alignment: _descriptor_7.alignment() }).encode() } },
                                                                          'member',
                                                                          { popeq: { cached: true,
                                                                                     result: undefined } }]).value);
      },
      lookup(...args_0) {
        if (args_0.length !== 1) {
          throw new __compactRuntime.CompactError(`lookup: expected 1 argument, received ${args_0.length}`);
        }
        const key_0 = args_0[0];
        if (!(typeof(key_0) === 'bigint' && key_0 >= 0n && key_0 <= 65535n)) {
          __compactRuntime.typeError('lookup',
                                     'argument 1',
                                     'registry.compact line 150 char 1',
                                     'Uint<0..65536>',
                                     key_0)
        }
        return _descriptor_13.fromValue(__compactRuntime.queryLedgerState(context,
                                                                          partialProofData,
                                                                          [
                                                                           { dup: { n: 0 } },
                                                                           { idx: { cached: false,
                                                                                    pushPath: false,
                                                                                    path: [
                                                                                           { tag: 'value',
                                                                                             value: { value: _descriptor_9.toValue(9n),
                                                                                                      alignment: _descriptor_9.alignment() } }] } },
                                                                           { idx: { cached: false,
                                                                                    pushPath: false,
                                                                                    path: [
                                                                                           { tag: 'value',
                                                                                             value: { value: _descriptor_7.toValue(key_0),
                                                                                                      alignment: _descriptor_7.alignment() } }] } },
                                                                           { popeq: { cached: false,
                                                                                      result: undefined } }]).value);
      },
      [Symbol.iterator](...args_0) {
        if (args_0.length !== 0) {
          throw new __compactRuntime.CompactError(`iter: expected 0 arguments, received ${args_0.length}`);
        }
        const self_0 = state.asArray()[9];
        return self_0.asMap().keys().map(  (key) => {    const value = self_0.asMap().get(key).asCell();    return [      _descriptor_7.fromValue(key.value),      _descriptor_13.fromValue(value.value)    ];  })[Symbol.iterator]();
      }
    },
    anchorTree: {
      isFull(...args_0) {
        if (args_0.length !== 0) {
          throw new __compactRuntime.CompactError(`isFull: expected 0 arguments, received ${args_0.length}`);
        }
        return _descriptor_3.fromValue(__compactRuntime.queryLedgerState(context,
                                                                         partialProofData,
                                                                         [
                                                                          { dup: { n: 0 } },
                                                                          { idx: { cached: false,
                                                                                   pushPath: false,
                                                                                   path: [
                                                                                          { tag: 'value',
                                                                                            value: { value: _descriptor_9.toValue(10n),
                                                                                                     alignment: _descriptor_9.alignment() } }] } },
                                                                          { idx: { cached: false,
                                                                                   pushPath: false,
                                                                                   path: [
                                                                                          { tag: 'value',
                                                                                            value: { value: _descriptor_9.toValue(1n),
                                                                                                     alignment: _descriptor_9.alignment() } }] } },
                                                                          { push: { storage: false,
                                                                                    value: __compactRuntime.StateValue.newCell({ value: _descriptor_10.toValue(4096n),
                                                                                                                                 alignment: _descriptor_10.alignment() }).encode() } },
                                                                          'lt',
                                                                          'neg',
                                                                          { popeq: { cached: true,
                                                                                     result: undefined } }]).value);
      },
      checkRoot(...args_0) {
        if (args_0.length !== 1) {
          throw new __compactRuntime.CompactError(`checkRoot: expected 1 argument, received ${args_0.length}`);
        }
        const rt_0 = args_0[0];
        if (!(typeof(rt_0) === 'object' && typeof(rt_0.field) === 'bigint' && rt_0.field >= 0 && rt_0.field <= __compactRuntime.MAX_FIELD)) {
          __compactRuntime.typeError('checkRoot',
                                     'argument 1',
                                     'registry.compact line 151 char 1',
                                     'struct MerkleTreeDigest<field: Field>',
                                     rt_0)
        }
        return _descriptor_3.fromValue(__compactRuntime.queryLedgerState(context,
                                                                         partialProofData,
                                                                         [
                                                                          { dup: { n: 0 } },
                                                                          { idx: { cached: false,
                                                                                   pushPath: false,
                                                                                   path: [
                                                                                          { tag: 'value',
                                                                                            value: { value: _descriptor_9.toValue(10n),
                                                                                                     alignment: _descriptor_9.alignment() } }] } },
                                                                          { idx: { cached: false,
                                                                                   pushPath: false,
                                                                                   path: [
                                                                                          { tag: 'value',
                                                                                            value: { value: _descriptor_9.toValue(2n),
                                                                                                     alignment: _descriptor_9.alignment() } }] } },
                                                                          { push: { storage: false,
                                                                                    value: __compactRuntime.StateValue.newCell({ value: _descriptor_2.toValue(rt_0),
                                                                                                                                 alignment: _descriptor_2.alignment() }).encode() } },
                                                                          'member',
                                                                          { popeq: { cached: true,
                                                                                     result: undefined } }]).value);
      },
      root(...args_0) {
        if (args_0.length !== 0) {
          throw new __compactRuntime.CompactError(`root: expected 0 arguments, received ${args_0.length}`);
        }
        const self_0 = state.asArray()[10];
        return ((result) => result             ? __compactRuntime.CompactTypeMerkleTreeDigest.fromValue(result)             : undefined)(self_0.asArray()[0].asBoundedMerkleTree().rehash().root()?.value);
      },
      firstFree(...args_0) {
        if (args_0.length !== 0) {
          throw new __compactRuntime.CompactError(`first_free: expected 0 arguments, received ${args_0.length}`);
        }
        const self_0 = state.asArray()[10];
        return __compactRuntime.CompactTypeField.fromValue(self_0.asArray()[1].asCell().value);
      },
      pathForLeaf(...args_0) {
        if (args_0.length !== 2) {
          throw new __compactRuntime.CompactError(`path_for_leaf: expected 2 arguments, received ${args_0.length}`);
        }
        const index_0 = args_0[0];
        const leaf_0 = args_0[1];
        if (!(typeof(index_0) === 'bigint' && index_0 >= 0 && index_0 <= __compactRuntime.MAX_FIELD)) {
          __compactRuntime.typeError('path_for_leaf',
                                     'argument 1',
                                     'registry.compact line 151 char 1',
                                     'Field',
                                     index_0)
        }
        if (!(leaf_0.buffer instanceof ArrayBuffer && leaf_0.BYTES_PER_ELEMENT === 1 && leaf_0.length === 32)) {
          __compactRuntime.typeError('path_for_leaf',
                                     'argument 2',
                                     'registry.compact line 151 char 1',
                                     'Bytes<32>',
                                     leaf_0)
        }
        const self_0 = state.asArray()[10];
        return ((result) => result             ? new __compactRuntime.CompactTypeMerkleTreePath(12, _descriptor_0).fromValue(result)             : undefined)(  self_0.asArray()[0].asBoundedMerkleTree().rehash().pathForLeaf(    index_0,    {      value: _descriptor_0.toValue(leaf_0),      alignment: _descriptor_0.alignment()    }  )?.value);
      },
      findPathForLeaf(...args_0) {
        if (args_0.length !== 1) {
          throw new __compactRuntime.CompactError(`find_path_for_leaf: expected 1 argument, received ${args_0.length}`);
        }
        const leaf_0 = args_0[0];
        if (!(leaf_0.buffer instanceof ArrayBuffer && leaf_0.BYTES_PER_ELEMENT === 1 && leaf_0.length === 32)) {
          __compactRuntime.typeError('find_path_for_leaf',
                                     'argument 1',
                                     'registry.compact line 151 char 1',
                                     'Bytes<32>',
                                     leaf_0)
        }
        const self_0 = state.asArray()[10];
        return ((result) => result             ? new __compactRuntime.CompactTypeMerkleTreePath(12, _descriptor_0).fromValue(result)             : undefined)(  self_0.asArray()[0].asBoundedMerkleTree().rehash().findPathForLeaf(    {      value: _descriptor_0.toValue(leaf_0),      alignment: _descriptor_0.alignment()    }  )?.value);
      },
      history(...args_0) {
        if (args_0.length !== 0) {
          throw new __compactRuntime.CompactError(`history: expected 0 arguments, received ${args_0.length}`);
        }
        const self_0 = state.asArray()[10];
        return self_0.asArray()[2].asMap().keys().map(  (elem) => __compactRuntime.CompactTypeMerkleTreeDigest.fromValue(elem.value))[Symbol.iterator]();
      }
    }
  };
}
const _emptyContext = {
  callContext: { currentQueryContext: new __compactRuntime.QueryContext(new __compactRuntime.ContractState().data, __compactRuntime.dummyContractAddress()), currentGasCost: __compactRuntime.emptyRunningCost() }
};
const _dummyContract = new Contract({
  stewardSecret: (...args) => undefined,
  relaySecret: (...args) => undefined,
  revocationEvidence: (...args) => undefined,
  memberPath: (...args) => undefined
});
export const pureCircuits = {
  stewardKeyOf: (...args_0) => {
    if (args_0.length !== 1) {
      throw new __compactRuntime.CompactError(`stewardKeyOf: expected 1 argument (as invoked from Typescript), received ${args_0.length}`);
    }
    const sk_0 = args_0[0];
    if (!(sk_0.buffer instanceof ArrayBuffer && sk_0.BYTES_PER_ELEMENT === 1 && sk_0.length === 32)) {
      __compactRuntime.typeError('stewardKeyOf',
                                 'argument 1',
                                 'registry.compact line 176 char 1',
                                 'Bytes<32>',
                                 sk_0)
    }
    return _dummyContract._stewardKeyOf_0(sk_0);
  },
  relayKeyOf: (...args_0) => {
    if (args_0.length !== 1) {
      throw new __compactRuntime.CompactError(`relayKeyOf: expected 1 argument (as invoked from Typescript), received ${args_0.length}`);
    }
    const sk_0 = args_0[0];
    if (!(sk_0.buffer instanceof ArrayBuffer && sk_0.BYTES_PER_ELEMENT === 1 && sk_0.length === 32)) {
      __compactRuntime.typeError('relayKeyOf',
                                 'argument 1',
                                 'registry.compact line 180 char 1',
                                 'Bytes<32>',
                                 sk_0)
    }
    return _dummyContract._relayKeyOf_0(sk_0);
  },
  memberLeafOf: (...args_0) => {
    if (args_0.length !== 2) {
      throw new __compactRuntime.CompactError(`memberLeafOf: expected 2 arguments (as invoked from Typescript), received ${args_0.length}`);
    }
    const idc_0 = args_0[0];
    const quota_0 = args_0[1];
    if (!(idc_0.buffer instanceof ArrayBuffer && idc_0.BYTES_PER_ELEMENT === 1 && idc_0.length === 32)) {
      __compactRuntime.typeError('memberLeafOf',
                                 'argument 1',
                                 'registry.compact line 184 char 1',
                                 'Bytes<32>',
                                 idc_0)
    }
    if (!(Array.isArray(quota_0) && quota_0.length === 4 && quota_0.every((t) => typeof(t) === 'bigint' && t >= 0n && t <= 65535n))) {
      __compactRuntime.typeError('memberLeafOf',
                                 'argument 2',
                                 'registry.compact line 184 char 1',
                                 'Vector<4, Uint<0..65536>>',
                                 quota_0)
    }
    return _dummyContract._memberLeafOf_0(idc_0, quota_0);
  },
  idcOf: (...args_0) => {
    if (args_0.length !== 1) {
      throw new __compactRuntime.CompactError(`idcOf: expected 1 argument (as invoked from Typescript), received ${args_0.length}`);
    }
    const a0_0 = args_0[0];
    if (!(typeof(a0_0) === 'bigint' && a0_0 >= 0 && a0_0 <= __compactRuntime.MAX_FIELD)) {
      __compactRuntime.typeError('idcOf',
                                 'argument 1',
                                 'registry.compact line 188 char 1',
                                 'Field',
                                 a0_0)
    }
    return _dummyContract._idcOf_0(a0_0);
  },
  anchorLeafOf: (...args_0) => {
    if (args_0.length !== 2) {
      throw new __compactRuntime.CompactError(`anchorLeafOf: expected 2 arguments (as invoked from Typescript), received ${args_0.length}`);
    }
    const window_0 = args_0[0];
    const root_0 = args_0[1];
    if (!(typeof(window_0) === 'bigint' && window_0 >= 0n && window_0 <= 18446744073709551615n)) {
      __compactRuntime.typeError('anchorLeafOf',
                                 'argument 1',
                                 'registry.compact line 192 char 1',
                                 'Uint<0..18446744073709551616>',
                                 window_0)
    }
    if (!(root_0.buffer instanceof ArrayBuffer && root_0.BYTES_PER_ELEMENT === 1 && root_0.length === 32)) {
      __compactRuntime.typeError('anchorLeafOf',
                                 'argument 2',
                                 'registry.compact line 192 char 1',
                                 'Bytes<32>',
                                 root_0)
    }
    return _dummyContract._anchorLeafOf_0(window_0, root_0);
  },
  rlnA1: (...args_0) => {
    if (args_0.length !== 4) {
      throw new __compactRuntime.CompactError(`rlnA1: expected 4 arguments (as invoked from Typescript), received ${args_0.length}`);
    }
    const a0_0 = args_0[0];
    const epoch_0 = args_0[1];
    const sizeClass_0 = args_0[2];
    const credit_0 = args_0[3];
    if (!(typeof(a0_0) === 'bigint' && a0_0 >= 0 && a0_0 <= __compactRuntime.MAX_FIELD)) {
      __compactRuntime.typeError('rlnA1',
                                 'argument 1',
                                 'registry.compact line 199 char 1',
                                 'Field',
                                 a0_0)
    }
    if (!(typeof(epoch_0) === 'bigint' && epoch_0 >= 0n && epoch_0 <= 18446744073709551615n)) {
      __compactRuntime.typeError('rlnA1',
                                 'argument 2',
                                 'registry.compact line 199 char 1',
                                 'Uint<0..18446744073709551616>',
                                 epoch_0)
    }
    if (!(typeof(sizeClass_0) === 'bigint' && sizeClass_0 >= 0n && sizeClass_0 <= 255n)) {
      __compactRuntime.typeError('rlnA1',
                                 'argument 3',
                                 'registry.compact line 199 char 1',
                                 'Uint<0..256>',
                                 sizeClass_0)
    }
    if (!(typeof(credit_0) === 'bigint' && credit_0 >= 0n && credit_0 <= 65535n)) {
      __compactRuntime.typeError('rlnA1',
                                 'argument 4',
                                 'registry.compact line 199 char 1',
                                 'Uint<0..65536>',
                                 credit_0)
    }
    return _dummyContract._rlnA1_0(a0_0, epoch_0, sizeClass_0, credit_0);
  },
  rlnX: (...args_0) => {
    if (args_0.length !== 1) {
      throw new __compactRuntime.CompactError(`rlnX: expected 1 argument (as invoked from Typescript), received ${args_0.length}`);
    }
    const eid_0 = args_0[0];
    if (!(eid_0.buffer instanceof ArrayBuffer && eid_0.BYTES_PER_ELEMENT === 1 && eid_0.length === 32)) {
      __compactRuntime.typeError('rlnX',
                                 'argument 1',
                                 'registry.compact line 203 char 1',
                                 'Bytes<32>',
                                 eid_0)
    }
    return _dummyContract._rlnX_0(eid_0);
  }
};
export const expectedVk = {
  'activateParams': '1cc1b3578b5599ad1fd54892ac6fdb4fe945eca7d8193a8b470cac88f2050c1b',
  'addRelay': 'c3bc18bb4ce595f1fe23d1c57d90b1491c94d3c9f28c3c6e92d4c5f7d4c477e9',
  'anchorRootValid': '9e8a750f48e115a6306156c89b46ee6ec5633197a635ade9d20064d72485617c',
  'pause': '8530e41c504e38c9c1cd22cb79e6b0ae113c9be466c87ebbcf0aa56c498a9888',
  'postAnchor': '5c0f9751537d7fe0cd0bb14cb0fdd2ea505564d08b4b5162fa73c3083f95da0f',
  'proposeParams': 'bdd6782e55b4347512152c45cc08d8c9e289b87155344a7622adc771eb0ba1ae',
  'pruneAnchor': '04dec9771b426a247f5ac30840fd2afb4bc18b34cb629f4ccb26ce50d3839e12',
  'prunePeriod': 'bed26616f50161029eb35c82f0b52b7b9bfac5a35ea63b0626a5c3b0cd5adefc',
  'register': '77447fef660768bb959d63d1c9cb0dd4d0c295a64a1bded2a56e03ed6d8aedc7',
  'removeRelay': 'd50d40d0c89f84eb22422be2e81a37a417e315611fb0154e4f7da60a7ee13a1d',
  'revoke': 'a6ca866b8b5d9f0a679ba3da7f5a276aee9a1934c4b608fa2f0617213a7cfdaf',
  'setSteward': 'c8850653587b0a7dbca83f79429828f6077a1114caeb52d9d328b843cbae01d0',
  'unpause': '882feead3960f3876436049287de300dcd6f72ae8b311c5d80f1a5a5f2aee487',
};

export const circuitSignatures = {
  'stewardKeyOf': {pure: true, provable: false, argumentTypes: [{tag: 'Bytes', length: 32}], resultType: {tag: 'Bytes', length: 32}},
  'relayKeyOf': {pure: true, provable: false, argumentTypes: [{tag: 'Bytes', length: 32}], resultType: {tag: 'Bytes', length: 32}},
  'memberLeafOf': {pure: true, provable: false, argumentTypes: [{tag: 'Bytes', length: 32}, {tag: 'Vector', length: 4, type: {tag: 'Uint', maxval: '65535'}}], resultType: {tag: 'Bytes', length: 32}},
  'idcOf': {pure: true, provable: false, argumentTypes: [{tag: 'Field'}], resultType: {tag: 'Bytes', length: 32}},
  'anchorLeafOf': {pure: true, provable: false, argumentTypes: [{tag: 'Uint', maxval: '18446744073709551615'}, {tag: 'Bytes', length: 32}], resultType: {tag: 'Bytes', length: 32}},
  'rlnA1': {pure: true, provable: false, argumentTypes: [{tag: 'Field'}, {tag: 'Uint', maxval: '18446744073709551615'}, {tag: 'Uint', maxval: '255'}, {tag: 'Uint', maxval: '65535'}], resultType: {tag: 'Field'}},
  'rlnX': {pure: true, provable: false, argumentTypes: [{tag: 'Bytes', length: 32}], resultType: {tag: 'Field'}},
  'register': {pure: false, provable: true, argumentTypes: [{tag: 'Bytes', length: 32}, {tag: 'Uint', maxval: '4294967295'}], resultType: {tag: 'Tuple', types: []}},
  'revoke': {pure: false, provable: true, argumentTypes: [{tag: 'Uint', maxval: '4294967295'}, {tag: 'Uint', maxval: '65535'}], resultType: {tag: 'Tuple', types: []}},
  'prunePeriod': {pure: false, provable: true, argumentTypes: [{tag: 'Uint', maxval: '4294967295'}], resultType: {tag: 'Tuple', types: []}},
  'addRelay': {pure: false, provable: true, argumentTypes: [{tag: 'Bytes', length: 32}, {tag: 'Struct', name: 'RelayEntry', elements: [{name: 'operatorId', type: {tag: 'Bytes', length: 32}}, {name: 'roles', type: {tag: 'Struct', name: 'Roles', elements: [{name: 'relay', type: {tag: 'Boolean'}}, {name: 'store', type: {tag: 'Boolean'}}, {name: 'bootstrapper', type: {tag: 'Boolean'}}, {name: 'gateway', type: {tag: 'Boolean'}}, {name: 'anchorer', type: {tag: 'Boolean'}}]}}, {name: 'keyCommitment', type: {tag: 'Bytes', length: 32}}]}, {tag: 'Uint', maxval: '65535'}], resultType: {tag: 'Tuple', types: []}},
  'removeRelay': {pure: false, provable: true, argumentTypes: [{tag: 'Bytes', length: 32}, {tag: 'Uint', maxval: '65535'}], resultType: {tag: 'Tuple', types: []}},
  'proposeParams': {pure: false, provable: true, argumentTypes: [{tag: 'Struct', name: 'Params', elements: [{name: 'epochLength', type: {tag: 'Uint', maxval: '4294967295'}}, {name: 'membershipPeriod', type: {tag: 'Uint', maxval: '4294967295'}}, {name: 'rootWindow', type: {tag: 'Uint', maxval: '4294967295'}}, {name: 'quota', type: {tag: 'Vector', length: 4, type: {tag: 'Uint', maxval: '65535'}}}, {name: 'anchorWindow', type: {tag: 'Uint', maxval: '4294967295'}}, {name: 'anchorHistory', type: {tag: 'Uint', maxval: '4294967295'}}, {name: 'shardCount', type: {tag: 'Uint', maxval: '255'}}, {name: 'activationHeight', type: {tag: 'Uint', maxval: '18446744073709551615'}}, {name: 'maxVersion', type: {tag: 'Uint', maxval: '255'}}, {name: 'bootstrapHash', type: {tag: 'Bytes', length: 32}}]}, {tag: 'Uint', maxval: '18446744073709551615'}, {tag: 'Uint', maxval: '65535'}], resultType: {tag: 'Tuple', types: []}},
  'activateParams': {pure: false, provable: true, argumentTypes: [], resultType: {tag: 'Tuple', types: []}},
  'pause': {pure: false, provable: true, argumentTypes: [{tag: 'Uint', maxval: '65535'}], resultType: {tag: 'Tuple', types: []}},
  'unpause': {pure: false, provable: true, argumentTypes: [{tag: 'Uint', maxval: '65535'}], resultType: {tag: 'Tuple', types: []}},
  'setSteward': {pure: false, provable: true, argumentTypes: [{tag: 'Bytes', length: 32}, {tag: 'Uint', maxval: '65535'}], resultType: {tag: 'Tuple', types: []}},
  'postAnchor': {pure: false, provable: true, argumentTypes: [{tag: 'Bytes', length: 32}, {tag: 'Uint', maxval: '18446744073709551615'}, {tag: 'Uint', maxval: '18446744073709551615'}, {tag: 'Uint', maxval: '65535'}, {tag: 'Bytes', length: 32}, {tag: 'Vector', length: 8, type: {tag: 'Uint', maxval: '4294967295'}}], resultType: {tag: 'Tuple', types: []}},
  'pruneAnchor': {pure: false, provable: true, argumentTypes: [{tag: 'Uint', maxval: '65535'}], resultType: {tag: 'Tuple', types: []}},
  'anchorRootValid': {pure: false, provable: true, argumentTypes: [{tag: 'Struct', name: 'MerkleTreeDigest', elements: [{name: 'field', type: {tag: 'Field'}}]}], resultType: {tag: 'Boolean'}},
};

export const declaredInterfaces = {};

//# sourceMappingURL=index.js.map
