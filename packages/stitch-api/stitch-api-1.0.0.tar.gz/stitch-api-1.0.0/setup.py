import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='stitch-api',
    version='1.0.0',
    author='Thomas Bennett',
    author_email='tbennett@talend.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Talend/stitch-api',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License (GPL)",
            "Operating System :: OS Independent"
    ],
)