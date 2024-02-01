import gradio as gr

import chatbot_engine

# チャットのコアロジックと連携
def respond(message, chat_history):
    bot_message = chatbot_engine.chat(message)
    chat_history.append((message, bot_message))
    return "", chat_history


# gradioの設定
with gr.Blocks() as demo:
    # チャット表示用の画面
    chatbot = gr.Chatbot()
    # 入力用のテキストフィールド
    msg = gr.Textbox()
    # 初期化ボタン
    clear = gr.Button("Clear")

    # メッセージの送信時のアクション
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    # 入力したテキストやこれまでのチャットをクリア
    clear.click(lambda: None, None, chatbot, queue=False)


if __name__ == "__main__":
    demo.launch()

