# This is the only way I could figure how to do it so this will have to do for now

import os
import gradio
import requests

# returns boilerplate text from path operation function
def get_root():
    headers = {
        "accept": "application/json",
    }
    response = requests.get("http://localhost:8000/", headers=headers)
    return response.json()


# generate shortened url along with its admin url
def shorten_url(input_url_textbox: str):
    response = requests.post(
        "http://localhost:8000/url",
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
        },
        json={
            "target_url": input_url_textbox,
        },
    )
    return {response.json()["url"], response.json()["admin_url"]}


# to get long url behind a shortened url
def peek_url(short_url: str):
    headers = {
        "accept": "application/json",
    }
    response = requests.get(f"http://localhost:8000/peek/{short_url}", headers=headers)
    return response.json()[0]


# admin panel for analytics and admin operations on links
def admin_details(admin_url: str):

    headers = {
        "accept": "application/json",
    }

    response = requests.get(f"http://localhost:8000/admin/{admin_url}", headers=headers)
    return response.json()


# delete link via secret key, admin only
def delete_url(admin_url: str):
    headers = {
        "accept": "application/json",
    }
    response = requests.delete(
        f"http://localhost:8000/admin/{admin_url}", headers=headers
    )
    return response.json()["detail"] + " ✅"


# setup gradio Blocks as frontend
with gradio.Blocks(
    css=".gradio-container {background-image: url('file=img/background.png'); background-size: cover}"
) as demo:
    gradio.Image(value=os.path.join("img", "LinkBite.png")).style(height=128)

    gradio.Markdown(
        f"""
    ## Welcome to {get_root()}!
    """
    )

    # shorten URLs
    with gradio.Box():
        with gradio.Row():
            input_url_textbox = gradio.Textbox(
                placeholder="URLs will be validated",
                lines=2,
                label="What URL do you want to shorten?",
            )
            shorten_button = gradio.Button("Shorten your URL")
            output_url_textbox = gradio.Textbox(
                placeholder="Your shortened URL comes here",
                lines=2,
                label="Here are the details of your shortened URL",
            )
            shorten_button.click(
                fn=shorten_url, inputs=input_url_textbox, outputs=output_url_textbox
            )

    # peek URLs
    with gradio.Box():
        with gradio.Row():
            peek_url_input = gradio.Textbox(
                placeholder="Paste a shortened URL",
                lines=2,
                label="Looking to know where a shortened URL will lead to? Try here!",
            )
            peek_button = gradio.Button("Peek at URL")
            peek_url_output = gradio.Textbox(
                placeholder="Long URL", lines=2, label="Your URL leads here"
            )
            peek_button.click(
                fn=peek_url, inputs=peek_url_input, outputs=peek_url_output
            )

    # an admin panel
    with gradio.Box():
        with gradio.Row():
            input_admin_url = gradio.Textbox(
                placeholder="An admin URL consists of your shortened link followed by your secret key",
                lines=2,
                label="Enter your admin URL here",
            )
            admin_details_button = gradio.Button("Get details for your URL")
            output_admin_url = gradio.Textbox(
                placeholder="View analytics and metadata here",
                lines=2,
                label="Admin details",
            )
            admin_details_button.click(
                fn=admin_details, inputs=input_admin_url, outputs=output_admin_url
            )

    # delete links
    with gradio.Box():
        with gradio.Row():
            with gradio.Column():
                link_to_delete = gradio.Textbox(
                    placeholder="Paste your link's secret key",
                    lines=1,
                    label="Don't need a link anymore? Delete it from here!",
                )
                deletion_output = gradio.Textbox(lines=1, label="")
            delete_button = gradio.Button("Delete shortened URL")
            delete_button.click(
                fn=delete_url, inputs=link_to_delete, outputs=deletion_output
            )

demo.launch(show_api=False, server_name="0.0.0.0", server_port=7860)
