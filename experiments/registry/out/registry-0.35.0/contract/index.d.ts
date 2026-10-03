import type * as __compactRuntime from '@midnight-ntwrk/compact-runtime';

export type Params = { epochLength: bigint;
                       membershipPeriod: bigint;
                       rootWindow: bigint;
                       quota: bigint[];
                       anchorWindow: bigint;
                       anchorHistory: bigint;
                       shardCount: bigint;
                       activationHeight: bigint;
                       maxVersion: bigint;
                       bootstrapHash: Uint8Array
                     };

export type PendingParams = { params: Params; effectiveAt: bigint };

export type Roles = { relay: boolean;
                      store: boolean;
                      bootstrapper: boolean;
                      gateway: boolean;
                      anchorer: boolean
                    };

export type RelayEntry = { operatorId: Uint8Array;
                           roles: Roles;
                           keyCommitment: Uint8Array
                         };

export type AnchorRecord = { window: bigint; root: Uint8Array; counts: bigint[]
                           };

export type AnchorLeaf = { domain: Uint8Array; window: bigint; root: Uint8Array
                         };

export type MemberLeaf = { domain: Uint8Array; idc: Uint8Array; quota: bigint[]
                         };

export type Share = { eid: Uint8Array; y: bigint };

export type Evidence = { a0: bigint;
                         epoch: bigint;
                         sizeClass: bigint;
                         credit: bigint;
                         quota: bigint[];
                         s1: Share;
                         s2: Share
                       };

export type Witnesses<PS> = {
  stewardSecret(context: __compactRuntime.WitnessContext<Ledger, PS>): [PS, Uint8Array];
  relaySecret(context: __compactRuntime.WitnessContext<Ledger, PS>): [PS, Uint8Array];
  revocationEvidence(context: __compactRuntime.WitnessContext<Ledger, PS>): [PS, Evidence];
  memberPath(context: __compactRuntime.WitnessContext<Ledger, PS>): [PS, { leaf: Uint8Array,
                                                                           path: { sibling: { field: bigint
                                                                                            },
                                                                                   goes_left: boolean
                                                                                 }[]
                                                                         }];
}

