import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

class GraphGenerator:
    def __init__(self):
        pass  # Any initialization logic can be included here if needed

    @staticmethod
    def bar_chart(library, df, eixo_x, eixo_y):
        fig = None
        if library == 'matplotlib':
            plt.bar(eixo_x, eixo_y)
            plt.xlabel(eixo_x)
            plt.ylabel(eixo_y)
            fig = plt.show()
        elif library == 'seaborn':
            sns.barplot(x=eixo_x, y=eixo_y, data=df)
            plt.xlabel(eixo_x)
            plt.ylabel(eixo_y)
            plt.show()
        elif library == 'plotly':
            fig = px.bar(df, x=eixo_x, y=eixo_y, text_auto='.2s')
            fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        else:
            raise ValueError("Library não suportada. Escolha entre 'matplotlib', 'seaborn' ou 'plotly'.")
        return fig

    @staticmethod
    def criar_grafico_pizza(library, df, eixo_x, eixo_y, metrica):
        if library == 'matplotlib':
            plt.pie(eixo_y, labels=eixo_x, autopct='%1.1f%%')
            plt.show()
        elif library == 'seaborn':
            raise ValueError("Seaborn não suporta gráficos de pizza diretamente. Considere usar matplotlib.")
        elif library == 'plotly':
            fig = px.pie(df, names=eixo_x, values=eixo_y)
            fig.show()
        else:
            raise ValueError("Library não suportada. Escolha entre 'matplotlib', 'seaborn' ou 'plotly'.")

    @staticmethod
    def criar_grafico_linha(library, df, eixo_x, eixo_y):
        fig = None
        if library == 'matplotlib':
            plt.plot(df[eixo_x], df[eixo_y])
            plt.xlabel(eixo_x)
            plt.ylabel(eixo_y)
            plt.show()
        elif library == 'seaborn':
            sns.lineplot(x=eixo_x, y=eixo_y, data=df)
            plt.xlabel(eixo_x)
            plt.ylabel(eixo_y)
            plt.show()
        elif library == 'plotly':
            fig = px.line(df, x=eixo_x, y=eixo_y)
            fig.show()
        else:
            raise ValueError("Library não suportada. Escolha entre 'matplotlib', 'seaborn' ou 'plotly'.")

    @staticmethod
    def criar_grafico_combo(library, df, eixo_x, eixo_y1, eixo_y2, metrica):
        fig = None
        if library == 'matplotlib':
            fig, ax1 = plt.subplots()

            ax1.bar(df[eixo_x], df[eixo_y1], color='b', label=f'{eixo_y1}')
            ax1.set_xlabel(eixo_x)
            ax1.set_ylabel(eixo_y1, color='b')
            ax1.tick_params('y', colors='b')

            ax2 = ax1.twinx()
            ax2.plot(df[eixo_x], df[eixo_y2], 'r-', label=f'{eixo_y2}')
            ax2.set_ylabel(eixo_y2, color='r')
            ax2.tick_params('y', colors='r')

            fig.suptitle(f'Combo Chart - {metrica}')
            plt.show()
        elif library == 'seaborn':
            raise ValueError("Seaborn não suporta gráficos combo diretamente. Considere usar matplotlib.")
        elif library == 'plotly':
            fig = px.scatter(df, x=eixo_x, y=eixo_y1, labels={eixo_y1: f'{eixo_y1}', eixo_y2: f'{eixo_y2}'})
            fig.add_trace(px.line(df, x=eixo_x, y=eixo_y2).data[0])
            fig.show()
        else:
            raise ValueError("Library não suportada. Escolha entre 'matplotlib', 'seaborn' ou 'plotly'.")
