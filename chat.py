import streamlit as st
from streamlit_chat import message

import openai

#设置openai_key
openai.api_key ="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"

#记录对话 ###因为streamlit的原理没能成功
# messages=[
#       {"role": "system", "content": "You are a helpful assistant."},
#       {"role": "user", "content": "Who won the world series in 2020?"},
#       {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
#   ]

messages=[]

#调用模型
def openai_create(messages):

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=1.0,#越大每次回答变异越大 (0-2)
        max_tokens=4000,#设置token数，目前最大4096，其他2048
        top_p=1,
        frequency_penalty=0,# (-2,2)
        presence_penalty=0.6,# (-2,2)
        stop=[" Human:", " AI:"]
    )

    return response.choices[0].message.content  #返回AI的回答

#对话输入和记录
def chatgpt_clone(input):
    messages.append({"role": "user", "content": input})
    output = openai_create(messages)
    messages.append({"role": "assistant", "content":output})
    session=[]
    session.append((input, output))
    return session, messages

# Streamlit App
st.set_page_config(
    page_title="Cai's Streamlit Chat",
    page_icon=":robot:"
)

st.header("ChatGPT with Streamlit(目前无上下文联系)")


if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []


def get_text():
    input_text = st.text_input("在这里输入，按回车发送",key="input")
    return input_text

#获取输入
user_input = get_text()


if user_input:
    output,messages = chatgpt_clone(user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output[0][1])

# @st.cache_data
# def get_messages():
#     return messages
# messages = get_messages()

# st.write(messages)

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i],
                is_user=True, key=str(i) + '_user',
                avatar_style="Thumbs",
                seed=123,
                )
