from tqdm.contrib import tenumerate
from tifffile import imwrite

from scipy import ndimage, interpolate
import numpy as np

class Image:
	def __init__(self, int_stop, int_num, pixels, x_ival):
		ints = np.zeros(int_num)

		ints[int(len(ints)*0.3):int(len(ints)*0.5)] = int_stop/2*(1 - np.exp(-np.linspace(0,1,num=(int(len(ints)*0.5) - int(len(ints)*0.3)))/0.12))
		ints[int(len(ints)*0.5):int(len(ints)*0.8)] = int_stop/2
		ints[int(len(ints)*0.8):] = int_stop/2*(np.exp(-np.linspace(0, 1, num=(len(ints) - int(len(ints)*0.8)))/0.12))

		self.value = np.asarray([np.tile((np.real(np.tanh(np.linspace(-x_ival, x_ival, pixels))) + 1)*val, (pixels, 1)) for val in ints])

	def poisson_noise(self):
		self.value = np.asarray([img + np.random.poisson(img) for img in self.value])

	def gaussian_filter(self, sigma):
		self.value = np.asarray([np.fft.ifft2(ndimage.fourier_gaussian(np.fft.fft2(img), sigma)).real for img in self.value])

	def reslice(self, number):
		return np.asarray([*self.value[number:], *self.value[:number]]) if number > 0 else np.asarray([*self.value[number:], *self.value[:number]])

	def interpolate(self, images, factor, order=3, mode='grid-wrap', grid_mode=True):
		return ndimage.zoom(images[::factor], [factor, 1, 1], order=order, mode=mode, grid_mode=grid_mode)

	def chi_squared(self, steps, shifts, offset, orders=[1, 2, 3], mode='grid-wrap', grid_mode=True):
		chi_squared = np.zeros((len(shifts), len(orders), len(steps)))

		for i, shift in tenumerate(shifts, desc='Shifts'):
			for j, order in tenumerate(orders, desc='Orders', leave=False):
				for k, step in tenumerate(steps, desc='Steps', leave=False):
					chi_squared[i, j, k] = np.mean(np.sum(np.square(np.subtract(self.reslice(shift) + offset, self.interpolate(self.reslice(shift), step, order, mode, grid_mode) + offset))/(self.reslice(shift) + offset), axis=0), axis=(0,1))

		return chi_squared

	def save_image(self, file_name, dtype=np.float32, photometric='minisblack'):
		imwrite(file_name, self.value.astype(dtype), photometric=photometric)