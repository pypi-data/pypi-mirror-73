
from setuptools import setup, find_packages 

with open('DESCRIPTION.md') as readme_file:
    DESCRIPTION = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='neuralnet_visualize',
    version='0.0.4',
    description='Generate a neural network architecture Image',
    long_description_content_type='text/markdown',
    long_description=DESCRIPTION+"\n\n\n"+HISTORY,
    license='Apache License 2.0',
    packages=find_packages(),
    author='Anurag Peddi',
    author_email='anurag.peddi1998@gmail.com',
    keywords=['Neural', 'Network', 'Visualize', 'Graphviz'],
    url='https://github.com/AnuragAnalog/nn_visualize',
    download_url='https://pypi.org/project/neuralnet-visualize/',
    classifiers=[
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires='>=3.6'
)

install_requirments = [
    'graphviz>=0.14'
    'tensorflow>=2.0.0a0'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requirments)