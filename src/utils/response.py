
from sdks.novavision.src.helper.package import PackageHelper
from components.CropCompare.src.models.PackageModel import PackageModel, PackageConfigs, ConfigExecutor, CropExecutorOutputs, CropExecutorResponse, CropExecutor, OutputImage


def build_response(context):
    outputImage = OutputImage(value=context.image)
    cropExecutorOutputs= CropExecutorOutputs(outputImage=outputImage)
    cropExecutorResponse = CropExecutorResponse(outputs=cropExecutorOutputs)
    cropExecutor = CropExecutor(value=cropExecutorResponse)
    executor = ConfigExecutor(value=cropExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel