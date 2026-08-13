print(
    "TICKER HISTORY FORMATTER LOADED"
)



def format_history(

        ticker,

        history

):


    text = (

        f"📈 История {ticker}\n\n"

    )


    for index, item in enumerate(

            history,

            start=1

    ):


        text += (

            f"{index}. {item['date']}\n"

            f"💰 Закрытие: {item['close']:.2f} ₽\n"

            f"⬆ Максимум: {item['high']:.2f} ₽\n"

            f"⬇ Минимум: {item['low']:.2f} ₽\n\n"

        )


    return text