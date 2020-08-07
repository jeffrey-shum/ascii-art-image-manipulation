from PIL import Image

def pixels(filepath):
    im = Image.open(filepath)
    return print(f'Image size: {im.size[0]} x {im.size[1]}')

def main(argv):
    return pixels(argv[1])

if __name__ == '__main__':
    import sys
    main(sys.argv)
