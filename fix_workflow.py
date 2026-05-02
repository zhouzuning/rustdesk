
import re

with open('.github/workflows/flutter-build.yml', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
new_lines = []

i = 0
while i &lt; len(lines):
    line = lines[i]
    if 'softprops/action-gh-release' in line:
        # This is a publish step
        # Find the line with "- name: Publish..."
        j = i
        while j &gt;= 0 and not lines[j].strip().startswith('- name: Publish'):
            j -= 1
        
        # Copy lines from j to i
        for k in range(j, i):
            new_lines.append(lines[k])
        
        # Add if: false before the uses line
        if i &gt; 0 and 'if:' not in lines[i-1]:
            # Check the indentation
            indent = len(lines[i]) - len(lines[i].lstrip())
            new_lines.append(' ' * indent + 'if: false')
        
        new_lines.append(line)
        i += 1
    else:
        new_lines.append(line)
        i += 1

# Also modify publish_unsigned job
new_content = '\n'.join(new_lines)
new_content = new_content.replace('if: ${{ inputs.upload-artifact }}', 'if: false', 1)

with open('.github/workflows/flutter-build.yml', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Done')
