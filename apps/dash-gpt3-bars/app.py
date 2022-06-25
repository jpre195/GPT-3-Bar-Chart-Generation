import black
import os
from textwrap import dedent

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dash import no_update
from dash.dependencies import Input, Output, State
import plotly.express as px
import openai


def Header(name, app):
    title = html.H1(name, style={"margin-top": 5})
    logo = html.Img(
        src=app.get_asset_url("dash-logo.png"), style={"float": "right", "height": 60}
    )
    return dbc.Row([dbc.Col(title, md=8), dbc.Col(logo, md=4)])


# Authentication
openai.api_key = os.getenv("OPENAI_KEY")


# Define the prompt
# desc = "Our zoo has three twenty giraffes, fourteen orangutans, 3 monkeys more than the number of giraffes we have."
# code_exp = "px.bar(x=['giraffes', 'orangutans', 'monkeys'], y=[20, 14, 23], labels=dict(x='animals', y='count'), title='Our Zoo')"
# formatted_exp = black.format_str(code_exp, mode=black.FileMode(line_length=50))

desc = \
    """
    Our zoo has three twenty giraffes, fourteen orangutans, 3 monkeys more than 
    the number of giraffes we have and 12 zebras. Make color of giraffe bar yellow and orangutan bar green.
    """
# code_exp = \
#     """
#     # df = pd.DataFrame({'animals' : ['giraffes', 'orangutans', 'monkeys'], 'count' : [20, 14, 23], 'color' : ['yellow', 'green', 'blue']})
#     df['animals'] = ['giraffes', 'orangutans', 'monkeys']
#     df['count'] = [20, 14, 23]
#     df['color'] = ['yellow', 'green', 'blue']
    
#     # fig = px.bar(x=['giraffes', 'orangutans', 'monkeys'], 
#     #         y=[20, 14, 23], 
#     #         labels=dict(x='animals', y='count'), 
#     #         color=['yellow', 'green', 'blue'],
#     #         color_discrete_map='identity',
#     #         title='Our Zoo')
    
#     fig = px.bar(data_frame=df, x='animals', y='count', labels=dict(x='animals', y='count'), color='color', title='Our Zoo')
#     """
# code_exp = "df = pd.DataFrame({'animals' : ['giraffes', 'orangutans', 'monkeys'], 'count' : [20, 14, 23], 'color' : ['yellow', 'green', 'blue']})\nfig = px.bar(data_frame=df, x='animals', y='count', labels=dict(x='animals', y='count'), color='color', title='Our Zoo')"
code_exp = "px.bar(x=['giraffes', 'orangutans', 'monkeys', 'zebras'], y=[320, 14, 23, 12], labels=dict(x='animals', y='count'), color = ['yellow', 'green', 'blue', 'blue'], color_discrete_map = 'identity', title='Our Zoo')"
formatted_exp = black.format_str(code_exp, mode=black.FileMode(line_length=10000))

descs = ['Our zoo has three twenty giraffes, fourteen orangutans, 3 monkeys more than the number of giraffes we have and 12 zebras. Make color of giraffe bar yellow and orangutan bar green.',
         'Sales were at $100 on Monday and have increased by 30 dollar every day this week.',
         'Create a bar chart with 6 bars with values of 10, 20, 60, 3, twenty-five, and seventy sorted ascending by value.',
         'Make a bar graph with values of 10, 20, 60, 3, twenty-five, and seventy sorted descending by value.'
         ]
code_exps = ["""
             px.bar(x=['giraffes', 'orangutans', 'monkeys', 'zebras'], y=[320, 14, 323, 12], labels=dict(x='animals', y='count'), color = ['yellow', 'green', 'blue', 'blue'], color_discrete_map = 'identity', title='Our Zoo')
             """,
             """             
             px.bar(x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], y=[100, 130, 160, 190, 220], labels=dict(x='Day', y='Dollars'), title='Sales')
             """,
             """
             px.bar(y=[3, 10, 20, 25, 60, 70], labels=dict(x='', y='Value'))
             """,
             """
             px.bar(y=[70, 60, 25, 20, 10, 3], labels=dict(x='', y='Value'))
             """
             ]
# code_exps = ["""
#              df = pd.DataFrame()
#              df['animals'] = ['giraffes', 'orangutans', 'monkeys', 'zebras']
#              df['count'] = [320, 14, 23, 12]
#              fig = px.bar(data_frame = df, x='animals', y='count', labels=dict(x='animals', y='count'), color = ['yellow', 'green', 'blue', 'blue'], color_discrete_map = 'identity', title='Our Zoo')
#              """,
#              """
#              df = pd.DataFrame()
#              df['Day'] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
#              df['Dollars'] = [100, 130, 160, 190, 220]
             
