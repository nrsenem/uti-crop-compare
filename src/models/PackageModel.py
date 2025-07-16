from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, \
    Config


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


class InputSecondImage(Input):
    name: Literal["inputSecondImage"] = "inputSecondImage"
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

class OutputSecondImage(Output):
    name: Literal["outputSecondImage"] = "outputSecondImage"
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


class KeepSideFalse(Config):
    name: Literal["False"] = "False"
    value: Literal[False] = False
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Disable"


class KeepSideTrue(Config):
    name: Literal["True"] = "True"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Enable"


class KeepSideBBox(Config):
    """
        Rotate image without catting off sides.
    """
    name: Literal["KeepSide"] = "KeepSide"
    value: Union[KeepSideTrue, KeepSideFalse]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Keep Sides"


class Degree(Config):
    name: Literal["Degree"] = "Degree"
    value: int = Field(ge=0, le=100, default=0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[0, 100]"] = "[0, 100]"

    class Config:
        title = "Crop Percent"


class CompareExecutorInputs(Inputs):
    inputImage: InputImage
    inputSecondImage: InputSecondImage

class CompareExecutorConfigs(Configs):
    drawBBox: KeepSideBBox



class CompareExecutorOutputs(Outputs):
    outputImage: OutputImage
    outputSecondImage: OutputSecondImage


class CompareExecutorRequest(Request):
    inputs: Optional[CompareExecutorInputs]
    configs: CompareExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class CompareExecutorResponse(Response):
    outputs: CompareExecutorOutputs


class CompareExecutor(Config):
    name: Literal["CompareExecutor"] = "CompareExecutor"
    value: Union[CompareExecutorRequest, CompareExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Compare"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class CropExecutorInputs(Inputs):
    inputImage: InputImage


class CropExecutorConfigs(Configs):
    degree: Degree
    drawBBox: KeepSideBBox


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
        title = "Crop"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[CropExecutor, CompareExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["CropCompare"] = "CropCompare"
