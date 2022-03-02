import plotly.graph_objects as go

x = ['A', 'B', 'C']
y1 = [1, 2, 3]
y2 = [6, 4, 2]
plot = go.Figure(data=[
    go.Bar(
        name='test 1',
        x=x,
        y=y1
    ),
    go.Bar(
        name='test 2',
        x=x,
        y=y2
    )
]
)
plot.update_layout(barmode='stack')
plot.show()
