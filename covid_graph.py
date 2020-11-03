import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

nakaza = pd.read_csv('https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakaza.csv')

nakaza['7_denni_prumer_nakazenych'] = nakaza.iloc[:,1].rolling(window=7).mean()

#testy = pd.read_csv('https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/testy.csv')

aktualni_stav = pd.read_csv('https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv')

aktualni_stav['prirustkovy_pocet_vylecenych'] = - aktualni_stav['kumulativni_pocet_vylecenych'].diff()
aktualni_stav['7_denni_prumer_vylecenych'] = aktualni_stav.iloc[:,5].rolling(window=7).mean()
aktualni_stav['aktualni_pocet_nakazenych'] = aktualni_stav['kumulativni_pocet_nakazenych'] - aktualni_stav['kumulativni_pocet_vylecenych'] - aktualni_stav['kumulativni_pocet_umrti']

#kresleni

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Scatter(x = nakaza['datum'], y = nakaza['prirustkovy_pocet_nakazenych'], name='Přírůstkový počet nakažených', line_shape='spline',line=dict(color='rgb(255,0,0)'), fill='tozeroy', fillcolor='rgba(255,0,0,0.3)'),secondary_y=False)
fig.add_trace(go.Scatter(x = nakaza['datum'], y = nakaza['7_denni_prumer_nakazenych'], name='7denní průměr nakažených', line_shape='spline',line=dict(color='rgb(200,0,0)')),secondary_y=False)


fig.add_trace(go.Scatter(x = aktualni_stav['datum'], y = aktualni_stav['prirustkovy_pocet_vylecenych'], name='Přírůstkový počet vyléčených', line_shape='spline',line=dict(color='rgb(0,200,0)'), fill='tozeroy', fillcolor='rgba(0,200,0,0.3)'),secondary_y=False)
fig.add_trace(go.Scatter(x = aktualni_stav['datum'], y = aktualni_stav['7_denni_prumer_vylecenych'], name='7 denní průměr vyléčených', line_shape='spline',line=dict(color='rgb(0,150,0)')),secondary_y=False)


#fig.add_trace(go.Scatter(x = aktualni_stav['datum'], y = aktualni_stav['aktualni_pocet_nakazenych'], name='Aktivní případy', line_shape='spline'),secondary_y=True)

fig.add_layout_image(dict(
            source="https://upload.wikimedia.org/wikipedia/commons/c/cb/Flag_of_the_Czech_Republic.svg",
            xref="x domain",
            yref="y domain",
            x=0.5,
            y=0.5,
            xanchor="center",
            yanchor="middle",
            sizex=1,
            sizey=1,
            opacity=0.1,
			sizing="stretch",
            layer="below")
)

fig.update_layout()

fig.update_layout(title='COVID-19 v ČR',
                   showlegend=True)

#fig.show()

fig.write_image("fig1.png", width=1000, height=600,)