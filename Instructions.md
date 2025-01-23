**# Why use Gemini LiveAPI**

1. It's super powerfull & is totally free to use.
2. It Support Function Calling
3. It Supports multiple Voices : Aoede, Charon, Fenrir, Kore, and Puck.
4. It's a multilingual Model.
5. It supports System Prompts as well.

# Limitations:

1. Session duration is limited to up to 15 minutes for audio or up to 2 minutes of audio and video. When the session duration exceeds the limit, the connection is terminated.
2. Rate limits: 3 concurrent sessions per API key, 4M tokens per minute
3. You can make 3 calls at the same time from the same API key.

# Notes:

1.Multimodal Live API supports the following audio formats: - Input audio format: Raw 16 bit PCM audio at 16kHz little-endian - Output audio format: Raw 16 bit PCM audio at 24kHz little-endian

# https://ai.google.dev/api/multimodal-live

**# Why FastAPI**

1. It's super Fast:
   1. Starleete -> async programming
   2. Pydantic -> Data Validation,Data Parsing
2. It's super Easy to use & Easy to deploy, plus it's super fast & powerfull.

# client Side Code

1. When we call navigator.mediaDevices.getUserMedia() the browser acesss the user microphone & start capturing the user audio in raw binary format. - the microhphone audio data comes as float32 data. - we convert the float32 data into int16 16-bit PCM format. It's like preparing the sound for delivery! - Once in PCM format, Our code converts it into Base64 format. This makes it easier to send over the WebSocket. 🚀 - Finally the Base64 data is wrapped up in payload (a neat package (json format)) and sent over the WebSocket.

# C:\python\Product-wintaX\WintaX-Product

# Server Side code

1. We receive the Base64 data from the client & send it to the Google Geimini API. The API returns the audio data in Base64 format. We decode the Base64 data & convert it into float32 format. This is the audio data that we send to the client.
