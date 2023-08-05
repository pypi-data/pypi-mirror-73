from plotly.subplots import make_subplots

import plotly.graph_objs as go



def generate_rebalanced_indice_weight_composition(weights_df):
    fig = make_subplots(rows=2, cols=1)

    fig.append_trace(
        go.Scatter(
            x=weights_df.index,
            y=weights_df.indice,
            name='Rebalanced Indice',
            opacity=0.8),
        row=1, col=1)

    constituents = [col for col in weights_df.columns if col not in ['indice']]
    for me_constituent in constituents:
        trace_sig = go.Scatter(
            x=weights_df.index,
            y=weights_df[me_constituent],
            name=me_constituent,
            opacity=0.8)
        fig.append_trace(trace_sig, row=2, col=1)

    fig.update_layout(height=600, width=1600, title_text="Weights composition")

    return fig

