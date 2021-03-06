import numpy as np
from pyqtgraph import PlotWidget, mkPen, mkBrush
from kmap.config.config import config


class LMFitPlot(PlotWidget):

    def __init__(self, *args, **kwargs):

        super(LMFitPlot, self).__init__(*args, **kwargs)
        self._setup()

        self.plot_item = self.getPlotItem()

    def clear(self):

        self.plot_item.clear()


    def get_data(self):

        data_sets = []

        for item in self.plot_item.listDataItems():
            name = item.name()
            x, y = item.getData()
            data_sets.append({'name': name, 'x': x, 'y': y})

        return data_sets
        
    def plot(self, x, y, title):

        index = len(self.plot_item.listDataItems())
        colors = config.get_key('profile_plot', 'colors')
        color = colors.split(',')[index % len(colors)]
        line_width = int(config.get_key('profile_plot', 'line_width'))
        symbols = config.get_key('profile_plot', 'symbols')
        symbol = symbols.split(',')[index % len(symbols)]
        symbol_size = int(config.get_key('profile_plot', 'symbol_size'))

        self.plot_item.plot(x, y,
                            name=title,
                            pen=mkPen(color, width=line_width),
                            symbol=symbol,
                            symbolPen=mkPen(color, width=symbol_size),
                            symbolBrush=mkBrush(color))

    def set_label(self, x, y):

        self.setLabel('left', text=y)
        self.setLabel('bottom', text=x)
        
    def _setup(self):
        pass
        self.addLegend()
