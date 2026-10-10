import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# 1. Importar los datos y establecer la columna 'date' como índice (parseando fechas)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# 2. Limpiar los datos filtrando el 2.5% superior e inferior
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]


def draw_line_plot():
    # Copia de los datos
    df_line = df.copy()

    # Configuración de la figura
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df_line.index, df_line['value'], color='red', linewidth=1)

    # Título y etiquetas de los ejes
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Guardar y devolver la imagen
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copia y preparación de los datos
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.strftime('%B')

    # Orden cronológico de los meses
    months_order = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]

    # Agrupar y pivotar para obtener el promedio mensual por año
    df_pivot = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    df_pivot = df_pivot.reindex(columns=months_order)

    # Dibujar gráfico de barras
    fig = df_pivot.plot(kind='bar', figsize=(9, 7), legend=True).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')

    # Guardar y devolver la imagen
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Preparar datos para los diagramas de caja
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Orden cronológico abreviado de los meses
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Crear figura con dos subplots adyacentes
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 7))

    # Gráfico 1: Por año (Trend)
    sns.boxplot(x='year', y='value', data=df_box, ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')

    # Gráfico 2: Por mes (Seasonality)
    sns.boxplot(x='month', y='value', data=df_box, order=month_order, ax=ax2)
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')

    # Guardar y devolver la imagen
    fig.savefig('box_plot.png')
    return fig