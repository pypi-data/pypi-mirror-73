from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='janus-highvar',
      version='0.0.2',
      description='Dungeons and Dragons High Variance Die Roller',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Alex Philpott',
      url='https://github.com/alexphi314/janus',
      packages=find_packages(),
      entry_points={
            "console_scripts": [
                  "janus = janus.main:roll_die"
            ]
      },
      extras_require={":python_version<'3.3'": ["mock"]},
      python_requires='>=2.7',
      )
