from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config


class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image],Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class CropVariable(Config):
    """
         Ne kadar crop yapmak istediğinizi yüzdelik üzerinden giriniz.
    """
    name: Literal["cropVariable"] = "cropVariable"
    value: int = Field(default=1, ge=1, le=100)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["integers between [0, 100]"] = "integers between [0, 100]"

    class Config:
        title = "Crop Percentage"

class CropExecutorInputs(Inputs):
    inputImage: InputImage


class CropExecutorConfigs(Configs):
   cropVariable:CropVariable


class CropExecutorOutputs(Outputs):
    outputImage: OutputImage


class CropExecutorRequest(Request):
    inputs: Optional[CropExecutorInputs]
    configs: CropExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class CropExecutorResponse(Response):
    outputs: CropExecutorOutputs


class CropExecutor(Config):
    name: Literal["CropExecutor"] = "CropExecutor"
    value: Union[CropExecutorRequest, CropExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Package"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[CropExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"
        json_schema_extra = {
            "target": "value"
        }


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["CropCompare"] = "CropCompare"
