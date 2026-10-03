import type * as __compactRuntime from '@midnight-ntwrk/compact-runtime';

export type PathStep = { sibling: Uint8Array;
                         siblingLeft: boolean;
                         skip: boolean
                       };

export type EventWitness = { eid: Uint8Array;
                             window: bigint;
                             shardPath: PathStep[];
                             windowPath: PathStep[];
                             anchorPath: { leaf: Uint8Array,
                                           path: { sibling: { field: bigint },
                                                   goes_left: boolean
                                                 }[]
                                         };
                             eventSecret: Uint8Array
                           };

export type AnchorLeaf = { domain: Uint8Array; window: bigint; root: Uint8Array
                         };

export type RfcLeaf = { tag: Uint8Array; eid: Uint8Array };

export type RfcNode = { tag: Uint8Array; left: Uint8Array; right: Uint8Array };

export type Witnesses<PS> = {
  eventWitness(context: __compactRuntime.WitnessContext<Ledger, PS>): [PS, EventWitness];
}

export type ImpureCircuits<PS> = {
  react(context: __compactRuntime.CircuitContext<PS>,
        notAfter_0: bigint,
        action_0: Uint8Array): Promise<__compactRuntime.CircuitResults<PS, []>>;
}

export type ProvableCircuits<PS> = {
  react(context: __compactRuntime.CircuitContext<PS>,
        notAfter_0: bigint,
        action_0: Uint8Array): Promise<__compactRuntime.CircuitResults<PS, []>>;
}

export type PureCircuits = {
  rfcLeaf(eid_0: Uint8Array): Uint8Array;
  rfcNode(l_0: Uint8Array, r_0: Uint8Array): Uint8Array;
  anchorLeafOf(window_0: bigint, root_0: Uint8Array): Uint8Array;
}

export type Circuits<PS> = {
  rfcLeaf(context: __compactRuntime.CircuitContext<PS>, eid_0: Uint8Array): Promise<__compactRuntime.CircuitResults<PS, Uint8Array>>;
  rfcNode(context: __compactRuntime.CircuitContext<PS>,
          l_0: Uint8Array,
          r_0: Uint8Array): Promise<__compactRuntime.CircuitResults<PS, Uint8Array>>;
  anchorLeafOf(context: __compactRuntime.CircuitContext<PS>,
               window_0: bigint,
               root_0: Uint8Array): Promise<__compactRuntime.CircuitResults<PS, Uint8Array>>;
  react(context: __compactRuntime.CircuitContext<PS>,
        notAfter_0: bigint,
        action_0: Uint8Array): Promise<__compactRuntime.CircuitResults<PS, []>>;
}

export type Ledger = {
  readonly registry: { bytes: Uint8Array };
  readonly networkId: Uint8Array;
  readonly lifetime: bigint;
  readonly windowLength: bigint;
  consumed: {
    isEmpty(): boolean;
    size(): bigint;
    member(key_0: Uint8Array): boolean;
    lookup(key_0: Uint8Array): Uint8Array;
    [Symbol.iterator](): Iterator<[Uint8Array, Uint8Array]>
  };
  readonly reactions: bigint;
}

export declare class Contract<PS = any, W extends Witnesses<PS> = Witnesses<PS>> {
  witnesses: W;
  circuits: Circuits<PS>;
  impureCircuits: ImpureCircuits<PS>;
  provableCircuits: ProvableCircuits<PS>;
  constructor(witnesses: W);
  initialState(context: __compactRuntime.ConstructorContext<PS>,
               r_0: { bytes: Uint8Array },
               n_0: Uint8Array): Promise<__compactRuntime.ConstructorResult<PS>>;
}

export declare function ledger(state: __compactRuntime.StateValue | __compactRuntime.ChargedState): Ledger;
export declare const pureCircuits: PureCircuits;
export declare const expectedVk: Record<string, string>;
export declare const circuitSignatures: __compactRuntime.CircuitSignatures;
export declare const declaredInterfaces: __compactRuntime.DeclaredInterfaces;
