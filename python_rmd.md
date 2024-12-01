Python in R Markdown
================

- [Python in `.Rmd` files](#python-in-rmd-files)
  - [Load libraries](#load-libraries)
  - [Load data](#load-data)
  - [plot data](#plot-data)
  - [Subsetting data in `pandas`](#subsetting-data-in-pandas)
  - [And inline python code within markdown
    text!](#and-inline-python-code-within-markdown-text)
  - [Sourcing a Python script](#sourcing-a-python-script)

To use Python in R Markdown, we need to load the
{[reticulate](https://rstudio.github.io/reticulate/)} R package in a
code chunk, we do it here in the setup code chunk. We also load the
{[ggplot2](https://ggplot2.tidyverse.org/)} R package so we can plot
some data from a Python `pandas` data frame later on!

## Python in `.Rmd` files

### Load libraries

Just like R, you can use Python in `.Rmd` files! Here we import the
Python package that we need to import our data into Python, `pandas`.
`pandas` is a Python package that adds data reading, wrangling, and
simple data visualization functionality to Python where sometimes depend
on `matplotlib` functions. It holds a similar place as the {tidyverse} R
meta-package does (however `pandas` is not a meta-package, just a very
large package). If you want to learn more about pandas, see the “[10
minutes to
pandas](https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html)”
in the docs our checkout this free interactive course:
<https://prog-learn.mds.ubc.ca/en>.

To [install Python
packages](https://rstudio.github.io/reticulate/articles/python_packages.html)
please run the cell below

``` r
py_config() # optional: to check python configuration setups
```

    ## python:         /Users/kewalinsamart/Library/r-miniconda/envs/r-reticulate/bin/python
    ## libpython:      /Users/kewalinsamart/Library/r-miniconda/envs/r-reticulate/lib/libpython3.8.dylib
    ## pythonhome:     /Users/kewalinsamart/Library/r-miniconda/envs/r-reticulate:/Users/kewalinsamart/Library/r-miniconda/envs/r-reticulate
    ## version:        3.8.20 (default, Oct  3 2024, 10:25:41)  [Clang 14.0.6 ]
    ## numpy:          /Users/kewalinsamart/Library/r-miniconda/envs/r-reticulate/lib/python3.8/site-packages/numpy
    ## numpy_version:  1.24.3
    ## 
    ## NOTE: Python version was forced by RETICULATE_PYTHON

``` r
py_install("pandas") # install pandas
```

    ## + /Users/kewalinsamart/Library/r-miniconda/bin/conda install --yes --prefix /Users/kewalinsamart/Library/r-miniconda/envs/r-reticulate -c conda-forge pandas

``` r
py_install("matplotlib") # install matplotlib
```

    ## + /Users/kewalinsamart/Library/r-miniconda/bin/conda install --yes --prefix /Users/kewalinsamart/Library/r-miniconda/envs/r-reticulate -c conda-forge matplotlib

``` python
import pandas as pd
import matplotlib.pyplot as plt
```

### Load data

Let’s load the titanic data (which lives in the `data` directory of this
project) and view the data:

``` python
titanic  = pd.read_csv("data/titanic.csv")
```

### plot data

#### Using Python and `pandas`

First, let’s use some quick and simple `pandas` plotting functions:

``` python
titanic.plot.scatter(x='age', y='fare', alpha=0.3)
plt.show()
```

<img src="python_rmd_files/figure-gfm/python-plot-1.png" width="672" />

Want to learn more about getting started plotting in Python using
`pandas`, see this page to get started:
<https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html>

#### Using R and {ggplot2}

We can also access the Python environment in this R Markdown document
from R! This allows us to apply R’s functions on our Python objects! We
can use the `py$obbject` syntax to do this and create a data
visualization using {ggplot2}!

``` r
ggplot2::ggplot(py$titanic, aes(x = age, y = fare)) +
  geom_point()
```

![](python_rmd_files/figure-gfm/r-plot-3.png)<!-- -->

### Subsetting data in `pandas`

Here we subset the age and fare columns:

``` python
titanic[["age", "fare"]]
```

    ##           age      fare
    ## 0     29.0000  211.3375
    ## 1      0.9167  151.5500
    ## 2      2.0000  151.5500
    ## 3     30.0000  151.5500
    ## 4     25.0000  151.5500
    ## ...       ...       ...
    ## 1304  14.5000   14.4542
    ## 1305      NaN   14.4542
    ## 1306  26.5000    7.2250
    ## 1307  27.0000    7.2250
    ## 1308  29.0000    7.8750
    ## 
    ## [1309 rows x 2 columns]

Here we filter for rows containing passengers who’s age was 70 or
greater:

``` python
titanic[titanic["age"] > 70]
```

    ##       pclass  survived  ...   body                home.dest
    ## 9          1         0  ...   22.0      Montevideo, Uruguay
    ## 14         1         1  ...    NaN            Hessle, Yorks
    ## 61         1         1  ...    NaN  Little Onn Hall, Staffs
    ## 135        1         0  ...    NaN             New York, NY
    ## 727        3         0  ...  171.0                      NaN
    ## 1235       3         0  ...    NaN                      NaN
    ## 
    ## [6 rows x 14 columns]

Here we find the destination of the first passenger:

``` python
first_dest = titanic["home.dest"][0]
first_dest
```

    ## 'St Louis, MO'

Why 0 as the numerical index above? Python counts from 0, not 1!

### And inline python code within markdown text!

We can use the R Markdown inline syntax and the `py$` syntax to reach
into the Python environment and access the `first_dest` python object
(which is a string).

The destination of the first passenger is St Louis, MO.

### Sourcing a Python script

#### Example 1: `greeting.py` (contains a function named greeting with Python code to call the function within the same script)

``` r
# source the Python script
source_python('greeting.py')
```

    ## Hello R-Ladies Aurora !

``` r
# call the Python function and pass a new name
greeting("Kewalin")
```

    ## Hello Kewalin !

#### Example 2: `titanic.py` (only contains a function named read_titanic)

``` r
# source the Python script
source_python("titanic.py")

# call the Python function and pass the Titanic dataset
titanic <- read_titanic("data/titanic.csv")

# load ggplot2 for visualization
library(ggplot2)

# plot the Titanic data
ggplot(titanic, aes(x = age, y = fare, color = as.factor(survived))) +
  geom_point(alpha = 0.6) +
  labs(
    title = "Age vs Fare (Colored by Survival)",
    x = "Age",
    y = "Fare",
    color = "Survived"
  ) +
  theme_minimal()
```

![](python_rmd_files/figure-gfm/unnamed-chunk-5-1.png)<!-- -->
