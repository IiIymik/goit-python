from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='0.0.2',
    description='Clean your system  for bug',
    url='https://github.com/IiIymik/goit-python',
    author='IiIymik',
    author_email='vladyslav.shumkov@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean-folder = clean_folder.clean:get_file']}
)