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
class TextWriterText(Config):
    name: Literal["textWriterText"] = "textWriterText"
    value: str
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Text Writer Input"

class Left(Config):
    configEdit: TextWriterText
    name: Literal["Left"] = "Left"
    value: Literal["Left"] = "Left"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Left"

class Right(Config):
    configEdit: TextWriterText
    name: Literal["Right"] = "Right"
    value: Literal["Right"] = "Right"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Right"

class Bottom(Config):
    configEdit: TextWriterText
    name: Literal["Bottom"] = "Bottom"
    value: Literal["Bottom"] = "Bottom"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Bottom"

class Top(Config):
    configEdit: TextWriterText
    name: Literal["Top"] = "Top"
    value: Literal["Top"] = "Top"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Top"

class Center(Config):
    configEdit: TextWriterText
    name: Literal["Center"] = "Center"
    value: Literal["Center"] = "Center"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Center"


class ConfigTypeTextWriter(Config):
    """
        Yazınızın resimde ki konumu.
    """
    name: Literal["configTypeTextWriter"] = "configTypeTextWriter"
    value: Union[Center, Top, Left, Right, Bottom]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Text Writer"


class CropVariable(Config):
    """
      NE KADAR KIRPMAK İSTİYORSANIZ YÜZDE CİNSİNDEN GİRİNİZ
    """
    name: Literal["cropVariable"] = "cropVariable"
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
    configTypeTextWriter: ConfigTypeTextWriter


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
    cropVariable: CropVariable



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
    value: Union[CropExecutor,CompareExecutor]
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