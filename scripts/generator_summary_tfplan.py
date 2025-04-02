import re

input_file = "tfplan.txt"
output_file = "tfplan_summary.md"

with open(input_file, "r") as f:
    plan_text = f.read()

# Count actions
to_create = len(re.findall(r'will be created', plan_text))
to_update = len(re.findall(r'will be updated in-place', plan_text))
to_destroy = len(re.findall(r'will be destroyed', plan_text))

# Extract created resources
create_blocks = re.findall(r'# (.*?) will be created\n\s+\+ resource .*?{.*?^\s+}', plan_text, flags=re.DOTALL | re.MULTILINE)
created_resources = [line.strip().split(" ")[0] for line in create_blocks]

# Extract updated resources with tag changes
update_blocks = re.findall(
    r'# (.*?) will be updated in-place\s+~ resource "(.*?)" "(.*?)" {(.*?)~ tags\s+= {(.*?)} -> \(known after apply\)',
    plan_text, flags=re.DOTALL
)

# Build markdown summary
lines = []

lines.append(f"## ✅ Resources to be *created* ({to_create})\n")
for res in created_resources:
    if "data_collection_endpoint" in res:
        lines.append(f"- **{res.split('.')[1]}** – Data Collection Endpoint")
    elif "data_collection_rule" in res:
        lines.append(f"- **{res.split('.')[1]}** – Data Collection Rule")
lines.append("")

lines.append(f"## 🔁 Resources to be *updated* ({to_update})\n")
if update_blocks:
    for full_id, res_type, res_name, block_text, tag_block in update_blocks:
        lines.append(f"- **{res_name}** – {res_type.replace('_', ' ').title()}")
        tag_lines = tag_block.strip().split('\n')
        if tag_lines:
            lines.append(f"  - Tags to be removed:")
            for tag in tag_lines:
                tag_clean = tag.strip().lstrip('-').strip()
                if tag_clean:
                    lines.append(f"    - `{tag_clean}`")
else:
    lines.append("No specific tag changes found.")
lines.append("")

lines.append(f"## ❌ Resources to be *destroyed* ({to_destroy})\n")
lines.append("None.\n" if to_destroy == 0 else "Some resources will be destroyed.\n")

lines.append("## 📊 Summary")
lines.append(f"- **Create**: {to_create} resources")
lines.append(f"- **Update**: {to_update} resources")
lines.append(f"- **Destroy**: {to_destroy} resources")

# Write markdown file
with open(output_file, "w") as f:
    f.write("\n".join(lines))

print(f"✅ Markdown summary saved to: {output_file}")
