from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='pip-gui-tools',
    version='0.0.1',
    description='A tool for python pip package management',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Sam Sultan',
    author_email='sam.ibrahim.sultan@gmail.com',
    keywords=['PIP', 'UI'],
    url='',
    download_url='',
    include_package_data=True
)

install_requires = [
    'pip'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)