

def init_napoleon_colab():
    from napoleontoolbox.signal import signal_utility
    from napoleontoolbox.analyzer import minutely_market, hourly_market, market
    from datetime import datetime
    import pandas as pd
    from napoleontoolbox.file_saver import dropbox_file_saver
    from __future__ import print_function
    from ipywidgets import interact, interactive, fixed, interact_manual
    import ipywidgets as widgets
    from napoleontoolbox.utility import metrics

    from pathlib import Path

    import matplotlib.pyplot as plt


    import plotly.offline as py
    py.init_notebook_mode(connected=True)
    import plotly.graph_objs as go
    import plotly
    from plotly.offline import iplot

    def configure_plotly_browser_state():
      import IPython
      display(IPython.core.display.HTML('''
            <script src="/static/components/requirejs/require.js"></script>
            <script>
              requirejs.config({
                paths: {
                  base: '/static/base',
                  plotly: 'https://cdn.plot.ly/plotly-latest.min.js?noext',
                },
              });
            </script>
            '''))
    import IPython

    configure_plotly_browser_state()
    IPython.get_ipython().events.register('pre_run_cell', configure_plotly_browser_state)