# Utility Functions
# Common utility functions for the linked list application

def create_code_block_html(title, code, language="python"):
    """Create a styled code block with copy functionality"""
    return f"""
    <div class="code-container">
    <div class="code-header">
    <span>🔧 {title}</span>
    <button class="copy-button" onclick="navigator.clipboard.writeText(`{code.replace('`', '\\`')}`)">Copy</button>
    </div>
    <div class="code-content">
{code}
    </div>
    </div>
    """

def create_feature_card(icon, title, description, delay=0):
    """Create a feature card with animation"""
    return f"""
    <div class="feature-card" style="animation-delay: {delay}s; min-height: 120px;">
    <h4 style="margin-bottom: 0.5rem;">{icon} {title}</h4>
    <p style="font-size: 0.9em; opacity: 0.9;">{description}</p>
    </div>
    """

def create_metric_card(value, label, description=""):
    """Create a metric card for statistics"""
    desc_html = f'<div style="font-size: 0.8em; opacity: 0.7; margin-top: 0.5rem;">{description}</div>' if description else ""
    return f"""
    <div class="metric-card">
    <div class="metric-value">{value}</div>
    <div class="metric-label">{label}</div>
    {desc_html}
    </div>
    """

def create_interactive_card(title, content, border_color="#f5576c"):
    """Create an interactive card with custom styling"""
    return f"""
    <div class="interactive-card" style="border-left: 4px solid {border_color};">
    <h3 style="color: {border_color}; margin-bottom: 1rem;">{title}</h3>
    {content}
    </div>
    """

def format_complexity_table_data():
    """Return formatted complexity comparison data"""
    return {
        'Operation': [
            'Insert at Beginning',
            'Insert at End',
            'Insert at Position',
            'Delete from Beginning',
            'Delete from End',
            'Delete by Value',
            'Search by Value',
            'Traversal',
            'Access by Index'
        ],
        'Singly Linked List': [1, 'n', 'n', 1, 'n', 'n', 'n', 'n', 'n'],
        'Doubly Linked List': [1, 1, 'n', 1, 1, 'n', 'n', 'n', 'n'],
        'Circular Linked List': [1, 'n', 'n', 1, 'n', 'n', 'n', 'n', 'n'],
        'Dynamic Array': ['n', 1, 'n', 'n', 1, 'n', 'n', 'n', 1]
    }

def get_real_world_applications():
    """Return list of real-world applications for linked lists"""
    return [
        {"icon": "🎵", "title": "Music Playlists", "desc": "Songs linked in sequence for easy navigation"},
        {"icon": "🌐", "title": "Browser History", "desc": "Web pages linked for back/forward navigation"},
        {"icon": "↩️", "title": "Undo Functionality", "desc": "Operations stored as linked list in editors"},
        {"icon": "🔗", "title": "Hash Tables", "desc": "Collision resolution using separate chaining"},
        {"icon": "💾", "title": "Memory Management", "desc": "Free memory blocks tracking in OS"},
        {"icon": "📈", "title": "Polynomial Representation", "desc": "Mathematical terms linked by degree"}
    ]

def create_timeline_item(title, description):
    """Create a timeline item for learning path"""
    return f"""
    <div class="timeline-item">
    <div class="timeline-content">
    <h5>{title}</h5>
    <p>{description}</p>
    </div>
    </div>
    """

def create_memory_block_visualization(block_id, data, address, is_null=False):
    """Create memory block visualization HTML"""
    if is_null:
        return f"""
        <div style="border: 2px solid #f44336; border-radius: 10px; padding: 10px; margin: 5px; background: #ffebee;">
            <div style="font-weight: bold; color: #f44336;">NULL</div>
            <div>End of List</div>
            <div style="font-size: 0.8em; color: #666;">Address: {address}</div>
        </div>
        """
    else:
        return f"""
        <div style="border: 2px solid #1e3c72; border-radius: 10px; padding: 10px; margin: 5px; background: #e3f2fd;">
            <div style="font-weight: bold; color: #1e3c72;">Memory Block {block_id}</div>
            <div>Data: {data}</div>
            <div style="font-size: 0.8em; color: #666;">Address: {address}</div>
        </div>
        """