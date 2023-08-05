from setuptools import setup

setup(
    name='demographer',
    version='1.0.0',
    author='Zach Wood-Doughty, Paiheng Xu, Xiao Liu, Praateek Mahajan, Rebecca Knowles, Josh Carroll, Mark Dredze',  # noqa
    author_email='mdredze@cs.jhu.edu',
    packages=['demographer'],
    package_dir={'demographer': 'demographer'},
    package_data={'demographer': ['data/*']},
    include_package_data=True,
    url='https://bitbucket.org/mdredze/demographer',
    download_url='https://bitbucket.org/mdredze/demographer/get/0.1.2.zip',
    license='LICENSE.txt',
    description='Simple name demographics for Twitter names',
    install_requires=[
        "numpy",
        "scikit-learn",
    ]
)