#              fig = px.bar(data_frame = df, x='Day', y='Dollars', labels=dict(x='Day', y='Dollars'), title='Sales')
#              """,
#              """
#              df = pd.DataFrame()
#              df['Value'] = [3, 10, 20, 25, 60, 70]
             
#              fig = px.bar(data_frame = df, y='Value', labels=dict(x='', y='Value'))
#              """,
#              """
#              df = pd.DataFrame()
#              df['Value'] = [10, 20, 60, 3, 25, 70]
             
#              df.sort_values('Value', ascending = False, inplace = True)
#              fig = px.bar(data_frame = df, y='Value', labels=dict(x='', y='Value'))
             
#              """,
#              "px.bar(y=['giraffes', 'orangutans', 'monkeys', 'zebras'], x=[320, 14, 23, 12], labels=dict(x='animals', y='count'), color = ['yellow', 'green', 'blue', 'blue'], color_discrete_map = 'identity', orientation = 'h', title='Our Zoo')",
#              """
#              df = pd.DataFrame()
#              df['animals'] = ['giraffes', 'orangutans', 'monkeys', 'zebras']
#              df['count'] = [320, 14, 23, 12]
#              df['colors'] = ['yellow', 'green', 'blue', 'blue']
             
#              px.bar(y='animals', x='count', labels=dict(x='animals', y='count'), color = 'colors', color_discrete_map = 'identity', orientation = 'h', title='Our Zoo')
#              """,
#              """
#              df = pd.DataFrame()
#              df['animals'] = ['giraffes', 'orangutans', 'monkeys', 'zebras']
#              df['count'] = [320, 14, 23, 12]
#              df['colors'] = ['yellow', 'green', 'blue', 'blue']
             
#              px.bar(y='animals', x='count', labels=dict(x='animals', y='count'), color = 'colors', color_discrete_map = 'identity', orientation = 'v', title='Our Zoo')
#              """]

# formatted_exps = [black.format_str(code, mode=black.FileMode(line_length=10000)) for code in code_exps]

# Create
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

content_style = {"height": "475px"}

controls = [
    dbc.InputGroup(
        [
            dbc.Input(
                id="input-text",
                placeholder="Specify what you want GPT-3 to generate...",
            ),
            dbc.InputGroupAddon(
                dbc.Button("Submit", id="button-submit", color="primary"),
                addon_type="append",
            ),
        ]
    )
]
output_graph = [
    dbc.CardHeader("Plotly Express Graph"),
    dbc.CardBody(dcc.Graph(id="output-graph", style={"height": "400px"})),
]
output_code = [
    dbc.CardHeader("GPT-3 Generated Code"),
    dcc.Markdown(id="output-code", style={"margin": "50px 5px"}),
]

explanation = f"""
*GPT-3 can generate Plotly graphs from a simple description of what you want!
We only needed to give the following prompt to GPT-3:*

Description: **{desc}**

Code:
```
{code_exp}
```
"""
explanation_card = [
    dbc.CardHeader("What am I looking at?"),
    dbc.CardBody(dcc.Markdown(explanation)),
]

app.layout = dbc.Container(
    [
        Header("Dash GPT-3 Chart Generation", app),
        html.Hr(),
        html.Div(controls, style={"padding-bottom": "15px"}),
        dbc.Spinner(
            dbc.Row(
                [
                    dbc.Col(dbc.Card(comp, style=content_style))
                    for comp in [output_graph, output_code]
                ],
                style={"padding-bottom": "15px"},
            )
        ),
        dbc.Card(explanation_card),
    ],
    fluid=False,
)


@app.callback(
    [Output("output-graph", "figure"), Output("output-code", "children")],
    [Input("button-submit", "n_clicks"), Input("input-text", "n_submit")],
    [State("input-text", "value")],
)
def generate_graph(n_clicks, n_submit, text):
    if text is None:
        return dash.no_update, dash.no_update

    prompt = dedent(
        # f"""
        # description: {desc}
        # code:
        # {code_exp}

        # description: {text}
        # code:
        # """
        '\n'.join([f'description: {desc}\ncode:\n{code}\n' for desc, code in zip(descs, code_exps)]) + f'description: {text}\ncode: '
    ).strip("\n")

    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1000,
        stop=["description:", "code:"],
        temperature=0
    )
    output = response.choices[0].text.strip()

    code = f"import plotly.express as px\nfig={output}\nfig.show()"
    formatted = black.format_str(code, mode=black.FileMode(line_length=10000))

    try:
        fig = eval(output).update_layout(margin=dict(l=35, r=35, t=35, b=35))
    except Exception as e:
        fig = px.line(title=f"Exception: {e}. Please try again!")
        print(f'{formatted}')

    return fig, f"```\n{formatted}\n```"


if __name__ == "__main__":
    app.run_server(debug=False)
