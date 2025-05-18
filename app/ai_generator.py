from mistralai import Mistral
from dotenv import load_dotenv

import os


load_dotenv()

api_key = os.environ.get('AI_KEY')
model = 'mistral-large-latest'

client = Mistral(api_key=api_key)

async def generate_post_text(before_text: str, additional_data: str = ''):
    prompt = f'Есть пост с канала, немного переделай его заменяя слова на подходящие синонимы и меняя порядок предложения, убери упоминания автора про себя (если есть), но сохрани стилистическую окраску, смысл, цитаты и имена. Тут markdown_v2 поэтому курсив помечается _ с двух сторон а жирны текст *. {additional_data}. Отправь только готовый текст, текст поста: {before_text}'
    try:
        chat_response = await client.chat.complete_async(
            model = model,
            messages = [
                {
                    'role': 'user',
                    'content': prompt,
                },
            ],
            max_tokens=1500
        )
        return chat_response.choices[0].message.content
    except:
        try:
            chat_response = await client.chat.complete_async(
                model = model,
                messages = [
                    {
                        'role': 'user',
                        'content': prompt,
                    },
                ],
                max_tokens=1500
            )
            return chat_response.choices[0].message.content
        except:
            return 'Ошибка'