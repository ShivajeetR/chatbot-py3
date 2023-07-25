import openai

with open('hidden.txt') as file:
    openai.api_key = file.read()

def get_api_response(prompt: str) -> str | None:
    text: str | None = None

    try:
        response: dict = openai.Completion.create(
            model= 'text-davinci-003',
            prompt= prompt,
            temperature= 0.9,
            max_tokens= 150,
            top_p= 1,
            frequency_penalty= 0,
            presence_penalty= 0.6,
            stop=['Human:', 'AI:']
        )
        choices = response.get('choices')[0]
        text = choices.get('text')

    except Exception as e:
        print("Error:", e)

    return text

def update_list(message: str, pl: list[str]):
    pl.append(message)

def create_prompt(message, pl):
    p_message = f'\nHuman: {message}'
    update_list(p_message, pl)
    prompt = ''.join(pl)
    return prompt

def get_bot_response(message, pl):
    prompt = create_prompt(message, pl)
    bot_response = get_api_response(prompt)

    if bot_response:
        update_list(bot_response, pl)
        #pos = bot_response.find('\nAI: ')
        #bot_response = bot_response[pos+4:]
    else:
        bot_response = "Something went wrong!"

    return bot_response


def main():
    pl = []
    while True:
        user_input = input('You: ')
        response = get_bot_response(user_input, pl)
        print(response.strip())


if __name__ == '__main__':
    main()