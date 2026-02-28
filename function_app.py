import logging
import azure.functions as func
from azure.functions import Out # Шығыс байламын (Output Binding) пайдалану үшін
from PIL import Image
import io 

# Function App-ты іске қосу (V2 моделінің негізі)
app = func.FunctionApp()

# ImageResizer функциясы
# 1. @app.blob_output: Шығыс байламы - Кішірейтілген суретті output-images бакетіне сақтайды.
# 2. @app.blob_trigger: Кіріс байламы - input-images бакетіне сурет жүктелгенде іске қосады.
@app.blob_output(arg_name="outputblob", path="output-images/{name}",
                 connection="AzureWebJobsStorage")
@app.blob_trigger(arg_name="inputblob", path="input-images/{name}",
                  connection="AzureWebJobsStorage")
def ImageResizer(inputblob: func.InputStream, outputblob: func.Out[bytes]):
    logging.info(f"Python Blob trigger function processed blob \n"
                 f"Name: {inputblob.name}\n"
                 f"Blob Size: {inputblob.length} bytes")

    try:
        # 1. Кіріс Blob деректерін оқу
        image_data = inputblob.read()
        
        # 2. Pillow арқылы суретті ашу
        img = Image.open(io.BytesIO(image_data))
        
        # 3. Суреттің өлшемін кішірейту
        # Біз 100x100 пиксел өлшемін қолданамыз
        new_size = (100, 100)
        img.thumbnail(new_size)
        
        # 4. Кішірейтілген суретті Output Bytes буферіне сақтау (JPG форматында)
        # Суреттің сапасын сақтау үшін JPEG форматын қолданыңыз
        output_buffer = io.BytesIO()
        img.save(output_buffer, format='JPEG')
        
        # 5. Шығыс Blob-қа деректерді жазу
        outputblob.set(output_buffer.getvalue())

        logging.info(f"Image '{inputblob.name}' successfully resized and saved to output-images.")

    except Exception as e:
        logging.error(f"Error processing image {inputblob.name}: {e}")
        # Қате болса, Azure Log Stream-ге жазып, оны көтеру
        raise