import base64
import json

import pandasai.pandas as pd
from pandasai.responses.response_type import ResponseType


class ResponseSerializer:
    @staticmethod
    def serialize_dataframe(df: pd.DataFrame):
        json_data = json.loads(df.to_json(orient="split", date_format="iso"))
        return {"headers": json_data["columns"], "rows": json_data["data"]}

    @staticmethod
    def serialize(result: ResponseType) -> ResponseType:
        """
        Format output response
        Args:
            result (ResponseType): response returned after execution

        Returns:
            ResponseType: formatted response output
        """

        if "type" in result and result["type"] == "dataframe":
            if isinstance(result["value"], pd.Series):
                result["value"] = result["value"].to_frame()
            if isinstance(result["value"], pd.DataFrame):
                df_dict = ResponseSerializer.serialize_dataframe(result["value"])
            else :
                df_dict = result["value"]    
            
            return {"type": result["type"], "value": df_dict}

        elif "type" in result and result["type"] == "plot" and isinstance(result["value"], str):
            # check if already in base64 str return
            if "data:image/png;base64" in result["value"]:
                return result

            with open(result["value"], "rb") as image_file:
                image_data = image_file.read()
            # Encode the image data to Base64
            base64_image = (
                f"data:image/png;base64,{base64.b64encode(image_data).decode()}"
            )
            return {
                "type": result["type"],
                "value": base64_image,
            }
        else:
            return result
