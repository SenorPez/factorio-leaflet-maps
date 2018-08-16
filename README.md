# Factorio to Leaflet Maps

A Python script to convert [Factorio](http://factorio.com/) screenshots into [Leaflet](https://leafletjs.com/) map tiles.

## Getting Factorio Screenshots

1. In Factorio, open the console. The default hotkey for the console is **`**.
2. Paste the following command and press **Enter**.

```(lua)
/c game.player.surface.daytime = 0; for x=-1000,1000 do for y=-1000,1000 do if game.forces["player"].is_chunk_charted(1, {x, y}) then game.take_screenshot{show_entity_info=true, zoom=1, resolution={1024,1024}, position={x=32*x+16,y=32*y+16}, path="factoriomaps/chunk_"..x.."_"..y..".jpg"}; end; end; end;
```

> **NOTE:** Using console commands disables achievements in your current game. To retain achievements, reload your save after running the command.

3. A set of screenshots is taken and saved to `%APPDATA%\Factorio\script-output\factoriomaps`

## Getting Leaflet Tiles

### Script Requirements
  * [Python 3.6+](https://www.python.org/downloads/release/latest)
  * [Pillow](https://pypi.org/project/Pillow/)
  * [tqdm](https://pypi.org/project/tqdm/)
  
1. Execute the script: `python3 factoriomap.py [source] [destination]`
  * **Source:** The path to the directory containing the screenshots, or the path to a tar file containing the screenshots.
  * **Destination:** The path to a directory to hold the Leaflet tiles.
  
> **NOTE:** Depending on your system configuration, the command to run a Python 3 script (`python3` above) may differ. Use the appropriate command for your system.
> **NOTE:** The tar file option is useful if the screenshots need to be uploaded to a remote server before running the script.

2. The screenshots are converted to Leaflet tiles.

## Creating a Leaflet Map

1. Create an HTML page to launch Leaflet. A simple example page is included in the repository. Change `PATH_TO_TILE_DIRECTORY` to the actual path of the tile directory.

2. For further customation, see the Leaflet documentation.
