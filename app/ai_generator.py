import os
from mistralai import Mistral

api_key = os.environ.get('AI_KEY')
model = 'mistral-large-latest'

client = Mistral(api_key=api_key)

async def generate_post_text(before_text: str, additional_data: str = ''):
    prompt = f'Есть пост с канала, переделай его заменяя слова на подходящие синонимы и меняя порядок предложения, но сохраняя стилистическую окраску, смысл, цитаты, имена. Замени markdown на html (только стили a, b, i, цитаты и так далее, без тегов p, br, hr). {additional_data} Отправь только готовый текст, текст поста: {before_text}'
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