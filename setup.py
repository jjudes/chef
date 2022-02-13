from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='training',
      version='0.1',
      description='Parse recipes for measurements and ingredients',
      long_description=readme(),
      classifiers=[
          'Programming Language :: Python :: 3.7',
          'Topic :: NLP :: NER :: Text Processing :: Recipes',
      ],
      url='http://github.com/jjudes/chef',
      author='Jef Judes',
      author_email='jefrey.judes@gmail.com',
      license='MIT',
      packages=['training'],
      install_requires=[
          'spacy',
          'python-crfsuite',
          'recipe-scrapers'
      ],
      include_package_data=True,
      zip_safe=False)
