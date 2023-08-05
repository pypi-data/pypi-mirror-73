from distutils.core import setup


setup(
  name='qbc_animal',
  packages=['qbc_animal'],
  package_data={'qbc_animal': ['data/*', '*.py', 'test.jpg']},
  version='1.0.0',
  description='Recognition Image Animal',
  long_description='Recognition Image Animal',
  author='Charles',
  author_email='charlesmeng@shinelab.cn',
  keywords=['pip3', 'python3', 'python', 'Recognition Image Animal'],
  license='MIT',
  install_requires=['requests', 'ybc_config', 'ybc_exception', 'ybc_player']
)
