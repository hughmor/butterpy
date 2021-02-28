from butterpy.plot.colors import get_cmap
from butterpy.plot.camera import Camera
from butterpy.config import get_animation_filename
import matplotlib.pyplot as plt
import matplotlib.animation as plt_anim
from numpy import sqrt

class LineAnimation:
    def __init__(self, system, **params):
        # get data from system
        self._sys = system

        # initialize figure
        self._fig, self._ax = self._init_fig(params)

        # set line aesthetics and plot
        self._line_visible = params.get("plot_line", True)
        if self._line_visible:
            col_name = params.get('line_color', None)
            cmap_name = params.get('line_cmap', None)
            if col_name is None and cmap_name is None:
                raise ValueError("must provide a line_color or line_cmap parameter")
            elif cmap_name is not None:
                self._solid_line_color = False
                self._line_cmap = get_cmap(cmap_name)
            elif col_name is not None:
                self._solid_line_color = True
                self._line_color = col_name

            self._line_width = params.get('line_width', 0.5)
            line_fraction = params.get("line_length", 0.1)
            self._line_len = int(line_fraction * self._sys.trajectory.shape[1])
            self._start_frame = self._line_len if params.get("line_start_visible", True) else 0
            lines = self.plot_trajectory(self._sys)
        else:
            lines = []
            self._start_frame = 0

        # set marker aesthetics and plot
        self._marker_visible = params.get("plot_marker", True)
        if self._marker_visible:
            self._marker_size = params.get("marker_size", 1.0)
            self._marker_color = params.get("marker_color", "white")
            marker = self.plot_marker(self._sys)
        else:
            marker = None

        # set background colour
        bg_color = params.get('bg_color', 'black')
        self._fig.set(facecolor=bg_color)
        self._ax.set(facecolor=bg_color)

        # set frame drawing parameters
        num_frames = self._sys.trajectory.shape[1] - 1 - self._start_frame
        self.frames = range(0, num_frames, 1)
        
        # get camera movement generator and set initial positions
        dist = params.get("distance", 5.0)
        azim = params.get("azimuth", 10.0)
        elev = params.get("elevation", 1.0)
        camera = Camera(num_frames, dist, azim, elev)
        self._ax.dist, self._ax.azim, self._ax.elev = next(camera)

        # make mpl animation
        artists = [marker] + lines
        animated_plot = plt_anim.FuncAnimation(
            self._fig, self._update_artists, self.frames, fargs=(self._sys.trajectory, artists, camera), interval=params["intvl"])
                    
        # make animation file and metadata
        filename = get_animation_filename(params)
        metadata = { #TODO: generalize this
            "artist": 'Hugh Morison',
            "title": f'{self._sys.__class__.__name__} System',
            "comment": f'System parameters: (sigma,rho,beta)=({(x for x in self._sys.parameters)})\nInitial State: (x,y,z)=({(x for x in self._sys.initial_state)})\n',
        }
        movie_writer = params.get('movie_writer','ffmpeg')
        dpi = params.get("dpi", 256)
        fps = params["fps"]
        br = params["br"]
        Writer = plt_anim.writers[movie_writer]
        writer = Writer(fps=fps, metadata=metadata, bitrate=br) #, extra_args=extras)

        animated_plot.save(filename, writer=writer, dpi=dpi)

        print(f"Done rendering: saved as {filename}")

    def _update_artists(self, frame_num, data, artists, camera):
        lead_point = self._start_frame + frame_num
        if self._marker_visible:
            marker = artists[0]
            marker.set_data(data[0:2, lead_point+1])
            marker.set_3d_properties(data[2, lead_point+1])

        if self._line_visible:
            lines = artists[1:]
            lines[lead_point].set_visible(True) # add next line
            
            line_end = lead_point-self._line_len
            if line_end >= 0:
                lines[line_end].set_visible(False) # remove furthest back line
        
        try:
            self._ax.dist, self._ax.azim, self._ax.elev = next(camera)
        except:
            print(frame_num)
            raise

        return [marker] + lines

    def plot_trajectory(self, system):
        trajectory = system.trajectory
        speeds = system.speeds
        lines = []
        for i in range(0,len(trajectory[0])-1,1):
            color = self._line_color if self._solid_line_color else self._line_cmap(speeds[i]/system.max_speed)
            lines.append(self._ax.plot(trajectory[0, i:i+2], trajectory[1, i:i+2], trajectory[2, i:i+2], lw=self._line_width, color=color)[0])
            if i >= self._start_frame:
                lines[i].set_visible(False)
        return lines

    def plot_marker(self, system):
        trajectory = system.trajectory
        speeds = system.speeds
        frame = self._start_frame+2
        dot = self._ax.plot(trajectory[0, frame], trajectory[1, frame], trajectory[2, frame], '.', markersize=self._marker_size, color=self._marker_color)[0] # , linestyle='None'
        return dot
                    
    def _init_fig(self, params):
        figsize = params.get("fig_size", (12,12))
        dpi = params.get("dpi", 256)
        fig = plt.figure(figsize=figsize, dpi=dpi)
        ax = fig.add_subplot(projection="3d")
        plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0) # remove margin between ax and fig
        if params.get("hide_axes", True):
            ax.set_axis_off()
        else:
            raise NotImplementedError("Need to add axis styling")
        return fig,ax