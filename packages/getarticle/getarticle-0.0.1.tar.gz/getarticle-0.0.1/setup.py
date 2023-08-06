import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='getarticle',
	description="getarticle is a package based on SciHub and Google Scholar\
	   that can download articles based on DOI or website address. \
	   It can also download related articles given keywords.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      version='0.0.1',
      url='https://github.com/HTian1997/getarticle',
      author='Hao Tian',
      author_email='htian1997@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      zip_safe=False
)