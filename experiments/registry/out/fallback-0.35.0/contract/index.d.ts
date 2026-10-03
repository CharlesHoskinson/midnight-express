import type * as __compactRuntime from '@midnight-ntwrk/compact-runtime';

export type Witnesses<PS> = {
}

export type ImpureCircuits<PS> = {
  publishPart(context: __compactRuntime.CircuitContext<PS>,
              name_0: Uint8Array,
              payload_0: Uint8Array): Promise<__compactRuntime.CircuitResults<PS, []>>;
  publishClass0(context: __compactRuntime.CircuitContext<PS>, body_0: Uint8Array): Promise<__compactRuntime.CircuitResults<PS, []>>;
  publishClass1(context: __compactRuntime.CircuitContext<PS>,
                parts_0: Uint8Array[]): Promise<__compactRuntime.CircuitResults<PS, []>>;
  publishClass2(context: __compactRuntime.CircuitContext<PS>,
                parts_0: Uint8Array[]): Promise<__compactRuntime.CircuitResults<PS, []>>;
}

export type ProvableCircuits<PS> = {
  publishPart(context: __compactRuntime.CircuitContext<PS>,
              name_0: Uint8Array,
              payload_0: Uint8Array): Promise<__compactRuntime.CircuitResults<PS, []>>;
  publishClass0(context: __compactRuntime.CircuitContext<PS>, body_0: Uint8Array): Promise<__compactRuntime.CircuitResults<PS, []>>;
  publishClass1(context: __compactRuntime.CircuitContext<PS>,
                parts_0: Uint8Array[]): Promise<__compactRuntime.CircuitResults<PS, []>>;
  publishClass2(context: __compactRuntime.CircuitContext<PS>,
                parts_0: Uint8Array[]): Promise<__compactRuntime.CircuitResults<PS, []>>;
}

export type PureCircuits = {
}

export type Circuits<PS> = {
  publishPart(context: __compactRuntime.CircuitContext<PS>,
              name_0: Uint8Array,
              payload_0: Uint8Array): Promise<__compactRuntime.CircuitResults<PS, []>>;
  publishClass0(context: __compactRuntime.CircuitContext<PS>, body_0: Uint8Array): Promise<__compactRuntime.CircuitResults<PS, []>>;
  publishClass1(context: __compactRuntime.CircuitContext<PS>,
                parts_0: Uint8Array[]): Promise<__compactRuntime.CircuitResults<PS, []>>;
  publishClass2(context: __compactRuntime.CircuitContext<PS>,
                parts_0: Uint8Array[]): Promise<__compactRuntime.CircuitResults<PS, []>>;
}

export type Ledger = {
}

export declare class Contract<PS = any, W extends Witnesses<PS> = Witnesses<PS>> {
  witnesses: W;
  circuits: Circuits<PS>;
  impureCircuits: ImpureCircuits<PS>;
  provableCircuits: ProvableCircuits<PS>;
  constructor(witnesses: W);
  initialState(context: __compactRuntime.ConstructorContext<PS>): Promise<__compactRuntime.ConstructorResult<PS>>;
}

export declare function ledger(state: __compactRuntime.StateValue | __compactRuntime.ChargedState): Ledger;
export declare const pureCircuits: PureCircuits;
export declare const expectedVk: Record<string, string>;
export declare const circuitSignatures: __compactRuntime.CircuitSignatures;
export declare const declaredInterfaces: __compactRuntime.DeclaredInterfaces;
