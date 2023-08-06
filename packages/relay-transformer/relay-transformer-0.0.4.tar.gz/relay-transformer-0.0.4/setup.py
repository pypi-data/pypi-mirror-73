from setuptools import setup, find_packages

setup(
  name = 'relay-transformer',
  packages = find_packages(exclude=["examples"]),
  version = '0.0.4',
  license='MIT',
  description = 'Relay Transformer, a long-range transformer',
  author = 'Phil Wang',
  author_email = 'lucidrains@gmail.com',
  url = 'https://github.com/lucidrains/relay-transformer',
  keywords = ['transformers', 'attention', 'artificial intelligence'],
  install_requires=[
      'torch',
      'local-attention'
  ],
  classifiers=[
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'Topic :: Scientific/Engineering :: Artificial Intelligence',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3.6',
  ],
)