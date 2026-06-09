from dotenv import load_dotenv
from ingestion.ingestion import ingest


def main():
    ingest()
    print("Hello from cis-benchmark-rag!")


if __name__ == "__main__":
    load_dotenv()
    main()
