from setuptools import setup

with open("/home/workspace/5_exercise_upload_to_pypi/gabd_probability/README.md", "r") as fh:
    long_description = fh.read()


setup(name='gabd_probability',
      version='0.1.2',
      description='Gaussian and Binomial distributions',
      packages=['gabd_probability'],
      author='Biswajeet Mahato',
      author_email='biswajeetm156@gmail.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/biswa-star",
#       packages=setuptools.find_packages(),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      python_requires='>=3.6',
      zip_safe=False)
