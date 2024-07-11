import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt

def neural_style_transfer(content_image_path, style_image_path, output_image_path):
    """
    Apply neural style transfer to an image using TensorFlow.

    :param content_image_path: Path to the content image.
    :param style_image_path: Path to the style image.
    :param output_image_path: Path to save the output image.
    :return: The image with the style transferred.
    """
    content_image = plt.imread(content_image_path)
    style_image = plt.imread(style_image_path)
    
    # Load the pre-trained model
    hub_module = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
    
    # Preprocess the images
    content_image = tf.image.convert_image_dtype(content_image, tf.float32)[tf.newaxis, ...]
    style_image = tf.image.convert_image_dtype(style_image, tf.float32)[tf.newaxis, ...]
    
    # Apply style transfer
    stylized_image = hub_module(content_image, style_image)[0]
    
    # Save the output image
    tf.keras.preprocessing.image.save_img(output_image_path, stylized_image[0])
    
    return stylized_image

# Example usage:
content_image_path = 'path_to_content_image.jpg'
style_image_path = 'path_to_style_image.jpg'
output_image_path = 'output_image.jpg'
stylized_image = neural_style_transfer(content_image_path, style_image_path, output_image_path)
plt.imshow(stylized_image)
plt.show()
