from setuptools import setup
setup(
  name='flaskapp',
  packages=['flaskapp'],
  include_package_data=True,
  author="Cristian Rodriguez",
  author_email="me@criselgeek.com",
  python_requires="3.5.x",
  install_requires=[
    'flask'
  ]
)