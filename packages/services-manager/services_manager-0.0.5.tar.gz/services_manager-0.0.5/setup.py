from setuptools import setup, find_packages

# To upload to test pypi:
# twine upload -r testpypi dist/*

setup(
    name='services_manager',
    version='0.0.5',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask==1.1.2",
        "psutil~=5.7.0",
        "click~=7.1.2"
    ],
    entry_points='''
        [console_scripts]
        services_manager=services_manager.server:cli
    ''',
)
