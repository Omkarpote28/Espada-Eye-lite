# !pip install transformers gradio
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
from PIL import Image
import gradio as gr

# Load the model, image processor, and tokenizer
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
image_processor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

# Move the model to the specified device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Set the maximum length and number of beams for generation
max_length = 20
num_beams = 5
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

# Define the prediction function
def predict_step(image):
    # Convert Gradio Image interface output to PIL Image
    pil_image = Image.fromarray(image.astype('uint8'), 'RGB')

    # Extract features and move to the specified device
    pixel_values = image_processor(images=pil_image, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)

    # Generate captions using the model
    output_ids = model.generate(pixel_values, **gen_kwargs)

    # Decode and format the predictions
    preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
    preds = [pred.strip() for pred in preds]
    return preds[0]  # Return the first prediction

# Create a Gradio interface
iface = gr.Interface(
    fn=predict_step,
    inputs=gr.Image(),
    outputs="text",
    live=True,
    title="Espada Eye v1.0",
    description="Provide an image to Espada and he will describe the image...",
)

# Launch the Gradio interface
iface.launch()
