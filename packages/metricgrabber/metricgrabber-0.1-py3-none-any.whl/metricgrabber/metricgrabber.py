import socket
from kthread import KThread
from flask import Flask, make_response

class MetricGrabber:
    objects = []
    newline = "\n"
    _webserver_process = None

    def __init__(self, host="127.0.0.1", port=None):
        if port is not None:
            self.start_web_server(host, port)

    def create_flask_server(self, host, port, metricgrabber_object):
        app = Flask(__name__)

        @app.route('/metrics')
        def get_metrics():
            response = make_response(metricgrabber_object.get_all_metrics_string())
            response.headers['Content-Type'] = 'text/plain'
            return response

        self._webserver_app = app

        app.run(host=host, port=port)

    def start_web_server(self, host, port):
        self._webserver_process = KThread(target=self.create_flask_server, args=(host, port, self))
        self._webserver_process.start()
        pass
    
    def stop_web_server(self):
        if self._webserver_process is not None:
            self._webserver_process.kill()
            self._webserver_process = None

    def get_all_metrics(self):
        metrics = []
        for obj in self.objects:
            if hasattr(obj, 'get_metrics'):
                metrics.extend(obj.get_metrics())
        return metrics

    def get_all_metrics_string(self):
        metrics_strings = []
        for metric_category in self.get_all_metrics():
            category_name = metric_category.name

            # Category header
            metrics_strings.append('# HELP %s %s' % (category_name, metric_category.cat_help))
            metrics_strings.append('# TYPE %s %s' % (category_name, metric_category.cat_type))
            
            # Values
            for metric in metric_category.metrics:
                params = metric.params
                params['hostname'] = socket.gethostname()
                metrics_strings.append('%s{%s} %s' % (category_name, ", ".join(f'{key}="{value}"' for key, value in params.items()), metric.value))

            # Add newline
            metrics_strings.append(self.newline)
            
        metrics = self.newline.join(metrics_strings)
        return metrics

    def add_metric_object(self, obj):
        if isinstance(obj, list):
            self.objects.extend(obj)
        else:
            self.objects.append(obj)

    def pack(self, *args):
        return list(args)