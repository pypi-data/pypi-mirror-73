from distutils.core import setup

setup(
    name='qbc_qrcode',
    version='1.0.4',
    description='generate a qrcode',
    long_description='generate a qrcode according input text',
    author='charlesmeng',
    author_email='charlesmeng@shinelab.cn',
    keywords=['pip3', 'qrcode', 'python3', 'python'],
    url='https://www.shinelab.cn/',
    packages=['qbc_qrcode'],
    package_data={'qbc_qrcode': ['*.py']},
    license='MIT',
    install_requires=[
        'qrcode',
        'ybc_exception'
    ],
)
