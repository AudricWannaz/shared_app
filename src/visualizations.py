import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

@st.experimental_memo
def create_histograms(full_df, abbreviated_df, x_axis, title):

	trace1 = go.Histogram(
    x=abbreviated_df[x_axis],
    histfunc='count',
    name='Abbreviations',
	opacity=1.0,
	marker=dict(color='rgba(255, 0, 0, 0.6)'),
	nbinsx=20,
	hovertemplate='Period Min: %{x}<br>Abbrev Count: %{y}<br>'
)

	# Create a histogram trace for all the data
	trace2 = go.Histogram(
    x=full_df[x_axis],
    histfunc='count',
    name='All words',
    opacity=0.6,
    marker=dict(color='rgba(0, 0, 255, 0.6)'),
	hovertemplate='Period Min: %{x}<br>Word Count: %{y}<br>'
	)

	# Combine the traces in a single figure
	fig = go.Figure()

	fig.add_trace(trace1)
	fig.add_trace(trace2)
	# Customize the layout
	fig.update_layout(
		barmode='overlay', # This will make the histograms overlap
		title=title,
		xaxis_title=x_axis.title(),
		yaxis_title='Count',
		legend_title='Legend',
		margin=dict(t=50, b=0),
        xaxis=dict(
            tickformat="%Y"
        )
	)

	# Display the figure
	return fig

@st.experimental_memo
def create_barplot(full_df, abbreviated_df):
    # Compute the counts for each period_min value in both DataFrames
    full_counts = full_df['period'].value_counts().sort_index()
    abbrev_counts = abbreviated_df['period'].value_counts().sort_index()

    trace1 = go.Bar(
        x=abbrev_counts.index,
        y=abbrev_counts.values,
        name='Abbreviations',
        opacity=1.0,
        marker=dict(color='rgba(0, 0, 255, 0.6)'),
        hovertemplate='Period Min: %{x}<br>Abbrev Count: %{y}<br>'
    )

    trace2 = go.Bar(
        x=full_counts.index,
        y=full_counts.values,
        name='All words',
        opacity=0.3,
        marker=dict(color='rgba(255, 0, 0, 0.6)'),
        hovertemplate='Period Min: %{x}<br>Word Count: %{y}<br>'
    )

    fig = go.Figure()

    fig.add_trace(trace1)
    fig.add_trace(trace2)

    # Customize the layout
    fig.update_layout(
        barmode='overlay',
        title={
            'text': 'Frequencies of words vs abbreviations over time',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'size': 24,
                'color': 'black',
            }
        },
        xaxis=dict(
            title='Period Min',
            titlefont=dict(size=16, color='black'),
            tickfont=dict(size=14, color='black'),
        ),
        yaxis=dict(
            title='Count',
            titlefont=dict(size=16, color='black'),
            tickfont=dict(size=14, color='black'),
        ),
        legend=dict(
            font=dict(size=14, color='black'),
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        plot_bgcolor='white',
        xaxis_showgrid=True,
        yaxis_showgrid=True,
        xaxis_gridcolor='lightgrey',
        yaxis_gridcolor='lightgrey',
    )

    # Update the bar borders
    fig.update_traces(marker=dict(line=dict(color='black', width=1)))

    return fig
# def create_barplot(full_df, abbreviated_df):

#     # Compute the counts for each period_min value in both DataFrames
#     full_counts = full_df['period'].value_counts().sort_index()
#     abbrev_counts = abbreviated_df['period'].value_counts().sort_index()

#     trace1 = go.Bar(
#         x=abbrev_counts.index,
#         y=abbrev_counts.values,
#         name='Abbreviations',
#         opacity=1.0,
#         marker=dict(color='rgba(0, 0, 255, 0.6)'),
#         hovertemplate='Period Min: %{x}<br>Abbrev Count: %{y}<br>'
#     )

#     trace2 = go.Bar(
#         x=full_counts.index,
#         y=full_counts.values,
#         name='All words',
#         opacity=0.3,
#         marker=dict(color='rgba(255, 0, 0, 0.6)'),
#         hovertemplate='Period Min: %{x}<br>Word Count: %{y}<br>'
#     )

#     fig = go.Figure()

#     fig.add_trace(trace1)
#     fig.add_trace(trace2)
#         # Explicitly set the legend colors to match the trace colors
#     fig.update_traces(marker=dict(line=dict(color='rgba(0, 0, 255, 0.6)', width=0)), selector=dict(name='Abbreviations'))
#     fig.update_traces(marker=dict(line=dict(color='rgba(255, 0, 0, 0.6)', width=0)), selector=dict(name='All words'))
#     fig.update_layout(
#         barmode='overlay',
#         title='Frequencies of words vs abbreviations over time',
#         xaxis_title='Period Min',
#         yaxis_title='Count',
#         legend_title='Legend',
#         margin=dict(t=50, b=0),
#     )
#     return fig
@st.experimental_memo
def create_pie_chart(counts, title):
    # Iterate over each column in the counts DataFrame and create a pie chart
    # Create a pie chart
    # fig = go.Figure(go.Pie(labels=counts.index, values=counts.values,
    #                         hovertemplate='Category: %{label}<br>Count: %{value}<br>'))

    # # Customize the layout
    # fig.update_layout(title=title)
        # Create a pie chart
    fig = go.Figure(go.Pie(labels=counts.index, values=counts.values,
                            hovertemplate='Category: %{label}<br>Count: %{value}<br>',
                            textinfo='label+percent',
                            insidetextorientation='radial'))
    
    # Customize the layout
    fig.update_layout(
        title={
            'text': title,
            'y': 1.0,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'size': 24,
                'color': 'black',
            }
        },
        legend=dict(
            font=dict(size=14, color='black'),
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        # Change the background color of the plot
        plot_bgcolor='white',
    )

    # Customize the color scale
    fig.update_traces(marker=dict(
        colors=px.colors.qualitative.Plotly, # Choose a color scale: https://plotly.com/python/discrete-color/
        line=dict(color='black', width=1) # Add a border to the pie slices
    ))

    return fig
        # Display the figure
@st.experimental_memo
def create_3d_bar_plot(df, x, y, color, title):
    #fig = px.bar(df, x=x, y=y, color=color, title=title)
    fig = px.bar(df, x=x, y=y, color=color, title=title)
    
    # Customize the layout
    fig.update_layout(
        title={
            'text': title,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'size': 24,
                'color': 'black',
            }
        },
        xaxis=dict(
            title=x,
            titlefont=dict(size=16, color='black'),
            tickfont=dict(size=14, color='black'),
        ),
        yaxis=dict(
            title=y,
            titlefont=dict(size=16, color='black'),
            tickfont=dict(size=14, color='black'),
        ),
        legend=dict(
            font=dict(size=14, color='black'),
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        # Change the background color of the plot and the color of the gridlines
        plot_bgcolor='white',
        xaxis_showgrid=True,
        yaxis_showgrid=True,
        xaxis_gridcolor='lightgrey',
        yaxis_gridcolor='lightgrey',
    )

    # Customize the color scale
    fig.update_traces(marker=dict(
        colorscale='Viridis', # Choose a colorscale: https://plotly.com/python/builtin-colorscales/
        line=dict(color='black', width=0.1) # Add a border to the bars
    ))

    return fig