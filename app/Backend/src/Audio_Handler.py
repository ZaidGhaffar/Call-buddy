import asyncio 
import pyaudio
from google import genai
from asyncio import TaskGroup
from dotenv import load_dotenv
load_dotenv()
from prompts import RAG_data

# Configs
FORMAT = pyaudio.paInt16
CHANNELS = 1
SEND_SAMPLE_RATE = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNKS = 1024
SYSTEM_PROMPT = RAG_data
VOICE = "Aoede"  # Choose from Aoede, Charon, Fenrir, Kore, Puck
MODEL = "models/gemini-2.0-flash-exp"



class AudioHandler:
    def __init__(self):
        self.ai_speaking = False
        self.queue_in_audio = asyncio.Queue()
        self.queue_out_audio = asyncio.Queue()
        self.client = genai.Client(http_options={"api_version":"v1alpha"})
        self.config = {"generation_config": {
            "response_modalities": ["AUDIO"],
            "system_instruction": SYSTEM_PROMPT},
            "speech_config": {
                "voice_config": {
                    "prebuilt_voice_config": {
                        "voice_name": VOICE
                    }
                }
            }          
                       }
        self.pya = pyaudio.PyAudio()
    
    async def listen_to_audio(self):
        device_info = self.pya.get_default_input_device_info()
        input_stream = self.pya.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=SEND_SAMPLE_RATE,
            input=True,
            input_device_index=device_info["index"],
            frames_per_buffer=CHUNKS,
        )
        try:
            print("Listening...")
            while True:
                if not self.ai_speaking:
                    data = await asyncio.to_thread(
                        input_stream.read,CHUNKS, exception_on_overflow=False
                    )
                    await self.queue_in_audio.put(data)
                else:
                    await asyncio.sleep(0.1)
            
        except Exception as e:
            print("Sorry an Error ❌ accured in listen_to_audio Function",e)
        finally:
            input_stream.stop_stream()
            input_stream.close()
            
            
    
    async def SendData_to_Gemini(self,session):
        try:
            while True:
                audio_data = await self.queue_in_audio.get()
                if audio_data is None:
                    break
                await session.send(input={"data":audio_data,"mime_type": "audio/pcm"},end_of_turn=True)
                
        except Exception as e:
            print("Sorry an Error ❌ accured in Send audio data to Gemini Function",e)
    
    
    
    async def GetResponse_from_Gemini(self,session):
        try:
            while True:
                turns = session.receive()
                async for response in turns:
                    data = response.data
                    if data: 
                        await self.queue_out_audio.put(data)
                    text = response.text
                    if text:
                        print(f"Gemini  :     {text}")
        except Exception as e:
            print("Sorry an Error ❌ accured in Gemini Response Function",e)
    
    
    
    async def PlayAudio(self):
        output_stream = self.pya.open(
            format=FORMAT,
            rate=RECEIVE_SAMPLE_RATE,
            channels=CHANNELS,
            output=True
        )
        try:
            while True:
                data = await self.queue_out_audio.get()
                if not self.ai_speaking:
                    self.ai_speaking=True
                    print("AI Started Speaking...")
                await asyncio.to_thread(output_stream.write,data)
                if self.queue_out_audio.empty():
                    self.ai_speaking = False  # AI has finished speaking
                    print("You can speak now.")
        except Exception as e:
            print("Sorry an Error ❌ accured in PlayAudio Function",e)
    
    async def Run(self):
        try:
            async with (self.client.aio.live.connect(model=MODEL, config=self.config) as session,TaskGroup() as tg,):
                tg.create_task(self.listen_to_audio())
                tg.create_task(self.SendData_to_Gemini(session))
                tg.create_task(self.GetResponse_from_Gemini(session))
                tg.create_task(self.PlayAudio())
                
                # Keep the main coroutine alive
                await asyncio.Event().wait()   
        except Exception as e:
            print("Sorry an Error ❌ accured in RUN Function",e)
    
    
    def close(self):
        self.pya.terminate()



if __name__ == "__main__":
    pass
