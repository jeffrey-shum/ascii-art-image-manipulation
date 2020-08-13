import numpy as np
from PIL import Image

def calc_pixels(filepath):
    '''
    Print the number of pixels in a given image file
    '''
    im = Image.open(filepath)
    print('Pixel matrix size:', im.width, 'x', im.height)
    
def create_matrix(filepath):
    '''
    Emit an array containing the RGB values for each pixel in a given image file
    '''
    im = Image.open(filepath)
    # width = im.size[0]
    # print('Image width:', width)
    # height = im.size[1]
    # print('Image height:', height)
    # matrix = np.zeros([width, height, 3], dtype=np.uint8)
    # print('Empty matrix:', matrix)
    pixels = list(im.getdata())
    pixel_matrix = [ pixels[i:i+im.width] for i in range(0, len(pixels), im.width) ]
    return pixel_matrix

def intensity_matrix(pixel_matrix):
    '''
    Emit an array of the intensity values of a given pixel matrix
    ''' 
    intensity_matrix = [ [0 for i in pixel_matrix[0] ] for i in pixel_matrix] 

    for x in range(0, len(pixel_matrix)):
        for y in range(0, len(pixel_matrix[0])):
            pixel = pixel_matrix[x][y]
            pixel_intensity = sum(pixel)/3
            intensity_matrix[x][y] = round(pixel_intensity)
    return intensity_matrix

def main(filepath):
    pixel_matrix = create_matrix(filepath)
    brightness_matrix = intensity_matrix(pixel_matrix)
    print('Successfully constructed brightness matrix!')
    print('Brightness matrix size:', len(brightness_matrix[0]), 'x', len(brightness_matrix))
    print('Iterating through pixel brightness:')
    for i in brightness_matrix[0]:
        print(i)

 
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        main('ascii-pineapple.jpg')
    else:
        main(sys.argv[1])
