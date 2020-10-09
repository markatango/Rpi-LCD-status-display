from FBpyGIF import fb
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-img", action="store", required=True, dest="image_name", help="name of splash image")

args = parser.parse_args()

BIT_DEPTH = 8
FRAME_BUFFER = 1
fb.ready_fb(BIT_DEPTH, FRAME_BUFFER)

fb.show_img(fb.ready_img(args.image_name))
