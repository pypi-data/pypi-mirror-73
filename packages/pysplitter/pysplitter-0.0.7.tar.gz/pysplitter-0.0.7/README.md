# Tutorial using the pysplit package

pysplit is a Python package used for splitting large files into smaller chunks.

Currently the default chunk size is 100MB. This size was chosen to work around GitHub's upload file size limit.

### Install the latest version of pysplitter
Run the cell below to ensure you have the latest version of `pysplitter` installed on your machine.


```python
# !pip install --upgrade pysplitter
```

### Import required packages


```python
import pysplitter as pysp
import numpy as np
```

### Import helpful packages


```python
import sys
import os
```

### Create a numpy array that will exceed 100MB when saved to disk.

The numeric values of the data are not important. Random values were used for convenience only.


```python
dim = 250
num = int(dim * dim * dim)
x = np.random.normal(size=num).reshape(dim, dim, dim)
x.shape
```




    (250, 250, 250)



### Save numpy array to disk and list directory contents


```python
np.save('x.npy', x)
```


```python
os.listdir()
```




    ['.ipynb_checkpoints',
     '1-split-unsplit-tutorial.ipynb',
     'x.npy']



### Display size of file on disk


```python
size = os.path.getsize('x.npy')
print(f'{size / 1e6} MB')
```

    125.000128 MB
    

As many people may know, GitHub will not allow files exceeding 100 MB to be uploaded.

Use the commands below to split the original (and too large) file into multiple `.split` files.

Currently the default split size is <= **100 MB**, but this may become a variable paramter in furture distributions.


```python
os.listdir()
```




    ['.ipynb_checkpoints',
     '1-split-unsplit-tutorial.ipynb',
     'x(unsplit).npy',
     'x.npy']




```python
src = 'x.npy'
pysp.split(src)
```

    2 file(s) written.
    

Check file size of the two chunks that were just written.


```python
os.listdir()
```




    ['.ipynb_checkpoints',
     '1-split-unsplit-tutorial.ipynb',
     'x(unsplit).npy',
     'x.npy',
     'x0000.npy.split',
     'x0001.npy.split']




```python
print(os.path.getsize('x0000.npy.split') / 1e6, 'MB')
```

    100.0 MB
    


```python
print(os.path.getsize('x0001.npy.split') / 1e6, 'MB')
```

    25.000128 MB
    

As is clearly shown from the output of the above cells, both chunks are <= 100MB. This means that this data can now pushed  to GitHub as any other file would.

### Recombine the data chunks back into a single file


```python
search_pattern = './x*.split'
dst = '.'
pysp.unsplit(search_pattern, dst, validate=True, orig_src=src)
```

    File reconstructed without loss: True
    


```python
os.listdir()
```




    ['.ipynb_checkpoints',
     '1-split-unsplit-tutorial.ipynb',
     'x(unsplit).npy',
     'x.npy',
     'x0000.npy.split',
     'x0001.npy.split']




```python
x_unsplit = np.load('x(unsplit).npy')
x_unsplit.shape
```




    (250, 250, 250)



### Show that the manipulated data `x_unsplit` is the same as the original data `x`.


```python
np.allclose(x, x_unsplit)
```




    True




```python

```
