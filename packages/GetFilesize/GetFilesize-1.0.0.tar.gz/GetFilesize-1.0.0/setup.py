from setuptools import setup, find_packages

setup(
    name="GetFilesize",
    packages=find_packages(),
    version='1.0.0',
    description="adaptive getting the file size",
    author="shliang",
    author_email='shliang0603@gmail.com',
    maintainer='shliang',
    maintainer_email='shliang0603@gmail.com',
    url="https://github.com/shliang0603",
    download_url='https://github.com/shliang0603',
    keywords=['get-file-size', 'tool'],
    classifiers=[],
    install_requires=[
        'os'],
    python_requires='>=3'
)
