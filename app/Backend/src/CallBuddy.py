from Audio_Handler import AudioHandler
import asyncio

class CallBuddy_App:
    def __init__(self):
        self.handler = AudioHandler()
    
    async def main(self):
        try:
            await self.handler.Run()
        except Exception as e:
            print("Error ❌ in Callbuddy Application.py file  ",e)
        finally:
            self.handler.close()
    
if __name__ == "__main__":
    app = CallBuddy_App()
    asyncio.run(app.main())