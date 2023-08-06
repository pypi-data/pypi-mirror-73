from setuptools import setup
import pathlib

HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


setup(
    name='ems-dash-utils',
    author="Jesper Halkjær Jensen",
    author_email="gedemagt@gmail.com",
    description="A utility package for dash apps",
    version='0.0.1',
    url='https://github.com/',
    packages=['dash_utils'],
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    python_requires='>=3.6', install_requires=['dash', 'flask', 'pytz']
)
