from setuptools import find_packages, setup

setup(
    name="DalmengSimpleTodo",
    version="0.0.1",
    description="A simple TODO APIs",
    author="Dalmeng",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.8",
)
