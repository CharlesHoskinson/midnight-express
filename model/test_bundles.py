import copy,json,shutil,tempfile,unittest
from pathlib import Path
from bundles import load_bundle,publish_bundle,register_legacy,negotiate,digest,encode,filehash
from validator import ROOT

class Bundles(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
  for name in ['bundles','profiles','releases']:shutil.copytree(ROOT/name,self.root/name)
 def tearDown(self):self.temp.cleanup()
 def loaded(self):return load_bundle(self.root,'rfq.v0.2')
 def test_verified_snapshot_and_no_implementation_hash(self):
  m,h=self.loaded();self.assertEqual(set(m['resources']),{'schema.json','rules.json','core.json'});self.assertEqual(m['schemaObject']['properties']['mpeprofile']['const'],'rfq.v0.2')
 def test_immutable_bundle_refuses_overwrite(self):
  m,h=self.loaded();folder=self.root/'bundles'/h[7:];(folder/'schema.json').write_text('{}')
  with self.assertRaises(ValueError):publish_bundle(self.root,'rfq.v0.2',m['schemaObject'],m['coreObject'],m['normative'])
 def test_two_installed_contracts_and_exact_selection(self):
  old,h1=self.loaded();rules=copy.deepcopy(old['normative']);rules['rules'].append('test-only reviewed alternative')
  h2=publish_bundle(self.root,'rfq.v0.2',old['schemaObject'],old['coreObject'],rules)
  self.assertNotEqual(h1,h2);self.assertEqual(load_bundle(self.root,'rfq.v0.2',h1)[1],h1);self.assertEqual(load_bundle(self.root,'rfq.v0.2',h2)[1],h2);self.assertEqual(negotiate([h1,h2],[h2]),[h2]);self.assertEqual(negotiate([h1],[h2]),[])
 def test_legacy_registered_read_only(self):
  installed=json.loads((self.root/'profiles/installed.json').read_text());legacy=[(h,e) for h,e in installed.items() if e['mode']=='historical-read-only'];self.assertEqual(len(legacy),3)
  for h,e in legacy:
   with self.assertRaisesRegex(ValueError,'historical-read-only'):load_bundle(self.root,e['profile'],h)
 def test_integrity_tamper(self):
  _,h=self.loaded();(self.root/'bundles'/h[7:]/'rules.json').write_text('{}')
  with self.assertRaisesRegex(ValueError,'integrity'):self.loaded()
 def test_symlink_and_escape(self):
  _,h=self.loaded();f=self.root/'bundles'/h[7:]/'schema.json';f.unlink();f.symlink_to('/tmp/untrusted-mpe-schema')
  with self.assertRaisesRegex(ValueError,'escape'):self.loaded()
  p=self.root/'profiles/installed.json';installed=json.loads(p.read_text());installed[h]['directory']='../outside';p.write_text(json.dumps(installed))
  with self.assertRaises(ValueError):self.loaded()
 def test_remote_dynamic_reference_refused_before_install(self):
  m,_=self.loaded()
  for k in ['$ref','$dynamicRef','$recursiveRef']:
   s=copy.deepcopy(m['schemaObject']);s[k]='https://no-fetch.invalid/schema'
   with self.assertRaisesRegex(ValueError,'standalone'):publish_bundle(self.root,'rfq.v0.2',s,m['coreObject'],m['normative'])
 def test_unknown_contract_and_capability_bounds(self):
  with self.assertRaises(ValueError):load_bundle(self.root,'rfq.v0.2','sha256:'+'0'*64)
  with self.assertRaises(ValueError):negotiate(['https://no-fetch.invalid'],[])
 def test_dependency_changes_do_not_rekey_unrelated_profile(self):
  m,_=load_bundle(self.root,'invoice.v0.2');rfq=json.loads((self.root/'profiles/lock.json').read_text())['rfq.v0.2'];rules=copy.deepcopy(m['normative']);rules['rules'].append('test-only invoice meaning correction');new=publish_bundle(self.root,'invoice.v0.2',m['schemaObject'],m['coreObject'],rules);self.assertNotEqual(new,load_bundle(ROOT,'invoice.v0.2')[1]);self.assertEqual(load_bundle(self.root,'rfq.v0.2')[1],rfq)
if __name__=='__main__':unittest.main()
