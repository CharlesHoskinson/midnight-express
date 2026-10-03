import * as __compactRuntime from '@midnight-ntwrk/compact-runtime';
__compactRuntime.checkRuntimeVersion('0.20.0');

const _descriptor_0 = new __compactRuntime.CompactTypeBytes(288);

const _descriptor_1 = new __compactRuntime.CompactTypeBytes(256);

const _descriptor_2 = new __compactRuntime.CompactTypeVector(16, _descriptor_1);

const _descriptor_3 = new __compactRuntime.CompactTypeVector(4, _descriptor_1);

const _descriptor_4 = new __compactRuntime.CompactTypeBytes(32);

const _descriptor_5 = new __compactRuntime.CompactTypeUnsignedInteger(18446744073709551615n, 8);

const _descriptor_6 = __compactRuntime.CompactTypeBoolean;

class _Either_0 {
  alignment() {
    return _descriptor_6.alignment().concat(_descriptor_4.alignment().concat(_descriptor_4.alignment()));
  }
  fromValue(value_0) {
    return {
      is_left: _descriptor_6.fromValue(value_0),
      left: _descriptor_4.fromValue(value_0),
      right: _descriptor_4.fromValue(value_0)
    }
  }
  toValue(value_0) {
    return _descriptor_6.toValue(value_0.is_left).concat(_descriptor_4.toValue(value_0.left).concat(_descriptor_4.toValue(value_0.right)));
  }
}

const _descriptor_7 = new _Either_0();

const _descriptor_8 = new __compactRuntime.CompactTypeUnsignedInteger(340282366920938463463374607431768211455n, 16);

class _ContractAddress_0 {
  alignment() {
    return _descriptor_4.alignment();
  }
  fromValue(value_0) {
    return {
      bytes: _descriptor_4.fromValue(value_0)
    }
  }
  toValue(value_0) {
    return _descriptor_4.toValue(value_0.bytes);
  }
}

const _descriptor_9 = new _ContractAddress_0();

class _UserAddress_0 {
  alignment() {
    return _descriptor_4.alignment();
  }
  fromValue(value_0) {
    return {
      bytes: _descriptor_4.fromValue(value_0)
    }
  }
  toValue(value_0) {
    return _descriptor_4.toValue(value_0.bytes);
  }
}

const _descriptor_10 = new _UserAddress_0();

class _Either_1 {
  alignment() {
    return _descriptor_6.alignment().concat(_descriptor_9.alignment().concat(_descriptor_10.alignment()));
  }
  fromValue(value_0) {
    return {
      is_left: _descriptor_6.fromValue(value_0),
      left: _descriptor_9.fromValue(value_0),
      right: _descriptor_10.fromValue(value_0)
    }
  }
  toValue(value_0) {
    return _descriptor_6.toValue(value_0.is_left).concat(_descriptor_9.toValue(value_0.left).concat(_descriptor_10.toValue(value_0.right)));
  }
}

const _descriptor_11 = new _Either_1();

class _Maybe_0 {
  alignment() {
    return _descriptor_6.alignment().concat(_descriptor_11.alignment());
  }
  fromValue(value_0) {
    return {
      is_some: _descriptor_6.fromValue(value_0),
      value: _descriptor_11.fromValue(value_0)
    }
  }
  toValue(value_0) {
    return _descriptor_6.toValue(value_0.is_some).concat(_descriptor_11.toValue(value_0.value));
  }
}

const _descriptor_12 = new _Maybe_0();

const _descriptor_13 = new __compactRuntime.CompactTypeUnsignedInteger(255n, 1);

