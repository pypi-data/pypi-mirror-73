import panel as pn
import numpy as np # used for the arrays and other mathematical operations
import astropy.io.fits as pyfits # used to handle fits files
import matplotlib.pyplot as plt # used for making plots
from matplotlib.figure import Figure
pn.extension()


class Cube:
    
    def __init__(self, file_name):

        # Open the .fits, get the data and the header, close the file
        cube_fits = pyfits.open(file_name)
        self.data = cube_fits[0].data
        self.header = cube_fits[0].header
        cube_fits.close()
        
        # Create other class variables based on the data
        # number of frames
        self.nframes = int(max(self.data.shape))
        self.trimmed_data = self.data.copy()
        
    def trimData(self, s1, e1, s2, e2):
        self.trimmed_data = self.data[:, s1:e1, s2:e2].copy()
        
        
    def displayFrameInteractive(self, frame_number, needs_grid, s1, e1, s2, e2):
        fig, ax = plt.subplots(figsize = (8,8))
        ax.set_xlabel('Pixel Number')
        ax.set_ylabel('Pixel Number')
        ax.set_title('Frame Displayer')
        
        im = ax.imshow(self.data[frame_number, s1:e1, s2:e2], cmap='gray')

        plt.colorbar(im)
        
        if needs_grid:
            plt.grid()

        return fig
    
    def interactiveDataDisplay(self):
        
        # Create all the widgets used
        
        # First we have an Int Slider for the frame number being displayed
        frame_number_w = pn.widgets.IntSlider(name='Frame', start=0, 
                                              end=self.nframes-1, 
                                              step=1, value=0)
        frame_number_w.bar_color = '#59C1DD'
        
        
        # We have a Checkbox to display a grid on top of the meshgrid
        needs_grid_w = pn.widgets.Checkbox(name='Display Grid')
        
        
        # Now we have four widgets used to set the start and end indexes for both axes
        # lower limit of first axis
        l1_number1_w = pn.widgets.IntSlider(name="First Axis' start", start=0, 
                                            end=self.data.shape[1]-1, 
                                            step=1, value=0)

        l1_number1_w.bar_color = '#59C1DD'
        
        # upper limit of first axis
        l1_number2_w = pn.widgets.IntSlider(name="First Axis' end", start=0, 
                                            end=self.data.shape[1]-1, 
                                            step=1, value=self.data.shape[1]-1)

        l1_number2_w.bar_color = '#59C1DD'
        
        # lower limit of second axis
        l2_number1_w = pn.widgets.IntSlider(name="Second Axis' start", start=0, 
                                            end=self.data.shape[2]-1, 
                                            step=1, value=0)
        
        l2_number1_w.bar_color = '#59C1DD'
        
        # upper limit of second axis
        l2_number2_w = pn.widgets.IntSlider(name="Second Axis' end", start=0, 
                                            end=self.data.shape[2]-1, 
                                            step=1, value=self.data.shape[2]-1)

        l2_number2_w.bar_color = '#59C1DD'
        
        # dimensions of the trimmed cube
        dim_txt_w = pn.widgets.StaticText(value=f"Dimensions of Trimmed Data: ({self.trimmed_data.shape[0]}, {self.trimmed_data.shape[1]}, {self.trimmed_data.shape[2]})")
        
        
        # trim button
        trim_button_w = pn.widgets.Button(name='Trim Data', button_type='primary')
        
        
        # Now we define the reactive funtion for the visualization and the funtion that trims the data
        def internal_trim_data(event):
            
            # Trim the data
            self.trimmed_data = self.data[:, l1_number1_w.value:l1_number2_w.value, l2_number1_w.value:l2_number2_w.value]
            
            # Update the static text
            dim_txt_w.value = f"Dimensions of Trimmed Data: ({self.trimmed_data.shape[0]}, {self.trimmed_data.shape[1]}, {self.trimmed_data.shape[2]})"
            
            
            
        
        @pn.depends(frame_number_w, needs_grid_w, l1_number1_w, l1_number2_w, l2_number1_w, l2_number2_w)
        def reactive_frames(frame_number, needs_grid, s1, e1, s2, e2):
            
            plt.close()
            
            # Update the max and min values for the trimming int sliders
            l1_number1_w.end = l1_number2_w.value - 1
            l1_number2_w.start = l1_number1_w.value + 1
            
            l2_number1_w.end = l2_number2_w.value - 1
            l2_number2_w.start = l2_number1_w.value + 1
            
            
            return self.displayFrameInteractive(frame_number, needs_grid, s1, e1, s2, e2)

        
        # assing the trim function to the trim button
        trim_button_w.on_click(internal_trim_data)
        
        # create the dashboard
        self.data_display = pn.Row(reactive_frames, 
                                   pn.Column('<br>\n# Interactive Data Display',
                                             frame_number_w,
                                             needs_grid_w,
                                             dim_txt_w,
                                             '<br>\n### Change the start and end positions of both axes',
                                             l1_number1_w,
                                             l1_number2_w,
                                             l2_number1_w,
                                             l2_number2_w,
                                             trim_button_w))
        
        # Display the dashboard
        self.data_display.show()
    
    def displayFrameStatic(self, frame_number, needs_grid=False):

        fig, ax = plt.subplots(figsize = (8,8))
        ax.set_xlabel('Pixel Number')
        ax.set_ylabel('Pixel Number')
        ax.set_title('Frame Displayer')
        im = ax.imshow(self.data[frame_number,:,:], cmap='gray')
        plt.colorbar(im)
        
        if needs_grid:
            plt.grid()

        plt.show()

