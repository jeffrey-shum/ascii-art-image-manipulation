from PIL import Image
import subprocess

# 65 ASCII characters:
ascii_chars = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

print_width = 300
display_setting = "average" # valid display settings: "average", "min_max", and "luminosity"
brightness_inversion = False
use_webcam = False

def calc_pixels(filepath):
    '''
    Print the number of pixels in a given image file
    '''
    im = Image.open(filepath)
    print('Pixel matrix size:', im.width, 'x', im.height)
    
def create_matrix(filepath):
    '''
    Emit a matrix containing tuples of RGB values for each pixel in a given image file
    '''
    im = Image.open(filepath)
    width, height = im.size
    im.thumbnail((print_width, height))
    pixels = list(im.getdata())
    pixel_matrix = [ pixels[i:i+im.width] for i in range(0, len(pixels), im.width) ]
    return pixel_matrix

def calc_pixel(pixel):
    '''
    Emits a pixel value in accordance with a specified display setting.
    '''
    if display_setting == "average":
        return sum(pixel)/3
    elif display_setting == "min_max":
        return (max(pixel) + min(pixel)) / 2
    elif display_setting == "luminosity":
        return (0.21 * pixel[0] + 0.72 * pixel[1] + 0.07 * pixel[2])
    else:
        raise ValueError("Invalid display settings: use 'average', 'min_max', or 'luminosity'")

def intensity_matrix(filepath):
    '''
    Emit a matrix of the intensity values of a given pixel matrix
    ''' 
    pixel_matrix = create_matrix(filepath)
    intensity_matrix = [ [0 for i in pixel_matrix[0] ] for i in pixel_matrix] 

    for x in range(0, len(pixel_matrix)):
        for y in range(0, len(pixel_matrix[0])):
            pixel = pixel_matrix[x][y]
            pixel_intensity = calc_pixel(pixel)
            intensity_matrix[x][y] = round(pixel_intensity)
    return intensity_matrix

def ascii_matrix(filepath):
    '''
    Emit a matrix of ASCII characters corresponding to the brightness levels
    in a given intensity matrix
    '''
    intensities = intensity_matrix(filepath)
    ascii_matrix = [ ['' for i in intensities[0]] for i in intensities]
    for x in range(0, len(intensities)):
        for y in range(0, len(intensities[0])):
            intensity = intensities[x][y]
            val = (intensity/255)*65
            rounded_val = round(val)
            if brightness_inversion:
                ascii_matrix[x][y] = ascii_chars[-rounded_val]
            else:
                ascii_matrix[x][y] = ascii_chars[rounded_val-1]   
    return ascii_matrix

def capture_image():
    subprocess.run('imagesnap')
    img = 'snapshot.jpg'
    return img

def colorize(rgb_tuple):
    r, g, b = rgb_tuple
    colorized = f"\u001b[38;2;{r};{g};{b}m{ascii_str} \u001b[38;2;255;255;255m"
    return colorized

def main(filepath):
    a_matrix = ascii_matrix(filepath)
    rgb_pixels = create_matrix(filepath)
    print('Successfully constructed ascii matrix!')
    for x in range(0, len(a_matrix)):
        for y in range(0, len(a_matrix[0])):
            r, g, b = rgb_pixels[x][y]
            ascii_str = a_matrix[x][y]*3
            print(f"\u001b[38;2;{r};{g};{b}m{ascii_str}", end='')
            if y == len(a_matrix[0]) - 1:
                print("\u001b[0m") # ANSI Reset Code

if __name__ == '__main__':
    import sys
    if use_webcam == True:
        main(capture_image())
    elif len(sys.argv) < 2:
        main('ascii-pineapple.jpg')
    else:
        main(sys.argv[1])
