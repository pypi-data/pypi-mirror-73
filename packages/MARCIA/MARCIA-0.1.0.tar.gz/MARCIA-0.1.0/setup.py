from setuptools import setup, find_namespace_packages


setup(
    name='MARCIA',
    version='0.1.0',
    description='Manual hyperspectral data classifier',
    url='https://github.com/hameye/marcia',
    author='Hadrien Meyer',
    author_email='meyerhadrien96@gmail.com',
    license='GPL v3',
    packages=find_namespace_packages(exclude=[
            'doc', 'doc.*']),
    install_requires=[
        'pandas',
        'scikit-image',
        'numpy',
        'seaborn',
        'hyperspy',
        'python-ternary'
    ],
    zip_safe=False
)
