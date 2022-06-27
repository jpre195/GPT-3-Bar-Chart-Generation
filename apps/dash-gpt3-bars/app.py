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
desc = \
    """
    Our zoo has three twenty giraffes, fourteen orangutans, 3 monkeys more than 
    the number of giraffes we have and 12 zebras.
    """

code_exp = "px.bar(x=['giraffes', 'orangutans', 'monkeys', 'zebras'], y=[320, 14, 23, 12], labels=dict(x='animals', y='count'), title='Our Zoo')"
formatted_exp = black.format_str(code_exp, mode=black.FileMode(line_length=10000))

descs = ['Our zoo has twenty giraffes, fourteen gorillas, 3 monkeys more than the number of giraffes we have and 12 zebras.',
         'Make y-axis range from 10 to 400',
         'Change giraffes bar to 32',
         'Update title to Hello world',
         'Update y-axis title to number of animals'
         # 'Create a bar chart with values 10, 3, twenty-five, and seventy sorted descending by value. X-axis should range from 0 to 100',
         # 'DisneyLands FY17 earnings was at 20000. They have increased 15000 every year since. Make a horizontal bar graph'
         ]
code_exps = ["""
             px.bar(x=['giraffes', 'gorillas', 'monkeys', 'zebras'], y=[20, 14, 23, 12], labels=dict(x='animals', y='count'), title='Our Zoo')
             """,
             """
             update_layout(yaxis_range=[10, 400])
             """,
             """
             update(data=[{'y' : [32, 14, 23, 12]}])
             """,
             """
             update_layout(title='Hellow world')
             """,
             """
             update_yaxes(title = 'Number of animals')
             """
             # """
             # px.bar(y=sorted([10, 3, 25, 70], reverse = True), color = ['blue', 'blue', 'blue', 'blue'], color_discrete_map = 'identity',  labels=dict(x='', y='Value', text = sorted([10, 3, 25, 70], reverse = True)), range_x = [0, 100])
             # """,
             # """
             # px.bar(x = [20000, 20000 + 1 * 15000, 20000 + 2 * 15000, 20000 + 3 * 15000, 20000 + 4 * 15000], y=['FY17', 'FY18', 'FY19', 'FY20', 'FY21'], labels=dict(x='Earnings', y='FY'), orientation = 'h', title = 'Disneyland earnings', text = [20000, 20000 + 1 * 15000, 20000 + 2 * 15000, 20000 + 3 * 15000, 20000 + 4 * 15000])
             # """
             ]

formatted_exps = [black.format_str(code, mode=black.FileMode(line_length=10000)) for code in code_exps]

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
    dbc.CardBody(
        dbc.Spinner(dcc.Markdown("", id = "conversation-id")), style={"height" : "725px"}),
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
    [State("input-text", "value"), State("conversation-id", "children"), State("output-code", "children")],
)
def generate_graph(n_clicks, n_submit, text, conversation, output_code):
    if text is None:
        return dash.no_update, dash.no_update
    
    conversation += dedent(f"""
                           description: {text}
                           code: 
                           """)

    prompt = dedent(
        '\n'.join([f'description: {desc}\ncode:\n{code}\n' for desc, code in zip(descs, formatted_exps)])
    ).strip("\n")

    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt + conversation,
        max_tokens=1000,
        stop=["description:", "code:"],
        temperature=0
    )
    output = response.choices[0].text.strip()
    
    conversation += f'{output}\n'
    
    if output_code is None:
        
        output_code = f'{output}'
        
    else:
    
        output_code += f'.{output}'
        
    code = f"import plotly.express as px\nfig={output_code}\nfig.show()"
    formatted = black.format_str(code, mode=black.FileMode(line_length=10000))

    try:
        fig = eval(output_code).update_layout(margin=dict(l=35, r=35, t=35, b=35))
    except Exception as e:
        fig = px.line(title=f"Exception: {e}. Please try again!")
        print(f'{formatted}')
        print(f'{e}')

    return fig, output_code


if __name__ == "__main__":
    app.run_server(debug=False)
