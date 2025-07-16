
from sdks.novavision.src.helper.package import PackageHelper
from components.CropCompare.src.models.PackageModel import PackageModel, PackageConfigs, ConfigExecutor, CropExecutorOutputs, CropExecutorResponse, CropExecutor, CompareExecutorOutputs, CompareExecutorResponse, CompareExecutor, OutputSecondImage, OutputImage


def build_response_crop(context):
    outputImage = OutputImage(value=context.image)
    cropExecutorOutputs= CropExecutorOutputs(outputImage=outputImage)
    cropExecutorResponse = CropExecutorResponse(outputs=cropExecutorOutputs)
    cropExecutor = CropExecutor(value=cropExecutorResponse)
    executor = ConfigExecutor(value=cropExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel

def build_response_compare(context):
    outputImage = OutputImage(value=context.image)
    outputSecondImage = OutputSecondImage(value=context.secondImage)
    compareExecutorOutputs= CompareExecutorOutputs(outputImage=outputImage, outputSecondImage=outputSecondImage)
    compareExecutorResponse = CompareExecutorResponse(outputs=compareExecutorOutputs)
    compareExecutor = CompareExecutor(value=compareExecutorResponse)
    executor = ConfigExecutor(value=compareExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel
