import pandas as pd # type: ignore
import plotly.express as px # type: ignore

data = {'valores': [5, 7, 7, 13, 7, 11, 14, 13, 15, 5,
                    5, 200, 7, 14, 13, 7, 210, 5, 11, 13]}

df = pd.DataFrame(data)

fig = px.box(df, y='valores', points='all')

fig.update_layout(
    title='Gráfico de Caja de Valores Atípicos',
    yaxis_title='Valores',
    template='plotly_dark'
)

fig.show()