

def plot_dataframe(data):
    import plotly.graph_objs as go
    import plotly
    from plotly.offline import iplot
    data_list = []
    for me_commo in data.columns:
        trace_sig = go.Scatter(
            x=data.index,
            y=data[me_commo],
            name=me_commo,
            opacity=0.8)
        data_list.append(trace_sig)
    iplot(data_list)


def plot_weights_df(data):
    import plotly.graph_objs as go
    import plotly
    from plotly.offline import iplot
    data_list = []
    for me_commo in data.columns:
        trace_sig = go.Scatter(
            x=data.index,
            y=data[me_commo],
            name=me_commo,
            opacity=0.8)
        data_list.append(trace_sig)
    iplot(data_list)


