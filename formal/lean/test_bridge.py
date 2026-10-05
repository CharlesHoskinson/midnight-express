"""Regression tests for the trusted translator's fail-closed fidelity boundary."""
import copy
import unittest

import check
from bridge import coefficient, context, decimal, event, instant, natural, text


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.cases = check.collect()
        self.agent = next(e for label, e, _, _ in self.cases if label == 'fixture_agent')
        self.ctx = self.cases[0][3]

    def test_every_vector_roundtrips(self):
        for label, e, _, c in self.cases:
            with self.subTest(label=label):
                self.assertIsInstance(event(e), str)
                self.assertIsInstance(context(c, 'fixtureCommitment'), str)

    def test_noncanonical_coefficients_rejected(self):
        for malformed in ('01', ' 7 ', '+1', '-1', '1_000', '١', '１２', '', 1, True):
            with self.subTest(value=malformed), self.assertRaises(ValueError):
                coefficient(malformed)

    def test_negative_model_bound_and_scales_preserved(self):
        source = {'coefficient': '99999999999999999900', 'scale': 3}
        node = decimal(source)
        self.assertEqual(node.wire, source)
        self.assertIn('99999999999999999900', node.code)
        self.assertIn('scale := 3', node.code)
        self.assertEqual(coefficient('0').code, '0')

    def test_unread_keys_rejected_at_every_level(self):
        for path in ((), ('data',), ('data', 'proposal'), ('data', 'proposal', 'budget')):
            e = copy.deepcopy(self.agent); target = e
            for key in path: target = target[key]
            target['memo'] = 'unexpected'
            with self.subTest(path=path), self.assertRaises(ValueError): event(e)
        c = copy.deepcopy(self.ctx); c['sources'][next(iter(c['sources']))]['memo'] = 'unexpected'
        with self.assertRaises(ValueError): context(c, 'fixtureCommitment')

    def test_fixed_tags_rejected_without_repair(self):
        for field, value in (('operation', 'Execute'), ('environment', 'Production')):
            e = copy.deepcopy(self.agent); e['data']['proposal'][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError): event(e)
        e = copy.deepcopy(self.agent); del e['data']['human']
        with self.assertRaises(ValueError): event(e)

    def test_canonical_instant_and_nat(self):
        for bad in ('2026-10-4T11:00:00.000Z', '2026-02-30T11:00:00.000Z', '2026-10-04T11:00:00Z'):
            with self.subTest(value=bad), self.assertRaises(ValueError): instant(bad)
        self.assertEqual(instant('1969-12-31T23:59:59.000Z').code, '(-1)')
        for bad in (-1, True, '1', 1.0):
            with self.subTest(value=bad), self.assertRaises(ValueError): natural(bad)

    def test_lean_escape_spelling(self):
        node = text('x\b\f\x00\\"😀')
        self.assertEqual(node.wire, 'x\b\f\x00\\"😀')
        self.assertEqual(node.code, '"x\\x08\\x0c\\x00\\\\\\"😀"')
        with self.assertRaises(UnicodeError): text('\ud800')


if __name__ == '__main__':
    unittest.main()
