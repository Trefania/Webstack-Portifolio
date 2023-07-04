"""
Content Generation Engine
"""
import os
import openai

if not openai.api_key:
    with open('hidden.txt') as file:
        openai.api_key = file.read()

def get_api_response(prompt: str) -> str | None:
    """Gets A Response from API"""
    text: str | None = None

    try:
       response: dict == response = openai.Completion.create(
           model="text-davinci-003",
           prompt=prompt,
           temperature=1,
           max_tokens=150,
           top_p=1,
           frequency_penalty=0,
           presence_penalty=0,
           stop=[' User:', ' ASSIST AI:']
       )

       choices: dict = response.get('choices')[0]
       text = choices.get('text')

    except Exception as e:
        print('ERROR:', e)

    return text


def update_list(message: str, pl: list[str]):
    pl.append(message)


def create_prompt(message: str, pl: list[str]) -> str:
    p_message: str = f'\nUser: {message}'
    update_list(p_message, pl)
    prompt: str = ''.join(pl)
    return prompt


def get_bot_response(message: str, pl: list[str]) -> str:
    prompt: str = create_prompt(message, pl)
    bot_response: str = get_api_response(prompt)

    if bot_response:
        update_list(bot_response, pl)
        pos: int = bot_response.find('\nASSIST AI: ')
        bot_response = bot_response[pos + 11:]
    else:
        bot_response = 'Something went wrong...'

    return bot_response


def main():
    prompt_list: list[str] = ['You will Pretend to be a very Knowledgable, Fun, Intuitive, Kind and Considerate Assistant Bot. Your Name is `ASSIST AI`',
                              '\nUser: Hello ASSIST AI',
                              '\nASSIST AI: Hello Dear User, What Can I Do for You Today?']
    
    while True:
        user_input: str = input('User: ')
        response: str = get_bot_response(user_input, prompt_list)
        print(f'Assist AI: {response}')

if __name__ == '__main__':
    main()