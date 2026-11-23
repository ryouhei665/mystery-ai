import os

import time

import streamlit as st

from google import genai



MODEL = "gemini-3.6-flash"





def get_secret(name):

    """クラウドではSecretsから、自分のPCでは環境変数から読む"""

    try:

        return st.secrets[name]

    except Exception:

        return os.environ.get(name)





client = genai.Client(api_key=get_secret("GEMINI_API_KEY"))

app_password = get_secret("APP_PASSWORD")





def ask(prompt):

    for i in range(3):

        try:

            response = client.models.generate_content(model=MODEL, contents=prompt)

            return response.text

        except Exception:

            time.sleep(10)

    return None





st.title("トリック作りAI")



# パスワードが設定されている場合は、入力するまで先に進めない

if app_password:

    pw = st.text_input("パスワード", type="password")

    if pw != app_password:

        if pw:

            st.error("パスワードが違います")

        st.stop()



joukyou = st.text_area(

    "状況を入力してください",

    height=200,

    placeholder="■場所:\n■被害者:\n■密室の状態:\n■時間帯:\n■容疑者:",

)

num = st.slider("案の数", 1, 5, 3)

avoid = st.text_input("避けたいトリック（任意）")



if st.button("トリック案を作る"):

    if not joukyou.strip():

        st.warning("状況を入力してください")

    else:

        prompt = f"""あなたは本格ミステリー作家のアシスタントです。

以下の状況から、小説の謎として成立するトリック案を{num}つ提案してください。



【ルール】

- 各案は、互いに方向性が異なること

- 有名な既存作品のトリックの単純な流用は避ける

- 避けたいトリック: {avoid if avoid else "特になし"}

- 現実に起こりうる範囲で、物語上の仕掛けとして説明する（犯罪の具体的な手順書にはしない）



【各案の形式】

案名／トリックの概要（3〜4行）／読者に提示すべき手がかり／弱点・矛盾しやすい点／見破られやすさ（1〜5、5が見破られやすい）



【状況】

{joukyou}

"""

        with st.spinner("考え中..."):

            result = ask(prompt)

        if result is None:

            st.error("失敗しました。少し待ってからもう一度お試しください")

        else:

            st.markdown(result)


