from setuptools import setup, find_packages
import choicesfilter

setup(
    name='twentytab-choicesfilter',
    version=choicesfilter.__version__,
    description='A django app that initializes admin changelist view with select filters usin jquery-plugin select2',
    author='20tab S.r.l.',
    author_email='info@20tab.com',
    url='https://github.com/20tab/twentytab-choicesfilter',
    license='MIT License',
    install_requires=[
        'Django >=1.6',
        'twentytab-select2'
    ],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.html', '*.css', '*.js', '*.gif', '*.png', ],
}
)
