from PIL import Image, ImageFilter
import rembg


inpiut_path = "./input.png"
output_path = "./output.png"

img = Image.open(inpiut_path)
# img_blurred = img.filter(ImageFilter.GaussianBlur(10))
# img_blurred.save(output_path)
img_no_bckg = rembg.remove(img)
img_no_bckg.save(output_path)
