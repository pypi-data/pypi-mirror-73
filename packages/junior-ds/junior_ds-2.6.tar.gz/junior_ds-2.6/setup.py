from setuptools import setup




setup(
		name = 'junior_ds',
		version = 2.6,
		description = 'This package is like having a junior Data Scientist working for you. So that you can delegate a lot of work and you focus on bringing insights. Techniques for making machine learning easy',
		package = ['junior_ds'],
		author = 'Samarth Agrawal',
		author_email = 'samarth.agrawal.86@gmail.com',
		python_requires='>=3.6',
		zip_safe = False,
        install_requires=['seaborn']
	)