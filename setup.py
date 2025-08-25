from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='thonny-SystemPowershell',
    version='0.1',
    author='Jysume',
    author_email='jysume@outlook.com',
    description='Add a buttom to open system powershell for Thonny IDE in Windows',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Jysume/thonny-SystemPowershell',
    license='MIT',
    packages=['thonnycontrib.SystemPowershell'],
    include_package_data=True,
    install_requires=['thonny >= 3.0.0'],
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Education",
        "Topic :: Software Development",
        "Topic :: Software Development :: Embedded Systems",
    ],
    keywords="IDE education programming Thonny development shell powershell",
    platforms=["Windows"],
)
