from app.services.analysis_ticker_chart_service import (
    AnalysisTickerChartService
)

from app.services.analysis_ticker_chart_media_service import (
    AnalysisTickerChartMediaService
)


print(
    "CHART ATTACHMENT SERVICE LOADED"
)


class AnalysisTickerChartAttachmentService:


    def __init__(self):

        self.chart_service = AnalysisTickerChartService()

        self.media_service = AnalysisTickerChartMediaService()



    # ==================================================
    # Построить график и вернуть вложение для сообщения
    # ==================================================

    async def get_chart_attachment(
            self,
            ticker: str,
            limit: int = 1
    ):

        try:

            # 1. Создаем график

            file_path = await self.chart_service.create_price_chart(

                ticker=ticker,

                limit=limit

            )


            if not file_path:

                print(
                    "CHART NOT CREATED"
                )

                return None



            # 2. Загружаем изображение в MAX
            #    Возвращается готовый объект AttachmentUpload
            #    с type=image и payload=AttachmentPayload(token=...)
            #    Его можно сразу подставлять в attachments

            upload_result = await self.media_service.upload_image(

                file_path

            )


            if upload_result is None:

                print(
                    "UPLOAD RESULT IS NONE"
                )

                return None



            print(
                "CHART ATTACHMENT READY"
            )


            return upload_result


        except Exception as e:

            # Если с графиком что-то пошло не так —
            # просто отправим текст без графика

            print(
                "CHART ATTACHMENT ERROR:",
                e
            )

            return None