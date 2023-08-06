from setuptools import setup, find_packages 

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='neuralnet_visualize',
    version='0.0.2',
    description='Generate a neural network architecture Image',
    long_description_content_type='text/markdown',
    long_description=README,
    license='Apache License 2.0',
    packages=find_packages(),
    author='Anurag Peddi',
    author_email='anurag.peddi1998@gmail.com',
    keywords=['Neural', 'Network', 'Visualize', 'Graphviz'],
    url='https://github.com/AnuragAnalog/nn_visualize',
    download_url='https://pypi.org/project/',
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.6'
)

install_requirments = [
    'graphviz>=0.14'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requirments)
