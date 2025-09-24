# import gradio as gr

# # --- Custom CSS for a dark, modern Perplexity-like look ---
# custom_css = """
# body, .gradio-container { background: #16181c !important; }
# #sidebar { 
#     min-width: 205px; 
#     max-width: 250px; 
#     background: #1A1B22;
#     border-right: 1px solid #22232b;
#     padding-top: 10px;
# }
# #new_chat_btn { 
#     background: #FF7900;
#     color: #FFF;
#     font-weight: bold;
#     border-radius: 8px;
#     margin-bottom: 18px !important;
#     width: 95%;
#     box-shadow: none;
#     border: none;
# }
# .sidebar-content-btn {
#     background: #23242c;
#     margin-bottom: 8px;
#     border-radius: 8px;
#     width: 95%;
#     color: #fafafa;
#     border: none;
# }
# #chatbox_div {
#     background: #191A20;
#     border-radius: 9px;
#     border: 1.5px solid #23242c;
#     min-height: 330px;
#     margin: 0 0 14px 0;
#     color: #ddd;
# }
# #bottom_input {
#     border-radius: 7px;
#     border: 1.5px solid #383a47;
#     padding-left: 10px;
#     font-size: 1.08rem;
#     background: #23242c;
#     color: #fafafa;
# }
# #bottom_input textarea { background: #23242c; color: #fafafa; }
# .gr-chatbot-message { color: #fafafa; }
# .gr-chatbot { background: #191A20; border-radius: 9px; }
# #prompt_footer {
#     text-align: left; 
#     font-size: 0.95rem; 
#     color: #d6d8e1;
#     margin-top: 8px;
#     background: none;
# }
# .gr-row, .gr-column { background: none !important; }
# .gr-input, .gr-textbox { background: #23242c!important; color: #fafafa!important; }
# .gr-btn-secondary { background: #282a35; color: #fff; border-radius: 8px;}
# ::-webkit-scrollbar { width: 0.28em; background: #23242c; }
# ::-webkit-scrollbar-thumb { background: #282a35; border-radius: 6px; }
# """

# def echo_fn(message, history):
#     return f"You said: {message}"

# with gr.Blocks(css=custom_css, fill_width=True, analytics_enabled=False) as demo:
#     with gr.Row(equal_height=False):
#         with gr.Column(elem_id="sidebar", min_width=205, scale=14):
#             gr.Button(" New chat", elem_id="new_chat_btn")
#             gr.Button("How to write code\nwith gradio", elem_classes="sidebar-content-btn")
#         with gr.Column(scale=86):
#             with gr.Tabs(selected=0):
#                 with gr.TabItem(" Chatbot", id=0):
#                     with gr.Column():
#                         with gr.Row():
#                             gr.HTML("", visible=False)  # Padding if needed
#                         chatbox = gr.Chatbot(elem_id="chatbox_div", height=340)
#                     with gr.Row():
#                         user_input = gr.Textbox(
#                             placeholder="Type a message...", 
#                             elem_id="bottom_input", 
#                             lines=1, 
#                             show_label=False,
#                             scale=13
#                         )
#                         send_btn = gr.Button("➤", variant="secondary", scale=1)
#             gr.HTML(
#                 "<span id='prompt_footer'>gradio/chatinterface_streaming_echo built with <b>Gradio</b>."
#                 # "<span style='float:right;'>Hosted on <img style='display:inline-block;height:1.1em;vertical-align:middle' alt='Spaces' src='https://huggingface.co/front/assets/hf-logo.svg'></span></span>"
#             )

#     user_input.submit(echo_fn)
#     send_btn.click(echo_fn, [user_input, chatbox], [chatbox, user_input])

# demo.launch()


# from transformers import AutoModelForCausalLM, AutoTokenizer
# import gradio as gr

# checkpoint = "HuggingFaceTB/SmolLM2-135M-Instruct"
# device = "cpu"  # "cuda" or "cpu"
# tokenizer = AutoTokenizer.from_pretrained(checkpoint)
# model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device)

# def predict(message, history):
#     history.append({"role": "user", "content": message})
#     input_text = tokenizer.apply_chat_template(history, tokenize=False)
#     inputs = tokenizer.encode(input_text, return_tensors="pt").to(device)  
#     outputs = model.generate(inputs, max_new_tokens=100, temperature=0.2, top_p=0.9, do_sample=True)
#     decoded = tokenizer.decode(outputs[0])
#     response = decoded.split("<|im_start|>assistant\n")[-1].split("<|im_end|>")[0]
#     return response

# demo = gr.ChatInterface(predict, type="messages")

# demo.launch()


import gradio as gr
from gemini_client import gemini_client_test
import time
    
    
def alternatingly_agree(message, history):

    if len([h for h in history if h['role'] == "assistant"]) % 2 == 0:
        response = f"Yes, I do think that: {message}"
        for i in response:
            time.sleep(0.01)
            yield i
         
    else:
        return "I don't think so"


def format_history_for_gemini(history):
    """Convert message-style history to a prompt string."""
    lines = []
    for entry in history:
        role = "User" if entry["role"] == "user" else "Assistant"
        lines.append(f"{role}: {entry['content']}")
    return "\n".join(lines)



async def main_func(message, history):

    conversation = format_history_for_gemini(history)
    prompt = f"""System:
            You are a computer science professor with 30 years of experience. Answer user questions in the simplest way possible.

            Conversation so far:
            {conversation}

            User question:
            {message}
            """
    
    response = await gemini_client_test(prompt)
    return getattr(response, "text", str(response))


with gr.Blocks(fill_height=True, fill_width=True) as demo:
    
    gr.Markdown("Your Personal AI Restaurant Reservation System")
    gr.Markdown("Lets go, get you some good food !")
    
    with gr.Sidebar(visible=False, position="left"): # or position="right"
        gr.Markdown("This is the sidebar content.")
        dropdown = gr.Dropdown(choices=["Option 1", "Option 2"], label="Select an option")
    # with gr.Column():
    #     # gr.Markdown("Main Content")
    #     button = gr.Button("Click me")
    #     button.click(lambda: None, outputs=None)  # Placeholder for functionality
    # with gr.Row():
    #   btn_toggle_sidebar = gr.Button("Toggle Sidebar")
    #   sidebar_state = gr.State(False)

    #   def toggle_sidebar(state):
    #       state = not state
    #       return gr.update(visible=state), state

    #   btn_toggle_sidebar.click(toggle_sidebar, [sidebar_state], [demo.children[0], sidebar_state])

    
    gr.ChatInterface(
        fn=main_func,
        type="messages",
        chatbot=gr.Chatbot(placeholder="<strong>Book Now</strong><br>Ask Me Anything"),
        textbox=gr.Textbox(placeholder="write your question here", container=False, scale=7)
    )

demo.launch()
