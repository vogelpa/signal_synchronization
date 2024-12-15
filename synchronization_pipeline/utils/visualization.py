# utils/visualization.py
import plotly.graph_objects as go
import plotly.io as pio
import os

def plot_interactive_html(df1, df2, resampled_df2, signal_column1, signal_column2, input_file1, input_file2, plot_settings):
    scaling_factor_reference = plot_settings['scaling_factor_reference']
    scaling_factor_align = plot_settings['scaling_factor_align']

    fig = go.Figure()

    # Plot original signal from input_file1
    fig.add_trace(go.Scatter(
        x=df1['timestamp'],
        y=df1[signal_column1]*scaling_factor_reference,
        mode='lines',
        name=f'Original {os.path.basename(input_file1)}'
    ))

    # Plot original signal from input_file2
    fig.add_trace(go.Scatter(
        x=df2['timestamp'],
        y=df2[signal_column2]*scaling_factor_align,
        mode='lines',
        name=f'Original {os.path.basename(input_file2)}',
        line=dict(color='orange')
    ))

    # Plot resampled signal from input_file2
    fig.add_trace(go.Scatter(
        x=resampled_df2['timestamp'],
        y=resampled_df2[signal_column2]*scaling_factor_align,
        mode='lines',
        name='Resampled Signal 2',
        line=dict(color='purple')
    ))

    # Annotate even and odd events for input_file1
    even_events = df1[(df1['event_id'].notna()) & (df1['event_id'] % 2 == 0)]
    odd_events = df1[(df1['event_id'].notna()) & (df1['event_id'] % 2 == 1)]

    # Plot even events
    fig.add_trace(go.Scatter(
        x=even_events['timestamp'],
        y=even_events[signal_column1]*scaling_factor_reference,
        mode='markers',
        marker=dict(color='green', symbol='circle'),
        name='File 1 Even Event ID'
    ))

    # Plot odd events
    fig.add_trace(go.Scatter(
        x=odd_events['timestamp'],
        y=odd_events[signal_column1]*scaling_factor_reference,
        mode='markers',
        marker=dict(color='red', symbol='circle'),
        name='File 1 Odd Event ID'
    ))

    # Annotate even and odd events for input_file2
    even_events_2 = df2[(df2['event_id'].notna()) & (df2['event_id'] % 2 == 0)]
    odd_events_2 = df2[(df2['event_id'].notna()) & (df2['event_id'] % 2 == 1)]

    # Plot even events for original_df2
    fig.add_trace(go.Scatter(
        x=even_events_2['timestamp'],
        y=even_events_2[signal_column2]*scaling_factor_align,
        mode='markers',
        marker=dict(color='blue', symbol='diamond'),
        name='File 2 Even Event ID'
    ))

    # Plot odd events for original_df2
    fig.add_trace(go.Scatter(
        x=odd_events_2['timestamp'],
        y=odd_events_2[signal_column2]*scaling_factor_align,
        mode='markers',
        marker=dict(color='black', symbol='diamond'),
        name='File 2 Odd Event ID'
    ))

    # Set plot title and labels
    fig.update_layout(
        title='Detected Events and Signal Alignment',
        xaxis_title='Timestamp',
        yaxis_title='1D Signal',
        template='plotly_white'
    )

    # Save and open the plot as an HTML file
    pio.write_html(fig, file='interactive_plot.html', auto_open=True)
