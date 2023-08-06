from distutils.core import setup

with open('README.md') as f:
	long_description = f.read()

setup(name='met',
	version='1.0.2',
	description="Multinomial Exact Tests",
	author='Dreas Nielsen',
	url='https://pypi/project/met/',
	author_email='dnielsen@integral-corp.com',
	requires=[],
	python_requires = '>=2.7',
    license='GPL',
	py_modules=['met'],
	classifiers=[
		'Intended Audience :: End Users/Desktop',
		'Programming Language :: Python',
		'License :: OSI Approved :: GNU General Public License (GPL)',
		'Operating System :: OS Independent',
		'Topic :: Office/Business'
          ],
    keywords=['Statistics', 'Multnomial exact test', 'Multinomial'],
    long_description_content_type="text/markdown",
	long_description=long_description
	)
