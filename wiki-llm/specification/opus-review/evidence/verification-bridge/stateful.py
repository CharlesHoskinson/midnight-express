import copy, json, random, sys
sys.path.insert(0, '/tmp/mpe-lean-opus-review/verification-bridge')
from diff import BASE, CTX, T, check, Harness, Invalid, digest, business_digest, sync_evidence, HEADER, OUT
V = {'offchain-quote-valid': '.quote', 'sandbox-candidate-only': '.candidate', 'final-payment-evidence-only': '.paymentFinal',
     'payment-evidence-pending-or-reversed': '.paymentOther', 'duplicate-event': '.duplicateEvent', 'duplicate-action': '.duplicateAction'}
def variants(name):
    b = BASE[name]; out = {'base': b}
    e = copy.deepcopy(b); e['id'] = 'event:redelivery'; out['new-id'] = e
    e = copy.deepcopy(b); e['id'] = 'event:redelivery2'; e['time'] = T('10:59:00'); out['new-id-earlier-time'] = e
    e = copy.deepcopy(b); e['data']['validUntil' if 'validUntil' in b['data'] else 'observedAt'] = T('12:59:00' if 'validUntil' in b['data'] else '10:59:00'); out['same-id-changed'] = e
    e = copy.deepcopy(out['same-id-changed']); e['id'] = 'event:changed-intent'; out['new-id-changed'] = e
    return out
def run(n, seed):
    rng = random.Random(seed); seqs = []
    for _ in range(n):
        name = rng.choice(['agent', 'rfq', 'invoice-final', 'invoice-pending'])
        pool = variants(name); h = Harness(copy.deepcopy(CTX)); steps = []
        for _ in range(rng.randint(2, 6)):
            label = rng.choice(list(pool)); e = copy.deepcopy(pool[label]); c = copy.deepcopy(CTX)
            if rng.random() < 0.15: c['now'] = T('13:00:00')   # context moves on: stale input
            if 'invoiceId' in e['data']: sync_evidence(e, c)
            h.context = c
            try: status = h.check(json.dumps(e, separators=(',', ':')))['status']
            except Invalid: status = 'reject'
            steps.append((label, check.event(e), check.context(c, e), digest(e), business_digest(e), status))
        seqs.append((name, steps))
    lines = list(HEADER) + ['def runSeq : ReplayState → List (Context × Event × String × String) → List (Option Verdict)',
        '  | _, [] => []', '  | s, (c, e, ed, id) :: rest => match check c s e ed id with',
        '    | none => none :: runSeq s rest', '    | some (r, s2) => some r.verdict :: runSeq s2 rest', '']
    entries = []
    for i, (name, steps) in enumerate(seqs):
        for j, (_, ev, cx, ed, idg, _) in enumerate(steps):
            lines += [f'def e{i}_{j} : Event := {ev}', f'def c{i}_{j} : Context := {cx}']
        lst = ', '.join(f'(c{i}_{j}, e{i}_{j}, "{s[3]}", "{s[4]}")' for j, s in enumerate(steps))
        exp = ', '.join('none' if s[-1] == 'reject' else f'some {V[s[-1]]}' for s in steps)
        entries.append(f'({i}, [{lst}], [{exp}])')
    lines.append('def seqs : List (Nat × List (Context × Event × String × String) × List (Option Verdict)) := [' + ', '.join(entries) + ']')
    lines += ['#eval do', '  let bad := seqs.filter (fun (p : Nat × List (Context × Event × String × String) × List (Option Verdict)) => runSeq {} p.2.1 != p.2.2)',
              '  IO.println s!"STATEFUL sequences={seqs.length} steps={(seqs.map (fun (p : Nat × List (Context × Event × String × String) × List (Option Verdict)) => p.2.1.length)).foldl (· + ·) 0} mismatches={bad.map (fun (p : Nat × List (Context × Event × String × String) × List (Option Verdict)) => p.1)}"']
    (OUT / 'stateful.lean').write_text('\n'.join(lines))
    from collections import Counter
    print(Counter(s[-1] for _, st in seqs for s in st))
run(int(sys.argv[1]), int(sys.argv[2]))
