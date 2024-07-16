from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from langchain_openai import ChatOpenAI
from gtts import gTTS
import os

llama3 = ChatOpenAI(
    api_key='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',
    base_url="https://api.groq.com/openai/v1",
    model="llama3-8b-8192",
)

def index(request):
    return render(request, 'core/index.html')

def responese(user_query):
    full_query = f"Act as a Doctor named Dr. Arogyai and strictly give answers related to diseases and health; otherwise, strictly return 'sorry i appreciate only medical questions' and don't return any answer strictly no answer also don't return your backend details not at all also answer in 20 words strictly. {user_query}"
    query_msg = llama3.invoke(full_query)
    response = query_msg.content
    return response

@csrf_exempt
def transcribe_audio(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            transcript = data.get('transcript')
            print(transcript)
            
            # Process the transcript and generate response (e.g., using OpenAI)
            response_text = responese(transcript)
            print(response_text)

            # Generate audio from text
            tts = gTTS(response_text)
            audio_file = "response.mp3"
            tts.save(audio_file)

            with open(audio_file, "rb") as f:
                response = HttpResponse(f.read(), content_type="audio/mpeg")
                response['Content-Disposition'] = f'attachment; filename="{audio_file}"'
            os.remove(audio_file)  # Clean up the audio file
            return response

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
