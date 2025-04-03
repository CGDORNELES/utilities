import re
import argparse

parser = argparse.ArgumentParser(description="Generate a Markdown table summary from a Terraform/Tofu plan.")
parser.add_argument("--input", "-i", required=True, help="Path to the input tfplan file")
parser.add_argument("--output", "-o", default="tfplan_summary.md", help="Path to output markdown file")
args = parser.parse_args()

with open(args.input, "r") as f:
    content = f.read()

lines = []

def extract_blocks(symbol):
    return re.findall(rf'{re.escape(symbol)} resource "([^"]+)" "([^"]+)" {{(.*?)^  }}', content, flags=re.DOTALL | re.MULTILINE)

def parse_resource_block(res_type, res_name, block):
    name_match = re.search(r'\+ name\s+=\s+"([^"]+)"', block)
    rg_match = re.search(r'\+ resource_group_name\s+=\s+"([^"]+)"', block)
    loc_match = re.search(r'\+ location\s+=\s+"([^"]+)"', block)

    name = name_match.group(1) if name_match else res_name
    rg = rg_match.group(1) if rg_match else "-"
    location = loc_match.group(1) if loc_match else "-"
    return name, res_type, rg, location

def write_table(title, blocks, symbol_emoji):
    lines.append(f"## {symbol_emoji} Resources to be *{title}* ({len(blocks)} total)\n")
    lines.append("| Resource Name | Type | Resource Group | Location |")
    lines.append("|---------------|------|----------------|----------|")
    for res_type, res_name, block in blocks:
        name, res_type_clean, rg, location = parse_resource_block(res_type, res_name, block)
        lines.append(f"| `{name}` | `{res_type_clean}` | `{rg}` | `{location}` |")
    lines.append("")

# Blocos
created = extract_blocks("+")
updated = extract_blocks("~")
destroyed = extract_blocks("-")

# Tabelas
if created:
    write_table("created", created, "✅")
if updated:
    write_table("updated", updated, "🔁")
if destroyed:
    write_table("destroyed", destroyed, "❌")

# Sumário final
lines.append("## 📊 Summary")
lines.append(f"- **Create**: {len(created)} resources")
lines.append(f"- **Update**: {len(updated)} resources")
lines.append(f"- **Destroy**: {len(destroyed)} resources")

# Salva
with open(args.output, "w") as f:
    f.write("\n".join(lines))

print(f"✅ Markdown summary saved to: {args.output}")
