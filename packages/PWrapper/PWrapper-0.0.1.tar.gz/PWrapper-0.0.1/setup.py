from setuptools import setup, find_packages
setup(
    name = "PWrapper",
    version = "0.0.1",
    packages = find_packages(),

    # Dependencies
    install_requires = [
        'requests'
    ],

    # Metadata
    author = "Jpuf0",
    author_email = "Jpuf@jpuf.xyz",
    description = "Politics & War API wrapper for Python",
    license = "MIT",
    keywords = "pnw politicsandwar",
    url = "https://github.com/Jpuf0/PnWrapper",
)
