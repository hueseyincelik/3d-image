# 3D Image
Generate *n*-sized image stacks where both the intensity of a single image and the intensities between images scale with a (dis-)charging capacitor function (i.e. exponential), take every *k*-th image, interpolate the reduced image stack and compare it to the original one using the χ²-method.

Includes functions to add gaussian and poisson noise, "reslice" (i.e. take the first/last *j* images and append them to the beginning/end) the image stack and plot everything together in a single figure.

## Installation
Install all required packages with pip using:
```
pip3 install -r requirements.txt
```
and import the modules using:
```python
from src import image, plot
```
## Usage
For instructions on how to use the project, see [main.py](/main.py). Example [images](/images) and [plots](/plots) are provided in their respective folders.

## License
Copyright © 2022 [Hüseyin Çelik](https://www.github.com/hueseyincelik).

This project is licensed under [AGPL v3](/LICENSE).
