To install NVIDIA CUDA Toolkit on Windows, you can follow these steps:

Check if your system meets the minimum requirements by referring to the CUDA Toolkit release notes: https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html.

Download the CUDA Toolkit installer from the NVIDIA website: https://developer.nvidia.com/cuda-toolkit-archive.

Run the installer and follow the prompts to install the toolkit. During installation, you can choose to install the CUDA toolkit, the CUDA samples, and other components.

After the installation is complete, make sure to add the CUDA Toolkit installation directory to your system path.

Restart your system to ensure that the CUDA Toolkit is properly installed.

Note that the installation process may vary depending on your system configuration and the version of the CUDA Toolkit you are installing. You should refer to the installation guide provided by NVIDIA for your specific system and version of the CUDA Toolkit.

To install the cuDNN library, you can follow these steps:

Register on the NVIDIA website: https://developer.nvidia.com/developer-program.

Download the cuDNN library for your system from the NVIDIA website: https://developer.nvidia.com/cudnn.

Extract the contents of the downloaded archive to a location of your choice.

Add the location where you extracted the cuDNN library to your system path.

Ensure that your system has the appropriate version of the NVIDIA CUDA Toolkit installed. You can check the compatibility of the cuDNN library with different versions of the CUDA Toolkit on the NVIDIA website.

Restart your system to ensure that the cuDNN library is properly installed.

Note that the installation process may vary depending on your system configuration and the version of the cuDNN library you are installing. You should refer to the installation guide provided by NVIDIA for your specific system and version of the cuDNN library.


run 

pip install -r requirements.txt

export PATH="${PATH}:/usr/local/nvidia/bin:/usr/local/cuda/bin"
TF_GPU_ALLOCATOR=cuda_malloc_async


-- convert to js 
tensorflowjs_converter  --input_format=tf_saved_model  --output_node_names='MobilenetV1/Predictions/Reshape_1'  --saved_model_tags=serve  /flower_clasifier /web_model

tensorflowjs_converter --input_format=keras --output_format=tfjs_graph_model d:/work/tfjs/model_epoch_09_loss_0.94_acc_0.64_val_loss_1.65_val_acc_0.29.h5 d:/work/tfjs/output/model-tfjs-graph

docker run -it --rm -v "D:/work/aplicatii develbox/adblocker/pyton/fcn/snapshotsTest:/python" evenchange4/docker-tfjs-converter tensorflowjs_converter --input_format=keras --output_format=tfjs_graph_model python/model_epoch_02_loss_1.37_acc_0.44_val_loss_2.27_val_acc_0.13.h5 python/output/model-tfjs-graph

-- serve tf models 

docker run -d -v "d:/work/tfjs:/web" -p 9999:8080 halverneus/static-file-server:latest



