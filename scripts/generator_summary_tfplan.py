
import argparse
from pathlib import Path

def generate_markdown(tfplan_path, output_md_path):
    # Read the content of the tfplan file
    content = Path(tfplan_path).read_text()

    # Remove footer section
    content = content.split("─────────────────────────────────────────────────────────────────────────────")[0].rstrip()

    # Remove header section
    lines = content.splitlines()
    start_index = 0
    for i, line in enumerate(lines):
        if "OpenTofu will perform the following actions:" in line:
            start_index = i + 1
            break
    cleaned_content = "\n".join(lines[start_index:]).strip()

    # Extract summary line
    summary_line = [line for line in lines if line.startswith("Plan:")]
    add_count, change_count, destroy_count = 0, 0, 0
    if summary_line:
        parts = summary_line[0].split(" ")
        add_count = parts[1]
        change_count = parts[4]
        destroy_count = parts[7]

    # Build markdown content with summary table
    markdown = f"""# Terraform Plan Summary

```
{cleaned_content}
```

## Plan Summary Table

| 🟩 **Add**    | {add_count} resources will be added    |
|--------------|----------------------------------------|
| 🟨 **Change** | {change_count} resources will be changed   |
| 🟥 **Destroy**| {destroy_count} resources will be destroyed |
"""

    # Write to output file
    Path(output_md_path).write_text(markdown)
    print(f"Markdown file generated: {output_md_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Markdown table summary from a Terraform/Tofu plan.")
    parser.add_argument("--input", "-i", required=True, help="Path to the input tfplan file")
    parser.add_argument("--output", "-o", default="tfplan_summary.md", help="Path to output markdown file")
    args = parser.parse_args()

    generate_markdown(args.input, args.output)
