import json


print(
    "TICKER CHART MEDIA PARSER LOADED"
)


def parse_photo_upload(upload_result):


    # =====================================
    # Пустой ответ
    # =====================================

    if upload_result is None:

        print(
            "UPLOAD RESULT IS NONE"
        )

        return None


    # =====================================
    # Если пришел JSON строкой
    # =====================================

    if isinstance(upload_result, str):

        try:

            data = json.loads(
                upload_result
            )

        except json.JSONDecodeError:

            print(
                "UPLOAD RESULT JSON ERROR"
            )

            return None

    else:

        data = upload_result


    # =====================================
    # Получаем фотографии
    # =====================================

    photos = data.get(
        "photos",
        {}
    )


    if not photos:

        print(
            "NO PHOTOS IN RESPONSE"
        )

        return None


    # =====================================
    # Первая фотография
    # =====================================

    photo_id, photo = next(
        iter(photos.items())
    )


    token = photo.get(
        "token"
    )


    if not token:

        print(
            "PHOTO TOKEN NOT FOUND"
        )

        return None


    result = {

        "photo_id": photo_id,

        "token": token

    }


    print(
        "PHOTO PARSED:",
        result
    )


    return result