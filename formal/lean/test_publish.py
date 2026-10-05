"""Publication rejects stale proof citations, profile pins and downloaded source bytes."""
import contextlib
import io
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import publish


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.here = self.root / 'formal/lean'
        self.public = self.root / 'website/dist/formal/lean'
        for source in publish.sources():
            target = self.here / source.relative_to(publish.HERE)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        page = self.root / 'website/dist/specification.html'
        page.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(publish.ROOT / 'website/dist/specification.html', page)
        self.expected = publish.profile_pins()
        self.scope = patch.multiple(publish, ROOT=self.root, HERE=self.here, PUBLIC=self.public)
        self.scope.start()
        self.addCleanup(self.scope.stop)
        self.run_mode('--update')

    def run_mode(self, mode):
        with patch('sys.argv', ['publish.py', mode]), contextlib.redirect_stdout(io.StringIO()):
            publish.main()

    def test_downloaded_source_change_rejected(self):
        self.run_mode('--check')
        target = self.public / 'MidnightExpress/Replay.lean'
        target.write_text(target.read_text() + '\n-- stale public copy\n')
        with self.assertRaisesRegex(ValueError, 'Public source drift'):
            self.run_mode('--check')

    def test_nonexistent_cited_proof_rejected(self):
        page = self.root / 'website/dist/specification.html'
        page.write_text(page.read_text() + '<p data-proof="imaginary_guarantee">example</p>')
        with self.assertRaisesRegex(ValueError, 'missing Lean declarations.*imaginary_guarantee'):
            self.run_mode('--check')

    def test_changed_profile_pin_rejected(self):
        pin = self.here / 'MidnightExpress/ProfilePins.lean'
        pin.write_text(pin.read_text() + '\n-- unreviewed pin drift\n')
        with self.assertRaisesRegex(ValueError, 'ProfilePins.lean drift'):
            self.run_mode('--check')

    def test_extra_downloadable_file_rejected(self):
        (self.public / 'stale.lean').write_text('def oldClaim := true\n')
        with self.assertRaisesRegex(ValueError, 'Unexpected public source files'):
            self.run_mode('--check')


if __name__ == '__main__':
    unittest.main()
