 # Contributing Guidelines for NHGISXWALK

 Thank you for your interest in contributing! We work primarily on Github. Please review these contributing procedures/guidelines prior to starting an issue or pull request.


 ## Style and format

 1. Python 3.6, 3.7, and 3.8 are the officially supported versions.
 2. This project follows the formatting conventions of [`black`](https://black.readthedocs.io/en/stable/) and utilizes [`pre-commit`](https://pre-commit.com) to format commits prior to pull requests being made. 
     * LJ Miranda provides an [excellent, concise guide](https://ljvmiranda921.github.io/notebook/2018/06/21/precommits-using-black-and-flake8/) on setting up and implementing a `pre-commit` hook for `black`.
 3. Import packages, classes, and functions with their full name where possible.
   * For example:
     
     :white_check_mark:
     ```python
     import nhgisxwalk
     import pandas
     from numpy import array
     ```
     :x:
     ```python
     import nhgisxwalk as nhx
     import pandas as pd
     from snumpy import array as arr
     ```

 
