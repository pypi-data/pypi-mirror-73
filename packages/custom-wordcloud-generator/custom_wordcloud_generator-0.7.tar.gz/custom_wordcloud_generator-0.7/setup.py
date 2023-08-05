from setuptools import setup
from setuptools.extension import Extension

setup(name='custom_wordcloud_generator',
      version='0.7',
      description='Slightly modified Muellers Wordcloud generator',
      packages=['custom_wordcloud_generator'],
      author_email='ekertdenis@gmail.com',
      install_requires=['numpy>=1.6.1', 'pillow', 'matplotlib'],
      ext_modules=[Extension("custom_wordcloud_generator.query_integral_image",
                           ["custom_wordcloud_generator/query_integral_image.c"])],
      package_data={'custom_wordcloud_generator': ['stopwords']},
      zip_safe=False)
