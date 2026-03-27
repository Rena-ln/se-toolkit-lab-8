#!/usr/bin/env python3
"""Update docker-compose.yml to enable nanobot service."""

import yaml
import sys

# Read the file
with open('/root/se-toolkit-lab-8/docker-compose.yml', 'r') as f:
    content = f.read()

# Parse YAML
data = yaml.safe_load(content)

# Enable nanobot service
if 'nanobot' in data['services']:
    print("nanobot service already exists")
else:
    # Find the commented nanobot section and uncomment it
    lines = content.split('\n')
    new_lines = []
    skip_until_next_service = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check for nanobot comment block start
        if '# nanobot:' in line:
            # Start uncommenting
            indent = len(line) - len(line.lstrip())
            new_lines.append(line.strip().lstrip('# ').rstrip())
            i += 1
            # Continue uncommenting until we hit next service or end of block
            while i < len(lines):
                next_line = lines[i]
                if next_line.strip() == '' or (next_line.startswith('  #') and not next_line.startswith('  #   ')):
                    # End of nanobot block
                    break
                if next_line.startswith('  # '):
                    new_lines.append(next_line[2:])
                elif next_line.startswith('# '):
                    new_lines.append(next_line[2:])
                else:
                    new_lines.append(next_line)
                i += 1
            continue
        
        # Check for caddy depends_on nanobot
        if '# - nanobot' in line and 'caddy' in content.split('\n')[max(0,i-20):i]:
            new_lines.append(line.replace('# - nanobot', '    - nanobot'))
            i += 1
            continue
        
        # Check for NANOBOT_WEBCHAT_CONTAINER_PORT
        if '# - NANOBOT_WEBCHAT_CONTAINER_PORT' in line:
            new_lines.append(line.replace('# - ', '    - '))
            i += 1
            continue
        
        new_lines.append(line)
        i += 1
    
    content = '\n'.join(new_lines)

# Write back
with open('/root/se-toolkit-lab-8/docker-compose.yml', 'w') as f:
    f.write(content)

print("docker-compose.yml updated successfully")
