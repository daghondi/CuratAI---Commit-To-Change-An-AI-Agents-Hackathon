import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Create figure and axis
fig, ax = plt.subplots(1, 1, figsize=(16, 12))
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis('off')

# Title
ax.text(5, 11.5, 'CuratAI System Architecture', fontsize=24, fontweight='bold', ha='center')
ax.text(5, 11, 'Agentic AI for Artist Opportunity Curation', fontsize=14, style='italic', ha='center', color='gray')

# Color scheme
color_agent = '#FF6B6B'
color_web3 = '#4ECDC4'
color_utils = '#95E1D3'
color_opik = '#F38181'
color_data = '#AA96DA'

# ============ LAYER 1: AGENT ORCHESTRATION (Top) ============
ax.text(0.5, 10.2, 'AGENT ORCHESTRATION LAYER (Opik)', fontsize=11, fontweight='bold')

# Agent boxes
agents = [
    ('Opportunity\nScout Agent', 1.5, 9),
    ('Proposal\nDrafter Agent', 4.5, 9),
    ('Adaptive\nStrategy Agent', 7.5, 9),
]

for agent_name, x, y in agents:
    box = FancyBboxPatch((x-0.6, y-0.4), 1.2, 0.8, boxstyle='round,pad=0.1', 
                          edgecolor='black', facecolor=color_agent, linewidth=2, alpha=0.7)
    ax.add_patch(box)
    ax.text(x, y, agent_name, fontsize=9, ha='center', va='center', fontweight='bold')

# Calendar Manager
calendar_box = FancyBboxPatch((5.5, 7.5), 1.2, 0.8, boxstyle='round,pad=0.1',
                              edgecolor='black', facecolor=color_agent, linewidth=2, alpha=0.7)
ax.add_patch(calendar_box)
ax.text(6.1, 7.9, 'Calendar\nManager', fontsize=9, ha='center', va='center', fontweight='bold')

# Agent connections
for x in [1.5, 4.5, 7.5]:
    arrow = FancyArrowPatch((x, 8.6), (x, 7.8), arrowstyle='->', mutation_scale=20, 
                           linewidth=2, color='black', alpha=0.5)
    ax.add_patch(arrow)

# Opik orchestration box
opik_box = FancyBboxPatch((2, 6.8), 6, 0.6, boxstyle='round,pad=0.05',
                          edgecolor='black', facecolor=color_opik, linewidth=2, alpha=0.5)
ax.add_patch(opik_box)
ax.text(5, 7.1, 'Opik Orchestration: Metrics • Experiments • Dashboards • Monitoring', 
        fontsize=9, ha='center', va='center', fontweight='bold')

# ============ LAYER 2: WEB3 PROVENANCE LAYER ============
ax.text(0.5, 6.3, 'WEB3 PROVENANCE LAYER', fontsize=11, fontweight='bold')

web3_components = [
    ('DID\nManager', 1.5, 5.2, 'Decentralized\nIdentity'),
    ('IPFS\nProvenance', 4.5, 5.2, 'Immutable\nVersion History'),
    ('DAO\nConnector', 7.5, 5.2, 'Governance\n& Voting'),
]

for comp_name, x, y, sub_text in web3_components:
    box = FancyBboxPatch((x-0.6, y-0.4), 1.2, 0.8, boxstyle='round,pad=0.1',
                          edgecolor='black', facecolor=color_web3, linewidth=2, alpha=0.7)
    ax.add_patch(box)
    ax.text(x, y, comp_name, fontsize=9, ha='center', va='center', fontweight='bold')
    ax.text(x, y-0.8, sub_text, fontsize=8, ha='center', va='center', style='italic', color='gray')

# Connections from agents to Web3
for agent_x in [1.5, 4.5, 7.5]:
    arrow = FancyArrowPatch((agent_x, 8.6), (agent_x, 6.0), arrowstyle='<->', 
                           mutation_scale=15, linewidth=1.5, color='gray', 
                           linestyle='--', alpha=0.6)
    ax.add_patch(arrow)

# ============ LAYER 3: DATA & UTILITIES LAYER ============
ax.text(0.5, 3.8, 'DATA & UTILITIES LAYER', fontsize=11, fontweight='bold')

utilities = [
    ('Config\nManager', 1.2, 2.8),
    ('Data\nLoader', 2.8, 2.8),
    ('NLP\nTools', 4.4, 2.8),
    ('Text\nProcessor', 6.0, 2.8),
    ('Proposal\nAnalyzer', 7.6, 2.8),
]

for util_name, x, y in utilities:
    box = FancyBboxPatch((x-0.45, y-0.35), 0.9, 0.7, boxstyle='round,pad=0.05',
                          edgecolor='black', facecolor=color_utils, linewidth=1.5, alpha=0.7)
    ax.add_patch(box)
    ax.text(x, y, util_name, fontsize=8, ha='center', va='center', fontweight='bold')

