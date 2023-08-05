import ctypes
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
from pathlib import Path
from PIL import Image


def choose_files():
	Tk().withdraw()
	filenames = askopenfilenames(
		initialdir = "/",
		title = "Select file",
		filetypes = (("png files","*.png"),)
	)
	if len(filenames) == 0: quit()
	return filenames


def png_to_ico(filenames):
	counter = 0
	for file in filenames:
		p = Path(file)
		name = p.stem
		folder = p.parents[0]
		new_folder = folder.joinpath('ico')
		Path(new_folder).mkdir(parents=False, exist_ok=True)
		fname = new_folder.joinpath(name)

		img = Image.open(file)
		img.save(f'{fname}.ico', format = 'ICO')
		counter += 1
		print(counter, 'image(s) converted.')

	print('Images converted successfully.')


def main():
	ctypes.windll.shcore.SetProcessDpiAwareness(True)
	png_to_ico(choose_files())
