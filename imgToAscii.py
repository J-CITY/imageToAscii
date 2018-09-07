from random import randint
from PIL import Image, ImageDraw, ImageFont
import argparse
import math

class RGB:
	def __init__(self, _r, _g, _b):
		self.r = _r
		self.g = _g
		self.b = _b

class ImgToAscii:
	def __init__(self):
		print("Run params")
		self.imgPath = "in.png"
		self.outFile = "out.html"
		self.format = "txt"
		self.negative = False
		self.cellH = 2
		self.cellW = 1

		self.chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'."
		self.charsLen = len(self.chars)
		self.resAscii = ""
		self.resColors = []

	def GetGrayScale(self, r, g, b):
		#return r*0.2989 + g*0.5870 + b*0.1140
		return (r + g + b) / 3
		#return r*0.21 + g*0.73 + b*0.07

	def GetCharacterForGrayScale(self, scale) :
		return self.chars[math.ceil((self.charsLen - 1) * scale / 255)]

	def GetCharacterForGrayScaleNeg(self, scale) :
		return self.chars[self.charsLen - math.ceil((self.charsLen - 1) * scale / 255)]

	def ToAscii(self):
		print("Gen ascii image")
		img = Image.open(self.imgPath)
		width, height = img.size
		pixels = img.load()
		for y in range(0, height, self.cellH):
			for x in range(0, width, self.cellW):
				scale = 0
				cnt = 0
				_R = 0
				_G = 0
				_B = 0
				for _x in range(x, x+self.cellW):
					for _y in range(y, y+self.cellH):
						if _x >=0 and _x < width and _y >=0 and _y < height:
							r, g, b = pixels[_x, _y]
							scale += self.GetGrayScale(r,g,b)
							_R += r
							_G += g
							_B += b
							cnt += 1
				resScale = scale / cnt
				#char = "@"
				char = self.GetCharacterForGrayScale(resScale) if not self.negative else self.GetCharacterForGrayScaleNeg(resScale)
				self.resAscii += char
				self.resColors.append(RGB(_R/cnt,_G/cnt,_B/cnt))
			self.resAscii += "\n"

	def SaveToTxt(self):
		text_file = open(self.outFile, "w")
		text_file.write(self.resAscii)
		text_file.close()

	def SaveToHtml(self):
		resStr = "<body>"
		i = 0
		for c in self.resAscii:
			if c == '\n':
				resStr += "<br>\n"
			else:
				color = self.resColors[i]
				resStr += "<code style='color: rgb(" + str(color.r) + ","+str(color.g)+","+str(color.b)+")'>" + c + "</code>\n"
				i += 1
		resStr += "</body>"
		text_file = open(self.outFile, "w")
		text_file.write(resStr)
		text_file.close()

	def Save(self):
		if self.format == "txt":
			self.SaveToTxt()
		elif self.format == "html":
			self.SaveToHtml()
		print("Save to " + self.outFile + "\n")

image = ImgToAscii()

def parseArgs():
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--format", type=str, default='txt', help="Out format file")
	parser.add_argument("-in", "--input_file", type=str, default='in.png', help="Name of input file")
	parser.add_argument("-out", "--output_file", type=str, default='out.txt', help="Name of output file")
	parser.add_argument("-n", "--negative", action="store_true", help="Gen negative image", default=False)
	parser.add_argument("-cw", "--cell_width", type=int, default=1, help="Cell width")
	parser.add_argument("-ch", "--cell_height", type=int, default=2, help="Cell height")
					
	args = parser.parse_args()
	image.format = "txt" if args.format != "txt" and args.format != "html" else args.format
	image.imgPath = args.input_file
	image.outFile = args.output_file
	image.negative = args.negative
	image.cellW = args.cell_width
	image.cellH = args.cell_height
parseArgs()	
image.ToAscii()
image.Save()

# imgToAscii.py --input_file in.png --cell_width 2 --cell_height 4
# imgToAscii.py --input_file in.png  -out out.html --cell_width 2 --cell_height 4 --format html