from dash import html


def textbox(text, title=None):
    text_component = html.Div(html.Div(text, className="textbox-text"))

    if title is not None:
        title_component = html.Div(children=title, className="textbox-title")

        return [title_component, text_component]
    return [text_component]
