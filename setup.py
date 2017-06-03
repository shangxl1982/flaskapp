import setuptools

try:
    import multiprocessing  # noqa
except ImportError:
    pass

setuptools.setup(
    name='fib',
    version='1.0',
    packages=setuptools.find_packages(),
    author='sxl',
    author_email='shangxiaole@163.com',
    setup_requires=['pbr>=1.8'],
    pbr=True)

