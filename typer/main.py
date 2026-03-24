import typer

app = typer.Typer()

print("from the cli file")

@app.command()
def hello(name: str):
    print(f"Hello {name}")

@app.command()
def sayhi(name: str):
    print(f"Hello from yosef to {name}")

@app.command()
def prompt():
    person_name = typer.prompt("What is your name")
    print(f"Hello {person_name}")

@app.command()
def add():
    print("Wellcome to interactive calculator")
    numberOne = typer.prompt("Enter the first number",type=int)
    numberTwo = typer.prompt("Enter the second number", type=int)
    print(f"The sum of your number is {numberOne + numberTwo}")

if __name__ == "__main__":
    app()