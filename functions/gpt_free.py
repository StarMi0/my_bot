import g4f


# role = "программист python который специализируется на написании ботов на aiogram 3"
# content = "some text"


async def ask_gpt(role: str, content: str) -> str:
    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.gpt_4,
            messages=[{"role": role,
                       "content": content},
                      ],
            # stream=g4f.Provider.Bing.supports_stream,
        )
    except Exception as e:
        print(e)
        response = e
    # print(response, flush=True, end="")
    return f"GPT: {response}"