export type ImpureCircuits<PS> = {
  register(context: __compactRuntime.CircuitContext<PS>,
           idc_0: Uint8Array,
           period_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  revoke(context: __compactRuntime.CircuitContext<PS>,
         period_0: bigint,
         reason_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  prunePeriod(context: __compactRuntime.CircuitContext<PS>, period_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  addRelay(context: __compactRuntime.CircuitContext<PS>,
           peer_0: Uint8Array,
           entry_0: RelayEntry,
           reason_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  removeRelay(context: __compactRuntime.CircuitContext<PS>,
              peer_0: Uint8Array,
              reason_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  proposeParams(context: __compactRuntime.CircuitContext<PS>,
                p_0: Params,
                now_0: bigint,
                reason_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  activateParams(context: __compactRuntime.CircuitContext<PS>): Promise<__compactRuntime.CircuitResults<PS, []>>;
  pause(context: __compactRuntime.CircuitContext<PS>, reason_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  unpause(context: __compactRuntime.CircuitContext<PS>, reason_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  setSteward(context: __compactRuntime.CircuitContext<PS>,
             newKey_0: Uint8Array,
             reason_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  postAnchor(context: __compactRuntime.CircuitContext<PS>,
             peer_0: Uint8Array,
             window_0: bigint,
             q_0: bigint,
             slot_0: bigint,
             root_0: Uint8Array,
             counts_0: bigint[]): Promise<__compactRuntime.CircuitResults<PS, []>>;
  pruneAnchor(context: __compactRuntime.CircuitContext<PS>, slot_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  anchorRootValid(context: __compactRuntime.CircuitContext<PS>,
                  rt_0: { field: bigint }): Promise<__compactRuntime.CircuitResults<PS, boolean>>;
}

export type ProvableCircuits<PS> = {
  register(context: __compactRuntime.CircuitContext<PS>,
           idc_0: Uint8Array,
           period_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  revoke(context: __compactRuntime.CircuitContext<PS>,
         period_0: bigint,
         reason_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  prunePeriod(context: __compactRuntime.CircuitContext<PS>, period_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  addRelay(context: __compactRuntime.CircuitContext<PS>,
           peer_0: Uint8Array,
           entry_0: RelayEntry,
           reason_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  removeRelay(context: __compactRuntime.CircuitContext<PS>,
              peer_0: Uint8Array,
              reason_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  proposeParams(context: __compactRuntime.CircuitContext<PS>,
                p_0: Params,
                now_0: bigint,
                reason_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  activateParams(context: __compactRuntime.CircuitContext<PS>): Promise<__compactRuntime.CircuitResults<PS, []>>;
  pause(context: __compactRuntime.CircuitContext<PS>, reason_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  unpause(context: __compactRuntime.CircuitContext<PS>, reason_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  setSteward(context: __compactRuntime.CircuitContext<PS>,
             newKey_0: Uint8Array,
             reason_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  postAnchor(context: __compactRuntime.CircuitContext<PS>,
             peer_0: Uint8Array,
             window_0: bigint,
             q_0: bigint,
             slot_0: bigint,
             root_0: Uint8Array,
             counts_0: bigint[]): Promise<__compactRuntime.CircuitResults<PS, []>>;
  pruneAnchor(context: __compactRuntime.CircuitContext<PS>, slot_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  anchorRootValid(context: __compactRuntime.CircuitContext<PS>,
                  rt_0: { field: bigint }): Promise<__compactRuntime.CircuitResults<PS, boolean>>;
}

export type PureCircuits = {
  stewardKeyOf(sk_0: Uint8Array): Uint8Array;
  relayKeyOf(sk_0: Uint8Array): Uint8Array;
  memberLeafOf(idc_0: Uint8Array, quota_0: bigint[]): Uint8Array;
  idcOf(a0_0: bigint): Uint8Array;
  anchorLeafOf(window_0: bigint, root_0: Uint8Array): Uint8Array;
  rlnA1(a0_0: bigint, epoch_0: bigint, sizeClass_0: bigint, credit_0: bigint): bigint;
  rlnX(eid_0: Uint8Array): bigint;
}

export type Circuits<PS> = {
  stewardKeyOf(context: __compactRuntime.CircuitContext<PS>, sk_0: Uint8Array): Promise<__compactRuntime.CircuitResults<PS, Uint8Array>>;
  relayKeyOf(context: __compactRuntime.CircuitContext<PS>, sk_0: Uint8Array): Promise<__compactRuntime.CircuitResults<PS, Uint8Array>>;
  memberLeafOf(context: __compactRuntime.CircuitContext<PS>,
               idc_0: Uint8Array,
               quota_0: bigint[]): Promise<__compactRuntime.CircuitResults<PS, Uint8Array>>;
  idcOf(context: __compactRuntime.CircuitContext<PS>, a0_0: bigint): Promise<__compactRuntime.CircuitResults<PS, Uint8Array>>;
  anchorLeafOf(context: __compactRuntime.CircuitContext<PS>,
               window_0: bigint,
               root_0: Uint8Array): Promise<__compactRuntime.CircuitResults<PS, Uint8Array>>;
  rlnA1(context: __compactRuntime.CircuitContext<PS>,
        a0_0: bigint,
        epoch_0: bigint,
        sizeClass_0: bigint,
        credit_0: bigint): Promise<__compactRuntime.CircuitResults<PS, bigint>>;
  rlnX(context: __compactRuntime.CircuitContext<PS>, eid_0: Uint8Array): Promise<__compactRuntime.CircuitResults<PS, bigint>>;
  register(context: __compactRuntime.CircuitContext<PS>,
           idc_0: Uint8Array,
           period_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  revoke(context: __compactRuntime.CircuitContext<PS>,
         period_0: bigint,
         reason_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  prunePeriod(context: __compactRuntime.CircuitContext<PS>, period_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  addRelay(context: __compactRuntime.CircuitContext<PS>,
           peer_0: Uint8Array,
           entry_0: RelayEntry,
           reason_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  removeRelay(context: __compactRuntime.CircuitContext<PS>,
              peer_0: Uint8Array,
              reason_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  proposeParams(context: __compactRuntime.CircuitContext<PS>,
                p_0: Params,
                now_0: bigint,
                reason_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  activateParams(context: __compactRuntime.CircuitContext<PS>): Promise<__compactRuntime.CircuitResults<PS, []>>;
  pause(context: __compactRuntime.CircuitContext<PS>, reason_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  unpause(context: __compactRuntime.CircuitContext<PS>, reason_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  setSteward(context: __compactRuntime.CircuitContext<PS>,
             newKey_0: Uint8Array,
             reason_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  postAnchor(context: __compactRuntime.CircuitContext<PS>,
             peer_0: Uint8Array,
             window_0: bigint,
             q_0: bigint,
             slot_0: bigint,
             root_0: Uint8Array,
             counts_0: bigint[]): Promise<__compactRuntime.CircuitResults<PS, []>>;
  pruneAnchor(context: __compactRuntime.CircuitContext<PS>, slot_0: bigint): Promise<__compactRuntime.CircuitResults<PS, []>>;
  anchorRootValid(context: __compactRuntime.CircuitContext<PS>,
                  rt_0: { field: bigint }): Promise<__compactRuntime.CircuitResults<PS, boolean>>;
}

export type Ledger = {
  readonly networkId: Uint8Array;
  readonly paramsDelay: bigint;
  readonly steward: Uint8Array;
  readonly paused: boolean;
  readonly params: Params;
  readonly pending: { is_some: boolean, value: PendingParams };
  members: {
    isEmpty(): boolean;
    size(): bigint;
    member(key_0: bigint): boolean;
    lookup(key_0: bigint): {
      isFull(): boolean;
      checkRoot(rt_0: { field: bigint }): boolean;
      root(): __compactRuntime.MerkleTreeDigest;
      firstFree(): bigint;
      pathForLeaf(index_0: bigint, leaf_0: Uint8Array): __compactRuntime.MerkleTreePath<Uint8Array>;
      findPathForLeaf(leaf_0: Uint8Array): __compactRuntime.MerkleTreePath<Uint8Array> | undefined;
      history(): Iterator<__compactRuntime.MerkleTreeDigest>
    }
  };
  revoked: {
    isEmpty(): boolean;
    size(): bigint;
    member(elem_0: Uint8Array): boolean;
    [Symbol.iterator](): Iterator<Uint8Array>
  };
  relays: {
    isEmpty(): boolean;
    size(): bigint;
    member(key_0: Uint8Array): boolean;
    lookup(key_0: Uint8Array): RelayEntry;
    [Symbol.iterator](): Iterator<[Uint8Array, RelayEntry]>
  };
  anchors: {
    isEmpty(): boolean;
    size(): bigint;
    member(key_0: bigint): boolean;
    lookup(key_0: bigint): AnchorRecord;
    [Symbol.iterator](): Iterator<[bigint, AnchorRecord]>
  };
  anchorTree: {
    isFull(): boolean;
    checkRoot(rt_0: { field: bigint }): boolean;
    root(): __compactRuntime.MerkleTreeDigest;
    firstFree(): bigint;
    pathForLeaf(index_0: bigint, leaf_0: Uint8Array): __compactRuntime.MerkleTreePath<Uint8Array>;
    findPathForLeaf(leaf_0: Uint8Array): __compactRuntime.MerkleTreePath<Uint8Array> | undefined;
    history(): Iterator<__compactRuntime.MerkleTreeDigest>
  };
}

export declare class Contract<PS = any, W extends Witnesses<PS> = Witnesses<PS>> {
  witnesses: W;
  circuits: Circuits<PS>;
  impureCircuits: ImpureCircuits<PS>;
  provableCircuits: ProvableCircuits<PS>;
  constructor(witnesses: W);
  initialState(context: __compactRuntime.ConstructorContext<PS>,
               stewardKey_0: Uint8Array,
               n_0: Uint8Array,
               delay_0: bigint,
               p_0: Params): Promise<__compactRuntime.ConstructorResult<PS>>;
}

export declare function ledger(state: __compactRuntime.StateValue | __compactRuntime.ChargedState): Ledger;
export declare const pureCircuits: PureCircuits;
export declare const expectedVk: Record<string, string>;
export declare const circuitSignatures: __compactRuntime.CircuitSignatures;
export declare const declaredInterfaces: __compactRuntime.DeclaredInterfaces;
