"""Offline checks for proposed catalog metadata, never runtime event validation."""
from copy import deepcopy
import json
from pathlib import Path
import unittest
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator, FormatChecker, ValidationError

HERE = Path(__file__).resolve().parent
SCHEMA = json.loads((HERE / 'catalog.schema.json').read_text())
CATALOG = json.loads((HERE / 'chain-event-catalog.json').read_text())
Draft202012Validator.check_schema(SCHEMA)
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())


def validate_catalog(catalog):
    """Validate closed metadata plus identity, coverage and evidence invariants."""
    VALIDATOR.validate(catalog)
    ids = set()
    semantic_keys = set()
    coverage = set()
    for event in catalog['events']:
        expected = f"mpe.{event['chain']}.{event['family']}.{event['semanticName']}.v1"
        if event['id'] != expected:
            raise ValueError('event ID disagrees with chain/family/semantic name')
        key = (event['chain'], event['family'], event['semanticName'])
        if event['id'] in ids or key in semantic_keys:
            raise ValueError('duplicate catalog identity')
        ids.add(event['id'])
        semantic_keys.add(key)
        coverage.add((event['chain'], event['family']))
        parsed = urlsplit(event['primarySource'])
        if not parsed.hostname or parsed.username or parsed.password:
            raise ValueError('primary source must be an HTTPS source without credentials')
        if event['evidenceKind'] == 'intent':
            if event['messageKind'] not in ('intent', 'rpc-request', 'subscription-control'):
                raise ValueError('intent cannot be an observation or response')
        elif event['messageKind'] in ('intent', 'rpc-request', 'subscription-control'):
            raise ValueError('request/control requires intent evidence kind')
        if event['evidenceKind'] == 'derived' and event['scope'] != 'local':
            raise ValueError('derived claims must declare local provenance')
    expected_coverage = {(chain, family) for chain in catalog['chains'] for family in catalog['families']}
    if coverage != expected_coverage:
        raise ValueError('missing chain/family coverage')
    return len(ids)


class CatalogTests(unittest.TestCase):
    def test_catalog_valid(self):
        self.assertGreater(validate_catalog(CATALOG), 0)

    def reject(self, mutate):
        candidate = deepcopy(CATALOG)
        mutate(candidate)
        with self.assertRaises((ValueError, ValidationError)):
            validate_catalog(candidate)

    def test_duplicate_identity_rejected(self):
        self.reject(lambda c: c['events'].append(deepcopy(c['events'][0])))

    def test_cross_chain_identity_rejected(self):
        self.reject(lambda c: c['events'][0].update(chain='solana'))

    def test_unknown_metadata_rejected(self):
        self.reject(lambda c: c.update(runtimeProfile='enabled'))

    def test_unknown_event_fields_rejected(self):
        self.reject(lambda c: c['events'][0].update(payload={'amount': '1'}))

    def test_authority_escalation_rejected(self):
        self.reject(lambda c: c['events'][0].update(effectAuthority=True))
        self.reject(lambda c: c.update(effectAuthority=True))

    def test_implementation_claim_rejected(self):
        self.reject(lambda c: c['events'][0].update(status='implemented'))
        self.reject(lambda c: c.update(runtimeContracts=True))
        self.reject(lambda c: c.update(exhaustive=True))

    def test_source_required(self):
        self.reject(lambda c: c['events'][0].pop('primarySource'))
        self.reject(lambda c: c['events'][0].update(primarySource='file:///tmp/source'))
        self.reject(lambda c: c['events'][0].update(primarySource='https://user:secret@example.org/source'))

    def test_missing_family_rejected(self):
        self.reject(lambda c: c.update(events=[e for e in c['events'] if e['family'] != 'bridge']))

    def test_request_is_not_observation(self):
        def mutate(c):
            next(e for e in c['events'] if e['evidenceKind'] == 'intent')['messageKind'] = 'observation'
        self.reject(mutate)

    def test_derived_claim_is_not_native(self):
        def mutate(c):
            next(e for e in c['events'] if e['evidenceKind'] == 'derived')['scope'] = 'chain'
        self.reject(mutate)

    def test_no_unified_confirmation_enum(self):
        self.assertNotIn('confirmation', SCHEMA['properties'])
        by_id = {e['id']: e for e in CATALOG['events']}
        for chain, name in [('ethereum', 'safe-head-observed'), ('ethereum', 'finalized-head-observed'), ('solana', 'processed-observed'), ('solana', 'confirmed-observed'), ('solana', 'finalized-observed')]:
            event = by_id[f'mpe.{chain}.finality.{name}.v1']
            self.assertFalse(event['effectAuthority'])
            self.assertEqual(event['messageKind'], 'observation')


if __name__ == '__main__':
    print(f"Proposed catalog: {validate_catalog(CATALOG)} entries; metadata only, no runtime contracts.", flush=True)
    unittest.main()
