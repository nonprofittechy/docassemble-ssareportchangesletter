import os
import sys
from setuptools import setup, find_packages
from fnmatch import fnmatchcase
from distutils.util import convert_path

standard_exclude = ('*.pyc', '*~', '.*', '*.bak', '*.swp*')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build', './dist', 'EGG-INFO', '*.egg-info')
def find_package_data(where='.', package='', exclude=standard_exclude, exclude_directories=standard_exclude_directories):
    out = {}
    stack = [(convert_path(where), '', package)]
    while stack:
        where, prefix, package = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                if os.path.isfile(os.path.join(fn, '__init__.py')):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + '.' + name
                        stack.append((fn, '', new_package))
                else:
                    stack.append((fn, prefix + name + '/', package))
            else:
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix+name)
    return out

setup(name='docassemble.ssareportchangesletter',
      version='1.1.1',
      description=('An interview to help an SSI or SSDI recipient report changes to the Social Security Administration'),
      long_description='# docassemble.ssareportchangesletter\r\n\r\nAn interview to help an SSI or SSDI recipient report changes to the Social Security Administration\r\n\r\n## Author\r\n\r\nQuinten Steenhuis, qsteenhuis@gmail.com\r\n\r\n## Changelog\r\n* 2022-01-11 Bugfixes\r\n* 2021-12-18 Incorporate feedback from VLP\r\n* 2021-03-26 bugfixes\r\n* 2021-03-25 Add branding\r\n* 2020-12-31 Migrate to asking for details one at a time; more logical detail questions\r\n* 2020-12-04 Upgrade for newest docassemble version\r\n* 2019-09-21 Cleanup / integrate ssn + tel auto-input validation\r\n* 2019-08-26 Add phone number auto-format, complete template variable mapping\r\n* 2019-08-20 Reorganize question order to be more logical, add review/edit ledgers, separate deposits and withdrawals\r\n* 2019-08-18 Add section headings to record of dedicated account\r\n* 2019-03-23 Include the Record of dedicated account\r\n* 2019-03-06 Work on question order and commpleting letter\r\n* 2019-02-26 Use SSA API to list nearby offices',
      long_description_content_type='text/markdown',
      author='Quinten Steenhuis',
      author_email='qsteenhuis@gmail.com',
      license='The MIT License (MIT)',
      url='https://docassemble.org',
      packages=find_packages(),
      namespace_packages=['docassemble'],
      install_requires=['docassemble.income>=0.0.36'],
      zip_safe=False,
      package_data=find_package_data(where='docassemble/ssareportchangesletter/', package='docassemble.ssareportchangesletter'),
     )

