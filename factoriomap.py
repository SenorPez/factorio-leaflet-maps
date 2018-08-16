"""Convert a TAR file or directory of Factorio screenshots into Leaflet
map tiles.

Factorio Console Command to generate screenshots:
    /c game.player.surface.daytime = 0; for x=-1000,1000 do for y=-1000,1000 do if game.forces["player"].is_chunk_charted(1, {x, y}) then game.take_screenshot{show_entity_info=true, zoom=1, resolution={1024,1024}, position={x=32*x+16,y=32*y+16}, path="DIR/s_"..x.."_"..y..".jpg"}; end; end; end;

"""
import os
from glob import glob
import sys
import tarfile

from PIL import Image
from tqdm import tqdm

USAGE = '''
Usage: python3 factoriomap.py [source] [destination]
   source: directory or .tar file
   destination: directory
'''

def main():
    """Main executable function."""
    # Verify arguments; print usage on failure.
    if len(sys.argv) < 3 or not os.path.isdir(sys.argv[2]):
        print(USAGE)
        sys.exit()

    if os.path.isfile(sys.argv[1]):
        archive = tarfile.open(sys.argv[1])
        chunks = sorted(archive.getnames(), key=chunk_coordinates)
        for chunk in tqdm(chunks):
            chunk_to_tiles(archive.extractfile(chunk), chunk)
    else:
        chunks = sorted(glob(sys.argv[1]+'chunk_*.jpg'), key=chunk_coordinates)
        for chunk in tqdm(chunks):
            chunk_to_tiles(chunk)

    for zoom in range(9, 0, -1):
        tiles = sorted(
            glob('{}{}/*/*.jpg'.format(sys.argv[2], zoom+1)),
            key=tile_coordinates)
        for tile in tqdm(tiles):
            zoom_out(tile, zoom)

def zoom_out(filename, zoom):
    """Shrink and combine tiles to zoom view out."""
    source_x, source_y = tile_coordinates(filename)
    tile_x = source_x // 2
    tile_y = source_y // 2
    origin_x = tile_x * 2
    origin_y = tile_y * 2

    if not os.path.isfile(
            '{}{}/{}/{}.jpg'.format(sys.argv[2], zoom, tile_y, tile_x)):
        os.makedirs('{}{}/{}'.format(sys.argv[2], zoom, tile_y), exist_ok=True)

        tile_image = Image.new('RGB', (512, 512))
        for x_adj in range(2):
            for y_adj in range(2):
                try:
                    paste_image = Image.open('{}{}/{}/{}.jpg'.format(
                        sys.argv[2], zoom+1, origin_y+y_adj, origin_x+x_adj))
                except FileNotFoundError:
                    paste_image = Image.new('RGB', (256, 256))

                tile_image.paste(
                    paste_image,
                    (x_adj*256, y_adj*256))

        tile_image.resize((256, 256)).save('{}{}/{}/{}.jpg'.format(
            sys.argv[2], zoom, tile_y, tile_x))

def chunk_coordinates(filename):
    """Extract chunk coordinates from filename."""
    _, chunk_x, chunk_y = os.path.splitext(filename)[0].split('_')
    return (int(chunk_x), int(chunk_y))

def tile_coordinates(path):
    """Compute tile coordinates."""
    explosion = os.path.splitext(path)[0].split('/')
    return (int(explosion[-1]), int(explosion[-2]))

def chunk_to_tiles(chunk, chunkname=None):
    """Convert the chunk screenshot to Leaflet tiles at maximum zoom."""
    chunk_image = Image.open(chunk)
    if chunkname is None:
        chunk_x, chunk_y = chunk_coordinates(chunk)
    else:
        chunk_x, chunk_y = chunk_coordinates(chunkname)
    tile_x = chunk_x*4
    tile_y = chunk_y*4

    if not os.path.isfile(
            '{}{}/{}/{}.jpg'.format(sys.argv[2], 10, tile_y, tile_x)):
        for x_adj in range(4):
            for y_adj in range(4):
                os.makedirs(
                    '{}{}/{}'.format(
                        sys.argv[2], 10, tile_y+y_adj),
                    exist_ok=True)

                chunk_image.crop(
                    (
                        x_adj*256,
                        y_adj*256,
                        (x_adj+1)*256,
                        (y_adj+1)*256)
                    ).save('{}{}/{}/{}.jpg'.format(
                        sys.argv[2], 10, tile_y+y_adj, tile_x+x_adj))

if __name__ == '__main__':
    main()
