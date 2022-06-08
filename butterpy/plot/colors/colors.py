import matplotlib.pyplot as plt
from matplotlib import cm
from butterpy.util import get_file_lines

def get_cmap(name, n_colors=256):
    try:
        return plt.cm.get_cmap(name)
    except ValueError: # check in custom list
        lines = get_file_lines('cmaps.txt')
        colors = {}
        for l in lines:
            name,*hex_list = (s.strip() for s in l.split(','))
            colors[name] = hex_list
        if name in colors:
            return get_custom_cmap(colors, name)
        else:
            raise ValueError("color map name provided is not in mpl cmaps or custom defined maps")

def get_custom_cmap(custom_cmaps, cmap_name): #name, filename, mode='custom', map_name=None
    
    raise NotImplementedError("custom cmaps is broken currently")
    
    cols = [Color(cx) for cx in colors]
    n_arrays = len(cols_hex)-1
    cols_per_array = floor(N_cmap_cols/n_arrays)
    if interpolation_space.lower() == 'rgb':
        raise NotImplementedError()
    elif interpolation_space.lower() == 'hsv':
        raise NotImplementedError()
    elif interpolation_space.lower() == 'lch':
        raise NotImplementedError()
        ### this is broken -- in the middle of writing transformation from rgb-xyz-lab-lch (and back) ####
        colors_rgb = np.empty((3,N_cmap_cols), dtype=np.uint8)
        for i in range(n_arrays):
            bot_rgb_hex = [colors[i][1+2*j:3+2*j] for j in range(3)]
            top_rgb_hex = [colors[i+1][1+2*j:3+2*j] for j in range(3)]
            for comp,bot,top in zip(range(3), bot_rgb_hex, top_rgb_hex):
                b = int(bot,16)
                t = int(top,16)
                colors_rgb[comp, i*cols_per_array:(i+1)*cols_per_array] = [int((b+(t-b)*j/cols_per_array)) for j in range(cols_per_array)]
                colors_rgb[comp, cols_per_array*n_arrays:] = t # pad any extra slots from rounding errors
        cmaps[name] = colors_rgb # convert this to a cmap

    return cmaps

