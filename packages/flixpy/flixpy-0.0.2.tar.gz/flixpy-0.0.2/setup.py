import setuptools

with open('./README.md') as readme_file:
  readme = readme_file.read()

setuptools.setup(
    name='flixpy',
    version='0.0.2',
    # python_requires='>=3.6',
    packages=setuptools.find_packages(),
    license='MIT',
    url='https://flixpy.now.sh/',
    project_urls={
        "Bug Tracker": "https://github.com/ninest/flixpy/issues",
        "Documentation": "https://flixpy.now.sh/guide",
        "Source Code": "https://github.com/ninest/flixpy",
    },
    long_description_content_type="text/markdown",
    description='Get data on movies, shows, streaming providers, people, ratings, and more',
    long_description=readme,
)

'''
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*

'''