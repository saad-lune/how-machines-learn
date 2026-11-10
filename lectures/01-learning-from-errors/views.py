"""Small presentation layouts and charts for the opening story."""
from html import escape
from engine import TEACHING_RECORDS

INK = '#183331'
TEAL = '#007f78'
ORANGE = '#bd6236'
PAPER = '#faf8f2'


def frame(number, title, body):
    return f'''<article class="slide" data-slide="{number}">
    <header><h2>{escape(title)}</h2></header>
    <div class="slide-body">{body}</div>
    <footer class="footer"><span>{number}</span></footer></article>'''


def delivery_plot(preparation=None, rate=None, gaps=False, reveal=False, highlight_error=False):
    def point(distance, minutes):
        return 90 + 220 * distance, 285 - 11.5 * minutes
    parts = ['<svg class="delivery-plot" viewBox="0 0 1080 350" role="img" aria-label="Distance versus delivery time for three synthetic deliveries">']
    for t in (0,5,10,15,20):
        _,y=point(0,t)
        parts.append(f'<path d="M90 {y}H970" class="gridline"/><text x="65" y="{y+7}" text-anchor="end" class="axis-text">{t}</text>')
    for d in range(5):
        x,_=point(d,0)
        parts.append(f'<text x="{x}" y="315" text-anchor="middle" class="axis-text">{d}</text>')
    parts.append('<text x="90" y="24" class="axis-text">Delivery time (min)</text><text x="530" y="345" text-anchor="middle" class="axis-text">Distance (km)</text>')
    if preparation is not None:
        end_distance = min(4, (20-preparation)/rate) if rate > 0 else 4
        x0,y0=point(0,preparation);x1,y1=point(end_distance,preparation+end_distance*rate)
        fragment=' class="fragment" data-fragment-index="0"' if reveal else ''
        parts.append(f'<g{fragment}><path d="M{x0} {y0}L{x1} {y1}" class="model-line"/></g>')
        if gaps:
            parts.append('<g class="fragment" data-fragment-index="1">' if reveal else '<g>')
            for d,t in TEACHING_RECORDS:
                x,y=point(d,t);_,estimate=point(d,preparation+d*rate)
                parts.append(f'<path d="M{x} {y}V{estimate}" class="residual"/>')
            parts.append('</g>')
            if highlight_error:
                x,actual=point(2,11)
                _,predicted=point(2,preparation+2*rate)
                error=preparation+2*rate-11
                label=f"{abs(error):g} min too {'low' if error < 0 else 'high'}" if error else "No gap"
                parts.append(f'<text x="{x+18}" y="{(actual+predicted)/2+7}" class="error-label">{label}</text>')
    for d,t in TEACHING_RECORDS:
        x,y=point(d,t)
        parts.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{INK}"/>')
    parts.append('</svg>')
    return ''.join(parts)


def simulation_figure(simulation):
    import plotly.graph_objects as go
    state=simulation.snapshot()
    x,y=simulation.plot_data()
    fig=go.Figure([
        go.Scattergl(x=x,y=y,mode='markers',name='Observed deliveries',
                     marker=dict(size=6 if state['deliveries'] < 200 else 4 if state['deliveries'] < 5000 else 3, color='rgba(24, 51, 49, 0.65)' if state['deliveries'] < 200 else 'rgba(24, 51, 49, 0.12)' if state['deliveries'] < 5000 else 'rgba(24, 51, 49, 0.06)'),hoverinfo='skip'),
        go.Scattergl(x=[0,10.5],y=[state['preparation'],state['preparation']+10.5*state['minutes_per_km']],
                   mode='lines',name='Current prediction',line=dict(color=TEAL,width=4),hoverinfo='skip'),
    ])
    fig.update_layout(
        width=1080,height=310,margin=dict(l=65,r=25,t=10,b=55),
        paper_bgcolor=PAPER,plot_bgcolor=PAPER,
        font=dict(family='Arial, sans-serif',size=18,color=INK),
        xaxis=dict(title='Distance (km)',range=[0,10.5],fixedrange=True,gridcolor='#e0e5da',zeroline=False),
        yaxis=dict(title='Delivery time (min)',range=[0,40],fixedrange=True,gridcolor='#e0e5da',zeroline=False),
        showlegend=False,uirevision='delivery-stream',dragmode=False,
    )
    return fig
