from setuptools import setup

with open("lahiru_distributions/README.md", "r") as fh:
    long_description = fh.read()

setup(name='lahiru_distributions',
      version='0.4',
      description='Gaussian and Binomial distributions',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author = 'Lahiru Senevirathne',
      author_email = 'lahiru.16@cse.mrt.ac.lk',
      packages=['lahiru_distributions'],
      zip_safe=False)
