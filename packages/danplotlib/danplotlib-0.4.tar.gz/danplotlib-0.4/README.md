# danplotlib
Simple matplotlib wrapper

## Installation
`pip install .`

## Usage
```python
#Import automatically loads 'danplotlib/styles/matplotlibrc' (edit that file as needed)
import danplotlib as dpl

#Optional: Load other styles in 'danplotlib/styles/stylelib'
#dpl.use_style('latex')

#Use in the same way as matplotlib.pyplot
dpl.plot([1,2,3], [3,2,1])
dpl.xlabel("X")
dpl.ylabel("Y")
dpl.show()
dpl.close()
```
