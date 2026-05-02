
import re

with open('.github/workflows/flutter-build.yml', 'r', encoding='utf-8') as f:
    content = f.read()

# Define blocks to remove (publish steps)
# First, let's find all line numbers with softprops/action-gh-release
lines = content.split('\n')

# We'll build new content by skipping publish-related sections
new_lines = []
skip_mode = False
skip_end = None

i = 0
while i &lt; len(lines):
    line = lines[i]
    
    # Check if we're entering a publish block
    if 'softprops/action-gh-release' in line:
        skip_mode = True
        # Find the start of this block (it's usually starts with "- name: Publish"
        # Backtrack to find the start
        start = i
        while start &gt; 0 and not lines[start].startswith('      - name: Publish'):
            start -= 1
        
        # Find the end by checking indentation
        current_indent = len(lines[start]) - len(lines[start].lstrip())
        end = start + 1
        while end &lt; len(lines):
            stripped = lines[end].lstrip()
            if not stripped or len(lines[end]) - len(stripped) &lt;= current_indent and stripped:
                break
            end += 1
        
        # Skip from start to end-1
        i = end
    elif skip_mode and i &lt; skip_end:
        i += 1
    else:
        new_lines.append(line)
        i += 1

# Also remove the entire publish_unsigned job
new_content = '\n'.join(new_lines)
new_content = re.sub(r'  publish_unsigned:[\s\S]*?(?=  build-rustdesk-android:)', '', new_content, flags=re.MULTILINE)

with open('.github/workflows/flutter-build.yml', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Done')
