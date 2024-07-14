from fastapi import FastAPI
import bot
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/run-script")
def run_script():
    bot.run()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
