import pathlib
import re
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class SecurityRegressionTests(unittest.TestCase):
    def test_legacy_installer_does_not_package_add_path(self):
        build = (ROOT / 'windows-installer' / 'build.py').read_text(encoding='utf-8')
        installer = (ROOT / 'windows-installer' / 'diffuse.iss').read_text(encoding='utf-8')
        self.assertNotIn("ADD_PATH_HOME", build)
        self.assertNotRegex(
            installer,
            re.compile(r'^Filename:.*add_path', re.MULTILINE),
        )

    def test_xsltproc_calls_disable_network(self):
        files = [
            ROOT / 'utils' / 'makemanual.py',
            ROOT / 'utils' / 'makepdfmanual.sh',
            ROOT / 'windows-installer' / 'build.py',
        ]
        for path in files:
            with self.subTest(path=path):
                lines = path.read_text(encoding='utf-8').splitlines()
                commands = [
                    line for line in lines
                    if 'xsltproc' in line and (
                        'cmd =' in line or line.lstrip().startswith('xsltproc ')
                    )
                ]
                self.assertTrue(commands, str(path))
                self.assertTrue(all('--nonet' in line for line in commands), str(path))

    def test_flatpak_manifest_has_no_host_escape(self):
        manifest = (ROOT / 'io.github.mightycreak.Diffuse.yml').read_text(encoding='utf-8')
        self.assertNotIn('--talk-name=org.freedesktop.Flatpak', manifest)
        self.assertNotIn('--filesystem=home', manifest)
        self.assertNotIn('-Duse_flatpak=true', manifest)

    def test_workflows_pin_actions_to_full_sha(self):
        for path in (ROOT / '.github' / 'workflows').glob('*.yml'):
            for line in path.read_text(encoding='utf-8').splitlines():
                if 'uses:' not in line or line.lstrip().startswith('#'):
                    continue
                reference = line.split('@', 1)[1].split()[0]
                self.assertRegex(reference, r'^[0-9a-f]{40}$', str(path))

    def test_windows_and_linux_versions_match(self):
        meson = (ROOT / 'meson.build').read_text(encoding='utf-8')
        launcher = (ROOT / 'packaging' / 'windows' / 'launcher.py').read_text(encoding='utf-8')
        meson_version = re.search(r"version: '([^']+)'", meson).group(1)
        windows_version = re.search(r"VERSION = '([^']+)'", launcher).group(1)
        self.assertEqual(meson_version, windows_version)

    def test_direct_python_dependencies_are_exactly_pinned(self):
        requirements = [
            ROOT / 'requirements.txt',
            ROOT / 'requirements.dev.txt',
        ]
        for path in requirements:
            with self.subTest(path=path.name):
                contents = path.read_text(encoding='utf-8')
                self.assertNotIn('~=', contents)
                for line in contents.splitlines():
                    if line and not line.startswith(('#', '-r')):
                        self.assertIn('==', line)

    def test_postinstall_skips_absent_optional_directories(self):
        postinstall = (
            ROOT / 'build-aux' / 'meson' / 'postinstall.py'
        ).read_text(encoding='utf-8')
        self.assertIn("if path.isdir(schemas):", postinstall)

    def test_windows_build_bundles_russian_catalog(self):
        build = (ROOT / 'packaging' / 'windows' / 'build.sh').read_text(
            encoding='utf-8'
        )
        spec = (ROOT / 'packaging' / 'windows' / 'diffuse.spec').read_text(
            encoding='utf-8'
        )
        launcher = (ROOT / 'packaging' / 'windows' / 'launcher.py').read_text(
            encoding='utf-8'
        )
        self.assertIn('msgfmt', build)
        self.assertIn('diffuse.mo', build)
        self.assertIn("'locale' / 'ru' / 'LC_MESSAGES'", spec)
        self.assertIn("os.environ.setdefault('LANGUAGE'", launcher)


if __name__ == '__main__':
    unittest.main()
