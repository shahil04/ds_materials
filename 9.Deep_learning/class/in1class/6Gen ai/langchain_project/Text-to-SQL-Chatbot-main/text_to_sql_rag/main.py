def main():
    print("Hello from text-to-sql-rag!")

# from app.schema_loader import save_schema

# save_schema()

from app.pipeline import ask

question = input("Ask: ")
    
result = ask(question)

print(result)

if __name__ == "__main__":
    main()
