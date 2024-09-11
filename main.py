from fastapi import FastAPI


# create an instance of fastapi
app = FastAPI()


@app.get("/")
def index():
    return {
        "company": "Imittis",
        "founder": "Faisal Lawan Muhammad"
    }

@app.get("/about")
def about():
    return {"data": "Free to Dream"}