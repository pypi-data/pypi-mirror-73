import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'drf-nested-creator',         # How you named your package folder (MyLib)
  packages = ['drf_nested_creator'],   # Chose the same as "name"
  version = '0.3.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Django Rest Framework nested serializers and model creator',   # Give a short description about your library
  author = 'Utkucan Bıyıklı',                   # Type in your name
  author_email = 'utkucanbykl@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/UtkucanBykl/drf-nested-creator',   # Provide either the link to your github or to your website
  keywords = ['django', 'djangorestframework', 'serializers'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'django>=2',
          'djangorestframework>=3',
      ],
  long_description=long_description,
  long_description_content_type="text/markdown",
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.8',
  ],
)
