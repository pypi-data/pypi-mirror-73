from setuptools import setup, find_packages




setup(
		name = 'junior_ds',
		version = 3.2,
		description = 'This package is like having a junior Data Scientist working for you. So that you can delegate a lot of work and you focus on bringing insights. Techniques for making machine learning easy',
		packages=find_packages(include=['junior_ds', 'junior_ds.*']),
		author = 'Samarth Agrawal',
		author_email = 'samarth.agrawal.86@gmail.com',
		python_requires='>=3.6',
		zip_safe = False
	)