import tabulate
from contextlib import contextmanager
import os

def print2(*args):
  for arg in args:
    print(arg, end="\n\n")
    
def describe2(data):
  print2(data.shape, data.info())
  shape_ = {"Number of Rows":[data.shape[0]], "Number of Columns":[data.shape[1]]}
  des = tabulate.tabulate(data.describe(), headers=data.columns, tablefmt="fancy_grid")
  hd = tabulate.tabulate(data.head(), headers=data.columns, tablefmt="fancy_grid", showindex="never")
  ta = tabulate.tabulate(data.tail(), headers=data.columns, tablefmt="fancy_grid", showindex="never")
  sh = tabulate.tabulate(shape_, headers=shape_.keys(), tablefmt="fancy_grid", showindex="never")
  print2(des, hd, ta, sh)


@contextmanager
def changepath(path):
    currentpath = os.getcwd()

    os.chdir(path)

    try:
        yield 

    finally:
        os.chdir(currentpath)
  
