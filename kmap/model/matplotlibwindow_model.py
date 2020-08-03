from kmap.config.config import config


class MatplotlibWindowModel():

    def __init__(self, plot_data):

        self.image = plot_data.data
        self.x, self.y = self._calc_centered_axes(plot_data)
        '''
        if config.get_key('matplotlib', 'pixel_center') == 'True':
            self.x, self.y = self._calc_centered_axes()

        else:
            self.x, self.y = 0, 0'''

    def _calc_centered_axes(self, plot_data):

        x_step_size = plot_data.step_size[0]
        centered_range = plot_data.range[0] + \
            [-x_step_size / 2, x_step_size / 2]
        x = plot_data.axis_from_range(
            centered_range, len(plot_data.x_axis) + 1)

        y_step_size = plot_data.step_size[1]
        centered_range = plot_data.range[1] + \
            [-y_step_size / 2, y_step_size / 2]
        y = plot_data.axis_from_range(
            centered_range, len(plot_data.y_axis) + 1)

        return x, y
