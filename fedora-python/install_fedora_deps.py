#!/usr/bin/python
import sys
import subprocess

# install system PACKAGES for python packages
build_system = ['redhat-rpm-config', 'gcc']
build_system_ubuntu = ['build-essential']


PACKAGES = {
    'pillow': {
        'fedora': {
            'build': build_system + ['lcms2-devel', 'zlib-devel', 'libjpeg-turbo-devel', 'freetype-devel', 'openjpeg2-devel', 'libtiff-devel', 'libwebp-devel'],
            'run': ['lcms2', 'zlib', 'libjpeg-turbo', 'freetype', 'openjpeg2', 'libtiff', 'libwebp']
        },
        'ubuntu': {
            'build': build_system_ubuntu + ['liblcms2-dev', 'liblz-dev', 'libjpeg-turbo8-dev', 'libfreetype6-dev', 'libopenjpeg-dev', 'libtiff5-dev', 'libwebp-dev'],
            'run': ['liblcms2-2']
        }
    },
    'gitpython': {
        'fedora': {
            'run': ['git']
        }
    },
    'av': {
        'fedora': {
            'run': ['git'],
            'build': ['ffmpeg-devel']
        }
    },
    'cryptography': {
        'fedora': {
            'build': ['libffi-devel', 'openssl-devel']
        }
    },
    'lxml': {
        'fedora': {
            'build': ['libxml2-devel', 'libxslt-devel']
        }
    }
}

def main():
    system = 'fedora'
    build_packages = set()
    run_packages = set()
    with open(sys.argv[1]) as requirements:
        for dep in requirements:
            # ignore version for now
            if '=' in dep:
                dep = dep[:dep.find('=')]

            package = dep.strip().lower()
            if package in PACKAGES:
                deps = PACKAGES[package][system]
                build_packages.update(deps.get('build', []))
                run_packages.update(deps.get('run', []))

    packages = build_packages.union(run_packages)
    if packages:
        cmd = ['dnf', 'install', '-y']
        cmd += packages
        print cmd
        subprocess.check_call(cmd)


if __name__ == '__main__':
    main()
