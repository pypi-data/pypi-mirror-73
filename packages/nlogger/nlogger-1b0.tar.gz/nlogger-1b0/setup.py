from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='nlogger',
    version='1_beta',
    description='Package to use NLogger web service to send notification and logs to mobile devices.',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Balaviknesh Sekar',
    author_email='bala21karthick@gmail.com',
    keywords=['NLogger', 'Notifications', 'Logs', 'SmartPhones', 'iOS', 'Android'],
    url='',
    download_url='https://pypi.org/project/nlogger/'
)

install_requires = [
    'requests'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
