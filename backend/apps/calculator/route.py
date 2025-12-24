from fastapi import APIRouter, HTTPException
import base64
from io import BytesIO
from apps.calculator.utils import analyze_image
from schema import ImageData
from PIL import Image

router = APIRouter()

@router.post('/calculate') # पाथ यहाँ डिफाइन कर दिया गया है
async def run(data: ImageData):
    try:
        # 1. इमेज डेटा को डिकोड करना
        # Assumes data:image/png;base64,<data>
        image_data = base64.b64decode(data.image.split(",")[1])
        image_bytes = BytesIO(image_data)
        image = Image.open(image_bytes)
        
        # 2. इमेज को एनालाइज करना
        responses = analyze_image(image, dict_of_vars=data.dict_of_vars)
        
        # 3. डेटा को लिस्ट में डालना
        output_data = []
        for resp in responses:
            output_data.append(resp)
            print('Processing response: ', resp)

        # लूप के बाहर पूरी लिस्ट प्रिंट करना सुरक्षित है
        print('Total processed responses: ', len(output_data))
        
        return {
            "message": "Image processed", 
            "data": output_data, 
            "status": "success"
        }
        
    except Exception as e:
        # अगर कोई भी एरर आती है, तो वह आपके Python टर्मिनल में दिखेगी
        print(f"ERROR IN ROUTE: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))