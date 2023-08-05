from setuptools import setup

setup(name='d_distributions',
      version='0.1.5',
      description='Gaussian and Binomial distributions',
      packages=['d_distributions'],
      install_requires=[
          "matplotlib >= 3.2.2",
          "scipy"
      ],
      zip_safe=False)
