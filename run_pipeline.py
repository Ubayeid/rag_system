import subprocess
import sys

steps = [
    ("Converting documents to Markdown", "convert_to_markdown.py"),
    ("Converting Markdown to JSON", "markdown_to_json.py"),
    #("Generating entity maps from JSON", "entity_mapper.py"),
    ("Extracting entities", "entity_extractor.py"),
    ("Identifying relationships", "relationship_identifier.py"),
    ("Importing knowledge graph to Neo4j", "import_to_neo4j.py"),
]

def run_step(description, script):
    print(f"\n=== {description} ({script}) ===")
    try:
        result = subprocess.run([sys.executable, script], check=True, capture_output=True, text=True)
        print(result.stdout)
        print(f"[SUCCESS] {description}")
    except subprocess.CalledProcessError as e:
        print(e.stdout)
        print(e.stderr)
        print(f"[FAILED] {description}")
        sys.exit(1)

def main():
    for desc, script in steps:
        run_step(desc, script)
    print("\nPipeline completed successfully!")

if __name__ == "__main__":
    main()