import setuptools

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(name='ronglian_sms_sdk',
      version='1.0',
      description='RongLian SMS SDK',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Panxd',
      author_email='panxd@yuntongxun.com',
      url='https://github.com/cloopen/python-sms-sdk',
      packages=setuptools.find_packages(),
      install_requires=['requests'],
      keywords='ronglian sms ronglian_sms_sdk',
      classifiers=["Programming Language :: Python :: 3.6"])
