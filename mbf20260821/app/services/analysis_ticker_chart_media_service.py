from pathlib import Path

from maxapi.enums import UploadType
from maxapi.types.input_media import InputMediaBuffer

from app.bot.client import bot


class AnalysisTickerChartMediaService:

    async def upload_image(
            self,
            file_path: str
    ):

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(file_path)

        # читаем изображение
        image_bytes = path.read_bytes()

        media = InputMediaBuffer(
            buffer=image_bytes,
            filename=path.name,
            type=UploadType.IMAGE
        )

        print("MEDIA BUFFER CREATED")

        try:
            result = await bot.upload_media(media)

            print("MEDIA RESULT:", result)

            # После успешной загрузки удаляем локальный файл
            try:
                path.unlink()
                print(f"LOCAL CHART REMOVED: {path}")
            except Exception as e:
                print(f"FAILED TO REMOVE LOCAL CHART: {e}")

            return result

        except Exception:
            # Если загрузка не удалась,
            # файл оставляем для отладки
            print("UPLOAD FAILED, LOCAL FILE KEPT")
            raise