#!/usr/bin/env python3

from os import environ, path
from shutil import which
from subprocess import run

prefix = environ.get('MESON_INSTALL_PREFIX', '/usr/local')
datadir = path.join(prefix, 'share')
destdir = environ.get('DESTDIR', '')


def require_program(name):
    program = which(name)
    if program is None:
        raise FileNotFoundError(f'Required program is unavailable: {name}')
    return program


# Package managers set this so we don't need to run
if not destdir:
    icon_cache = path.join(datadir, 'icons', 'hicolor')
    if path.isdir(icon_cache):
        print('Updating icon cache...')
        run([require_program('gtk-update-icon-cache'), '-qtf', icon_cache], check=True)

    applications = path.join(datadir, 'applications')
    if path.isdir(applications):
        print('Updating desktop database...')
        run([require_program('update-desktop-database'), '-q', applications], check=True)

    schemas = path.join(datadir, 'glib-2.0', 'schemas')
    if path.isdir(schemas):
        print('Compiling GSettings schemas...')
        run([require_program('glib-compile-schemas'), schemas], check=True)
