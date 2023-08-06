class Category():
    def __init__(self, name=None, cat_type="gauge", cat_help="No help added to the category"):
        self.name = name
        self.cat_type = cat_type
        self.cat_help = cat_help
        self.metrics = []

    def add_metric(self, metric):
        self.metrics.append(metric)
        metric.category = self

    def remove_metric(self, metric):
        self.metrics.remove(metric)
        metric.category = None

    def clear(self):
        self.metrics.clear()