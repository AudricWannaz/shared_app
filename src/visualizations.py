import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

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
        # Calculate the proportions (percentages)
    abbrev_proportions = ((abbrev_counts / full_counts)*100).round(2)
    abbrev_proportions_text = abbrev_proportions.astype(str) + '%'
    non_abbrev_proportions_text = ((100-abbrev_proportions).round(2)).astype(str) +'%'
    trace1 = go.Bar(
        x=abbrev_counts.index,
        y=abbrev_counts.values,
        name='Abbreviations',
        opacity=1.0,
        marker=dict(color='rgba(0, 0, 255, 0.6)'),
        hovertemplate='Period Min: %{x}<br>Abbrev Count: %{y}<br>',
        text=abbrev_proportions_text
    )

    trace2 = go.Bar(
        x=full_counts.index,
        y=full_counts.values,
        name='Not abbreviated',
        opacity=0.3,
        marker=dict(color='rgba(255, 0, 0, 0.6)'),
        hovertemplate='Period: %{x}<br>Word Count: %{y}<br>',
        text=non_abbrev_proportions_text
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
            title='Period',
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
        yaxis_gridcolor='lightgrey'
    )

    # Update the bar borders
    fig.update_traces(marker=dict(line=dict(color='black', width=1)),
    textfont=dict(size=14, color='black'))

    return fig

@st.experimental_memo
def create_pie_chart(counts, title):

    counts = counts.sort_index()
    # Sort the counts Series by index (alphabetically)

    # Define the color scale
    color_scale = px.colors.qualitative.Plotly

    # Create a color mapping dictionary based on the sorted index
    color_mapping = {category: color_scale[i % len(color_scale)] for i, category in enumerate(sorted(counts.index))}

    # Get the colors for the current categories
    category_colors = [color_mapping[category] for category in counts.index]

    fig = go.Figure(go.Pie(labels=counts.index, values=counts.values,
                            hovertemplate='Category: %{label}<br>Count: %{value}<br>',
                            textinfo='label+percent',
                            insidetextorientation='radial',
                            marker_colors=category_colors))
    
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
        plot_bgcolor='white'
    )
    fig.update_layout(margin=dict(t=120))
    # Customize the color scale and add a border to the pie slices
    fig.update_traces(marker=dict(line=dict(color='black', width=1)))

    return fig
        # Display the figure

@st.experimental_memo
def create_stacked_bar_plot(df, x, y, color, title):
    grouped_df = df.groupby([x, color])[y].sum().reset_index()
    total_count = grouped_df.groupby(x)[y].sum().reset_index()
    total_count.columns = [x, 'total']

    merged_df = pd.merge(grouped_df, total_count, on=x)
    merged_df['proportion'] = (merged_df[y] / merged_df['total']) * 100
    merged_df['text'] = merged_df['proportion'].round(2).astype(str) + '%'

    fig = go.Figure()

    for cat in merged_df[color].unique():
        cat_df = merged_df[merged_df[color] == cat]
        fig.add_trace(go.Bar(
            x=cat_df[x],
            y=cat_df[y],
            name=cat,
            text=cat_df['text'],
            textposition='inside',
            insidetextanchor='start',
            textfont=dict(size=10, color='white')
        ))

    fig.update_layout(
        title=title,
        xaxis_title=x,
        yaxis_title=y,
        barmode='stack'
    )

    return fig