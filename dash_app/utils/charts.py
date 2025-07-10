import plotly.graph_objects as go
from theme.colours import *
from datetime import datetime, timedelta

# N.B comment out fig.show()

def create_progress_chart(meas_data, GOAL_WEIGHT):
    start_date = datetime.strptime(meas_data['Date'].iloc[0],"%Y-%m-%d")
    current_date = datetime.strptime(meas_data['Date'].iloc[-1],"%Y-%m-%d")
    current_progress = ((meas_data['Weight'].iloc[0] - meas_data['Weight'].iloc[-1]) / (meas_data['Weight'].iloc[0] - GOAL_WEIGHT))
    percent_lost = ((meas_data['Weight'].iloc[0] - meas_data['Weight'].iloc[-1]) / (meas_data['Weight'].iloc[0] - GOAL_WEIGHT)) * 100
    elapsed_time = current_date - start_date
    projected_total_duration = elapsed_time / current_progress
    projected_end_date = start_date + projected_total_duration

    start_str = start_date.strftime("%d %b %Y")
    current_str = current_date.strftime("%d %b %Y")
    projected_str = projected_end_date.strftime("%d %b %Y")

    fig = go.Figure()

    # Completed section
    fig.add_trace(go.Bar(
        x=[percent_lost],
        y=["Progress"],
        orientation="h",
        marker=dict(color=DASH_PURPLE_LIGHT),
        name="Completed",
        width=0.08
    ))

    # Remaining section
    fig.add_trace(go.Bar(
        x=[100 - percent_lost],
        y=["Progress"],
        orientation="h",
        marker=dict(color=DASH_GREY_LIGHT),
        name="Remaining",
        width=0.08
    ))

    fig.add_trace(go.Scatter(x=[0,100], y=["Progress","Progress"],mode='markers', marker=dict(size=12,color=DASH_PURPLE_DARK, symbol='circle'),showlegend=False))
    fig.add_trace(go.Scatter(x=[percent_lost], y=["Progress"],mode='markers', marker=dict(size=12,line=dict(color=DASH_PURPLE_DARK,width=3),color='white', symbol='circle'),showlegend=False))

    fig.add_annotation(
            x=0.2,
            y=0,  # position below the axis (adjust as needed)
            xref='x',
            yref='paper',
            text=" Start date",
            showarrow=False,
            font=dict(size=12, color='darkgrey'),
            align='center'
        )
    fig.add_annotation(
            x=percent_lost,
            y= 0,  # position below the axis (adjust as needed)
            xref='x',
            yref='paper',
            text=f"Current Date",
            showarrow=False,
            font=dict(size=12, color='darkgrey'),
            
            align='center'
        )
    fig.add_annotation(
            x=100,
            y= 0.7,  # position below the axis (adjust as needed)
            xref='x',
            yref='paper',
            text=f"Projected End",
            showarrow=False,
            align='center',
            font=dict(size=12, color='darkgrey'),
            
        )
    fig.add_annotation(
            x=100,
            y= 0.85,  # position below the axis (adjust as needed)
            xref='x',
            yref='paper',
            text=f"<b>{projected_str}</b>",
            showarrow=False,
            align='center',
            font=dict(size=16, color=DASH_PURPLE),
            
        )
    fig.add_annotation(
            x=0,
            y= 0.1,  # position below the axis (adjust as needed)
            xref='x',
            yref='paper',
            text=f"{start_str}",
            showarrow=False,
            align='center',
            font=dict(size=14, color='darkgrey'),
            
        )
    fig.add_annotation(
            x=percent_lost,
            y= 0.1,  # position below the axis (adjust as needed)
            xref='x',
            yref='paper',
            text=f"{current_str}",
            showarrow=False,
            align='center',
            font=dict(size=14, color='darkgrey'),  
        )

    fig.update_layout(
        barmode="stack",
        title=dict(text="You could reach your goal by:", font=dict(size=14, color='darkgrey'), y=0.9, x=0),
        xaxis=dict(
            range=[-10, 110], showticklabels=False
        ),
        yaxis=dict(showticklabels=False),
        height=200,
        margin=dict(l=12, r=30, t=0, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor='white',
        showlegend=False,   
    )
    # fig.show()
    return fig


def create_percentage_chart(meas_data, unit, GOAL_WEIGHT):
    
    if unit == 'kg':
        unit_label='kg'
        y_data = meas_data['Weight']
        percent_lost = ((meas_data['Weight'].iloc[0] - meas_data['Weight'].iloc[-1]) / (meas_data['Weight'].iloc[0] - GOAL_WEIGHT)) * 100
        start = y_data.iloc[0]
        current = y_data.iloc[-1]
        goal = GOAL_WEIGHT
    else:
        unit_label='lb'
        y_data = meas_data['Weight lbs']
        percent_lost = ((meas_data['Weight'].iloc[0] - meas_data['Weight'].iloc[-1]) / (meas_data['Weight'].iloc[0] - GOAL_WEIGHT)) * 100
        start = y_data.iloc[0]
        current = y_data.iloc[-1]
        goal = GOAL_WEIGHT * 2.2046226218
        
        
    start_weight = f'{y_data.iloc[0]:.1f} {unit_label}'
    current_weight = f'{y_data.iloc[-1]:.1f} {unit_label}'
    
    
    fig = go.Figure(go.Bar(
        x=[percent_lost],
        y=[""],
        orientation='h',
        marker=dict(color=DASH_PURPLE),
        text=f"{percent_lost:.1f}%",
        textfont=dict(color='white', size=16),
        textposition="inside", 
        insidetextanchor='end', 
        hoverinfo='x'
        ))
    fig.add_annotation(
        x=percent_lost,
        y=-1,  # position below the axis (adjust as needed)
        xref='x',
        yref='paper',
        text=f"<b>{current_weight}</b>",
        showarrow=False,
        font=dict(size=16, color=DASH_PURPLE),
        align='center'
    )
    fig.add_annotation(
        x=percent_lost,
        y=-1.4,  # position below the axis (adjust as needed)
        xref='x',
        yref='paper',
        text="(Current)",
        showarrow=False,
        font=dict(size=12, color='darkgrey'),
        align='center'
    )


    fig.update_layout(
            title=f"You're {percent_lost:.1f}% of the way to your goal!",
            title_font=dict(size=14,color='darkgrey'),
            xaxis=dict(range=[0, 100], showgrid=False, title="",tickvals=[0, percent_lost, 100],        
            ticktext=[start_weight, "", f"{goal:.1f}{unit_label}"],
            showticklabels=True),
            
            font=dict(color='darkgrey'),
            
            yaxis=dict(showticklabels=False),
            height=100,
            margin=dict(l=20, r=20, t=30, b=40),
            plot_bgcolor='lightgrey',
            paper_bgcolor='rgba(0,0,0,0)'
        )
    # fig.show()
    return fig

def create_weight_over_time(meas_data,unit):
    if unit == 'kg': 
        
        y_col = 'Weight'
        avg_col = 'weekly_avg_weight'
    else:
        y_col = 'Weight lbs'
        avg_col = 'weekly_avg_weight lbs'
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=meas_data['Date'], y=meas_data[y_col], mode='lines', name=f'Weight {unit}', 
                                 line=dict(shape='spline',color=DASH_BLUE, width=1),
                                 fill='tozeroy',
                                 fillgradient=dict(type="vertical",colorscale=[(0.0,'white'), (0.5,'white'), (1.0, DASH_BLUE)],
                            ),
                        ))   
    fig.add_trace(go.Scatter(x=meas_data['Date'], y=meas_data[avg_col], mode='markers',
                            name=f'Weekly Average Weight {unit}', 
                            marker=dict(color=DASH_BLUE, size=4)
                        ))
    
    fig.update_layout(
                        yaxis=dict(
                                    title=f'Weight ({unit})',title_standoff=8,
                                    ticklen=15,automargin=True),
                        xaxis=dict( 
                                   title_standoff=8,ticklen=15,
                                   range=[meas_data['Date'].min(),meas_data['Date'].max()],
                                   automargin=True),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        legend=dict(
                                    x=0.75,               
                                    y=1,                  
                                    xanchor='left',       
                                    yanchor='top',        
                                    bgcolor='rgba(255,255,255,0.7)',
                                    bordercolor='rgba(0,0,0,0)',
                                    borderwidth=1),
                                    margin=dict(l=40, r=20, t=40, b=40),
                                    yaxis_range=[meas_data[y_col].min(),meas_data[y_col].max()]
                                                
                        )
    
    # fig.show()
    return fig
