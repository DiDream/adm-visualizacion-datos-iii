import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class ADMChart:
    def __init__(self, x_axis_name, y_axis_name, csv_data):
        self.x_axis_name = x_axis_name if len(x_axis_name) > 1 else x_axis_name[0]
        self.y_axis_name = y_axis_name if len(y_axis_name) > 1 else y_axis_name[0]
        self.csv_data = csv_data

    def get_axis_size(self):
        if isinstance(self.x_axis_name, list):
            return len(self.x_axis_name)
        else:
            return len(self.csv_data[self.x_axis_name])

    def generate_chart(self, chart_name):
        x_axis_size = self.get_axis_size()
        figure_width = x_axis_size * 0.15
        if figure_width < 15:
            figure_width = 15
        elif figure_width > 25:
            figure_width = 25

        chart = plt.figure(figsize=(figure_width, 5))

        # Ancho adaptable al contenido -> https://stackoverflow.com/a/54756766
        axes_left = 1 / figure_width
        axes = chart.add_axes([axes_left, 0.15, 0.98 - axes_left, 0.75])
        axes.set_title(chart_name)
        axes.grid()
        axes.tick_params(axis='x', which='major', labelsize=8.5)
        axes.tick_params(axis='x', labelrotation=90)
        axes.margins(x=(1 / x_axis_size))

        self.set_type_chart(axes)

        if isinstance(self.x_axis_name, list) or isinstance(self.y_axis_name, list):
            chart.legend()

        return chart

    def set_type_chart(self, axes):
        pass


class LineChart(ADMChart):
    def set_type_chart(self, axes):
        if isinstance(self.x_axis_name, list):
            for index, row in self.csv_data.iterrows():
                axes.plot(row[self.x_axis_name], label=row[self.y_axis_name])
        elif isinstance(self.y_axis_name, list):
            axes.set_xlabel(self.x_axis_name)
            for name in self.y_axis_name:
                axes.plot(self.csv_data[self.x_axis_name], self.csv_data[name], label=name)
        else:
            axes.set_xlabel(self.x_axis_name)
            axes.set_ylabel(self.y_axis_name)
            axes.plot(self.csv_data[self.x_axis_name], self.csv_data[self.y_axis_name])


class BarChart(ADMChart):

    def set_type_chart(self, axes):
        if isinstance(self.x_axis_name, list):
            x_axis_range = np.arange(len(self.x_axis_name))
            series_number = len(self.csv_data)
            axes.margins(x=0)
            padding = 0.05
            bar_width = (1 - padding) / series_number

            for index, row in self.csv_data.iterrows():
                axes.bar(
                    (x_axis_range - (0.5 - (padding / 2)) + (bar_width / 2)) + (index * bar_width),
                    row[self.x_axis_name],
                    label=row[self.y_axis_name],
                    width=bar_width
                )
            plt.xticks(x_axis_range, self.x_axis_name)

        elif isinstance(self.y_axis_name, list):
            axes.set_xlabel(self.x_axis_name)
            x_axis = self.csv_data[self.x_axis_name]

            x_axis_range = np.arange(len(x_axis))
            series_number = len(self.y_axis_name)
            axes.margins(x=0)
            padding = 0.05
            bar_width = (1 - padding) / series_number

            for index in range(len(self.y_axis_name)):
                name = self.y_axis_name[index]
                axes.bar(
                    (x_axis_range - (0.5 - (padding / 2)) + (bar_width / 2)) + (index * bar_width),
                    self.csv_data[name],
                    label=name,
                    width=bar_width
                )
            plt.xticks(x_axis_range, x_axis)
        else:
            axes.set_xlabel(self.x_axis_name)
            axes.set_ylabel(self.y_axis_name)
            axes.bar(self.csv_data[self.x_axis_name], self.csv_data[self.y_axis_name])


class ScatterChart(ADMChart):
    def __init__(self, x_axis_name, y_axis_name, csv_data):
        super().__init__(x_axis_name, y_axis_name, csv_data)
        self.x_axis_name = self.x_axis_name[0] if isinstance(self.x_axis_name, list) else self.x_axis_name
        self.y_axis_name = self.y_axis_name[0] if isinstance(self.y_axis_name, list) else self.y_axis_name

    def set_type_chart(self, axes):
        axes.set_xlabel(self.x_axis_name)
        axes.set_ylabel(self.y_axis_name)
        axes.scatter(self.csv_data[self.x_axis_name], self.csv_data[self.y_axis_name])


class ViolinChart(ADMChart):
    def __init__(self, x_axis_name, y_axis_name, csv_data):
        super().__init__(x_axis_name, y_axis_name, csv_data)
        self.x_axis_name = self.x_axis_name[0] if isinstance(self.x_axis_name, list) else self.x_axis_name
        self.y_axis_name = self.y_axis_name[0] if isinstance(self.y_axis_name, list) else self.y_axis_name

    def generate_chart(self, chart_name):
        fig = plt.figure()
        fig.suptitle(chart_name)

        chart = sns.violinplot(x=self.csv_data[self.x_axis_name], y=self.csv_data[self.y_axis_name])
        chart.set_xticklabels(chart.get_xticklabels(), rotation=45, horizontalalignment='right')
        return fig


# No es necesario --y-axis
class HistogramChart(ADMChart):
    def generate_chart(self, chart_name):
        fig = plt.figure()

        fig.suptitle(chart_name)

        # Disable Kernel density estimation -> https://stackoverflow.com/a/57802471
        sns.distplot(self.csv_data[self.x_axis_name], kde=False, norm_hist=False)

        return fig


class BoxPlotChart(ADMChart):
    def __init__(self, x_axis_name, y_axis_name, csv_data):
        super().__init__(x_axis_name, y_axis_name, csv_data)
        self.x_axis_name = self.x_axis_name[0] if isinstance(self.x_axis_name, list) else self.x_axis_name
        self.y_axis_name = self.y_axis_name[0] if isinstance(self.y_axis_name, list) else self.y_axis_name

    def generate_chart(self, chart_name):
        fig = plt.figure()
        fig.suptitle(chart_name)

        chart = sns.boxplot(x=self.csv_data[self.x_axis_name], y=self.csv_data[self.y_axis_name])
        chart.set_xticklabels(chart.get_xticklabels(), rotation=45, horizontalalignment='right')
        return fig


chart_constructors = {
    'bar': BarChart,
    'line': LineChart,
    'scatter': ScatterChart,
    'violin': ViolinChart,
    'histogram': HistogramChart,
    'box': BoxPlotChart
}