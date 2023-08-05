import setuptools

setuptools.setup(
    name = "githc",
    packages = {".": "githc"},
    version = "0.1.1",
    license="MIT",
    description = "Git history checkout tool",
    author = "Chris Gravel",
    author_email = "cpagravel@gmail.com",
    url = "https://github.com/cpagravel/gh",
    download_url = "https://github.com/cpagravel/gh/archive/0.1.1.tar.gz",
    keywords = ["git", "git history", "git checkout", "git workflow"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
  ],
  entry_points = {
      'console_scripts': [
          'gh = gh:main'
      ]
  },
)