const _descriptor_14 = new __compactRuntime.CompactTypeUnsignedInteger(4294967295n, 4);

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
    this.witnesses = witnesses_0;
    this.circuits = {
      publishPart: async (...args_1) => {
        if (args_1.length !== 3) {
          throw new __compactRuntime.CompactError(`publishPart: expected 3 arguments (as invoked from Typescript), received ${args_1.length}`);
        }
        const contextOrig_0 = args_1[0];
        const name_0 = args_1[1];
        const payload_0 = args_1[2];
        if (!(typeof(contextOrig_0) === 'object' && contextOrig_0.callContext.currentQueryContext != undefined)) {
          __compactRuntime.typeError('publishPart',
                                     'argument 1 (as invoked from Typescript)',
                                     'fallback.compact line 21 char 1',
                                     'CircuitContext',
                                     contextOrig_0)
        }
        if (!(name_0.buffer instanceof ArrayBuffer && name_0.BYTES_PER_ELEMENT === 1 && name_0.length === 32)) {
          __compactRuntime.typeError('publishPart',
                                     'argument 1 (argument 2 as invoked from Typescript)',
                                     'fallback.compact line 21 char 1',
                                     'Bytes<32>',
                                     name_0)
        }
        if (!(payload_0.buffer instanceof ArrayBuffer && payload_0.BYTES_PER_ELEMENT === 1 && payload_0.length === 256)) {
          __compactRuntime.typeError('publishPart',
                                     'argument 2 (argument 3 as invoked from Typescript)',
                                     'fallback.compact line 21 char 1',
                                     'Bytes<256>',
                                     payload_0)
        }
        const context = __compactRuntime.copyCircuitContext(contextOrig_0);
        const partialProofData = {
          input: {
            value: _descriptor_4.toValue(name_0).concat(_descriptor_1.toValue(payload_0)),
            alignment: _descriptor_4.alignment().concat(_descriptor_1.alignment())
          },
          output: undefined,
          publicTranscript: [],
          privateTranscriptOutputs: []
        };
        const result_0 = await this._publishPart_0(context,
                                                   partialProofData,
                                                   name_0,
                                                   payload_0);
        partialProofData.output = { value: [], alignment: [] };
        __compactRuntime.finalizeCallProofData(context, partialProofData);
        return { result: result_0, context: context, gasCost: context.callContext.currentGasCost };
      },
      publishClass0: async (...args_1) => {
        if (args_1.length !== 2) {
          throw new __compactRuntime.CompactError(`publishClass0: expected 2 arguments (as invoked from Typescript), received ${args_1.length}`);
        }
        const contextOrig_0 = args_1[0];
        const body_0 = args_1[1];
        if (!(typeof(contextOrig_0) === 'object' && contextOrig_0.callContext.currentQueryContext != undefined)) {
          __compactRuntime.typeError('publishClass0',
                                     'argument 1 (as invoked from Typescript)',
                                     'fallback.compact line 30 char 1',
                                     'CircuitContext',
                                     contextOrig_0)
        }
        if (!(body_0.buffer instanceof ArrayBuffer && body_0.BYTES_PER_ELEMENT === 1 && body_0.length === 256)) {
          __compactRuntime.typeError('publishClass0',
                                     'argument 1 (argument 2 as invoked from Typescript)',
                                     'fallback.compact line 30 char 1',
                                     'Bytes<256>',
                                     body_0)
        }
        const context = __compactRuntime.copyCircuitContext(contextOrig_0);
        const partialProofData = {
          input: {
            value: _descriptor_1.toValue(body_0),
            alignment: _descriptor_1.alignment()
          },
          output: undefined,
          publicTranscript: [],
          privateTranscriptOutputs: []
        };
        const result_0 = await this._publishClass0_0(context,
                                                     partialProofData,
                                                     body_0);
        partialProofData.output = { value: [], alignment: [] };
        __compactRuntime.finalizeCallProofData(context, partialProofData);
        return { result: result_0, context: context, gasCost: context.callContext.currentGasCost };
      },
      publishClass1: async (...args_1) => {
        if (args_1.length !== 2) {
          throw new __compactRuntime.CompactError(`publishClass1: expected 2 arguments (as invoked from Typescript), received ${args_1.length}`);
        }
        const contextOrig_0 = args_1[0];
        const parts_0 = args_1[1];
        if (!(typeof(contextOrig_0) === 'object' && contextOrig_0.callContext.currentQueryContext != undefined)) {
          __compactRuntime.typeError('publishClass1',
                                     'argument 1 (as invoked from Typescript)',
                                     'fallback.compact line 34 char 1',
                                     'CircuitContext',
                                     contextOrig_0)
        }
        if (!(Array.isArray(parts_0) && parts_0.length === 4 && parts_0.every((t) => t.buffer instanceof ArrayBuffer && t.BYTES_PER_ELEMENT === 1 && t.length === 256))) {
          __compactRuntime.typeError('publishClass1',
                                     'argument 1 (argument 2 as invoked from Typescript)',
                                     'fallback.compact line 34 char 1',
                                     'Vector<4, Bytes<256>>',
                                     parts_0)
        }
        const context = __compactRuntime.copyCircuitContext(contextOrig_0);
        const partialProofData = {
          input: {
            value: _descriptor_3.toValue(parts_0),
            alignment: _descriptor_3.alignment()
          },
          output: undefined,
          publicTranscript: [],
          privateTranscriptOutputs: []
        };
        const result_0 = await this._publishClass1_0(context,
                                                     partialProofData,
                                                     parts_0);
        partialProofData.output = { value: [], alignment: [] };
        __compactRuntime.finalizeCallProofData(context, partialProofData);
        return { result: result_0, context: context, gasCost: context.callContext.currentGasCost };
      },
      publishClass2: async (...args_1) => {
        if (args_1.length !== 2) {
          throw new __compactRuntime.CompactError(`publishClass2: expected 2 arguments (as invoked from Typescript), received ${args_1.length}`);
        }
        const contextOrig_0 = args_1[0];
        const parts_0 = args_1[1];
        if (!(typeof(contextOrig_0) === 'object' && contextOrig_0.callContext.currentQueryContext != undefined)) {
          __compactRuntime.typeError('publishClass2',
                                     'argument 1 (as invoked from Typescript)',
                                     'fallback.compact line 40 char 1',
                                     'CircuitContext',
                                     contextOrig_0)
        }
        if (!(Array.isArray(parts_0) && parts_0.length === 16 && parts_0.every((t) => t.buffer instanceof ArrayBuffer && t.BYTES_PER_ELEMENT === 1 && t.length === 256))) {
          __compactRuntime.typeError('publishClass2',
                                     'argument 1 (argument 2 as invoked from Typescript)',
                                     'fallback.compact line 40 char 1',
                                     'Vector<16, Bytes<256>>',
                                     parts_0)
        }
        const context = __compactRuntime.copyCircuitContext(contextOrig_0);
        const partialProofData = {
          input: {
            value: _descriptor_2.toValue(parts_0),
            alignment: _descriptor_2.alignment()
          },
          output: undefined,
          publicTranscript: [],
          privateTranscriptOutputs: []
        };
        const result_0 = await this._publishClass2_0(context,
                                                     partialProofData,
                                                     parts_0);
        partialProofData.output = { value: [], alignment: [] };
        __compactRuntime.finalizeCallProofData(context, partialProofData);
        return { result: result_0, context: context, gasCost: context.callContext.currentGasCost };
      }
    };
    this.impureCircuits = {
      publishPart: this.circuits.publishPart,
      publishClass0: this.circuits.publishClass0,
      publishClass1: this.circuits.publishClass1,
      publishClass2: this.circuits.publishClass2
    };
    this.provableCircuits = {
      publishPart: this.circuits.publishPart,
      publishClass0: this.circuits.publishClass0,
      publishClass1: this.circuits.publishClass1,
      publishClass2: this.circuits.publishClass2
    };
  }
  async initialState(...args_0) {
    if (args_0.length !== 1) {
      throw new __compactRuntime.CompactError(`Contract state constructor: expected 1 argument (as invoked from Typescript), received ${args_0.length}`);
    }
    const constructorContext_0 = args_0[0];
    if (typeof(constructorContext_0) !== 'object') {
      throw new __compactRuntime.CompactError(`Contract state constructor: expected 'constructorContext' in argument 1 (as invoked from Typescript) to be an object`);
    }
    if (!('initialZswapLocalState' in constructorContext_0)) {
      throw new __compactRuntime.CompactError(`Contract state constructor: expected 'initialZswapLocalState' in argument 1 (as invoked from Typescript)`);
    }
    if (typeof(constructorContext_0.initialZswapLocalState) !== 'object') {
      throw new __compactRuntime.CompactError(`Contract state constructor: expected 'initialZswapLocalState' in argument 1 (as invoked from Typescript) to be an object`);
    }
    const state_0 = new __compactRuntime.ContractState();
    let stateValue_0 = __compactRuntime.StateValue.newArray();
    state_0.data = new __compactRuntime.ChargedState(stateValue_0);
    state_0.setOperation('publishPart', new __compactRuntime.ContractOperation());
    state_0.setOperation('publishClass0', new __compactRuntime.ContractOperation());
    state_0.setOperation('publishClass1', new __compactRuntime.ContractOperation());
    state_0.setOperation('publishClass2', new __compactRuntime.ContractOperation());
    const context = __compactRuntime.createCircuitContext({circuitId: 'constructor', contractAddress: __compactRuntime.dummyContractAddress(), coinPublicKeyOrZswapState: constructorContext_0.initialZswapLocalState.coinPublicKey, contractState: state_0.data, privateState: constructorContext_0.initialPrivateState});
    const partialProofData = {
      input: { value: [], alignment: [] },
      output: undefined,
      publicTranscript: [],
      privateTranscriptOutputs: []
    };
    state_0.data = new __compactRuntime.ChargedState(context.callContext.currentQueryContext.state.state);
    return {
      currentContractState: state_0,
      currentPrivateState: context.callContext.currentPrivateState,
      currentZswapLocalState: context.callContext.currentZswapLocalState
    }
  }
  _envName_0() {
    return new Uint8Array([109, 112, 101, 47, 101, 110, 118, 47, 118, 49, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]);
  }
  async _publishPart_0(context, partialProofData, name_0, payload_0) {
    const n_0 = name_0;
    __compactRuntime.assert(this._equal_0(n_0, this._envName_0()),
                            'not the MPE envelope name');
    let t_0;
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newArray()
                                                          .arrayPush(__compactRuntime.StateValue.newCell({ value: _descriptor_14.toValue(1n),
                                                                                                           alignment: _descriptor_14.alignment() })).arrayPush(__compactRuntime.StateValue.newCell({ value: _descriptor_13.toValue(10n),
                                                                                                                                                                                                     alignment: _descriptor_13.alignment() })).arrayPush(__compactRuntime.StateValue.newCell({ value: _descriptor_0.toValue((t_0 = { name:
                                                                                                                                                                                                                                                                                                                                       n_0,
                                                                                                                                                                                                                                                                                                                                     payload:
                                                                                                                                                                                                                                                                                                                                       payload_0 },
                                                                                                                                                                                                                                                                                                                             Uint8Array.from([...Array.from(t_0.name,
                                                                                                                                                                                                                                                                                                                                                            BigInt),
                                                                                                                                                                                                                                                                                                                                              ...Array.from(t_0.payload,
                                                                                                                                                                                                                                                                                                                                                            BigInt)],
                                                                                                                                                                                                                                                                                                                                             Number))),
                                                                                                                                                                                                                                                                                               alignment: _descriptor_0.alignment() }))
                                                          .encode() } },
                                       'log']);
    return [];
  }
  async _publishClass0_0(context, partialProofData, body_0) {
    let t_0;
    __compactRuntime.queryLedgerState(context,
                                      partialProofData,
                                      [
                                       { push: { storage: false,
                                                 value: __compactRuntime.StateValue.newArray()
                                                          .arrayPush(__compactRuntime.StateValue.newCell({ value: _descriptor_14.toValue(1n),
                                                                                                           alignment: _descriptor_14.alignment() })).arrayPush(__compactRuntime.StateValue.newCell({ value: _descriptor_13.toValue(10n),
                                                                                                                                                                                                     alignment: _descriptor_13.alignment() })).arrayPush(__compactRuntime.StateValue.newCell({ value: _descriptor_0.toValue((t_0 = { name:
                                                                                                                                                                                                                                                                                                                                       this._envName_0(),
                                                                                                                                                                                                                                                                                                                                     payload:
                                                                                                                                                                                                                                                                                                                                       body_0 },
                                                                                                                                                                                                                                                                                                                             Uint8Array.from([...Array.from(t_0.name,
                                                                                                                                                                                                                                                                                                                                                            BigInt),
                                                                                                                                                                                                                                                                                                                                              ...Array.from(t_0.payload,
                                                                                                                                                                                                                                                                                                                                                            BigInt)],
                                                                                                                                                                                                                                                                                                                                             Number))),
                                                                                                                                                                                                                                                                                               alignment: _descriptor_0.alignment() }))
                                                          .encode() } },
                                       'log']);
    return [];
  }
  async _publishClass1_0(context, partialProofData, parts_0) {
    await this._folder_0(context,
                         partialProofData,
                         (async (context, partialProofData, t_0, p_0) =>
                          {
                            let t_1;
                            __compactRuntime.queryLedgerState(context,
                                                              partialProofData,
                                                              [
                                                               { push: { storage: false,
                                                                         value: __compactRuntime.StateValue.newArray()
                                                                                  .arrayPush(__compactRuntime.StateValue.newCell({ value: _descriptor_14.toValue(1n),
                                                                                                                                   alignment: _descriptor_14.alignment() })).arrayPush(__compactRuntime.StateValue.newCell({ value: _descriptor_13.toValue(10n),
                                                                                                                                                                                                                             alignment: _descriptor_13.alignment() })).arrayPush(__compactRuntime.StateValue.newCell({ value: _descriptor_0.toValue((t_1 = { name:
                                                                                                                                                                                                                                                                                                                                                               this._envName_0(),
                                                                                                                                                                                                                                                                                                                                                             payload:
                                                                                                                                                                                                                                                                                                                                                               p_0 },
                                                                                                                                                                                                                                                                                                                                                     Uint8Array.from([...Array.from(t_1.name,
                                                                                                                                                                                                                                                                                                                                                                                    BigInt),
                                                                                                                                                                                                                                                                                                                                                                      ...Array.from(t_1.payload,
                                                                                                                                                                                                                                                                                                                                                                                    BigInt)],
                                                                                                                                                                                                                                                                                                                                                                     Number))),
                                                                                                                                                                                                                                                                                                                       alignment: _descriptor_0.alignment() }))
                                                                                  .encode() } },
                                                               'log']);
                            return t_0;
                          }),
                         [],
                         parts_0);
    return [];
  }
  async _publishClass2_0(context, partialProofData, parts_0) {
    await this._folder_1(context,
                         partialProofData,
                         (async (context, partialProofData, t_0, p_0) =>
                          {
                            let t_1;
                            __compactRuntime.queryLedgerState(context,
                                                              partialProofData,
                                                              [
                                                               { push: { storage: false,
                                                                         value: __compactRuntime.StateValue.newArray()
                                                                                  .arrayPush(__compactRuntime.StateValue.newCell({ value: _descriptor_14.toValue(1n),
                                                                                                                                   alignment: _descriptor_14.alignment() })).arrayPush(__compactRuntime.StateValue.newCell({ value: _descriptor_13.toValue(10n),
                                                                                                                                                                                                                             alignment: _descriptor_13.alignment() })).arrayPush(__compactRuntime.StateValue.newCell({ value: _descriptor_0.toValue((t_1 = { name:
                                                                                                                                                                                                                                                                                                                                                               this._envName_0(),
                                                                                                                                                                                                                                                                                                                                                             payload:
                                                                                                                                                                                                                                                                                                                                                               p_0 },
                                                                                                                                                                                                                                                                                                                                                     Uint8Array.from([...Array.from(t_1.name,
                                                                                                                                                                                                                                                                                                                                                                                    BigInt),
                                                                                                                                                                                                                                                                                                                                                                      ...Array.from(t_1.payload,
                                                                                                                                                                                                                                                                                                                                                                                    BigInt)],
                                                                                                                                                                                                                                                                                                                                                                     Number))),
                                                                                                                                                                                                                                                                                                                       alignment: _descriptor_0.alignment() }))
                                                                                  .encode() } },
                                                               'log']);
                            return t_0;
                          }),
                         [],
                         parts_0);
    return [];
  }
  _equal_0(x0, y0) {
    if (!x0.every((x, i) => y0[i] === x)) { return false; }
    return true;
  }
  async _folder_0(context, partialProofData, f, x, a0) {
    for (let i = 0; i < 4; i++) { x = await f(context, partialProofData, x, a0[i]); }
    return x;
  }
  async _folder_1(context, partialProofData, f, x, a0) {
    for (let i = 0; i < 16; i++) { x = await f(context, partialProofData, x, a0[i]); }
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
  };
}
const _emptyContext = {
  callContext: { currentQueryContext: new __compactRuntime.QueryContext(new __compactRuntime.ContractState().data, __compactRuntime.dummyContractAddress()), currentGasCost: __compactRuntime.emptyRunningCost() }
};
const _dummyContract = new Contract({ });
export const pureCircuits = {};
export const expectedVk = {};

export const circuitSignatures = {
  'publishPart': {pure: false, provable: true, argumentTypes: [{tag: 'Bytes', length: 32}, {tag: 'Bytes', length: 256}], resultType: {tag: 'Tuple', types: []}},
  'publishClass0': {pure: false, provable: true, argumentTypes: [{tag: 'Bytes', length: 256}], resultType: {tag: 'Tuple', types: []}},
  'publishClass1': {pure: false, provable: true, argumentTypes: [{tag: 'Vector', length: 4, type: {tag: 'Bytes', length: 256}}], resultType: {tag: 'Tuple', types: []}},
  'publishClass2': {pure: false, provable: true, argumentTypes: [{tag: 'Vector', length: 16, type: {tag: 'Bytes', length: 256}}], resultType: {tag: 'Tuple', types: []}},
};

export const declaredInterfaces = {};

//# sourceMappingURL=index.js.map
