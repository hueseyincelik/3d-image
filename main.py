from src import image, plot

img_128px = image.Image(int_stop=10, int_num=1000, pixels=128, x_ival=2)
img_128px.poisson_noise()
img_128px.gaussian_filter()

steps = [8, 10, 20, 25, 40, 50, 100]
order = [1, 2, 3]
shifts = [-10, 0, 10]

chi = img_128px.chi_squared(steps, shifts, offset=0.01, orders=order)

pl = plot.Plot(steps, shifts, chi, df=999, orders=order)
pl.show()