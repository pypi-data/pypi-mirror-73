from __future__ import division, print_function, absolute_import
from distutils.core import setup, Extension
import os


version = "0.1.0"

with open("README.md") as file:
    long_description = file.read()


def main():
    print("setting up src_manip3 version: " + version)

    setup(name="src_manip3",
          version=version,
          description="Python - C interface for manipulating source code, but faster.",
          long_description=long_description,
          author="skyzip",
          author_email="skyzip96@gmail.com",
          url="https://gitlab.com/Skyzip/src_manip3",
          ext_modules=[Extension("src_manip.comment_remover.comment_remover", [
              "src_manip/comment_remover/comment_remover.c",
              "src_manip/comment_remover/_comment_remover.c"
          ])],
          packages=[
              "src_manip",
              "src_manip.comment_remover"
          ],
          package_data={
              "src_manip": ["__init__.py"],
              "src_manip.comment_remover": ["__init__.py", "js_comment_remover.py"],
          },
          license="GPL",
          classifiers=[
              "Programming Language :: Python :: 3",
              "Operating System :: OS Independent",
          ]
          )


if __name__ == '__main__':
    try:
        if os.environ.get('CI_COMMIT_TAG'):
            print("Getting CI_COMMIT_TAG.")
            version = os.environ['CI_COMMIT_TAG']
        else:
            version = os.environ['CI_JOB_ID']
            print("Getting CI_JOB_ID.")
    except KeyError:
        print("Unable to get environment variable.")
        print("Setting version manually to: " + str(version))

    main()