# ============ LAYER 4: DATA SOURCES & STORAGE ============
ax.text(0.5, 2.1, 'DATA SOURCES & STORAGE', fontsize=11, fontweight='bold')

data_sources = [
    ('User\nProfiles', 1.5, 1.0),
    ('Opportunity\nDatabase', 3.5, 1.0),
    ('Submission\nHistory', 5.5, 1.0),
    ('Web3\nRecords', 7.5, 1.0),
]

for src_name, x, y in data_sources:
    box = FancyBboxPatch((x-0.55, y-0.35), 1.1, 0.7, boxstyle='round,pad=0.05',
                          edgecolor='black', facecolor=color_data, linewidth=1.5, alpha=0.7)
    ax.add_patch(box)
    ax.text(x, y, src_name, fontsize=8, ha='center', va='center', fontweight='bold')

# Connections from utilities to data
for util_x in [1.2, 2.8, 4.4, 6.0, 7.6]:
    arrow = FancyArrowPatch((util_x, 2.45), (util_x, 1.4), arrowstyle='<->', 
                           mutation_scale=12, linewidth=1, color='gray', alpha=0.5)
    ax.add_patch(arrow)

# ============ DATA FLOW ARROWS ============
# Main flow: Data Sources -> Utilities -> Web3 -> Agents -> Opik
main_arrow_x = 0.2
arrow1 = FancyArrowPatch((main_arrow_x, 1.4), (main_arrow_x, 2.45), arrowstyle='->', 
                        mutation_scale=20, linewidth=2.5, color='#2C3E50', alpha=0.7)
ax.add_patch(arrow1)

arrow2 = FancyArrowPatch((main_arrow_x, 3.0), (main_arrow_x, 4.8), arrowstyle='->', 
                        mutation_scale=20, linewidth=2.5, color='#2C3E50', alpha=0.7)
ax.add_patch(arrow2)

arrow3 = FancyArrowPatch((main_arrow_x, 5.4), (main_arrow_x, 6.8), arrowstyle='->', 
                        mutation_scale=20, linewidth=2.5, color='#2C3E50', alpha=0.7)
ax.add_patch(arrow3)

arrow4 = FancyArrowPatch((main_arrow_x, 7.2), (main_arrow_x, 8.2), arrowstyle='->', 
                        mutation_scale=20, linewidth=2.5, color='#2C3E50', alpha=0.7)
ax.add_patch(arrow4)

ax.text(0.05, 7.2, 'DATA\nFLOW', fontsize=9, ha='center', va='center', 
        fontweight='bold', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# ============ FEEDBACK LOOPS ============
# Opik to Agents feedback
feedback_arrow = FancyArrowPatch((9.5, 7.5), (9.5, 9.2), arrowstyle='<->', 
                                mutation_scale=20, linewidth=2, color='#E74C3C', alpha=0.7)
ax.add_patch(feedback_arrow)
ax.text(9.7, 8.4, 'Continuous\nMonitoring &\nLearning', fontsize=8, ha='left', va='center',
        color='#E74C3C', fontweight='bold')

# Strategy feedback loop
strategy_arrow = FancyArrowPatch((8.2, 4.8), (8.2, 4.2), arrowstyle='<->', 
                               mutation_scale=15, linewidth=1.5, color='#27AE60', 
                               linestyle='--', alpha=0.7)
ax.add_patch(strategy_arrow)
ax.text(8.5, 4.5, 'Outcome\nFeedback', fontsize=8, ha='left', va='center',
        color='#27AE60', fontweight='bold', style='italic')

# ============ KEY FEATURES ============
features_y = 0.3
ax.text(5, features_y, '🎯 Autonomous Agents  •  🔐 Web3 Security  •  📊 Full Observability  •  🧠 Continuous Learning', 
        fontsize=10, ha='center', va='center', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#F0F0F0', edgecolor='black', linewidth=2))

# Legend
legend_y = -0.3
ax.text(0.5, legend_y, '■ Agents', fontsize=9, ha='left', color=color_agent, fontweight='bold')
ax.text(2.5, legend_y, '■ Web3', fontsize=9, ha='left', color=color_web3, fontweight='bold')
ax.text(4.2, legend_y, '■ Utilities', fontsize=9, ha='left', color=color_utils, fontweight='bold')
ax.text(6.0, legend_y, '■ Opik', fontsize=9, ha='left', color=color_opik, fontweight='bold')
ax.text(7.8, legend_y, '■ Data', fontsize=9, ha='left', color=color_data, fontweight='bold')

plt.tight_layout()
plt.savefig('docs/ArchitectureDiagram.png', dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
print('✅ Architecture diagram created: docs/ArchitectureDiagram.png')
plt.close()
