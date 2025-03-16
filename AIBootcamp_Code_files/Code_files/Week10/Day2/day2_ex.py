import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import convolve

# Load a sample grayscale image
image = np.random.rand(10, 10)

#print(image)

# Define convolution kernels(filters)
edge_detection_kernel = np.array([
    [-1, -1, -1],
    [-1, 8, -1],
    [-1, -1, -1],
])

blur_kernel = np.array([
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
]) / 9

# Apply Convolution
edge_detected_image = convolve(image, edge_detection_kernel)
blurred_image = convolve(image, blur_kernel)

# Visualize original and filtered image
# fig, axes = plt.subplots(1, 3, figsize=(12, 4))
# axes[0].imshow(image, cmap="gray")
# axes[0].set_title("Original Image")
# axes[1].imshow(edge_detected_image, cmap="gray")
# axes[1].set_title("Edge Detected")
# axes[2].imshow(blurred_image, cmap="gray")
# axes[2].set_title("Blurred")
# plt.show()


import tensorflow as tf

# Create a sample input tesnor (batch_size, height, width, channels)
image_tensor = tf.random.normal([1, 10, 10, 1])

# Define a convolutional layer
conv_layer = tf.keras.layers.Conv2D(
    filters=1,
    kernel_size=(3,3),
    strides=(1, 1),
    padding='same'
)

# APplying convolution
output_tensor = conv_layer(image_tensor)

print(f"Original Shape: {image_tensor.shape}")
print(f"Ouput Shape: {output_tensor.shape}")

import torch
import torch.nn as nn

# Create a sample input tensor (batch_size, channels, height, width)
image_tensor_pt = torch.randn(1, 1, 10, 10)

# Define a convolutional layer
conv_layer_pt = nn.Conv2d(
    in_channels=1,
    out_channels=1, 
    kernel_size=3, 
    stride=1,
    padding=1
)

# APply Convolution
output_tensor_pt = conv_layer_pt(image_tensor_pt)

print(f"Original Shape: {image_tensor_pt.shape}")
print(f"Oytput Shape: {output_tensor_pt.shape}")

# TensorFlow Example
conv_layer_large_kernel = tf.keras.layers.Conv2D(filters=1, kernel_size=(5, 5), strides=(1, 1), padding="same")
output_large_kernel = conv_layer_large_kernel(image_tensor)

print(f"Large Kernel Output Shape: {output_large_kernel.shape}")

# Pytorch Example
conv_layer_stride_2 = nn.Conv2d(in_channels=1, out_channels=1, kernel_size=3, stride=2, padding=1)
output_stride_2 = conv_layer_stride_2(image_tensor_pt)

print(f"Stride Output Shape: {output_stride_2.shape}")