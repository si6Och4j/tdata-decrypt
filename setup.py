from setuptools import setup

setup(
    name="tdata-decrypt",
    version="1.2",
    description='Telegram Desktop\'s tdata decryption tool',
    packages=['tdata_decrypt'],
    install_requires=['tgcrypto'],
    entry_points={
        'console_scripts': [
            'tdata-decrypt = tdata_decrypt:cli',
        ],
    },
)
