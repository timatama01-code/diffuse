import io
import os
import stat
import tempfile
import unittest

from unittest import mock

from diffuse import security


class SecurityTests(unittest.TestCase):
    def test_rejects_oversized_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, 'large.txt')
            with open(path, 'wb') as stream:
                stream.write(b'1234')
            with self.assertRaises(OSError):
                security.read_file_bytes(path, max_bytes=3)

    def test_rejects_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            target = os.path.join(directory, 'target.txt')
            link = os.path.join(directory, 'link.txt')
            with open(target, 'wb') as stream:
                stream.write(b'secret')
            try:
                os.symlink(target, link)
            except (NotImplementedError, OSError):
                self.skipTest('symlink creation is unavailable')
            with self.assertRaises(OSError):
                security.read_file_bytes(link)

    def test_limits_process_output(self):
        with self.assertRaises(OSError):
            security.read_stream_limited(io.BytesIO(b'1234'), 3)

    def test_resolver_skips_executable_inside_repository(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = os.path.join(directory, 'repo')
            trusted = os.path.join(directory, 'trusted')
            os.mkdir(repository)
            os.mkdir(trusted)
            suffix = '.exe' if os.name == 'nt' else ''
            untrusted_exe = os.path.join(repository, 'git' + suffix)
            trusted_exe = os.path.join(trusted, 'git' + suffix)
            for path in (untrusted_exe, trusted_exe):
                with open(path, 'wb') as stream:
                    stream.write(b'placeholder')
                os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR)
            environment = {'PATH': os.pathsep.join((repository, trusted))}
            if os.name == 'nt':
                environment['PATHEXT'] = '.EXE'
            with mock.patch.dict(os.environ, environment, clear=False):
                resolved = security.resolve_executable('git', repository)
            self.assertEqual(os.path.realpath(resolved), os.path.realpath(trusted_exe))

    def test_flatpak_host_command_is_allowlisted(self):
        command = security.flatpak_host_command(['git', 'status'])
        self.assertEqual(command[-2:], ['/usr/bin/git', 'status'])
        with self.assertRaises(OSError):
            security.flatpak_host_command(['sh', '-c', 'id'])


if __name__ == '__main__':
    unittest.main()
