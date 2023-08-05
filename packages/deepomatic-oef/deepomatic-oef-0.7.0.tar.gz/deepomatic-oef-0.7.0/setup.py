import os
import io
import subprocess
from setuptools import find_namespace_packages, setup
from setuptools.command.sdist import sdist

from deepomatic.oef import VERSION

try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements


root = os.path.abspath(os.path.dirname(__file__))

def make(target):
    print("Calling Makefile (Generating protobuf)")
    subprocess.check_call(["make", "-C", root, target])  # generate protobuf
    # currently not used due to python 2 vs 3 incompatibility
    # p.check_returncode()


# Custom build command (invoked when running python setup.py sdist)
class CustomBuildCommand(sdist):
    """
    Customized setuptools install command:
    when called in CloudML, protobuf are already built and we need to install Darknet
    """

    def run(self):
        # There is not Makefile on CloudML, but the protobuf are already built
        # so we can skip this step
        if os.path.isfile(os.path.join(root, 'Makefile')):
            make('proto')  # build protobuf
        sdist.run(self)


with io.open(os.path.join(root, 'README.md'), 'r', encoding='utf-8') as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Read requirements
install_reqs = parse_requirements(os.path.join(root, 'requirements.txt'), session='hack')
try:  # for pip < 20.1
    install_requires = [str(ir.req) for ir in install_reqs]
except AttributeError:
    install_requires = [str(ir.requirement) for ir in install_reqs]

namespaces = ['deepomatic']

setup(
    name='deepomatic-oef',
    version=VERSION,
    description='Open Experiment Format',
    author='Deepomatic',
    author_email='support@deepomatic.com',
    url='https://github.com/Deepomatic/open-experiment-format',
    project_urls={
        'Product': 'https://deepomatic.com',
        'Source': 'https://github.com/deepomatic/open-experiment-format',
        'Tracker': 'https://github.com/deepomatic/open-experiment-format/issues',
    },
    license='MIT License',
    packages=find_namespace_packages(include=['deepomatic.*']),
    namespace_packages=namespaces,
    include_package_data=True,
    cmdclass={
        'sdist': CustomBuildCommand,
    },
    long_description=README,
    long_description_content_type='text/markdown',
    data_files=[('', ['requirements.txt', 'LICENSE'])],
    install_requires=install_requires,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
