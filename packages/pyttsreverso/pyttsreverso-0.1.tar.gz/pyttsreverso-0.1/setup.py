from setuptools import setup, find_packages


setup_args = dict(
    name='pyttsreverso',
    version='0.1',
    description='Useful tools to work with Resrervo TTS in Python',
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    author='Yuval Mejahez',
    author_email='yuval.teltech@gmail.com',
    keywords=['Resrervo', 'TTS', 'ResrervoTTS'],
    url='https://github.com/rt400/pyttsreverso',
    download_url='https://pypi.org/project/pyttsreverso/'
)

install_requires = [
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)