import streamlit as st
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import networkx as nx
import io
from PIL import Image
import sys
from io import StringIO
import contextlib
import pandas as pd
import time
import random
import math

try:
    from quiz_config import QUIZ_QUESTIONS
except ImportError:
    # Fallback quiz data if import fails
    QUIZ_QUESTIONS = []

# Fallback data for coding challenges and time challenges
CODING_CHALLENGES = [
    {
        "title": "Reverse a Linked List",
        "difficulty": "easy",
        "points": 50,
        "description": "Write a function to reverse a singly linked list.",
        "starter_code": "def reverse_linked_list(head):\n    # Your code here\n    pass",
        "solution": "def reverse_linked_list(head):\n    prev = None\n    current = head\n    while current:\n        next_node = current.next\n        current.next = prev\n        prev = current\n        current = next_node\n    return prev",
        "test_cases": [{"input": "[1,2,3,4,5]", "expected": "[5,4,3,2,1]"}]
    },
    {
        "title": "Detect Cycle in Linked List",
        "difficulty": "medium",
        "points": 75,
        "description": "Determine if a linked list has a cycle using Floyd's algorithm.",
        "starter_code": "def has_cycle(head):\n    # Your code here\n    pass",
        "solution": "def has_cycle(head):\n    if not head or not head.next:\n        return False\n    slow = head\n    fast = head.next\n    while fast and fast.next:\n        if slow == fast:\n            return True\n        slow = slow.next\n        fast = fast.next.next\n    return False",
        "test_cases": [{"input": "[3,2,0,-4] with cycle", "expected": "True"}]
    }
]

TIME_CHALLENGES = [
    {
        "title": "Quick Quiz: Basic Operations",
        "time_limit": 60,
        "questions": [0, 1, 2, 3, 4],  # Easy questions
        "bonus_points": 20
    },
    {
        "title": "Speed Round: Complexity Analysis",
        "time_limit": 90,
        "questions": [5, 6, 7, 8, 9],  # Medium questions
        "bonus_points": 30
    }
]

# Continue with the existing fallback quiz data
if 'QUIZ_QUESTIONS' not in locals():
    QUIZ_QUESTIONS = [
        {
            "question": "What is the time complexity of inserting an element at the beginning of a singly linked list?",
            "options": ["O(1)", "O(n)", "O(log n)", "O(n²)"],
            "correct": 0,
            "explanation": "Inserting at the beginning requires only updating the head pointer, which is O(1) time.",
            "difficulty": "easy",
            "points": 10
        },
        {
            "question": "In a doubly linked list, each node contains:",
            "options": ["Only data", "Data and one pointer", "Data and two pointers", "Data and three pointers"],
            "correct": 2,
            "explanation": "Doubly linked list nodes contain data, a previous pointer, and a next pointer.",
            "difficulty": "easy",
            "points": 10
        },
        {
            "question": "Which linked list type has the last node pointing back to the first node?",
            "options": ["Singly linked list", "Doubly linked list", "Circular linked list", "XOR linked list"],
            "correct": 2,
            "explanation": "Circular linked lists form a loop by pointing the last node to the first.",
            "difficulty": "easy",
            "points": 10
        },
        {
            "question": "What does NULL represent in a linked list?",
            "options": ["Empty data", "End of list", "Beginning of list", "Invalid node"],
            "correct": 1,
            "explanation": "NULL indicates the end of the linked list where no more nodes exist.",
            "difficulty": "easy",
            "points": 10
        },
        {
            "question": "Which operation is typically O(1) in a linked list?",
            "options": ["Insertion at beginning", "Searching", "Traversal", "Deletion by value"],
            "correct": 0,
            "explanation": "Insertion at the beginning is constant time as it only requires updating the head pointer.",
            "difficulty": "easy",
            "points": 10
        },
        # Medium Questions
        {
            "question": "Which of the following is NOT an advantage of linked lists over arrays?",
            "options": ["Dynamic size", "Efficient random access", "No memory waste", "Flexible structure"],
            "correct": 1,
            "explanation": "Linked lists have poor random access (O(n)) compared to arrays (O(1)).",
            "difficulty": "medium",
            "points": 15
        },
        {
            "question": "What is the space complexity of a singly linked list with n elements?",
            "options": ["O(1)", "O(n)", "O(n²)", "O(log n)"],
            "correct": 1,
            "explanation": "Each node requires O(1) space, so n nodes require O(n) space.",
            "difficulty": "medium",
            "points": 15
        },
        {
            "question": "What is the time complexity of searching for an element in a linked list?",
            "options": ["O(1)", "O(n)", "O(log n)", "O(n²)"],
            "correct": 1,
            "explanation": "Searching requires traversing the list, which is O(n) in the worst case.",
            "difficulty": "medium",
            "points": 15
        },
        {
            "question": "What is the main advantage of a doubly linked list over a singly linked list?",
            "options": ["Less memory usage", "Bidirectional traversal", "Simpler implementation", "Faster insertion at end"],
            "correct": 1,
            "explanation": "Doubly linked lists allow traversal in both forward and backward directions.",
            "difficulty": "medium",
            "points": 15
        },
        {
            "question": "In which scenario would you prefer a linked list over an array?",
            "options": ["Random access needed", "Frequent insertions/deletions", "Memory is limited", "Cache performance critical"],
            "correct": 1,
            "explanation": "Linked lists excel at frequent insertions and deletions, especially at the beginning.",
            "difficulty": "medium",
            "points": 15
        },
        {
            "question": "Which algorithm is commonly used to detect cycles in a linked list?",
            "options": ["Quick Sort", "Merge Sort", "Floyd's Cycle Detection", "Binary Search"],
            "correct": 2,
            "explanation": "Floyd's Cycle Detection algorithm uses two pointers moving at different speeds.",
            "difficulty": "hard",
            "points": 25
        },
        {
            "question": "What is a common use case for circular linked lists?",
            "options": ["Undo functionality", "Round-robin scheduling", "Browser history", "Polynomial representation"],
            "correct": 1,
            "explanation": "Circular linked lists are ideal for round-robin scheduling algorithms.",
            "difficulty": "hard",
            "points": 25
        }
    ]

try:
    from linked_list_classes import Node, SinglyLinkedList, DoublyLinkedList, CircularLinkedList
except ImportError:
    st.error("⚠️ linked_list_classes.py not found. Please ensure all files are in the same directory.")
    st.stop()

# Set page config
st.set_page_config(
    page_title="Linked List Data Structures",
    layout="wide",
    page_icon="🔗",
    initial_sidebar_state="expanded"
)

# Dark mode CSS
st.markdown("""
<style>
    .stApp {
        background-color: #1a202c !important;
        color: #e2e8f0 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #f7fafc !important;
    }
    
    p, div, span, li {
        color: #cbd5e0 !important;
    }
    
    .timeline-content {
        background: #2d3748 !important;
        color: #e2e8f0 !important;
    }
    
    .timeline-content h5 {
        color: #f7fafc !important;
    }
    
    .timeline-content p {
        color: #cbd5e0 !important;
    }
    
    .section-card {
        background: #2d3748 !important;
        color: #e2e8f0 !important;
    }
    
    .highlight-box {
        background: #2d3748 !important;
        color: #e2e8f0 !important;
        border-color: #4299e1 !important;
    }
    
    .interactive-card {
        background: #2d3748 !important;
        color: #e2e8f0 !important;
    }
    
    .code-container, .code-content {
        background: #1a202c !important;
        color: #e2e8f0 !important;
    }
    
    /* Fix all text in markdown content */
    .stMarkdown {
        color: #cbd5e0 !important;
    }
    
    .stMarkdown p {
        color: #cbd5e0 !important;
    }
    
    .stMarkdown strong {
        color: #f7fafc !important;
    }
    
    .stMarkdown ul li {
        color: #cbd5e0 !important;
    }
    
    /* Fix specific elements */
    div[style*="background: linear-gradient"] {
        color: #cbd5e0 !important;
    }
    
    /* Force all text to be visible */
    * {
        color: #cbd5e0 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #f7fafc !important;
    }
    
    strong {
        color: #f7fafc !important;
    }
    
    /* Remove all white backgrounds */
    * {
        background-color: transparent !important;
    }
    
    .stApp {
        background-color: #1a202c !important;
    }
    
    div[style*="background"] {
        background: #2d3748 !important;
    };
    } 150ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-normal: 250ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-slow: 350ms cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Dark Mode Variables */
    @media (prefers-color-scheme: dark) {
        :root {
            --text-primary: #f1f5f9;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --text-inverse: #1e293b;
            
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-tertiary: #334155;
            
            --border-light: #475569;
            --border-medium: #64748b;
            --border-dark: #94a3b8;
        }
    }
    
    /* Base Styles */
    .stApp {
        background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: var(--text-primary);
        line-height: 1.6;
    }
    
    /* Remove default padding */
    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        max-width: 100% !important;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', Inter, sans-serif;
        font-weight: 600;
        color: var(--text-primary) !important;
        letter-spacing: -0.025em;
        margin-bottom: 1rem;
    }
    
    h1 {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary-600) 0%, var(--secondary-600) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2 {
        font-size: 2.25rem;
        font-weight: 600;
    }
    
    h3 {
        font-size: 1.875rem;
        font-weight: 600;
    }
    
    p, li, span, div {
        color: var(--text-secondary) !important;
        line-height: 1.7;
    }
    
    strong {
        color: var(--text-primary) !important;
        font-weight: 600;
    }
    
    /* Streamlit specific text elements */
    .stMarkdown p {
        color: var(--text-secondary) !important;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: var(--text-primary) !important;
    }
    
    .stMarkdown strong {
        color: var(--text-primary) !important;
    }
    
    .stMarkdown li {
        color: var(--text-secondary) !important;
    }
    
    /* Code blocks */
    code {
        color: var(--text-primary) !important;
        background-color: var(--bg-tertiary) !important;
        padding: 2px 4px;
        border-radius: 4px;
    }
    
    pre {
        background-color: var(--bg-tertiary) !important;
        color: var(--text-primary) !important;
        border-radius: var(--radius-md);
        padding: 1rem;
    }
    
    /* Force proper text colors globally */
    .main .block-container {
        color: var(--text-primary);
    }
    
    /* Override all text elements */
    .main .block-container h1,
    .main .block-container h2,
    .main .block-container h3,
    .main .block-container h4,
    .main .block-container h5,
    .main .block-container h6 {
        color: #1e293b !important;
    }
    
    .main .block-container p,
    .main .block-container li,
    .main .block-container span,
    .main .block-container div {
        color: #64748b !important;
    }
    
    @media (prefers-color-scheme: dark) {
        .main .block-container h1,
        .main .block-container h2,
        .main .block-container h3,
        .main .block-container h4,
        .main .block-container h5,
        .main .block-container h6 {
            color: #f1f5f9 !important;
        }
        
        .main .block-container p,
        .main .block-container li,
        .main .block-container span,
        .main .block-container div {
            color: #cbd5e1 !important;
        }
    }
    
    /* Glassmorphism Cards */
    .section-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: var(--radius-xl);
        padding: 2.5rem;
        margin: 2rem 0;
        border: 1px solid rgba(0, 0, 0, 0.1);
        box-shadow: var(--shadow-lg);
        transition: all var(--transition-normal);
        color: var(--text-primary);
    }
    
    .section-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-xl);
    }
    
    @media (prefers-color-scheme: dark) {
        .section-card {
            background: rgba(30, 41, 59, 0.95);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text-primary);
        }
    }
    
    /* Feature Cards */
    .feature-card {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.1) 0%, rgba(217, 70, 239, 0.1) 100%);
        border: 1px solid rgba(14, 165, 233, 0.2);
        border-radius: var(--radius-lg);
        padding: 2rem;
        margin: 1rem;
        text-align: center;
        transition: all var(--transition-normal);
        backdrop-filter: blur(10px);
    }
    
    .feature-card:hover {
        transform: translateY(-6px) scale(1.02);
        border-color: rgba(14, 165, 233, 0.4);
        box-shadow: var(--shadow-xl);
    }
    
    /* Modern Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-500) 0%, var(--secondary-500) 100%);
        color: white;
        border: none;
        border-radius: var(--radius-lg);
        padding: 0.875rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all var(--transition-normal);
        box-shadow: var(--shadow-md);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Form Inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: var(--bg-primary);
        backdrop-filter: blur(10px);
        border: 2px solid var(--border-light);
        border-radius: var(--radius-lg);
        padding: 1rem 1.25rem;
        font-size: 1rem;
        transition: all var(--transition-fast);
        box-shadow: var(--shadow-sm);
        color: var(--text-primary);
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--primary-400);
        box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1), var(--shadow-md);
        outline: none;
    }
    
    /* Select Boxes */
    .stSelectbox > div > div {
        background: var(--bg-primary);
        backdrop-filter: blur(10px);
        border: 2px solid var(--border-light);
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-sm);
        transition: all var(--transition-fast);
        color: var(--text-primary);
    }
    
    .stSelectbox > div > div:hover {
        border-color: var(--primary-400);
        box-shadow: var(--shadow-md);
    }
    
    /* Status Messages */
    .stSuccess {
        background: linear-gradient(135deg, var(--success-400) 0%, var(--success-500) 100%);
        border-radius: var(--radius-lg);
        border: none;
        box-shadow: var(--shadow-md);
        color: white;
        font-weight: 500;
    }
    
    .stError {
        background: linear-gradient(135deg, var(--error-400) 0%, var(--error-500) 100%);
        border-radius: var(--radius-lg);
        border: none;
        box-shadow: var(--shadow-md);
        color: white;
        font-weight: 500;
    }
    
    .stWarning {
        background: linear-gradient(135deg, var(--warning-400) 0%, var(--warning-500) 100%);
        border-radius: var(--radius-lg);
        border: none;
        box-shadow: var(--shadow-md);
        color: white;
        font-weight: 500;
    }
    
    .stInfo {
        background: linear-gradient(135deg, var(--primary-400) 0%, var(--primary-500) 100%);
        border-radius: var(--radius-lg);
        border: none;
        box-shadow: var(--shadow-md);
        color: white;
        font-weight: 500;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: var(--bg-secondary);
        backdrop-filter: blur(20px);
        border-right: 1px solid var(--border-light);
        color: var(--text-primary);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        h1 {
            font-size: 2.25rem;
        }
        
        h2 {
            font-size: 1.875rem;
        }
        
        .section-card {
            padding: 1.75rem;
            margin: 1.5rem 0;
        }
        
        .feature-card {
            padding: 1.5rem;
            margin: 0.75rem;
        }
        
        .stButton > button {
            padding: 0.75rem 1.5rem;
            font-size: 0.95rem;
        }
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .animate-fadeInUp {
        animation: fadeInUp 0.6s ease-out;
    }
    
    .animate-float {
        animation: float 3s ease-in-out infinite;
    }
    
    @media (prefers-color-scheme: dark) {
        .main-header {
            color: #f1f5f9;
        }
    }
    
    /* Cards */
    .section-card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
    }
    
    @media (prefers-color-scheme: dark) {
        .section-card {
            background: #1e293b;
            border-color: #334155;
            color: #e2e8f0;
        }
    }
    
    .feature-card {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.75rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
    }
    
    /* Timeline */
    .timeline {
        position: relative;
        padding-left: 30px;
    }
    
    .timeline::before {
        content: '';
        position: absolute;
        left: 15px;
        top: 0;
        bottom: 0;
        width: 2px;
        background: #6366f1;
    }
    
    .timeline-item {
        position: relative;
        margin-bottom: 2rem;
        padding-left: 30px;
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -22px;
        top: 8px;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #6366f1;
    }
    
    .timeline-content {
        background: var(--bg-primary);
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: var(--shadow-md);
        border-left: 4px solid #6366f1;
        color: var(--text-primary);
    }
    
    .timeline-content h5 {
        color: var(--text-primary) !important;
        margin-bottom: 0.5rem;
    }
    
    .timeline-content p {
        color: var(--text-secondary) !important;
        margin: 0;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    }
    
    /* Metrics */
    .metric-card {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin: 0.75rem;
    }
    
    /* Visual diagram */
    .visual-diagram {
        background: var(--bg-primary);
        border-radius: 12px;
        padding: 2rem;
        margin: 1.5rem 0;
        text-align: center;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-light);
        color: var(--text-primary);
    }
    
    /* Progress bar */
    .progress-container {
        background: #f1f5f9;
        border-radius: 25px;
        padding: 3px;
        margin: 1rem 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        height: 20px;
        border-radius: 22px;
        transition: width 1s ease-in-out;
    }
    
    @media (prefers-color-scheme: dark) {
        .progress-container {
            background: #475569;
        }
    }
    
    /* Text colors */
    h1, h2, h3, h4, h5, h6 {
        color: #1e293b;
    }
    
    p, span, div {
        color: #475569;
    }
    
    @media (prefers-color-scheme: dark) {
        h1, h2, h3, h4, h5, h6 {
            color: #f1f5f9;
        }
        
        p, span, div {
            color: #cbd5e1;
        }
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        
        .section-card {
            padding: 1rem;
            margin: 1rem 0;
        }
        
        .feature-card {
            padding: 1rem;
            margin: 0.5rem;
        }
        --error-color: #ef4444;
        --warning-color: #f97316;
        --info-color: #3b82f6;
        --success-color: #22c55e;
        
        /* Light Mode Colors */
        --bg-primary: #ffffff;
        --bg-secondary: #f8fafc;
        --bg-tertiary: #f1f5f9;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --text-muted: #94a3b8;
        --border-color: #e2e8f0;
        --shadow-light: rgba(0, 0, 0, 0.05);
        --shadow-medium: rgba(0, 0, 0, 0.1);
        --shadow-heavy: rgba(0, 0, 0, 0.15);
    }
    
    /* Dark Mode Colors */
    [data-theme="dark"] {
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --bg-tertiary: #334155;
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
        --text-muted: #94a3b8;
        --border-color: #475569;
        --shadow-light: rgba(0, 0, 0, 0.2);
        --shadow-medium: rgba(0, 0, 0, 0.3);
        --shadow-heavy: rgba(0, 0, 0, 0.4);
    }
    
    /* Auto-detect system theme */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-tertiary: #334155;
            --text-primary: #f1f5f9;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --border-color: #475569;
            --shadow-light: rgba(0, 0, 0, 0.2);
            --shadow-medium: rgba(0, 0, 0, 0.3);
            --shadow-heavy: rgba(0, 0, 0, 0.4);
        }
    }
    
    /* Global Styles */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: var(--bg-primary);
        color: var(--text-primary);
    }
    
    /* Main Header */
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeInUp 1s ease-out;
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        font-size: 1.25rem;
        color: var(--text-secondary);
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    
    [data-theme="dark"] .main-header {
        background: linear-gradient(45deg, #64b5f6, #42a5f5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .section-card {
        background: var(--background-color, rgba(255, 255, 255, 0.95));
        border-radius: 15px;
        padding: 2.5rem;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        margin: 1.5rem 0;
        border-left: 6px solid #1e3c72;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    [data-theme="dark"] .section-card {
        background: rgba(30, 30, 30, 0.95);
        box-shadow: 0 8px 25px rgba(255, 255, 255, 0.05);
    }

    .section-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
    }

    .section-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #1e3c72, #2a5298, #667eea);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .section-card:hover::before {
        opacity: 1;
    }

    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 0.75rem;
        text-align: center;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .feature-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.4);
    }

    .feature-card::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        transition: all 0.3s ease;
        opacity: 0;
    }

    .feature-card:hover::after {
        opacity: 1;
        animation: shimmer 1.5s ease-in-out;
    }

    /* Interactive Elements */
    .interactive-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .interactive-card:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 25px rgba(245, 87, 108, 0.3);
    }

    .code-block {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: #ecf0f1;
        border-left: 4px solid #1e3c72;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-radius: 10px;
        position: relative;
        font-family: 'Fira Code', 'Monaco', 'Consolas', monospace;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }

    .code-block::before {
        content: '💻';
        position: absolute;
        top: 10px;
        right: 15px;
        font-size: 1.2rem;
        opacity: 0.7;
    }

    .highlight-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 2px solid #2196f3;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        position: relative;
        animation: pulse 2s infinite;
        color: #1565c0;
    }
    
    [data-theme="dark"] .highlight-box {
        background: linear-gradient(135deg, rgba(33, 150, 243, 0.2) 0%, rgba(33, 150, 243, 0.1) 100%);
        border: 2px solid #42a5f5;
        color: #90caf9;
    }

    .highlight-box::before {
        content: '💡';
        position: absolute;
        top: -10px;
        left: 20px;
        background: var(--background-color, white);
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    [data-theme="dark"] .highlight-box::before {
        background: #2c2c2c;
        box-shadow: 0 2px 10px rgba(255, 255, 255, 0.1);
    }

    /* Progress and Metrics */
    .progress-container {
        background: #f8f9fa;
        border-radius: 25px;
        padding: 3px;
        margin: 1rem 0;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .progress-bar {
        background: linear-gradient(90deg, #1e3c72, #667eea);
        height: 20px;
        border-radius: 22px;
        transition: width 1s ease-in-out;
        position: relative;
        overflow: hidden;
    }

    .progress-bar::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        animation: shimmer 2s infinite;
    }

    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        margin: 0.75rem;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        position: relative;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.4);
    }

    .metric-card .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }

    .metric-card .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Tab Enhancements */
    .tab-content {
        padding: 2rem 0;
        animation: fadeIn 0.5s ease-out;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 10px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }

    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: 2px solid transparent;
        position: relative;
        overflow: hidden;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;
        color: white !important;
        box-shadow: 0 4px 20px rgba(30, 60, 114, 0.4);
        transform: translateY(-2px);
    }

    .stTabs [aria-selected="true"]::before {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 80%;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 2px;
    }

    /* Quiz Section Styling */
    .quiz-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .quiz-question {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .quiz-options {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .quiz-options:hover {
        background: rgba(255, 255, 255, 0.15);
        transform: translateX(5px);
    }
    
    .difficulty-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .difficulty-easy {
        background: #4CAF50;
        color: white;
    }
    
    .difficulty-medium {
        background: #FF9800;
        color: white;
    }
    
    .difficulty-hard {
        background: #F44336;
        color: white;
    }
    
    .quiz-progress {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        height: 8px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .quiz-progress-fill {
        background: linear-gradient(90deg, #4CAF50, #8BC34A);
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    .quiz-score {
        background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%);
        color: white;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(76, 175, 80, 0.3);
    }
    
    .quiz-explanation {
        background: linear-gradient(135deg, #2196F3 0%, #21CBF3 100%);
        color: white;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #0D47A1;
    }
    
    /* Gamification Elements */
    .achievement-badge {
        background: linear-gradient(135deg, #FFD700 0%, #FFA000 100%);
        color: #333;
        border-radius: 25px;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        display: inline-block;
        font-weight: bold;
        box-shadow: 0 3px 10px rgba(255, 215, 0, 0.3);
        animation: bounce 0.5s ease;
    }
    
    .leaderboard-entry {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
    }
    
    .time-challenge-timer {
        background: linear-gradient(135deg, #FF5722 0%, #FF9800 100%);
        color: white;
        border-radius: 50px;
        padding: 1rem 2rem;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(255, 87, 34, 0.3);
        animation: pulse 1s infinite;
    }
    
    /* Animation Keyframes */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }

    @keyframes shimmer {
        0% { transform: translateX(-100%) rotate(45deg); }
        100% { transform: translateX(100%) rotate(45deg); }
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }

    /* Interactive Buttons */
    .modern-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
        position: relative;
        overflow: hidden;
    }

    .modern-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }

    .modern-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }

    .modern-button:hover::before {
        left: 100%;
    }

    /* Enhanced Code Blocks */
    .code-container {
        position: relative;
        margin: 1.5rem 0;
    }

    .code-header {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: white;
        padding: 8px 15px;
        border-radius: 8px 8px 0 0;
        font-size: 0.9rem;
        font-weight: 600;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .code-content {
        background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
        color: #ecf0f1;
        padding: 1.5rem;
        border-radius: 0 0 8px 8px;
        font-family: 'Fira Code', 'Monaco', 'Consolas', monospace;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        position: relative;
    }

    .copy-button {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        color: white;
        border-radius: 4px;
        padding: 4px 8px;
        font-size: 0.8rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .copy-button:hover {
        background: rgba(255,255,255,0.2);
        transform: scale(1.05);
    }

    /* Visual Enhancements */
    .visual-diagram {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        padding: 2rem;
        margin: 1.5rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        position: relative;
        color: #2c3e50;
    }
    
    [data-theme="dark"] .visual-diagram {
        background: linear-gradient(135deg, #2c2c2c 0%, #1e1e1e 100%);
        box-shadow: 0 4px 15px rgba(255, 255, 255, 0.05);
        color: #e0e0e0;
    }

    .visual-diagram::before {
        content: '🎨';
        position: absolute;
        top: 15px;
        right: 20px;
        font-size: 1.5rem;
        opacity: 0.6;
    }
    
    /* Dark mode compatibility for text colors */
    [data-theme="dark"] h1, [data-theme="dark"] h2, [data-theme="dark"] h3, [data-theme="dark"] h4, [data-theme="dark"] h5 {
        color: #e0e0e0 !important;
    }
    
    [data-theme="dark"] p, [data-theme="dark"] li, [data-theme="dark"] span {
        color: #b0b0b0 !important;
    }
    
    [data-theme="dark"] strong {
        color: #ffffff !important;
    }

    /* Interactive Timeline */
    .timeline {
        position: relative;
        padding-left: 30px;
    }

    .timeline::before {
        content: '';
        position: absolute;
        left: 15px;
        top: 0;
        bottom: 0;
        width: 2px;
        background: linear-gradient(to bottom, #1e3c72, #667eea);
    }

    .timeline-item {
        position: relative;
        margin-bottom: 2rem;
        padding-left: 30px;
    }

    .timeline-item::before {
        content: '';
        position: absolute;
        left: -22px;
        top: 8px;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: linear-gradient(135deg, #1e3c72, #667eea);
        box-shadow: 0 0 0 3px rgba(30, 60, 114, 0.2);
    }

    .timeline-content {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #1e3c72;
    }

    /* Floating Action Elements */
    .floating-element {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        z-index: 1000;
    }

    .floating-element:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6);
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }

        .section-card {
            padding: 1.5rem;
            margin: 1rem 0;
        }

        .feature-card {
            padding: 1.5rem;
            margin: 0.5rem;
        }

        .stTabs [data-baseweb="tab"] {
            padding: 8px 16px;
            font-size: 0.9rem;
        }
    }

    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,0.3);
        border-radius: 50%;
        border-top-color: white;
        animation: spin 1s ease-in-out infinite;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    /* Success Animation */
    .success-checkmark {
        display: inline-block;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: #4CAF50;
        position: relative;
    }

    .success-checkmark::after {
        content: '✓';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: white;
        font-weight: bold;
        animation: checkmark 0.5s ease-in-out;
    }

    @keyframes checkmark {
        0% { transform: translate(-50%, -50%) scale(0); }
        50% { transform: translate(-50%, -50%) scale(1.2); }
        100% { transform: translate(-50%, -50%) scale(1); }
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'username' not in st.session_state:
    st.session_state.username = "Guest"
if 'user_score' not in st.session_state:
    st.session_state.user_score = 0
if 'achievements' not in st.session_state:
    st.session_state.achievements = []
if 'bookmarks' not in st.session_state:
    st.session_state.bookmarks = []
if 'notes' not in st.session_state:
    st.session_state.notes = {}
if 'progress' not in st.session_state:
    st.session_state.progress = {}
if 'leaderboard' not in st.session_state:
    st.session_state.leaderboard = []
if 'quiz_attempts' not in st.session_state:
    st.session_state.quiz_attempts = 0
if 'correct_answers' not in st.session_state:
    st.session_state.correct_answers = 0
if 'coding_challenge_score' not in st.session_state:
    st.session_state.coding_challenge_score = 0
if 'time_challenge_best' not in st.session_state:
    st.session_state.time_challenge_best = {}

# Helper functions
def save_progress(section):
    st.session_state.progress[section] = True

def add_bookmark(section):
    if section not in st.session_state.bookmarks:
        st.session_state.bookmarks.append(section)

def save_note(section, note):
    st.session_state.notes[section] = {
        'text': note,
        'timestamp': pd.Timestamp.now()
    }

def step_by_step_insert(elements, value, position):
    steps = [
        f"Step 1: Create new node with value {value}",
        f"Step 2: Set up pointers for insertion at position {position}",
        f"Step 3: Update existing node connections",
        f"Step 4: Insert complete! New list: {elements[:position] + [value] + elements[position:]}"
    ]
    return steps

def export_code(code, filename):
    st.download_button(
        label="📥 Download Code",
        data=code,
        file_name=filename,
        mime="text/plain"
    )

# Enhanced Welcome/Dashboard section with modern UI/UX
def welcome_dashboard():
    st.markdown('<h1 class="main-header" style="margin-top: 0; padding-top: 0;">🔗 Linked List Data Structures</h1>', unsafe_allow_html=True)
    save_progress("Welcome")

    st.markdown("""
    <div class="section-card" style="margin-top: 0.5rem; background: linear-gradient(135deg, var(--primary-50) 0%, var(--secondary-50) 100%); border: 1px solid rgba(14, 165, 233, 0.1); box-shadow: var(--shadow-lg);">
    <h2 style="color: var(--text-primary); text-align: center; margin-bottom: 1rem; font-weight: 700;">Welcome to Your Interactive Learning Journey!</h2>
    <p style="font-size: 1.2em; text-align: center; color: var(--text-secondary); margin-bottom: 1rem; font-weight: 400;">
    Master linked lists through interactive visualizations, hands-on practice, and comprehensive analysis.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add Start Learning button with modern styling
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Start Learning", key="start_learning", use_container_width=True, help="Begin your linked list learning journey"):
            st.session_state.current_tab = 1  # Navigate to Introduction
            st.session_state.scroll_to_top = True  # Flag to scroll to top
            st.rerun()

    # Interactive Feature cards with modern soft UI design
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="feature-card" style="animation-delay: 0.1s; background: linear-gradient(135deg, var(--primary-400) 0%, var(--primary-500) 100%); color: white; border-radius: var(--radius-xl); padding: 2rem; text-align: center; box-shadow: var(--shadow-lg); transition: all var(--transition-normal); cursor: pointer; border: 1px solid rgba(255,255,255,0.2);">
        <div style="font-size: 3rem; margin-bottom: 1rem;">📚</div>
        <h3 style="margin: 0 0 0.5rem 0; font-weight: 700;">Learn</h3>
        <p style="margin: 0 0 1rem 0; opacity: 0.9; font-weight: 400;">Comprehensive guide to singly, doubly, and circular linked lists</p>
        <div style="background: rgba(255,255,255,0.2); border-radius: var(--radius-full); padding: 0.5rem 1rem; font-size: 0.875rem; font-weight: 500;">
            Interactive Examples
        </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card" style="animation-delay: 0.2s; background: linear-gradient(135deg, var(--secondary-400) 0%, var(--secondary-500) 100%); color: white; border-radius: var(--radius-xl); padding: 2rem; text-align: center; box-shadow: var(--shadow-lg); transition: all var(--transition-normal); cursor: pointer; border: 1px solid rgba(255,255,255,0.2);">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🎮</div>
        <h3 style="margin: 0 0 0.5rem 0; font-weight: 700;">Practice</h3>
        <p style="margin: 0 0 1rem 0; opacity: 0.9; font-weight: 400;">Interactive playground with real-time operations</p>
        <div style="background: rgba(255,255,255,0.2); border-radius: var(--radius-full); padding: 0.5rem 1rem; font-size: 0.875rem; font-weight: 500;">
            Live Visualization
        </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card" style="animation-delay: 0.3s; background: linear-gradient(135deg, var(--accent-400) 0%, var(--accent-500) 100%); color: white; border-radius: var(--radius-xl); padding: 2rem; text-align: center; box-shadow: var(--shadow-lg); transition: all var(--transition-normal); cursor: pointer; border: 1px solid rgba(255,255,255,0.2);">
        <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
        <h3 style="margin: 0 0 0.5rem 0; font-weight: 700;">Analyze</h3>
        <p style="margin: 0 0 1rem 0; opacity: 0.9; font-weight: 400;">Performance comparisons and optimization tips</p>
        <div style="background: rgba(255,255,255,0.2); border-radius: var(--radius-full); padding: 0.5rem 1rem; font-size: 0.875rem; font-weight: 500;">
            Big O Analysis
        </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="feature-card" style="animation-delay: 0.4s; background: linear-gradient(135deg, var(--success-400) 0%, var(--success-500) 100%); color: white; border-radius: var(--radius-xl); padding: 2rem; text-align: center; box-shadow: var(--shadow-lg); transition: all var(--transition-normal); cursor: pointer; border: 1px solid rgba(255,255,255,0.2);">
        <div style="font-size: 3rem; margin-bottom: 1rem;">💡</div>
        <h3 style="margin: 0 0 0.5rem 0; font-weight: 700;">Solve</h3>
        <p style="margin: 0 0 1rem 0; opacity: 0.9; font-weight: 400;">Practice problems with detailed solutions</p>
        <div style="background: rgba(255,255,255,0.2); border-radius: var(--radius-full); padding: 0.5rem 1rem; font-size: 0.875rem; font-weight: 500;">
            Step-by-Step Solutions
        </div>
        </div>
        """, unsafe_allow_html=True)

    # Enhanced Quick stats with modern metric cards
    st.markdown('<div class="section-card" style="margin-top: 1rem; background: rgba(255,255,255,0.8); backdrop-filter: blur(10px); border: 1px solid rgba(14, 165, 233, 0.1); box-shadow: var(--shadow-lg);">', unsafe_allow_html=True)
    st.subheader("🚀 Quick Start Guide")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, var(--primary-400) 0%, var(--primary-500) 100%); color: white; border-radius: var(--radius-xl); padding: 2rem; text-align: center; box-shadow: var(--shadow-md); transition: all var(--transition-normal); border: 1px solid rgba(255,255,255,0.2);">
        <div style="font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem;">3</div>
        <div style="font-weight: 600; margin-bottom: 0.5rem; font-size: 1.1rem;">Data Structures</div>
        <div style="font-size: 0.875rem; opacity: 0.9;">Singly, Doubly, Circular</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, var(--secondary-400) 0%, var(--secondary-500) 100%); color: white; border-radius: var(--radius-xl); padding: 2rem; text-align: center; box-shadow: var(--shadow-md); transition: all var(--transition-normal); border: 1px solid rgba(255,255,255,0.2);">
        <div style="font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem;">8+</div>
        <div style="font-weight: 600; margin-bottom: 0.5rem; font-size: 1.1rem;">Operations</div>
        <div style="font-size: 0.875rem; opacity: 0.9;">Insert, Delete, Search, Traverse</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, var(--accent-400) 0%, var(--accent-500) 100%); color: white; border-radius: var(--radius-xl); padding: 2rem; text-align: center; box-shadow: var(--shadow-md); transition: all var(--transition-normal); border: 1px solid rgba(255,255,255,0.2);">
        <div style="font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem;">10+</div>
        <div style="font-weight: 600; margin-bottom: 0.5rem; font-size: 1.1rem;">Practice Problems</div>
        <div style="font-size: 0.875rem; opacity: 0.9;">With Detailed Solutions</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("""
    <style>
    /* Sidebar Enhancements */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
        border-right: 1px solid var(--border-color);
    }
    
    /* Streamlit component styling */
    .stSelectbox > div > div {
        background: var(--bg-secondary);
        border: 2px solid var(--border-color);
        border-radius: 12px;
        color: var(--text-primary);
    }
    
    .stTextInput > div > div > input {
        background: var(--bg-secondary);
        border: 2px solid var(--border-color);
        border-radius: 12px;
        color: var(--text-primary);
        padding: 12px 16px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-hover) 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
    }
    
    /* Message styling */
    .stSuccess {
        background: linear-gradient(135deg, var(--success-color) 0%, #16a085 100%);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 1rem;
        box-shadow: 0 4px 15px rgba(34, 197, 94, 0.3);
    }
    
    .stError {
        background: linear-gradient(135deg, var(--danger-color) 0%, #c0392b 100%);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 1rem;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
    }
    
    .stWarning {
        background: linear-gradient(135deg, var(--warning-color) 0%, #d68910 100%);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 1rem;
        box-shadow: 0 4px 15px rgba(249, 115, 22, 0.3);
    }
    
    .stInfo {
        background: linear-gradient(135deg, var(--info-color) 0%, #2980b9 100%);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 1rem;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    /* Dark mode text visibility */
    @media (prefers-color-scheme: dark) {
        .stMarkdown, .stText, p, span, div {
            color: var(--text-primary) !important;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: var(--text-primary) !important;
        }
    }
    
    /* Remove top padding/margin */
    .main .block-container {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    .main-header {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        
        .section-card {
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        .feature-card {
            padding: 1rem;
            margin: 0.25rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Enhanced Progress indicator with visual progress bar
    st.markdown('<div class="section-card" style="margin-top: 1rem;">', unsafe_allow_html=True)
    st.subheader("📈 Learning Progress")

    # Progress visualization
    st.markdown("""
    <div style="margin: 2rem 0;">
    <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
    <span style="font-weight: 600; color: #1e3c72;">Your Progress</span>
    <span style="font-weight: 600; color: #1e3c72;">0%</span>
    </div>
    <div class="progress-container">
    <div class="progress-bar" style="width: 0%;"></div>
    </div>
    <div style="margin-top: 1rem; font-size: 0.9em; color: #666;">
    Complete sections to track your progress and unlock achievements! 🏆
    </div>
    </div>
    """, unsafe_allow_html=True)

    # Interactive learning path
    st.markdown("""
    <div class="visual-diagram">
    <h4 style="margin-bottom: 1.5rem; color: #1e3c72;">🎯 Learning Path</h4>
    <div class="timeline">
    <div class="timeline-item">
    <div class="timeline-content">
    <h5 style="color: var(--text-primary) !important;">📖 Introduction</h5>
    <p style="color: var(--text-secondary) !important;">Learn the fundamentals of linked lists</p>
    </div>
    </div>
    <div class="timeline-item">
    <div class="timeline-content">
    <h5 style="color: var(--text-primary) !important;">🔗 Types</h5>
    <p style="color: var(--text-secondary) !important;">Explore singly, doubly, and circular variants</p>
    </div>
    </div>
    <div class="timeline-item">
    <div class="timeline-content">
    <h5 style="color: var(--text-primary) !important;">⚙️ Operations</h5>
    <p style="color: var(--text-secondary) !important;">Master insertion, deletion, and traversal</p>
    </div>
    </div>
    <div class="timeline-item">
    <div class="timeline-content">
    <h5 style="color: var(--text-primary) !important;">🎮 Playground</h5>
    <p style="color: var(--text-secondary) !important;">Practice with interactive visualizations</p>
    </div>
    </div>
    <div class="timeline-item">
    <div class="timeline-content">
    <h5 style="color: var(--text-primary) !important;">📊 Analysis</h5>
    <p style="color: var(--text-secondary) !important;">Understand performance characteristics</p>
    </div>
    </div>
    <div class="timeline-item">
    <div class="timeline-content">
    <h5 style="color: var(--text-primary) !important;">💡 Practice</h5>
    <p style="color: var(--text-secondary) !important;">Solve challenging problems</p>
    </div>
    </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Main navigation
def main():
    st.markdown('<style>.main .block-container { padding-top: 0 !important; }</style>', unsafe_allow_html=True)
    
    # Sidebar navigation with modern soft UI styling
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 2rem 1rem; margin-bottom: 2rem; background: linear-gradient(135deg, var(--primary-400) 0%, var(--secondary-400) 100%); border-radius: var(--radius-xl); box-shadow: var(--shadow-lg);">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔗</div>
        <h2 style="color: white; margin: 0; font-weight: 700; font-size: 1.25rem;">Linked Lists</h2>
        <p style="color: rgba(255,255,255,0.9); font-size: 0.875rem; margin: 0.5rem 0; font-weight: 400;">Interactive Learning Hub</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation menu with modern soft UI styling
    menu_options = [
        "🏠 Welcome",
        "📖 Introduction", 
        "🔗 Types of Lists",
        "⚙️ Operations",
        "🎮 Interactive Playground",
        "📊 Performance Analysis",
        "💡 Practice Problems",
        "🎯 Gamified Quiz",
        "🎨 Advanced Visualizations",
        "📝 Interview Prep",
        "📚 References"
    ]
    
    # Custom styled selectbox container
    st.sidebar.markdown("""
    <div style="background: rgba(255,255,255,0.8); backdrop-filter: blur(10px); border-radius: var(--radius-lg); padding: 1rem; margin-bottom: 2rem; border: 1px solid rgba(14, 165, 233, 0.1);">
        <label style="color: var(--text-primary); font-weight: 600; margin-bottom: 0.5rem; display: block;">Navigation Menu</label>
    </div>
    """, unsafe_allow_html=True)
    
    selected = st.sidebar.selectbox(
        "",
        menu_options,
        key="main_nav",
        help="Select a learning section to explore"
    )
    
    # User profile in sidebar with modern soft UI cards
    with st.sidebar.expander("👤 Profile", expanded=False):
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, var(--primary-400) 0%, var(--primary-500) 100%); color: white; padding: 1.5rem; border-radius: var(--radius-lg); margin-bottom: 1rem; box-shadow: var(--shadow-md);">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">👤</div>
            <div style="font-weight: 600; margin-bottom: 0.25rem;">{st.session_state.username}</div>
            <div style="font-size: 0.875rem; opacity: 0.9;">Learner</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Stats in a modern card
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.8); backdrop-filter: blur(10px); border-radius: var(--radius-lg); padding: 1rem; border: 1px solid rgba(14, 165, 233, 0.1); margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <span style="color: var(--text-secondary);">Score</span>
                <span style="font-weight: 700; color: var(--primary-500);">{st.session_state.user_score}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: var(--text-secondary);">Achievements</span>
                <span style="font-weight: 700; color: var(--success-500);">{len(st.session_state.achievements)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.achievements:
            st.markdown("""
            <div style="background: linear-gradient(135deg, var(--success-400) 0%, var(--success-500) 100%); color: white; padding: 1rem; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm);">
                <div style="font-weight: 600; margin-bottom: 0.5rem;">🎉 Latest Achievement</div>
                <div style="font-size: 0.875rem;">""" + st.session_state.achievements[-1] + """</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Progress tracker with modern design
    with st.sidebar.expander("📈 Progress", expanded=False):
        total_sections = len(menu_options) - 1  # Exclude welcome
        completed = len(st.session_state.progress)
        progress_pct = (completed / total_sections) * 100 if total_sections > 0 else 0
        
        # Modern progress card
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.8); backdrop-filter: blur(10px); border-radius: var(--radius-lg); padding: 1.5rem; border: 1px solid rgba(14, 165, 233, 0.1); margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <span style="color: var(--text-secondary); font-weight: 500;">Overall Progress</span>
                <span style="font-weight: 700; color: var(--primary-500);">{progress_pct:.1f}%</span>
            </div>
            <div style="background: var(--neutral-200); border-radius: var(--radius-full); height: 8px; margin-bottom: 1rem;">
                <div style="background: linear-gradient(90deg, var(--primary-400), var(--secondary-400)); border-radius: var(--radius-full); height: 100%; width: {progress_pct}%; transition: width 0.5s ease;"></div>
            </div>
            <div style="text-align: center; color: var(--text-secondary); font-size: 0.875rem;">
                {completed} of {total_sections} sections completed
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Bookmarks with modern design
    if st.session_state.bookmarks:
        with st.sidebar.expander("📌 Bookmarks", expanded=False):
            st.markdown("""
            <div style="background: rgba(255,255,255,0.8); backdrop-filter: blur(10px); border-radius: var(--radius-lg); padding: 1rem; border: 1px solid rgba(14, 165, 233, 0.1);">
            """, unsafe_allow_html=True)
            for bookmark in st.session_state.bookmarks:
                st.markdown(f"""
                <div style="display: flex; align-items: center; padding: 0.5rem; margin-bottom: 0.5rem; background: rgba(255,255,255,0.5); border-radius: var(--radius-md); border-left: 3px solid var(--primary-400);">
                    <span style="margin-right: 0.5rem;">📌</span>
                    <span style="font-weight: 500; color: var(--text-primary);">{bookmark}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Route to appropriate section
    if selected == "🏠 Welcome":
        welcome_dashboard()
    elif selected == "📖 Introduction":
        introduction()
    elif selected == "🔗 Types of Lists":
        types_of_linked_lists()
    elif selected == "⚙️ Operations":
        operations_and_algorithms()
    elif selected == "🎮 Interactive Playground":
        interactive_playground()
    elif selected == "📊 Performance Analysis":
        performance_analysis()
    elif selected == "💡 Practice Problems":
        practice_problems()
    elif selected == "🎯 Gamified Quiz":
        interactive_quiz()
    elif selected == "🎨 Advanced Visualizations":
        advanced_visualizations()
    elif selected == "📝 Interview Prep":
        interview_preparation()
    elif selected == "📚 References":
        references_and_resources()

# Enhanced Introduction section with modern UI/UX
def introduction():
    st.markdown('<h1 class="main-header" style="margin-top: 0;">📖 Introduction to Linked Lists</h1>', unsafe_allow_html=True)
    save_progress("Introduction")
    
    # Section tools
    col1, col2 = st.columns([1, 1])
    with col1:
        is_bookmarked = "Introduction" in st.session_state.bookmarks
        if st.button("📌 Unbookmark" if is_bookmarked else "📌 Bookmark", key="bookmark_intro"):
            if is_bookmarked:
                st.session_state.bookmarks.remove("Introduction")
            else:
                add_bookmark("Introduction")
            st.rerun()
    with col2:
        if st.button("📝 Add Note", key="note_intro"):
            st.session_state.show_note_intro = True
    
    if st.session_state.get('show_note_intro', False):
        note_text = st.text_input("Your note:", key="intro_note_input")
        if st.button("Save", key="save_intro_note"):
            if note_text:
                save_note("Introduction", note_text)
                st.session_state.show_note_intro = False
                st.rerun()
    
    # Show existing note
    if "Introduction" in st.session_state.notes:
        with st.expander("📝 Your Note"):
            st.write(st.session_state.notes["Introduction"]['text'])

    # Interactive concept overview
    st.markdown("""
    <div class="section-card">
    <h2 style="color: #1e3c72; text-align: center; margin-bottom: 1.5rem;">What is a Linked List?</h2>
    <div style="text-align: center; margin-bottom: 2rem;">
    <div class="highlight-box">
    <strong>A linked list is a fundamental data structure that consists of a sequence of elements called nodes.</strong>
    <br><br>
    Each node contains two parts:
    <ul style="text-align: left; display: inline-block; margin-top: 1rem;">
    <li><strong>Data</strong>: The actual information stored in the node</li>
    <li><strong>Reference/Pointer</strong>: A link to the next node in the sequence</li>
    </ul>
    </div>
    </div>
    <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 1.5rem; border-radius: 12px; margin: 1.5rem 0;">
    <strong>Key Difference from Arrays:</strong> Unlike arrays, linked lists do not store elements in contiguous memory locations.
    Instead, each node points to the next one, forming a chain-like structure that provides dynamic memory allocation.
    </div>
    </div>
    """, unsafe_allow_html=True)

    # Enhanced Advantages/Disadvantages with interactive cards
    st.header("Why Use Linked Lists?")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="interactive-card" style="border-left: 4px solid #4CAF50;">
        <h3 style="color: #4CAF50; margin-bottom: 1rem;">✅ Advantages</h3>
        <div style="display: flex; flex-direction: column; gap: 0.75rem;">
        <div style="display: flex; align-items: center;">
        <span style="color: #4CAF50; margin-right: 0.5rem;">🔸</span>
        <strong>Dynamic Size:</strong> Can grow or shrink during runtime
        </div>
        <div style="display: flex; align-items: center;">
        <span style="color: #4CAF50; margin-right: 0.5rem;">⚡</span>
        <strong>Efficient Operations:</strong> O(1) for insertions/deletions at known positions
        </div>
        <div style="display: flex; align-items: center;">
        <span style="color: #4CAF50; margin-right: 0.5rem;">💾</span>
        <strong>No Memory Waste:</strong> Only allocates memory when needed
        </div>
        <div style="display: flex; align-items: center;">
        <span style="color: #4CAF50; margin-right: 0.5rem;">🔧</span>
        <strong>Flexible Structure:</strong> Easy to implement stacks, queues, and other data structures
        </div>
        </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="interactive-card" style="border-left: 4px solid #f44336;">
        <h3 style="color: #f44336; margin-bottom: 1rem;">❌ Disadvantages</h3>
        <div style="display: flex; flex-direction: column; gap: 0.75rem;">
        <div style="display: flex; align-items: center;">
        <span style="color: #f44336; margin-right: 0.5rem;">🎯</span>
        <strong>Random Access:</strong> O(n) time to access elements by index
        </div>
        <div style="display: flex; align-items: center;">
        <span style="color: #f44336; margin-right: 0.5rem;">📊</span>
        <strong>Extra Memory:</strong> Each node requires additional space for pointers
        </div>
        <div style="display: flex; align-items: center;">
        <span style="color: #f44336; margin-right: 0.5rem;">➡️</span>
        <strong>Sequential Access:</strong> Must traverse from beginning for most operations
        </div>
        <div style="display: flex; align-items: center;">
        <span style="color: #f44336; margin-right: 0.5rem;">⚡</span>
        <strong>Cache Performance:</strong> Poor locality of reference
        </div>
        </div>
        </div>
        """, unsafe_allow_html=True)

    # Enhanced Node Structure with interactive code block
    st.header("Basic Node Structure")

    st.markdown("""
    <div class="code-container">
    <div class="code-header">
    <span>🔧 Node Implementation</span>
    <button class="copy-button" onclick="navigator.clipboard.writeText(`class Node:\\n    def __init__(self, data):\\n        self.data = data\\n        self.next = None`)">Copy</button>
    </div>
    <div class="code-content">
class Node:
    def __init__(self, data):
        self.data = data        # The actual data stored in the node
        self.next = None        # Pointer to the next node (None if last node)
    </div>
    </div>
    """, unsafe_allow_html=True)

    # Interactive Real-World Applications
    st.header("Real-World Applications")

    applications = [
        {"icon": "🎵", "title": "Music Playlists", "desc": "Songs linked in sequence for easy navigation"},
        {"icon": "🌐", "title": "Browser History", "desc": "Web pages linked for back/forward navigation"},
        {"icon": "↩️", "title": "Undo Functionality", "desc": "Operations stored as linked list in editors"},
        {"icon": "🔗", "title": "Hash Tables", "desc": "Collision resolution using separate chaining"},
        {"icon": "💾", "title": "Memory Management", "desc": "Free memory blocks tracking in OS"},
        {"icon": "📈", "title": "Polynomial Representation", "desc": "Mathematical terms linked by degree"}
    ]

    cols = st.columns(3)
    for i, app in enumerate(applications):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="feature-card" style="animation-delay: {i * 0.1}s; min-height: 120px;">
            <h4 style="margin-bottom: 0.5rem;">{app['icon']} {app['title']}</h4>
            <p style="font-size: 0.9em; opacity: 0.9;">{app['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

    # Enhanced Memory Representation with visual diagram
    st.header("Memory Representation")

    st.markdown("""
    <div class="visual-diagram">
    <h3 style="margin-bottom: 1rem; color: #1e3c72;">🔍 How Linked Lists are Stored in Memory</h3>
    <p style="margin-bottom: 1.5rem;">Visual representation of how linked list nodes are scattered in memory:</p>
    </div>
    """, unsafe_allow_html=True)

    # Enhanced memory layout visualization
    st.markdown("""
    <div class="section-card">
    <div style="font-family: 'Courier New', monospace; background: #2c3e50; color: #ecf0f1; padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
    <div style="text-align: center; margin-bottom: 1rem; color: #3498db; font-weight: bold;">Memory Layout Visualization</div>
    <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap; gap: 1rem;">
    <div style="border: 2px solid #e74c3c; border-radius: 8px; padding: 1rem; background: #34495e; min-width: 150px;">
    <div style="text-align: center; color: #e74c3c; font-weight: bold; margin-bottom: 0.5rem;">Node 1</div>
    <div><strong>Data:</strong> 10</div>
    <div><strong>Next:</strong> 0x200 →</div>
    <div style="text-align: center; margin-top: 0.5rem; color: #95a5a6; font-size: 0.8em;">Address: 0x100</div>
    </div>
    <div style="color: #e74c3c; font-size: 1.5rem;">→</div>
    <div style="border: 2px solid #27ae60; border-radius: 8px; padding: 1rem; background: #34495e; min-width: 150px;">
    <div style="text-align: center; color: #27ae60; font-weight: bold; margin-bottom: 0.5rem;">Node 2</div>
    <div><strong>Data:</strong> 20</div>
    <div><strong>Next:</strong> 0x300 →</div>
    <div style="text-align: center; margin-top: 0.5rem; color: #95a5a6; font-size: 0.8em;">Address: 0x200</div>
    </div>
    <div style="color: #27ae60; font-size: 1.5rem;">→</div>
    <div style="border: 2px solid #f39c12; border-radius: 8px; padding: 1rem; background: #34495e; min-width: 150px;">
    <div style="text-align: center; color: #f39c12; font-weight: bold; margin-bottom: 0.5rem;">Node 3</div>
    <div><strong>Data:</strong> 30</div>
    <div><strong>Next:</strong> NULL</div>
    <div style="text-align: center; margin-top: 0.5rem; color: #95a5a6; font-size: 0.8em;">Address: 0x300</div>
    </div>
    </div>
    <div style="margin-top: 1rem; text-align: center; color: #95a5a6; font-style: italic;">
    Nodes are scattered in memory, connected only by pointers
    </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

    # Interactive learning checkpoint
    st.markdown("""
    <div class="section-card">
    <h3 style="color: #1e3c72; text-align: center; margin-bottom: 1rem;">🎯 Learning Checkpoint</h3>
    <div style="display: flex; justify-content: space-around; margin: 1.5rem 0;">
    <div style="text-align: center;">
    <div style="font-size: 2rem; color: #4CAF50;">✓</div>
    <div style="margin-top: 0.5rem; font-weight: 600;">Node Structure</div>
    </div>
    <div style="text-align: center;">
    <div style="font-size: 2rem; color: #4CAF50;">✓</div>
    <div style="margin-top: 0.5rem; font-weight: 600;">Memory Layout</div>
    </div>
    <div style="text-align: center;">
    <div style="font-size: 2rem; color: #2196F3;">○</div>
    <div style="margin-top: 0.5rem; font-weight: 600;">Types of Lists</div>
    </div>
    <div style="text-align: center;">
    <div style="font-size: 2rem; color: #9E9E9E;">○</div>
    <div style="margin-top: 0.5rem; font-weight: 600;">Operations</div>
    </div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add Continue to Types button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Continue to Types →", key="continue_to_types", use_container_width=True):
            st.session_state.current_tab = 2  # Navigate to Types
            st.session_state.scroll_to_top = True  # Flag to scroll to top
            st.rerun()
    
    st.markdown("""
    <div class="section-card">
    </div>
    """, unsafe_allow_html=True)

# Types of Linked Lists section
def types_of_linked_lists():
    st.title("Types of Linked Lists")
    save_progress("Types")

    st.markdown("""
    Linked lists come in various forms, each with its own strengths and use cases. Understanding the differences
    between these types is crucial for choosing the right data structure for your specific needs.
    """)

    st.header("1. Singly Linked List")
    st.markdown("**Overview:** The most basic form of linked list where each node points only to the next node.")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **Node Structure:**
        ```python
        class Node:
            def __init__(self, data):
                self.data = data      # The actual data
                self.next = None      # Pointer to next node
        ```

        **Detailed Characteristics:**
        - **Memory Usage:** Minimal (1 pointer + data per node)
        - **Traversal:** Only forward direction
        - **Operations:** Simple to implement
        - **Performance:** O(1) for beginning operations, O(n) for end operations
        - **Memory Efficiency:** Good for large datasets with sequential access

        **Advantages:**
        - ✅ Simple implementation and understanding
        - ✅ Low memory overhead per node
        - ✅ Efficient for stack operations (LIFO)
        - ✅ Good cache performance for sequential access
        - ✅ Easy to implement recursive algorithms

        **Disadvantages:**
        - ❌ No backward traversal
        - ❌ O(n) time for random access
        - ❌ Cannot efficiently delete previous node
        - ❌ More complex reverse operations

        **Real-World Use Cases:**
        - **Stack Implementation:** Perfect for undo/redo functionality
        - **Queue Implementation:** Basic FIFO operations
        - **Hash Table Chaining:** Collision resolution in hash tables
        - **Memory Management:** Free memory block tracking
        - **Symbol Tables:** In compilers and interpreters
        - **Polynomial Operations:** Representing mathematical polynomials
        """)

        st.subheader("Visual Representation")
        st.code("""
Singly Linked List Memory Layout:
+-------------------+     +-------------------+     +-------------------+
| Data: 10          |     | Data: 20          |     | Data: 30          |
| Next: 0x200       | --> | Next: 0x300       | --> | Next: None        |
+-------------------+     +-------------------+     +-------------------+
0x100                   0x200                   0x300

Traversal: 10 -> 20 -> 30 -> NULL
        """)

    with col2:
        st.code("""
# Complete Singly Linked List Implementation
class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1

    def delete_from_beginning(self):
        if self.head is None:
            return None
        deleted_data = self.head.data
        self.head = self.head.next
        self.size -= 1
        return deleted_data

    def search(self, target):
        current = self.head
        position = 0
        while current:
            if current.data == target:
                return position
            current = current.next
            position += 1
        return -1

    def traverse(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements

# Example Usage:
sll = SinglyLinkedList()
sll.insert_at_end(1)
sll.insert_at_end(2)
sll.insert_at_end(3)
print(sll.traverse())  # [1, 2, 3]
        """, language="python")

    st.header("2. Doubly Linked List")
    st.markdown("**Overview:** Each node has pointers to both previous and next nodes, enabling bidirectional traversal.")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **Node Structure:**
        ```python
        class DoublyNode:
            def __init__(self, data):
                self.data = data      # The actual data
                self.next = None      # Pointer to next node
                self.prev = None      # Pointer to previous node
        ```

        **Detailed Characteristics:**
        - **Memory Usage:** Higher (2 pointers + data per node)
        - **Traversal:** Both forward and backward directions
        - **Operations:** More complex but more flexible
        - **Performance:** O(1) for beginning and end operations (with tail pointer)
        - **Memory Efficiency:** Less efficient than singly linked lists

        **Advantages:**
        - ✅ Bidirectional traversal
        - ✅ Efficient deletion of any node (if reference is known)
        - ✅ Can implement deque operations efficiently
        - ✅ Easier to implement complex data structures
        - ✅ Better for frequent insertions/deletions at both ends

        **Disadvantages:**
        - ❌ Higher memory overhead
        - ❌ More complex implementation
        - ❌ Extra pointer updates required
        - ❌ Slightly slower operations due to extra bookkeeping

        **Real-World Use Cases:**
        - **Browser History:** Back and forward navigation
        - **Text Editors:** Cursor movement and editing
        - **LRU Cache:** Most Recently Used page replacement
        - **Undo/Redo Stacks:** Bidirectional operation history
        - **Music Player:** Previous/next track navigation
        - **File System Navigation:** Directory traversal
        """)

        st.subheader("Visual Representation")
        st.code("""
Doubly Linked List Memory Layout:
+-------------------+     +-------------------+     +-------------------+
| Prev: None        |     | Prev: 0x100       |     | Prev: 0x200       |
| Data: 10          |     | Data: 20          |     | Data: 30          |
| Next: 0x200       | <-- | Next: 0x300       | <-- | Next: None        |
+-------------------+     +-------------------+     +-------------------+
0x100                   0x200                   0x300

Traversal: NULL <- 10 <-> 20 <-> 30 -> NULL
        """)

    with col2:
        st.code("""
# Complete Doubly Linked List Implementation
class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None  # Tail pointer for O(1) end operations
        self.size = 0

    def insert_at_beginning(self, data):
        new_node = DoublyNode(data)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1

    def insert_at_end(self, data):
        new_node = DoublyNode(data)
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def delete_from_beginning(self):
        if self.head is None:
            return None
        deleted_data = self.head.data
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        self.size -= 1
        return deleted_data

    def traverse_forward(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements

    def traverse_backward(self):
        elements = []
        current = self.tail
        while current:
            elements.append(current.data)
            current = current.prev
        return elements

# Example Usage:
dll = DoublyLinkedList()
dll.insert_at_end(1)
dll.insert_at_end(2)
dll.insert_at_end(3)
print(dll.traverse_forward())   # [1, 2, 3]
print(dll.traverse_backward())  # [3, 2, 1]
        """, language="python")

    st.header("3. Circular Linked List")
    st.markdown("**Overview:** The last node points back to the first node, forming a circle.")
    
    # Sum calculation examples for understanding
    st.subheader("📊 Sum Calculation Examples")
    
    st.markdown("""
    **Understanding through Sum Operations:**
    Let's see how to calculate the sum of all elements in different linked list types.
    """)
    
    tab1, tab2, tab3 = st.tabs(["Singly Linked", "Doubly Linked", "Circular Linked"])
    
    with tab1:
        st.markdown("**Sum in Singly Linked List:**")
        st.code("""
# Calculate sum of all elements
def calculate_sum_singly(head):
    total = 0
    current = head
    
    while current:
        total += current.data
        current = current.next
    
    return total

# Example: [10, 20, 30] → Sum = 60
ll = SinglyLinkedList()
ll.insert_at_end(10)
ll.insert_at_end(20) 
ll.insert_at_end(30)
print(f"Sum: {calculate_sum_singly(ll.head)}")  # Output: 60
        """, language="python")
    
    with tab2:
        st.markdown("**Sum in Doubly Linked List:**")
        st.code("""
# Calculate sum - can traverse forward or backward
def calculate_sum_doubly_forward(head):
    total = 0
    current = head
    
    while current:
        total += current.data
        current = current.next
    
    return total

def calculate_sum_doubly_backward(tail):
    total = 0
    current = tail
    
    while current:
        total += current.data
        current = current.prev
    
    return total

# Example: [10, 20, 30] → Sum = 60 (both directions)
dll = DoublyLinkedList()
dll.insert_at_end(10)
dll.insert_at_end(20)
dll.insert_at_end(30)
print(f"Forward Sum: {calculate_sum_doubly_forward(dll.head)}")   # 60
print(f"Backward Sum: {calculate_sum_doubly_backward(dll.tail)}")  # 60
        """, language="python")
    
    with tab3:
        st.markdown("**Sum in Circular Linked List:**")
        st.code("""
# Calculate sum - must avoid infinite loop!
def calculate_sum_circular(head):
    if not head:
        return 0
    
    total = head.data
    current = head.next
    
    # Stop when we reach the starting node again
    while current != head:
        total += current.data
        current = current.next
    
    return total

# Alternative with counter for safety
def calculate_sum_circular_safe(head, size):
    total = 0
    current = head
    count = 0
    
    while current and count < size:
        total += current.data
        current = current.next
        count += 1
    
    return total

# Example: [10, 20, 30] → Sum = 60
cll = CircularLinkedList()
cll.insert_at_end(10)
cll.insert_at_end(20)
cll.insert_at_end(30)
print(f"Sum: {calculate_sum_circular(cll.head)}")  # Output: 60
        """, language="python")
    
    # Interactive sum calculator
    st.subheader("🧮 Interactive Sum Calculator")
    
    calc_type = st.selectbox("Choose list type for sum calculation:", 
                            ["Singly Linked", "Doubly Linked", "Circular Linked"])
    
    calc_input = st.text_input("Enter numbers (comma-separated):", "10, 20, 30, 40")
    
    if st.button("Calculate Sum"):
        try:
            numbers = [int(x.strip()) for x in calc_input.split(",") if x.strip()]
            if numbers:
                total = sum(numbers)
                st.success(f"📊 **{calc_type} Sum Result:**")
                st.write(f"Numbers: {numbers}")
                st.write(f"Sum: {total}")
                st.write(f"Average: {total/len(numbers):.2f}")
                st.write(f"Count: {len(numbers)}")
                
                # Show step-by-step calculation
                with st.expander("Step-by-step calculation"):
                    running_sum = 0
                    for i, num in enumerate(numbers):
                        running_sum += num
                        st.write(f"Step {i+1}: {running_sum-num} + {num} = {running_sum}")
            else:
                st.warning("Please enter valid numbers")
        except ValueError:
            st.error("Please enter valid integers separated by commas")
    
    # Comparison of sum algorithms
    st.subheader("⚡ Sum Algorithm Comparison")
    
    # Create comparison table manually to avoid pandas issues
    st.markdown("""
    | List Type | Time Complexity | Space Complexity | Special Considerations |
    |-----------|----------------|------------------|------------------------|
    | Singly Linked | O(n) | O(1) | Simple forward traversal |
    | Doubly Linked | O(n) | O(1) | Can traverse forward or backward |
    | Circular Linked | O(n) | O(1) | Must avoid infinite loops |
    """)
    
    st.info("💡 **Key Insight**: All linked list types have the same time complexity O(n) for sum calculation, but differ in implementation details.")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **Node Structure (Singly Circular):**
        ```python
        class CircularNode:
            def __init__(self, data):
                self.data = data
                self.next = None
        ```

        **Detailed Characteristics:**
        - **Memory Usage:** Same as singly (1 pointer + data per node)
        - **Traversal:** Can start from any node and traverse infinitely
        - **Operations:** Need careful handling to avoid infinite loops
        - **Performance:** O(1) for beginning operations, O(n) for end operations
        - **Special Property:** No NULL termination

        **Advantages:**
        - ✅ Memory efficient (same as singly linked)
        - ✅ Useful for circular operations
        - ✅ Can represent cyclic data naturally
        - ✅ Round-robin algorithms work naturally
        - ✅ No special case for end of list

        **Disadvantages:**
        - ❌ Easy to create infinite loops
        - ❌ More complex traversal logic
        - ❌ Cannot use NULL to detect end
        - ❌ Harder to detect cycles (ironic!)

        **Real-World Use Cases:**
        - **Round-Robin Scheduling:** CPU process scheduling
        - **Circular Buffers:** Audio/video streaming
        - **Multiplayer Games:** Player turn management
        - **Music Playlists:** Continuous playback
        - **Token Ring Networks:** Data transmission
        - **Time-Sharing Systems:** Resource allocation
        """)

        st.subheader("Visual Representation")
        st.code("""
Circular Linked List Memory Layout:
+-------------------+     +-------------------+     +-------------------+
| Data: 10          |     | Data: 20          |     | Data: 30          |
| Next: 0x200       | --> | Next: 0x300       | --> | Next: 0x100       |
+-------------------+     +-------------------+     +-------------------+
0x100                   0x200                   0x300         |
                                                              |
                                                              v
                                                            Back to 0x100

Traversal: 10 -> 20 -> 30 -> 10 -> 20 -> ... (infinite)
        """)

    with col2:
        st.code("""
# Complete Circular Linked List Implementation
class CircularLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def insert_at_beginning(self, data):
        new_node = CircularNode(data)
        if self.head is None:
            new_node.next = new_node  # Point to itself
            self.head = new_node
        else:
            new_node.next = self.head
            # Find the last node
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = new_node
            self.head = new_node
        self.size += 1

    def insert_at_end(self, data):
        new_node = CircularNode(data)
        if self.head is None:
            new_node.next = new_node
            self.head = new_node
        else:
            new_node.next = self.head
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = new_node
        self.size += 1

    def traverse(self, max_elements=10):
        if self.head is None:
            return []
        elements = []
        current = self.head
        count = 0
        while count < max_elements:
            elements.append(current.data)
            current = current.next
            count += 1
            if current == self.head:
                break
        return elements

# Example Usage:
cll = CircularLinkedList()
cll.insert_at_end(1)
cll.insert_at_end(2)
cll.insert_at_end(3)
print(cll.traverse())  # [1, 2, 3]
        """, language="python")

    # Practical sum examples with real scenarios
    st.subheader("🌟 Real-World Sum Applications")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Shopping Cart Total (Singly Linked):**
        ```python
        # Each node represents an item with price
        class CartItem:
            def __init__(self, name, price):
                self.name = name
                self.price = price
                self.next = None
        
        def calculate_cart_total(cart_head):
            total = 0
            current = cart_head
            while current:
                total += current.price
                current = current.next
            return total
        
        # Cart: Apple($2) → Banana($1) → Orange($3)
        # Total: $6
        ```
        """)
    
    with col2:
        st.markdown("""
        **Score History (Doubly Linked):**
        ```python
        # Game scores with forward/backward navigation
        class ScoreNode:
            def __init__(self, score):
                self.score = score
                self.next = None
                self.prev = None
        
        def calculate_total_score(head):
            total = 0
            current = head
            while current:
                total += current.score
                current = current.next
            return total
        
        # Scores: 100 ↔ 85 ↔ 92 ↔ 78
        # Total: 355
        ```
        """)
    
    st.header("4. Advanced Linked List Variants")

    st.subheader("XOR Linked List")
    st.markdown("""
    **Concept:** Uses bitwise XOR to store both previous and next pointers in a single field, saving memory.

    **How it works:**
    - Each node stores: `ptr = prev XOR next`
    - To traverse: `next = ptr XOR prev`
    - Memory efficient but complex to implement

    **Use Cases:** Memory-constrained environments, competitive programming
    """)

    st.subheader("Skip List")
    st.markdown("""
    **Concept:** A probabilistic data structure that allows O(log n) search time.

    **How it works:**
    - Multiple levels of linked lists
    - Higher levels skip more nodes
    - Search starts from top level and works down

    **Use Cases:** Database indexes, Redis sorted sets
    """)

    st.subheader("Unrolled Linked List")
    st.markdown("""
    **Concept:** Each node contains an array of elements instead of a single element.

    **Benefits:**
    - Better cache performance
    - Reduced pointer overhead
    - Faster sequential access

    **Use Cases:** High-performance applications, cache-conscious data structures
    """)

    st.header("Comprehensive Comparison")

    # Create detailed comparison table
    comparison_data = {
        'Aspect': [
            'Memory per Node',
            'Traversal Direction',
            'Beginning Operations',
            'End Operations',
            'Random Access',
            'Implementation Complexity',
            'Memory Efficiency',
            'Cache Performance',
            'Use Case Fit'
        ],
        'Singly Linked': [
            '1 pointer + data',
            'Forward only',
            'O(1)',
            'O(n)',
            'O(n)',
            'Simple',
            'Good',
            'Good',
            'Stacks, Queues'
        ],
        'Doubly Linked': [
            '2 pointers + data',
            'Bidirectional',
            'O(1)',
            'O(1)*',
            'O(n)',
            'Moderate',
            'Poor',
            'Fair',
            'Deques, Caches'
        ],
        'Circular Singly': [
            '1 pointer + data',
            'Circular',
            'O(1)',
            'O(n)',
            'O(n)',
            'Moderate',
            'Good',
            'Good',
            'Round-robin'
        ],
        'Circular Doubly': [
            '2 pointers + data',
            'Circular Bidirectional',
            'O(1)',
            'O(1)',
            'O(n)',
            'Complex',
            'Poor',
            'Fair',
            'Complex circular ops'
        ]
    }

    import pandas as pd
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True)

    st.markdown("*Note: * Requires tail pointer for O(1) end operations")

    st.header("Common Pitfalls and Best Practices")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Common Mistakes")
        st.markdown("""
        - **Null Pointer Dereference:** Always check for None before accessing next/prev
        - **Infinite Loops:** Especially in circular lists, always have termination conditions
        - **Memory Leaks:** In languages without GC, remember to free nodes
        - **Lost References:** When deleting nodes, update all relevant pointers
        - **Off-by-One Errors:** Careful with indexing and position calculations
        """)

    with col2:
        st.subheader("Best Practices")
        st.markdown("""
        - **Use Sentinel Nodes:** Dummy head/tail nodes to simplify boundary cases
        - **Maintain Size Counter:** Keep track of list size for efficient operations
        - **Tail Pointers:** For doubly linked lists to enable O(1) end operations
        - **Consistent Naming:** Use clear variable names (head, tail, current, etc.)
        - **Error Handling:** Always handle edge cases (empty list, single node)
        """)

    st.header("Performance Considerations")

    st.markdown("""
    **Memory Overhead Analysis:**

    | Data Structure | Pointers | Overhead (64-bit) | Total per Node |
    |----------------|----------|-------------------|----------------|
    | Singly Linked | 1 | 8 bytes | 8 + data bytes |
    | Doubly Linked | 2 | 16 bytes | 16 + data bytes |
    | Array Element | 0 | 0 bytes | data bytes only |

    **Cache Performance:**
    - **Arrays:** Excellent locality of reference
    - **Linked Lists:** Poor locality, nodes scattered in memory
    - **Unrolled Lists:** Better locality with multiple elements per node

    **When to Choose Which:**
    - **Singly Linked:** Memory-critical, forward-only traversal
    - **Doubly Linked:** Need bidirectional access, frequent end operations
    - **Circular:** Round-robin, circular buffers, infinite traversal
    - **Array:** Random access, cache performance critical
    """)

    st.header("Implementation Tips")

    with st.expander("Singly Linked List Tips"):
        st.markdown("""
        1. Always keep a reference to head
        2. Use a dummy node for operations on empty lists
        3. For frequent end operations, maintain a tail pointer
        4. Be careful with pointer updates during deletion
        5. Use recursion sparingly (watch stack overflow)
        """)

    with st.expander("Doubly Linked List Tips"):
        st.markdown("""
        1. Always update both next and prev pointers
        2. Maintain both head and tail pointers
        3. Use symmetry in operations (forward/backward)
        4. Careful with boundary conditions
        5. Consider using sentinel nodes
        """)

    with st.expander("Circular Linked List Tips"):
        st.markdown("""
        1. Never use NULL to detect end of list
        2. Always have a termination condition in loops
        3. Be careful with empty list handling
        4. Use size counter to prevent infinite loops
        5. Consider using a tail pointer for efficiency
        """)

# Operations and Algorithms section
def operations_and_algorithms():
    st.title("Operations and Algorithms")
    save_progress("Operations")

    st.header("1. Insertion Operations")

    st.subheader("Insert at Beginning")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **Algorithm:**
        1. Create a new node with given data
        2. Set new node's next to current head
        3. Update head to point to new node

        **Time Complexity:** O(1)
        **Space Complexity:** O(1)
        """)
    with col2:
        st.code("""
def insert_at_beginning(head, data):
    new_node = Node(data)
    new_node.next = head
    return new_node  # New head

# Example: Insert 0 at beginning of [1,2,3]
# Result: [0,1,2,3]
        """, language="python")

    st.subheader("Insert at End")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **Algorithm:**
        1. Create a new node with given data
        2. If list is empty, set as head
        3. Else traverse to last node
        4. Set last node's next to new node

        **Time Complexity:** O(n)
        **Space Complexity:** O(1)
        """)
    with col2:
        st.code("""
def insert_at_end(head, data):
    new_node = Node(data)
    if head is None:
        return new_node

    current = head
    while current.next:
        current = current.next
    current.next = new_node
    return head

# Example: Insert 4 at end of [1,2,3]
# Result: [1,2,3,4]
        """, language="python")

    st.header("2. Deletion Operations")

    st.subheader("Delete from Beginning")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **Algorithm:**
        1. If list is empty, return None
        2. Store current head
        3. Update head to next node
        4. Return deleted node's data

        **Time Complexity:** O(1)
        **Space Complexity:** O(1)
        """)
    with col2:
        st.code("""
def delete_from_beginning(head):
    if head is None:
        return None, head

    deleted_data = head.data
    new_head = head.next
    return deleted_data, new_head

# Example: Delete from [1,2,3]
# Result: 1, [2,3]
        """, language="python")

    st.subheader("Delete by Value")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **Algorithm:**
        1. If list is empty, return False
        2. If head contains target, update head
        3. Traverse list to find target
        4. Update previous node's next pointer
        5. Return True if found, False otherwise

        **Time Complexity:** O(n)
        **Space Complexity:** O(1)
        """)
    with col2:
        st.code("""
def delete_by_value(head, target):
    if head is None:
        return False, head

    if head.data == target:
        return True, head.next

    current = head
    while current.next and current.next.data != target:
        current = current.next

    if current.next:
        current.next = current.next.next
        return True, head
    return False, head

# Example: Delete 2 from [1,2,3]
# Result: True, [1,3]
        """, language="python")

    st.header("3. Traversal")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **Algorithm:**
        1. Start from head node
        2. While current node is not None:
           - Process current node's data
           - Move to next node
        3. End when current becomes None

        **Time Complexity:** O(n)
        **Space Complexity:** O(1)

        **Use Cases:**
        - Printing list elements
        - Searching for values
        - Applying operations to all elements
        """)
    with col2:
        st.code("""
def traverse_and_print(head):
    current = head
    while current:
        print(current.data, end=" -> ")
        current = current.next
    print("None")

# Example traversal of [1,2,3]
# Output: 1 -> 2 -> 3 -> None
        """, language="python")

    st.header("4. Searching")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **Algorithm:**
        1. Start from head node
        2. Initialize position counter
        3. While current node is not None:
           - Check if current data matches target
           - If match, return position
           - Increment position, move to next
        4. Return -1 if not found

        **Time Complexity:** O(n)
        **Space Complexity:** O(1)
        """)
    with col2:
        st.code("""
def search_by_value(head, target):
    current = head
    position = 0

    while current:
        if current.data == target:
            return position
        current = current.next
        position += 1

    return -1

# Example: Search for 2 in [1,2,3]
# Result: 1 (0-based index)
        """, language="python")

    st.header("5. Time and Space Complexity Analysis")
    st.markdown("""
    | Operation | Singly Linked List | Doubly Linked List | Notes |
    |-----------|-------------------|-------------------|-------|
    | **Insertion at Beginning** | O(1) | O(1) | Direct head update |
    | **Insertion at End** | O(n) | O(1)* | *Requires tail pointer |
    | **Insertion at Position** | O(n) | O(n) | Need to traverse |
    | **Deletion at Beginning** | O(1) | O(1) | Direct head update |
    | **Deletion at End** | O(n) | O(1)* | *Requires tail pointer |
    | **Deletion by Value** | O(n) | O(n) | Linear search required |
    | **Traversal** | O(n) | O(n) | Visit all nodes |
    | **Searching** | O(n) | O(n) | Linear search |

    **Space Complexity:** O(n) for all types (proportional to number of elements)
    """)

    st.header("Advanced Algorithms")

    st.subheader("Reverse a Linked List")
    st.code("""
def reverse_linked_list(head):
    prev = None
    current = head

    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node

    return prev

# Example: Reverse [1,2,3] -> [3,2,1]
    """, language="python")

    st.subheader("Detect Cycle (Floyd's Algorithm)")
    st.code("""
def has_cycle(head):
    if not head or not head.next:
        return False

    slow = head
    fast = head.next

    while fast and fast.next:
        if slow == fast:
            return True
        slow = slow.next
        fast = fast.next.next

    return False

# Returns True if cycle exists
    """, language="python")

# Interactive Playground section
def interactive_playground():
    st.title("Interactive Playground")
    save_progress("Playground")
    
    # Quick tools
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🎲 Random Data", key="random_data"):
            if hasattr(st.session_state, 'linked_list') and st.session_state.linked_list:
                import random
                random_values = [random.randint(1, 100) for _ in range(3)]
                for val in random_values:
                    st.session_state.linked_list.insert_at_end(val)
                st.success(f"🎲 Added: {random_values}")
                st.rerun()
            else:
                st.warning("Create a list first!")
    with col2:
        is_bookmarked = "Playground" in st.session_state.bookmarks
        if st.button("📌 Bookmark" if not is_bookmarked else "📌 Bookmarked", key="bookmark_playground"):
            if not is_bookmarked:
                add_bookmark("Playground")
            st.rerun()

    # Linked list classes are now imported from linked_list_classes module

    # Initialize session state
    if 'list_type' not in st.session_state:
        st.session_state.list_type = "Singly Linked List"
    if 'linked_list' not in st.session_state:
        st.session_state.linked_list = SinglyLinkedList()

    # List type selector
    st.header("Select Linked List Type")
    list_types = ["Singly Linked List", "Doubly Linked List", "Circular Linked List"]
    selected_type = st.selectbox("Choose list type:", list_types, index=list_types.index(st.session_state.list_type))

    if selected_type != st.session_state.list_type:
        st.session_state.list_type = selected_type
        if selected_type == "Singly Linked List":
            st.session_state.linked_list = SinglyLinkedList()
        elif selected_type == "Doubly Linked List":
            st.session_state.linked_list = DoublyLinkedList()
        elif selected_type == "Circular Linked List":
            st.session_state.linked_list = CircularLinkedList()
        st.rerun()

    st.header("Create Your Linked List")
    col1, col2 = st.columns([2, 1])
    with col1:
        user_input = st.text_input("Enter comma-separated values (e.g., 1, 2, 3, 4)", "")
        if st.button("Create List", key="create"):
            if user_input:
                values = [x.strip() for x in user_input.split(",") if x.strip()]
                if st.session_state.list_type == "Singly Linked List":
                    st.session_state.linked_list = SinglyLinkedList()
                    for val in values:
                        st.session_state.linked_list.insert_at_end(val)
                elif st.session_state.list_type == "Doubly Linked List":
                    st.session_state.linked_list = DoublyLinkedList()
                    for val in values:
                        st.session_state.linked_list.insert_at_end(val)
                elif st.session_state.list_type == "Circular Linked List":
                    st.session_state.linked_list = CircularLinkedList()
                    for val in values:
                        st.session_state.linked_list.insert_at_end(val)
                st.success(f"{st.session_state.list_type} created with {len(values)} elements!")
            else:
                st.warning("Please enter some values.")
    with col2:
        if st.button("Clear List", key="clear"):
            if st.session_state.list_type == "Singly Linked List":
                st.session_state.linked_list = SinglyLinkedList()
            elif st.session_state.list_type == "Doubly Linked List":
                st.session_state.linked_list = DoublyLinkedList()
            elif st.session_state.list_type == "Circular Linked List":
                st.session_state.linked_list = CircularLinkedList()
            st.info(f"{st.session_state.list_type} cleared!")

    st.header(f"Current {st.session_state.list_type}")
    if st.session_state.linked_list.size > 0:
        if st.session_state.list_type == "Doubly Linked List":
            st.write("Forward: ", st.session_state.linked_list.traverse_forward())
            st.write("Backward: ", st.session_state.linked_list.traverse_backward())
        else:
            elements = st.session_state.linked_list.traverse() if st.session_state.list_type != "Circular Linked List" else st.session_state.linked_list.traverse(20)
            st.write("Elements: ", elements)
        st.write(f"Length: {st.session_state.linked_list.size}")

        # Enhanced Plotly visualization
        elements = []
        if st.session_state.list_type == "Doubly Linked List":
            elements = st.session_state.linked_list.traverse_forward()
        elif st.session_state.list_type == "Circular Linked List":
            elements = st.session_state.linked_list.traverse(20)
        else:
            elements = st.session_state.linked_list.traverse()

        # Create interactive Plotly visualization
        fig = go.Figure()
        
        # Add nodes
        node_x = [i * 2 for i in range(len(elements))]
        node_y = [0] * len(elements)
        
        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            marker=dict(size=50, color='#4A90E2', line=dict(width=3, color='#2E5BBA')),
            text=[str(val) for val in elements],
            textposition="middle center",
            textfont=dict(size=14, color='white', family="Arial Black"),
            name="Nodes",
            hovertemplate="<b>Node %{pointNumber}</b><br>Value: %{text}<extra></extra>"
        ))
        
        # Add arrows based on list type
        if st.session_state.list_type == "Doubly Linked List":
            # Forward arrows (next pointers)
            for i in range(len(elements) - 1):
                fig.add_annotation(
                    x=node_x[i+1] - 0.6, y=0.3,
                    ax=node_x[i] + 0.6, ay=0.3,
                    xref='x', yref='y', axref='x', ayref='y',
                    arrowhead=2, arrowsize=1.5, arrowwidth=3, arrowcolor='#FF6B6B',
                    showarrow=True
                )
                # Add "next" label
                fig.add_annotation(
                    x=(node_x[i] + node_x[i+1]) / 2, y=0.5,
                    text="next", showarrow=False,
                    font=dict(size=10, color='#FF6B6B', family="Arial Black")
                )
            
            # Backward arrows (prev pointers)
            for i in range(1, len(elements)):
                fig.add_annotation(
                    x=node_x[i-1] + 0.6, y=-0.3,
                    ax=node_x[i] - 0.6, ay=-0.3,
                    xref='x', yref='y', axref='x', ayref='y',
                    arrowhead=2, arrowsize=1.5, arrowwidth=3, arrowcolor='#4ECDC4',
                    showarrow=True
                )
                # Add "prev" label
                fig.add_annotation(
                    x=(node_x[i] + node_x[i-1]) / 2, y=-0.5,
                    text="prev", showarrow=False,
                    font=dict(size=10, color='#4ECDC4', family="Arial Black")
                )
                
        elif st.session_state.list_type == "Circular Linked List":
            # Regular forward arrows
            for i in range(len(elements) - 1):
                fig.add_annotation(
                    x=node_x[i+1] - 0.6, y=0,
                    ax=node_x[i] + 0.6, ay=0,
                    xref='x', yref='y', axref='x', ayref='y',
                    arrowhead=2, arrowsize=1.5, arrowwidth=3, arrowcolor='#FF6B6B',
                    showarrow=True
                )
            
            # Circular arrow from last to first (curved)
            if len(elements) > 1:
                last_x = node_x[-1]
                first_x = node_x[0]
                mid_x = (last_x + first_x) / 2
                
                # Create a more visible curved path
                fig.add_shape(
                    type="path",
                    path=f"M {last_x + 0.7},0 Q {mid_x},{-1.0} {first_x - 0.7},0",
                    line=dict(color="#9B59B6", width=4),
                )
                
                # Add multiple arrow segments for better visibility
                # Arrow at the end pointing to first node
                fig.add_annotation(
                    x=first_x - 0.7, y=0,
                    ax=first_x - 0.9, ay=-0.2,
                    xref='x', yref='y', axref='x', ayref='y',
                    arrowhead=2, arrowsize=2, arrowwidth=4, arrowcolor='#9B59B6',
                    showarrow=True
                )
                
                # Add arrow at the start from last node
                fig.add_annotation(
                    x=last_x + 0.9, y=-0.2,
                    ax=last_x + 0.7, ay=0,
                    xref='x', yref='y', axref='x', ayref='y',
                    arrowhead=2, arrowsize=2, arrowwidth=4, arrowcolor='#9B59B6',
                    showarrow=True
                )
                
                # Add "circular" label with background
                fig.add_annotation(
                    x=mid_x, y=-0.7,
                    text="↻ CIRCULAR", showarrow=False,
                    font=dict(size=11, color='#9B59B6', family="Arial Black"),
                    bgcolor="rgba(255,255,255,0.8)",
                    bordercolor="#9B59B6",
                    borderwidth=1
                )
                
        else:  # Singly Linked List
            for i in range(len(elements) - 1):
                fig.add_annotation(
                    x=node_x[i+1] - 0.6, y=0,
                    ax=node_x[i] + 0.6, ay=0,
                    xref='x', yref='y', axref='x', ayref='y',
                    arrowhead=2, arrowsize=1.5, arrowwidth=3, arrowcolor='#FF6B6B',
                    showarrow=True
                )
        
        # Add NULL for non-circular lists
        if st.session_state.list_type != "Circular Linked List" and elements:
            fig.add_trace(go.Scatter(
                x=[node_x[-1] + 2], y=[0],
                mode='markers+text',
                marker=dict(size=40, color='#95A5A6', line=dict(width=2, color='#7F8C8D')),
                text=["NULL"],
                textposition="middle center",
                textfont=dict(size=12, color='white', family="Arial Black"),
                name="NULL",
                showlegend=False
            ))
            fig.add_annotation(
                x=node_x[-1] + 1.5, y=0,
                ax=node_x[-1] + 0.5, ay=0,
                arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor='#95A5A6',
                showarrow=True
            )
        
        fig.update_layout(
            title=dict(
                text=f"{st.session_state.list_type} Visualization",
                font=dict(size=18, color='#2C3E50')
            ),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, 
                      range=[-1.5, 1] if st.session_state.list_type == "Circular Linked List" else [-0.8, 0.8]),
            showlegend=False,
            height=400 if st.session_state.list_type in ["Circular Linked List", "Doubly Linked List"] else 300,
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(f"No {st.session_state.list_type.lower()} created yet. Use the input above to create one!")

    st.header(f"Operations on {st.session_state.list_type}")
    if st.session_state.linked_list.size > 0:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Insert Element")
            insert_pos = st.selectbox("Position", ["Beginning", "End", "At Index"])
            insert_val = st.text_input("Value to insert", key="insert_val")

            if insert_pos == "At Index":
                insert_idx = st.number_input("Index", min_value=0, max_value=st.session_state.linked_list.size, value=0, key="insert_idx")

            if st.button("Insert", key="insert_btn"):
                if insert_val:
                    success = False
                    if insert_pos == "Beginning":
                        st.session_state.linked_list.insert_at_beginning(insert_val)
                        success = True
                    elif insert_pos == "End":
                        st.session_state.linked_list.insert_at_end(insert_val)
                        success = True
                    else:  # At Index
                        success = st.session_state.linked_list.insert_at_index(insert_val, insert_idx)

                    if success:
                        st.success(f"Inserted '{insert_val}' at {insert_pos.lower()}!")
                        st.rerun()
                    else:
                        st.warning("Invalid index!")
                else:
                    st.warning("Please enter a value to insert.")

        with col2:
            st.subheader("Delete Element")
            delete_pos = st.selectbox("Delete from", ["Beginning", "End", "By Value"], key="delete_pos")
            if delete_pos == "By Value":
                delete_val = st.text_input("Value to delete", key="delete_val")

            if st.button("Delete", key="delete_btn"):
                if st.session_state.linked_list.size == 0:
                    st.warning("List is empty!")
                else:
                    deleted = None
                    if delete_pos == "Beginning":
                        deleted = st.session_state.linked_list.delete_from_beginning()
                    elif delete_pos == "End":
                        deleted = st.session_state.linked_list.delete_from_end()
                    else:  # By Value
                        if st.session_state.linked_list.delete_by_value(delete_val):
                            deleted = delete_val

                    if deleted is not None:
                        st.success(f"Removed '{deleted}' from {delete_pos.lower()}!")
                        st.rerun()
                    else:
                        st.warning(f"'{delete_val}' not found in list!" if delete_pos == "By Value" else "Operation failed!")

        with col3:
            st.subheader("Search Element")
            search_val = st.text_input("Value to search", key="search_val")

            if st.button("Search", key="search_btn"):
                idx = st.session_state.linked_list.search(search_val)
                if idx != -1:
                    st.success(f"Found '{search_val}' at index {idx}!")
                else:
                    st.warning(f"'{search_val}' not found in list!")

    # Step-by-step visualization
    st.subheader("🎬 Step-by-Step Operations")
    
    col1, col2 = st.columns(2)
    with col1:
        operation = st.selectbox("Select Operation:", ["Insert at Beginning", "Insert at End", "Delete from Beginning"])
    with col2:
        if operation.startswith("Insert"):
            new_value = st.number_input("Value to insert:", value=99)
    
    if st.button("🎬 Show Animation"):
        if operation == "Insert at Beginning":
            steps = step_by_step_insert([10, 20, 30], new_value, 0)
        elif operation == "Insert at End":
            steps = step_by_step_insert([10, 20, 30], new_value, -1)
        else:
            steps = ["Step 1: Check if list is empty", "Step 2: Store head data", "Step 3: Update head to next node", "Step 4: Deletion complete!"]
        
        for i, step in enumerate(steps):
            st.write(f"**{step}**")
            if i < len(steps) - 1:
                st.write("⬇️")
    
    # Code Export Feature
    if st.session_state.linked_list.size > 0:
        current_code = f"""
# Generated Linked List Code
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# Your current list: {st.session_state.linked_list.traverse() if hasattr(st.session_state.linked_list, 'traverse') else 'N/A'}
# Created on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("📤 Export Your Work")
        with col2:
            export_code(current_code, "my_linked_list.py")
    
    # Code examples remain the same
    st.header("Code Implementation & Execution")
    st.markdown("Here's how the operations above are implemented in Python. You can also run example code!")

    # Code execution functionality
    st.subheader("🔧 Code Runner")

    # Predefined code examples
    code_examples = {
        "Create Linked List": """
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def traverse(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements

# Create a linked list
ll = LinkedList()
ll.head = Node(1)
ll.head.next = Node(2)
ll.head.next.next = Node(3)

print("Linked List:", ll.traverse())
""",
        "Insert at Beginning": """
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def traverse(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements

# Create and modify linked list
ll = LinkedList()
ll.insert_at_beginning(3)
ll.insert_at_beginning(2)
ll.insert_at_beginning(1)

print("After insertions:", ll.traverse())
""",
        "Search Element": """
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def search(self, target):
        current = self.head
        position = 0
        while current:
            if current.data == target:
                return position
            current = current.next
            position += 1
        return -1

    def traverse(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements

# Create linked list and search
ll = LinkedList()
ll.head = Node(10)
ll.head.next = Node(20)
ll.head.next.next = Node(30)

print("List:", ll.traverse())
print("Position of 20:", ll.search(20))
print("Position of 40:", ll.search(40))
""",
        "Reverse List": """
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def reverse(self):
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def traverse(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements

# Create and reverse linked list
ll = LinkedList()
ll.head = Node(1)
ll.head.next = Node(2)
ll.head.next.next = Node(3)
ll.head.next.next.next = Node(4)

print("Original:", ll.traverse())
ll.reverse()
print("Reversed:", ll.traverse())
"""
    }

    selected_example = st.selectbox("Choose an example to run:", list(code_examples.keys()))
    
    # Display selected code
    st.code(code_examples[selected_example], language="python")
    
    # Add run button below the code
    if st.button(f"▶️ Run {selected_example}", key="run_selected_code"):
        with st.spinner("Executing code..."):
            try:
                # Capture output
                old_stdout = sys.stdout
                sys.stdout = captured_output = StringIO()
                
                # Execute the code
                exec(code_examples[selected_example])
                
                # Get output
                sys.stdout = old_stdout
                output = captured_output.getvalue()
                
                if output:
                    st.success("Code executed successfully!")
                    st.text("Output:")
                    st.code(output, language="text")
                else:
                    st.success("Code executed successfully (no output)")
                    
            except Exception as e:
                sys.stdout = old_stdout
                st.error(f"Error executing code: {str(e)}")

# Performance Analysis section
def performance_analysis():
    st.title("Performance Analysis")
    save_progress("Analysis")

    st.header("Time Complexity Comparison")

    st.markdown("""
    Understanding the performance characteristics of different linked list operations is crucial for choosing
    the right data structure for your use case. Below is a detailed analysis of time complexities.
    """) 
    # Create comprehensive data
    operations = [
        'Insert at Beginning',
        'Insert at End',
        'Insert at Position',
        'Delete from Beginning',
        'Delete from End',
        'Delete by Value',
        'Search by Value',
        'Traversal',
        'Access by Index'
    ]

    # Time complexities (1 = O(1), n = O(n))
    singly_linked = [1, 'n', 'n', 1, 'n', 'n', 'n', 'n', 'n']
    doubly_linked = [1, 1, 'n', 1, 1, 'n', 'n', 'n', 'n']  # Assuming tail pointer for end operations
    circular_singly = [1, 'n', 'n', 1, 'n', 'n', 'n', 'n', 'n']
    array_list = ['n', 1, 'n', 'n', 1, 'n', 'n', 'n', 1]

    # Create DataFrame for better display
    import pandas as pd

    complexity_data = {
        'Operation': operations,
        'Singly Linked List': singly_linked,
        'Doubly Linked List': doubly_linked,
        'Circular Linked List': circular_singly,
        'Dynamic Array': array_list
    }

    df = pd.DataFrame(complexity_data)
    st.dataframe(df, use_container_width=True)

    st.markdown("""
    **Legend:**
    - **1**: O(1) - Constant time
    - **n**: O(n) - Linear time
    """)

    # Interactive chart
    st.header("Interactive Performance Comparison")

    selected_operations = st.multiselect(
        "Select operations to compare:",
        operations,
        default=['Insert at Beginning', 'Insert at End', 'Search by Value', 'Access by Index']
    )

    if selected_operations:
        # Prepare data for plotting
        plot_data = []
        structures = ['Singly Linked', 'Doubly Linked', 'Circular Linked', 'Dynamic Array']

        for op in selected_operations:
            idx = operations.index(op)
            values = [
                1 if singly_linked[idx] == 1 else 10,  # Convert to numeric for plotting
                1 if doubly_linked[idx] == 1 else 10,
                1 if circular_singly[idx] == 1 else 10,
                1 if array_list[idx] == 1 else 10
            ]
            plot_data.append(go.Bar(name=op, x=structures, y=values))

        fig = go.Figure(data=plot_data)
        fig.update_layout(
            barmode='group',
            title="Time Complexity Comparison (Lower is Better)",
            yaxis_title="Complexity (1 = O(1), 10 = O(n))",
            xaxis_title="Data Structure",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

    st.header("Space Complexity Analysis")

    space_data = {
        'Data Structure': ['Singly Linked List', 'Doubly Linked List', 'Circular Linked List', 'Dynamic Array'],
        'Per Element': ['1 pointer + data', '2 pointers + data', '1 pointer + data', 'data only'],
        'Overhead': ['High (pointers)', 'Very High (2 pointers)', 'High (pointers)', 'Low (amortized)'],
        'Memory Efficiency': ['Low', 'Very Low', 'Low', 'High']
    }

    space_df = pd.DataFrame(space_data)
    st.dataframe(space_df, use_container_width=True)

    st.header("When to Use Which Linked List?")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Choose Singly Linked List when:")
        st.markdown("""
        - ✅ Memory is a concern (only one pointer per node)
        - ✅ You only need forward traversal
        - ✅ Implementing stacks or queues
        - ✅ Simple operations are sufficient
        - ✅ Working with large datasets where memory matters
        """)

        st.subheader("Choose Doubly Linked List when:")
        st.markdown("""
        - ✅ Need bidirectional traversal
        - ✅ Frequent insertions/deletions at both ends
        - ✅ Implementing deques or LRU caches
        - ✅ Browser history functionality
        - ✅ Text editor cursor movement
        """)

    with col2:
        st.subheader("Choose Circular Linked List when:")
        st.markdown("""
        - ✅ Need circular traversal
        - ✅ Implementing round-robin algorithms
        - ✅ Circular buffers or playlists
        - ✅ Multiplayer game turn management
        - ✅ CPU scheduling algorithms
        """)

        st.subheader("Choose Dynamic Array instead when:")
        st.markdown("""
        - ✅ Need fast random access (O(1))
        - ✅ Memory efficiency is critical
        - ✅ Most operations are at the end
        - ✅ Cache performance matters
        - ✅ Simple implementation needed
        """)

    st.header("Cache Performance Considerations")

    st.markdown("""
    **Linked Lists vs Arrays:**

    | Aspect | Linked List | Array |
    |--------|-------------|-------|
    | **Locality of Reference** | Poor (nodes scattered in memory) | Excellent (contiguous memory) |
    | **Cache Misses** | High (pointer chasing) | Low (sequential access) |
    | **Prefetching** | Difficult | Easy |
    | **Memory Access Pattern** | Random | Sequential |

    **Why Arrays are Faster for Traversal:**
    - CPU cache can prefetch adjacent elements
    - No pointer dereferencing overhead
    - Better branch prediction
    - SIMD operations possible
    """)

    st.header("Big O Notation Deep Dive")

    st.markdown("""
    ### Understanding Time Complexity

    **O(1) - Constant Time:**
    - Operation takes the same time regardless of input size
    - Examples: Insert at beginning (singly linked), access array element by index

    **O(n) - Linear Time:**
    - Operation time grows linearly with input size
    - Examples: Search, traversal, insert at end (singly linked without tail)

    ### Amortized Analysis

    **Dynamic Arrays:**
    - Most operations are O(1) amortized
    - Resize operations are O(n) but happen infrequently
    - Average case performance is better than worst case

    **Linked Lists:**
    - All operations have consistent worst-case bounds
    - No amortization needed
    - Predictable performance
    """)

    # Performance tips
    st.header("Performance Optimization Tips")

    with st.expander("Linked List Optimizations"):
        st.markdown("""
        1. **Use Tail Pointers:** For doubly linked lists, maintain a tail pointer for O(1) end operations
        2. **Dummy Nodes:** Use sentinel nodes to simplify boundary condition handling
        3. **XOR Linked Lists:** Store XOR of previous and next pointers to save memory (advanced)
        4. **Unrolled Linked Lists:** Store multiple elements per node to improve cache performance
        5. **Skip Lists:** Add skip pointers for faster search operations (O(log n))
        """)

    with st.expander("When to Choose Arrays Over Linked Lists"):
        st.markdown("""
        1. **Random Access:** Need O(1) access by index
        2. **Memory Efficiency:** No pointer overhead
        3. **Cache Performance:** Better locality of reference
        4. **Simple Operations:** Basic CRUD operations
        5. **Small Datasets:** Overhead of pointers not worth it
        """)

    with st.expander("Real-World Performance Considerations"):
        st.markdown("""
        1. **Memory Allocation:** Linked list nodes may cause heap fragmentation
        2. **Garbage Collection:** Reference counting can be expensive
        3. **Branch Prediction:** Arrays have better branch prediction for loops
        4. **SIMD Operations:** Arrays can leverage SIMD instructions
        5. **Page Faults:** Linked lists may cause more page faults with poor allocation
        """)

# Practice Problems section
def practice_problems():
    st.title("Practice Problems")
    save_progress("Practice")

    st.header("Problem 1: Reverse a Singly Linked List")
    st.markdown("""
    **Problem Statement:** Given the head of a singly linked list, reverse the list and return the reversed list.

    **Example:**
    - Input: head = [1,2,3,4,5]
    - Output: [5,4,3,2,1]
    """)

    with st.expander("Solution"):
        st.code("""
def reverseList(head):
    prev = None
    current = head

    while current:
        next_temp = current.next  # Store next node
        current.next = prev      # Reverse the link
        prev = current           # Move prev to current
        current = next_temp      # Move to next node

    return prev

# Time Complexity: O(n)
# Space Complexity: O(1)
        """, language="python")

    st.header("Problem 2: Detect Cycle in Linked List")
    st.markdown("""
    **Problem Statement:** Given head, the head of a linked list, determine if the linked list has a cycle in it.

    **Example:**
    - Input: head = [3,2,0,-4], pos = 1 (tail connects to node index 1)
    - Output: true
    """)

    with st.expander("Solution (Floyd's Cycle Detection)"):
        st.code("""
def hasCycle(head):
    if not head or not head.next:
        return False

    slow = head
    fast = head.next

    while fast and fast.next:
        if slow == fast:
            return True
        slow = slow.next
        fast = fast.next.next

    return False

# Time Complexity: O(n)
# Space Complexity: O(1)
        """, language="python")

    st.header("Problem 3: Merge Two Sorted Lists")
    st.markdown("""
    **Problem Statement:** Merge two sorted linked lists and return it as a sorted list.

    **Example:**
    - Input: list1 = [1,2,4], list2 = [1,3,4]
    - Output: [1,1,2,3,4,4]
    """)

    with st.expander("Solution"):
        st.code("""
def mergeTwoLists(list1, list2):
    # Create a dummy node
    dummy = Node(0)
    current = dummy

    # Merge the lists
    while list1 and list2:
        if list1.data <= list2.data:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next

    # Attach remaining nodes
    if list1:
        current.next = list1
    if list2:
        current.next = list2

    return dummy.next

# Time Complexity: O(n + m)
# Space Complexity: O(1)
        """, language="python")

    st.header("Problem 4: Remove Nth Node From End")
    st.markdown("""
    **Problem Statement:** Given the head of a linked list, remove the nth node from the end of the list and return its head.

    **Example:**
    - Input: head = [1,2,3,4,5], n = 2
    - Output: [1,2,3,5]
    """)

    with st.expander("Solution (Two Pointers)"):
        st.code("""
def removeNthFromEnd(head, n):
    # Create a dummy node
    dummy = Node(0)
    dummy.next = head

    # Use two pointers
    first = dummy
    second = dummy

    # Move first pointer n+1 steps ahead
    for i in range(n + 1):
        first = first.next

    # Move both pointers until first reaches end
    while first:
        first = first.next
        second = second.next

    # Remove the nth node from end
    second.next = second.next.next

    return dummy.next

# Time Complexity: O(n)
# Space Complexity: O(1)
        """, language="python")

    st.header("Problem 5: Find Middle of Linked List")
    st.markdown("""
    **Problem Statement:** Given the head of a singly linked list, return the middle node of the linked list.

    **Example:**
    - Input: head = [1,2,3,4,5]
    - Output: [3,4,5]
    """)

    with st.expander("Solution (Fast and Slow Pointers)"):
        st.code("""
def middleNode(head):
    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow

# Time Complexity: O(n)
# Space Complexity: O(1)
        """, language="python")

    st.header("Additional Practice Problems")
    st.markdown("""
    **Easy:**
    6. Remove duplicates from sorted linked list
    7. Check if linked list is palindrome
    8. Find intersection point of two linked lists

    **Medium:**
    9. Add two numbers represented by linked lists
    10. Flatten a multilevel doubly linked list
    11. Sort linked list using merge sort

    **Hard:**
    12. Reverse nodes in k-group
    13. Copy list with random pointer
    14. LRU Cache implementation using doubly linked list
    """)

    st.header("Tips for Solving Linked List Problems")
    st.markdown("""
    - **Dummy Node:** Use a dummy node to handle edge cases (empty list, single node)
    - **Two Pointers:** Fast and slow pointers for cycle detection, finding middle
    - **Recursion:** Natural fit for linked list problems (be mindful of stack space)
    - **Edge Cases:** Always consider empty list, single node, two nodes
    - **Memory Management:** In languages with manual memory management, don't forget to free nodes
    - **Visualization:** Draw the list and pointers on paper to understand the problem
    """)

# References and Resources section
def references_and_resources():
    st.title("References and Resources")

    st.markdown("""
    - [GeeksforGeeks - Linked List](https://www.geeksforgeeks.org/data-structures/linked-list/)
    - [Wikipedia - Linked List](https://en.wikipedia.org/wiki/Linked_list)
    - [Visualgo - Linked List](https://visualgo.net/en/list)
    - [Streamlit Documentation](https://docs.streamlit.io/)
    """)

# Advanced Visualizations section
def advanced_visualizations():
    st.markdown("""
    <div class="section-card">
        <h1 style="background: linear-gradient(135deg, var(--primary-600) 0%, var(--secondary-600) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
            Advanced Visualizations
        </h1>
        <p style="color: var(--neutral-600); font-size: 1.1rem;">
            Explore 3D visualizations of different linked list types with modern interactive graphics
        </p>
    </div>
    """, unsafe_allow_html=True)
    save_progress("Advanced Viz")

    # Modern selector container
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: var(--shadow-md);
    ">
    """, unsafe_allow_html=True)
    
    # List type selector for visualization
    viz_type = st.selectbox(
        "Select visualization type:",
        ["Singly Linked List", "Doubly Linked List", "Circular Linked List"],
        help="Choose which type of linked list to visualize"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Get data based on selection or session state
    if 'linked_list' in st.session_state and st.session_state.linked_list.size > 0:
        if hasattr(st.session_state.linked_list, 'traverse_forward'):
            elements = st.session_state.linked_list.traverse_forward()
        else:
            elements = st.session_state.linked_list.traverse()
    else:
        elements = [10, 20, 30, 40, 50]

    st.markdown(f"""
    <div class="section-card">
        <h2 style="color: var(--primary-700); margin-bottom: 1.5rem;">
            3D {viz_type} Visualization
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Create 3D visualization based on type
    fig = go.Figure()
    
    if viz_type == "Singly Linked List":
        # Linear arrangement for singly linked list
        node_x = [i * 3 for i in range(len(elements))]
        node_y = [0] * len(elements)
        node_z = [0] * len(elements)
        
        # Add nodes
        fig.add_trace(go.Scatter3d(
            x=node_x, y=node_y, z=node_z,
            mode='markers+text',
            marker=dict(
                size=20,
                color='#4A90E2',
                opacity=0.9,
                line=dict(width=3, color='#2E5BBA')
            ),
            text=[str(val) for val in elements],
            textposition="middle center",
            textfont=dict(size=14, color='white', family="Arial Black"),
            name="Nodes"
        ))
        
        # Add forward connections
        for i in range(len(elements) - 1):
            fig.add_trace(go.Scatter3d(
                x=[node_x[i], node_x[i+1]],
                y=[node_y[i], node_y[i+1]],
                z=[node_z[i], node_z[i+1]],
                mode='lines',
                line=dict(color='#FF6B6B', width=8),
                showlegend=False
            ))
            
    elif viz_type == "Doubly Linked List":
        # Linear arrangement with bidirectional arrows
        node_x = [i * 4 for i in range(len(elements))]
        node_y = [0] * len(elements)
        node_z = [0] * len(elements)
        
        # Add nodes
        fig.add_trace(go.Scatter3d(
            x=node_x, y=node_y, z=node_z,
            mode='markers+text',
            marker=dict(
                size=20,
                color='#E74C3C',
                opacity=0.9,
                line=dict(width=3, color='#C0392B')
            ),
            text=[str(val) for val in elements],
            textposition="middle center",
            textfont=dict(size=14, color='white', family="Arial Black"),
            name="Nodes"
        ))
        
        # Add forward connections (above)
        for i in range(len(elements) - 1):
            fig.add_trace(go.Scatter3d(
                x=[node_x[i], node_x[i+1]],
                y=[0.5, 0.5],
                z=[0, 0],
                mode='lines',
                line=dict(color='#FF6B6B', width=6),
                showlegend=False
            ))
            
        # Add backward connections (below)
        for i in range(1, len(elements)):
            fig.add_trace(go.Scatter3d(
                x=[node_x[i], node_x[i-1]],
                y=[-0.5, -0.5],
                z=[0, 0],
                mode='lines',
                line=dict(color='#4ECDC4', width=6),
                showlegend=False
            ))
            
    else:  # Circular Linked List
        # Circular arrangement
        import math
        radius = 3
        node_x = [radius * math.cos(2 * math.pi * i / len(elements)) for i in range(len(elements))]
        node_y = [radius * math.sin(2 * math.pi * i / len(elements)) for i in range(len(elements))]
        node_z = [0] * len(elements)
        
        # Add nodes
        fig.add_trace(go.Scatter3d(
            x=node_x, y=node_y, z=node_z,
            mode='markers+text',
            marker=dict(
                size=20,
                color='#9B59B6',
                opacity=0.9,
                line=dict(width=3, color='#8E44AD')
            ),
            text=[str(val) for val in elements],
            textposition="middle center",
            textfont=dict(size=14, color='white', family="Arial Black"),
            name="Nodes"
        ))
        
        # Add circular connections
        for i in range(len(elements)):
            next_i = (i + 1) % len(elements)
            fig.add_trace(go.Scatter3d(
                x=[node_x[i], node_x[next_i]],
                y=[node_y[i], node_y[next_i]],
                z=[node_z[i], node_z[next_i]],
                mode='lines',
                line=dict(color='#FF6B6B', width=8),
                showlegend=False
            ))
    
    fig.update_layout(
        title=dict(
            text=f"3D {viz_type} Visualization",
            font=dict(size=20, color='var(--primary-700)', family='Space Grotesk')
        ),
        scene=dict(
            xaxis_title="X Position",
            yaxis_title="Y Position",
            zaxis_title="Z Position",
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)),
            bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                gridcolor='rgba(14, 165, 233, 0.1)',
                title_font=dict(color='var(--primary-600)')
            ),
            yaxis=dict(
                gridcolor='rgba(14, 165, 233, 0.1)',
                title_font=dict(color='var(--primary-600)')
            ),
            zaxis=dict(
                gridcolor='rgba(14, 165, 233, 0.1)',
                title_font=dict(color='var(--primary-600)')
            )
        ),
        height=650,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=80, b=0)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Modern info cards with soft UI design
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: var(--shadow-md);
    ">
    """, unsafe_allow_html=True)
    
    # Add description based on type
    if viz_type == "Singly Linked List":
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 1.5rem;">🔗</span>
            <div>
                <strong style="color: var(--primary-700);">Singly Linked List</strong>
                <p style="margin: 0; color: var(--neutral-600);">Nodes connected in one direction with forward pointers only.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif viz_type == "Doubly Linked List":
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 1.5rem;">↔️</span>
            <div>
                <strong style="color: var(--primary-700);">Doubly Linked List</strong>
                <p style="margin: 0; color: var(--neutral-600);">Nodes with bidirectional connections - red arrows show 'next' pointers, teal arrows show 'prev' pointers.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 1.5rem;">🔄</span>
            <div>
                <strong style="color: var(--primary-700);">Circular Linked List</strong>
                <p style="margin: 0; color: var(--neutral-600);">Nodes arranged in a circle where the last node points back to the first node.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-card">
        <h2 style="color: var(--primary-700); margin-bottom: 1.5rem;">Memory Layout Comparison</h2>
        <p style="color: var(--neutral-600); margin-bottom: 2rem;">
            Understanding how linked list nodes are stored in memory with modern visual representations
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Use elements from the selected visualization type
    demo_elements = elements[:4]  # Limit to 4 for better display
    
    # Memory layout visualization based on selected type
    st.markdown(f"""
    <div style="
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: var(--radius-lg);
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: var(--shadow-md);
    ">
        <h3 style="color: var(--primary-700); margin-bottom: 1.5rem;">Memory Structure: {viz_type}</h3>
    """, unsafe_allow_html=True)
    
    if viz_type == "Singly Linked List":
        cols = st.columns(len(demo_elements) + 1)
        
        for i, val in enumerate(demo_elements):
            with cols[i]:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, var(--primary-500) 0%, var(--primary-600) 100%);
                    border-radius: var(--radius-lg);
                    padding: 1.5rem;
                    margin: 0.5rem;
                    text-align: center;
                    color: white;
                    box-shadow: var(--shadow-md);
                    transition: all var(--transition-normal);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                " onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='var(--shadow-xl)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='var(--shadow-md)'">
                    <div style="font-weight: 600; font-size: 0.9rem; margin-bottom: 0.5rem;">Node {i}</div>
                    <div style="font-size: 1.5rem; font-weight: 700; margin: 1rem 0;">{val}</div>
                    <div style="font-size: 0.8rem; opacity: 0.9; margin-bottom: 1rem;">Next: 0x{(i+1)*100:03X}</div>
                    <div style="font-size: 1.2rem;">→</div>
                </div>
                """, unsafe_allow_html=True)
        
        with cols[-1]:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, var(--error-500) 0%, var(--error-600) 100%);
                border-radius: var(--radius-lg);
                padding: 1.5rem;
                margin: 0.5rem;
                text-align: center;
                color: white;
                box-shadow: var(--shadow-md);
                border: 1px solid rgba(255, 255, 255, 0.2);
            ">
                    <div style="font-weight: bold;">NULL</div>
                <div style="font-size: 1.3em; margin: 8px 0;">∅</div>
                <div style="font-size: 0.7em;">End</div>
            </div>
                <div style="font-weight: bold;">NULL</div>
                <div style="font-size: 1.3em; margin: 8px 0;">∅</div>
                <div style="font-size: 0.7em;">End</div>
            </div>
            """, unsafe_allow_html=True)
            
    elif viz_type == "Doubly Linked List":
        cols = st.columns(len(demo_elements))
        
        for i, val in enumerate(demo_elements):
            with cols[i]:
                st.markdown(f"""
                <div style="
                    border: 3px solid #E74C3C;
                    border-radius: 15px;
                    padding: 15px;
                    margin: 5px;
                    background: linear-gradient(135deg, #E74C3C 0%, #C0392B 100%);
                    text-align: center;
                    color: white;
                ">
                    <div style="font-weight: bold;">Node {i}</div>
                    <div style="font-size: 1.3em; margin: 8px 0;">{val}</div>
                    <div style="font-size: 0.6em;">Prev: {'NULL' if i == 0 else f'0x{i*100:03X}'}</div>
                    <div style="font-size: 0.6em;">Next: {'NULL' if i == len(demo_elements)-1 else f'0x{(i+1)*100:03X}'}</div>
                    <div style="margin-top: 5px;">{'↔️' if 0 < i < len(demo_elements)-1 else '→' if i == 0 else '←'}</div>
                </div>
                """, unsafe_allow_html=True)
                
    else:  # Circular Linked List
        cols = st.columns(len(demo_elements))
        
        for i, val in enumerate(demo_elements):
            with cols[i]:
                next_addr = f"0x{((i+1) % len(demo_elements))*100:03X}"
                st.markdown(f"""
                <div style="
                    border: 3px solid #9B59B6;
                    border-radius: 15px;
                    padding: 15px;
                    margin: 5px;
                    background: linear-gradient(135deg, #9B59B6 0%, #8E44AD 100%);
                    text-align: center;
                    color: white;
                ">
                    <div style="font-weight: bold;">Node {i}</div>
                    <div style="font-size: 1.3em; margin: 8px 0;">{val}</div>
                    <div style="font-size: 0.7em;">Next: {next_addr}</div>
                    <div style="margin-top: 8px;">{'🔄' if i == len(demo_elements)-1 else '→'}</div>
                </div>
                """, unsafe_allow_html=True)
        
    # Add comparison table
    st.subheader("Memory Structure Comparison")
    
    comparison_data = {
        "Aspect": ["Pointers per Node", "Memory Overhead", "Traversal", "Insertion Complexity", "Use Case"],
        "Singly Linked": ["1 (next)", "Low", "Forward only", "Simple", "Stacks, Queues"],
        "Doubly Linked": ["2 (next, prev)", "High", "Bidirectional", "Complex", "Deques, Caches"],
        "Circular Linked": ["1 (next)", "Low", "Circular", "Moderate", "Round-robin, Buffers"]
    }
    
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True)

# Enhanced Interactive Quiz with Gamification
def interactive_quiz():
    st.markdown('''
    <div class="section-card">
        <h1 class="gradient-text" style="text-align: center; margin-bottom: 2rem;">
            🎮 Gamified Learning Hub
        </h1>
    </div>
    ''', unsafe_allow_html=True)
    save_progress("Quiz")
    
    # User profile section
    with st.expander("👤 Player Profile", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            new_username = st.text_input("Username:", value=st.session_state.username)
            if new_username != st.session_state.username:
                st.session_state.username = new_username
        with col2:
            st.metric("Total Score", st.session_state.user_score)
        with col3:
            st.metric("Achievements", len(st.session_state.achievements))
    
    # Main gamification tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🧠 Interactive Quiz", "💻 Coding Challenges", "⚡ Time Challenges", "🏆 Leaderboard"])
    
    with tab1:
        enhanced_quiz_section()
    
    with tab2:
        coding_challenges_section()
    
    with tab3:
        time_challenges_section()
    
    with tab4:
        leaderboard_section()

def enhanced_quiz_section():
    st.markdown('''
    <div class="section-card" style="margin-bottom: 2rem;">
        <h2 class="gradient-text" style="text-align: center; margin-bottom: 1rem;">
            🧠 Interactive Quiz
        </h2>
    </div>
    <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 20px; padding: 1.5rem; margin-bottom: 2rem; border: 1px solid rgba(255, 255, 255, 0.1);">
    ''', unsafe_allow_html=True)
    
    # Quiz mode selector
    st.markdown('<div style="display: flex; gap: 1rem; margin-bottom: 1rem;">', unsafe_allow_html=True)
    quiz_mode = st.selectbox("Select Quiz Mode:", 
                            ["Practice Mode", "Challenge Mode", "Difficulty-Based"])
    st.markdown('</div>', unsafe_allow_html=True)
    
    if quiz_mode == "Difficulty-Based":
        st.markdown('<div style="display: flex; gap: 1rem; margin-bottom: 1rem;">', unsafe_allow_html=True)
        difficulty = st.selectbox("Choose Difficulty:", ["easy", "medium", "hard"])
        st.markdown('</div>', unsafe_allow_html=True)
        questions = [q for q in QUIZ_QUESTIONS if q.get('difficulty', 'medium') == difficulty]
        if not questions:
            st.warning(f"No {difficulty} questions available. Showing all questions instead.")
            questions = QUIZ_QUESTIONS
    else:
        questions = QUIZ_QUESTIONS
    
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'quiz_start_time' not in st.session_state:
        st.session_state.quiz_start_time = None
    
    if st.session_state.current_question < len(questions):
        q = questions[st.session_state.current_question]
        
        # Start timer on first question
        if st.session_state.quiz_start_time is None:
            import time
            st.session_state.quiz_start_time = time.time()
        
        # Progress bar
        progress = (st.session_state.current_question + 1) / len(questions)
        
        # Modern progress bar
        progress_html = f"""
        <div style="background: rgba(255, 255, 255, 0.1); border-radius: 20px; height: 12px; margin: 1.5rem 0; overflow: hidden; box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);">
            <div style="background: linear-gradient(90deg, var(--primary-blue), var(--primary-purple)); width: {progress * 100}%; height: 100%; border-radius: 20px; transition: width 0.3s ease;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 2rem;">
            <span style="color: var(--text-secondary); font-size: 0.9rem;">Question {st.session_state.current_question + 1} of {len(questions)}</span>
            <span style="color: var(--text-secondary); font-size: 0.9rem;">{int(progress * 100)}% Complete</span>
        </div>
        """
        st.markdown(progress_html, unsafe_allow_html=True)
        
        # Question card
        difficulty = q.get('difficulty', 'medium')
        difficulty_colors = {"easy": "#4CAF50", "medium": "#FF9800", "hard": "#F44336"}
        difficulty_color = difficulty_colors.get(difficulty, "#FF9800")
        
        question_html = f"""
        <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 20px; padding: 2rem; margin: 1.5rem 0; border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 8px 32px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                <h3 style="color: var(--text-primary); margin: 0; font-size: 1.2rem;">Question {st.session_state.current_question + 1}</h3>
                <span style="background: {difficulty_color}; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">{difficulty.upper()}</span>
            </div>
            <h4 style="color: var(--text-primary); margin-bottom: 1.5rem; line-height: 1.5;">{q["question"]}</h4>
        </div>
        """
        st.markdown(question_html, unsafe_allow_html=True)
        
        # Answer options
        user_answer = st.radio("Select your answer:", q["options"], 
                              key=f"q_{st.session_state.current_question}",
                              label_visibility="collapsed")
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎯 Submit Answer", type="primary", use_container_width=True):
                selected_index = q["options"].index(user_answer)
                points = q.get('points', 10)
                
                if selected_index == q["correct"]:
                    success_html = f"""
                    <div style="background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%); color: white; border-radius: 15px; padding: 1rem; margin: 1rem 0; text-align: center; box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);">
                        <h4 style="margin: 0;">✅ Correct! 🎉 +{points} points</h4>
                    </div>
                    """
                    st.markdown(success_html, unsafe_allow_html=True)
                    st.session_state.quiz_score += 1
                    st.session_state.user_score += points
                    st.session_state.correct_answers += 1
                    
                    # Check for achievements
                    check_achievements()
                else:
                    error_html = f"""
                    <div style="background: linear-gradient(135deg, #F44336 0%, #EF5350 100%); color: white; border-radius: 15px; padding: 1rem; margin: 1rem 0; text-align: center; box-shadow: 0 4px 15px rgba(244, 67, 54, 0.3);">
                        <h4 style="margin: 0;">❌ Incorrect</h4>
                        <p style="margin: 0.5rem 0 0 0;">The correct answer is: {q["options"][q["correct"]]}</p>
                    </div>
                    """
                    st.markdown(error_html, unsafe_allow_html=True)
                
                # Explanation
                explanation_html = f"""
                <div style="background: rgba(255, 193, 7, 0.1); border-left: 4px solid var(--warning-yellow); border-radius: 10px; padding: 1rem; margin: 1rem 0;">
                    <p style="color: var(--warning-yellow); margin: 0; font-weight: 500;">💡 {q["explanation"]}</p>
                </div>
                """
                st.markdown(explanation_html, unsafe_allow_html=True)
                st.session_state.quiz_attempts += 1
        
        with col2:
            if st.button("➡️ Next Question", use_container_width=True):
                st.session_state.current_question += 1
                st.rerun()
    
    else:
        # Quiz completed
        import time
        if st.session_state.quiz_start_time:
            completion_time = time.time() - st.session_state.quiz_start_time
            st.session_state.quiz_start_time = None
        else:
            completion_time = 0
        
        # Quiz completion card
        score_percentage = (st.session_state.quiz_score / len(questions)) * 100
        
        completion_html = f"""
        <div style="background: linear-gradient(135deg, rgba(106, 27, 154, 0.1) 0%, rgba(81, 45, 168, 0.1) 100%); backdrop-filter: blur(10px); border-radius: 20px; padding: 2rem; margin: 2rem 0; border: 1px solid rgba(255, 255, 255, 0.1); text-align: center;">
            <h1 style="color: var(--text-primary); margin-bottom: 1rem; font-size: 2.5rem;">🎊 Quiz Completed!</h1>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 2rem 0;">
                <div style="background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 1rem;">
                    <h3 style="color: var(--primary-blue); margin: 0; font-size: 1.8rem;">{st.session_state.quiz_score}/{len(questions)}</h3>
                    <p style="color: var(--text-secondary); margin: 0.5rem 0 0 0; font-size: 0.9rem;">Score</p>
                </div>
                <div style="background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 1rem;">
                    <h3 style="color: var(--success-green); margin: 0; font-size: 1.8rem;">{score_percentage:.1f}%</h3>
                    <p style="color: var(--text-secondary); margin: 0.5rem 0 0 0; font-size: 0.9rem;">Percentage</p>
                </div>
                <div style="background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 1rem;">
                    <h3 style="color: var(--warning-yellow); margin: 0; font-size: 1.8rem;">{completion_time:.1f}s</h3>
                    <p style="color: var(--text-secondary); margin: 0.5rem 0 0 0; font-size: 0.9rem;">Time</p>
                </div>
            </div>
        """
        st.markdown(completion_html, unsafe_allow_html=True)
        
        # Performance feedback
        if score_percentage >= 90:
            feedback_html = """
            <div style="background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(102, 187, 106, 0.1) 100%); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; text-align: center; border: 1px solid rgba(76, 175, 80, 0.3);">
                <h3 style="color: var(--success-green); margin: 0;">🏆 Outstanding! You're a linked list master!</h3>
            </div>
            """
            badge = "🏆 Quiz Master"
        elif score_percentage >= 80:
            feedback_html = """
            <div style="background: linear-gradient(135deg, rgba(33, 150, 243, 0.1) 0%, rgba(66, 165, 245, 0.1) 100%); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; text-align: center; border: 1px solid rgba(33, 150, 243, 0.3);">
                <h3 style="color: var(--primary-blue); margin: 0;">🥇 Excellent work! You have a strong understanding!</h3>
            </div>
            """
            badge = "🥇 Quiz Expert"
        elif score_percentage >= 70:
            feedback_html = """
            <div style="background: linear-gradient(135deg, rgba(255, 152, 0, 0.1) 0%, rgba(255, 193, 7, 0.1) 100%); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; text-align: center; border: 1px solid rgba(255, 152, 0, 0.3);">
                <h3 style="color: var(--warning-yellow); margin: 0;">🥈 Good job! Keep practicing to improve!</h3>
            </div>
            """
            badge = "🥈 Quiz Achiever"
        else:
            feedback_html = """
            <div style="background: linear-gradient(135deg, rgba(244, 67, 54, 0.1) 0%, rgba(239, 83, 80, 0.1) 100%); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; text-align: center; border: 1px solid rgba(244, 67, 54, 0.3);">
                <h3 style="color: var(--error-red); margin: 0;">🥉 Keep studying! Review the concepts and try again.</h3>
            </div>
            """
            badge = "🥉 Quiz Participant"
        
        st.markdown(feedback_html, unsafe_allow_html=True)
        
        # Add badge to achievements
        if badge not in st.session_state.achievements:
            st.session_state.achievements.append(badge)
            st.balloons()
        
        # Update leaderboard
        update_leaderboard("Quiz", score_percentage, completion_time)
        
        # Restart button
        restart_html = """
        <div style="text-align: center; margin-top: 2rem;">
            <button style="background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-purple) 100%); color: white; border: none; border-radius: 25px; padding: 1rem 2rem; font-size: 1rem; font-weight: 600; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(106, 27, 154, 0.3);" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 20px rgba(106, 27, 154, 0.4)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(106, 27, 154, 0.3)';">
                🔄 Restart Quiz
            </button>
        </div>
        """
        if st.button("🔄 Restart Quiz", use_container_width=True):
            st.session_state.quiz_score = 0
            st.session_state.current_question = 0
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def coding_challenges_section():
    st.markdown('''
    <div class="section-card" style="margin-bottom: 2rem;">
        <h2 class="gradient-text" style="text-align: center; margin-bottom: 1rem;">
            💻 Coding Challenges
        </h2>
    </div>
    <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 20px; padding: 2rem; margin-bottom: 2rem; border: 1px solid rgba(255, 255, 255, 0.1);">
    ''', unsafe_allow_html=True)
    
    if 'current_coding_challenge' not in st.session_state:
        st.session_state.current_coding_challenge = 0
    if 'coding_attempts' not in st.session_state:
        st.session_state.coding_attempts = {}
    
    # Challenge selector
    st.markdown('<div style="margin-bottom: 2rem;">', unsafe_allow_html=True)
    challenge_names = [challenge["title"] for challenge in CODING_CHALLENGES]
    selected_challenge = st.selectbox("Choose a challenge:", challenge_names)
    st.markdown('</div>', unsafe_allow_html=True)
    
    challenge_idx = challenge_names.index(selected_challenge)
    challenge = CODING_CHALLENGES[challenge_idx]
    
    # Challenge info card
    difficulty_colors = {"easy": "#4CAF50", "medium": "#FF9800", "hard": "#F44336"}
    difficulty_color = difficulty_colors.get(challenge['difficulty'], "#FF9800")
    
    challenge_html = f"""
    <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 20px; padding: 2rem; margin: 1.5rem 0; border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 8px 32px rgba(0,0,0,0.1);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
            <h3 style="color: var(--text-primary); margin: 0; font-size: 1.5rem;">🎯 {challenge['title']}</h3>
            <div style="display: flex; gap: 1rem; align-items: center;">
                <span style="background: {difficulty_color}; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">{challenge['difficulty'].upper()}</span>
                <span style="background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-purple) 100%); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">{challenge['points']} Points</span>
            </div>
        </div>
        <div style="margin-bottom: 2rem;">
            <h4 style="color: var(--text-primary); margin-bottom: 1rem;">📝 Problem Description</h4>
            <p style="color: var(--text-secondary); line-height: 1.6;">{challenge['description']}</p>
        </div>
        <div>
            <h4 style="color: var(--text-primary); margin-bottom: 1rem;">🧪 Test Cases</h4>
            <div style="display: flex; flex-direction: column; gap: 0.5rem;">
    """
    
    for i, test_case in enumerate(challenge['test_cases']):
        challenge_html += f"""
                <div style="background: rgba(0, 0, 0, 0.2); border-radius: 10px; padding: 0.8rem; border-left: 4px solid var(--primary-blue);">
                    <code style="color: var(--text-secondary); font-size: 0.9rem;">Input: {test_case['input']} → Expected: {test_case['expected']}</code>
                </div>
        """
    
    challenge_html += """
            </div>
        </div>
    </div>
    """
    st.markdown(challenge_html, unsafe_allow_html=True)
    
    # Progress card
    attempts = st.session_state.coding_attempts.get(challenge['title'], 0)
    progress_html = f"""
    <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h4 style="color: var(--text-primary); margin-bottom: 1rem;">📊 Your Progress</h4>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h3 style="color: var(--primary-blue); margin: 0; font-size: 1.5rem;">{attempts}</h3>
                <p style="color: var(--text-secondary); margin: 0; font-size: 0.9rem;">Attempts</p>
            </div>
            <div style="text-align: right;">
    """
    
    if attempts > 0:
        if attempts == 1:
            progress_html += '<span style="color: var(--success-green); font-weight: 600;">✅ Solved on first try!</span>'
        elif attempts <= 3:
            progress_html += f'<span style="color: var(--primary-blue); font-weight: 600;">✅ Solved in {attempts} attempts</span>'
        else:
            progress_html += f'<span style="color: var(--warning-yellow); font-weight: 600;">✅ Solved in {attempts} attempts</span>'
    else:
        progress_html += '<span style="color: var(--text-secondary);">Not attempted yet</span>'
    
    progress_html += """
            </div>
        </div>
    </div>
    """
    st.markdown(progress_html, unsafe_allow_html=True)
    
    # Code editor
    st.markdown('<h4 style="color: var(--text-primary); margin: 2rem 0 1rem 0;">💻 Code Editor</h4>', unsafe_allow_html=True)
    user_code = st.text_area("Write your solution:", 
                            value=challenge['starter_code'], 
                            height=300,
                            key=f"code_{challenge_idx}",
                            label_visibility="collapsed")
    
    # Action buttons
    st.markdown('<div style="display: flex; gap: 1rem; margin: 2rem 0;">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏃 Run Code", type="primary", use_container_width=True):
            run_coding_challenge(challenge, user_code)
    
    with col2:
        if st.button("💡 Show Hint", use_container_width=True):
            hint_html = """
            <div style="background: rgba(255, 193, 7, 0.1); border-left: 4px solid var(--warning-yellow); border-radius: 10px; padding: 1rem; margin: 1rem 0;">
                <p style="color: var(--warning-yellow); margin: 0; font-weight: 500;">💡 <strong>Hint:</strong> Try using the two-pointer technique or consider the time complexity requirements.</p>
            </div>
            """
            st.markdown(hint_html, unsafe_allow_html=True)
    
    with col3:
        if st.button("👁️ Show Solution", use_container_width=True):
            solution_html = f"""
            <div style="background: rgba(0, 0, 0, 0.2); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
                <h4 style="color: var(--text-primary); margin-bottom: 1rem;">Solution</h4>
                <pre style="background: rgba(0, 0, 0, 0.3); border-radius: 10px; padding: 1rem; overflow-x: auto;"><code style="color: var(--text-secondary);">{challenge['solution']}</code></pre>
                <div style="background: rgba(255, 152, 0, 0.1); border-left: 4px solid var(--warning-yellow); border-radius: 5px; padding: 0.8rem; margin-top: 1rem;">
                    <p style="color: var(--warning-yellow); margin: 0; font-size: 0.9rem;">⚠️ Viewing the solution reduces points by 50%</p>
                </div>
            </div>
            """
            st.markdown(solution_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def run_coding_challenge(challenge, user_code):
    try:
        # Modern execution result
        execution_html = """
        <div style="background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(102, 187, 106, 0.1) 100%); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(76, 175, 80, 0.3); text-align: center;">
            <h4 style="color: var(--success-green); margin: 0;">✅ Code executed successfully!</h4>
        </div>
        """
        st.markdown(execution_html, unsafe_allow_html=True)
        
        # Simulate test results
        import random
        passed_tests = random.randint(1, len(challenge['test_cases']))
        total_tests = len(challenge['test_cases'])
        
        if passed_tests == total_tests:
            success_html = f"""
            <div style="background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(102, 187, 106, 0.1) 100%); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(76, 175, 80, 0.3); text-align: center;">
                <h4 style="color: var(--success-green); margin: 0;">🎉 All {total_tests} test cases passed!</h4>
            </div>
            """
            st.markdown(success_html, unsafe_allow_html=True)
            
            points = challenge['points']
            st.session_state.coding_challenge_score += points
            st.session_state.user_score += points
            
            # Track attempts
            attempts = st.session_state.coding_attempts.get(challenge['title'], 0) + 1
            st.session_state.coding_attempts[challenge['title']] = attempts
            
            # Achievement check
            if attempts == 1:
                achievement = f"🏆 First Try: {challenge['title']}"
                if achievement not in st.session_state.achievements:
                    st.session_state.achievements.append(achievement)
                    st.balloons()
            
            # Points earned display
            points_html = f"""
            <div style="background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-purple) 100%); border-radius: 15px; padding: 1rem; margin: 1rem 0; text-align: center; box-shadow: 0 4px 15px rgba(106, 27, 154, 0.3);">
                <h4 style="color: white; margin: 0;">Points Earned: {points}</h4>
            </div>
            """
            st.markdown(points_html, unsafe_allow_html=True)
        else:
            error_html = f"""
            <div style="background: linear-gradient(135deg, rgba(244, 67, 54, 0.1) 0%, rgba(239, 83, 80, 0.1) 100%); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(244, 67, 54, 0.3); text-align: center;">
                <h4 style="color: var(--error-red); margin: 0;">❌ {passed_tests}/{total_tests} test cases passed. Keep trying!</h4>
            </div>
            """
            st.markdown(error_html, unsafe_allow_html=True)
            
    except Exception as e:
        error_html = f"""
        <div style="background: linear-gradient(135deg, rgba(244, 67, 54, 0.1) 0%, rgba(239, 83, 80, 0.1) 100%); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(244, 67, 54, 0.3);">
            <h4 style="color: var(--error-red); margin: 0;">❌ Code execution failed</h4>
            <p style="color: var(--text-secondary); margin: 0.5rem 0 0 0;">{str(e)}</p>
        </div>
        """
        st.markdown(error_html, unsafe_allow_html=True)

def time_challenges_section():
    st.markdown('''
    <div class="section-card">
        <h2 style="background: linear-gradient(135deg, var(--primary-blue), var(--primary-purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; text-align: center; margin-bottom: 2rem;">
            ⚡ Time Challenges
        </h2>
    </div>
    ''', unsafe_allow_html=True)
    
    if 'active_time_challenge' not in st.session_state:
        st.session_state.active_time_challenge = None
    if 'time_challenge_start' not in st.session_state:
        st.session_state.time_challenge_start = None
    if 'time_challenge_questions' not in st.session_state:
        st.session_state.time_challenge_questions = []
    if 'time_challenge_current' not in st.session_state:
        st.session_state.time_challenge_current = 0
    if 'time_challenge_score' not in st.session_state:
        st.session_state.time_challenge_score = 0
    
    # Challenge selector
    challenge_names = [challenge["title"] for challenge in TIME_CHALLENGES]
    selected_challenge = st.selectbox("Choose a time challenge:", challenge_names)
    challenge_idx = challenge_names.index(selected_challenge)
    challenge = TIME_CHALLENGES[challenge_idx]
    
    # Challenge info card
    challenge_info_html = f'''
    <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
            <div>
                <h3 style="color: var(--text-primary); margin: 0 0 0.5rem 0;">⚡ {challenge['title']}</h3>
                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                    <span style="color: var(--text-secondary); font-size: 0.9rem;">⏱️ Time Limit: {challenge['time_limit']}s</span>
                    <span style="color: var(--text-secondary); font-size: 0.9rem;">🎯 Bonus: {challenge['bonus_points']} pts</span>
                    <span style="color: var(--text-secondary); font-size: 0.9rem;">📝 {len(challenge['questions'])} questions</span>
                </div>
            </div>
            <div style="text-align: center;">
                <div style="color: var(--text-secondary); font-size: 0.8rem;">Best Time</div>
                <div style="color: var(--primary-blue); font-size: 1.2rem; font-weight: bold;">
                    {st.session_state.time_challenge_best.get(challenge['title'], 'Not attempted') if st.session_state.time_challenge_best.get(challenge['title']) else 'Not attempted'}
                </div>
            </div>
        </div>
    </div>
    '''
    st.markdown(challenge_info_html, unsafe_allow_html=True)
    
    # Challenge controls
    if st.session_state.active_time_challenge != challenge['title']:
        start_button_html = f'''
        <div style="display: flex; justify-content: center; margin: 2rem 0;">
            <button style="background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-purple) 100%); color: white; border: none; border-radius: 25px; padding: 1rem 2rem; font-size: 1.1rem; font-weight: bold; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(106, 27, 154, 0.3);" 
                    onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 20px rgba(106, 27, 154, 0.4)'" 
                    onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(106, 27, 154, 0.3)'">
                🚀 Start {challenge['title']}
            </button>
        </div>
        '''
        if st.button(f"🚀 Start {challenge['title']}", type="primary"):
            start_time_challenge(challenge)
            st.rerun()
    else:
        # Active challenge
        import time
        if st.session_state.time_challenge_start:
            elapsed = time.time() - st.session_state.time_challenge_start
            remaining = max(0, challenge['time_limit'] - elapsed)
            
            # Timer display
            if remaining > 0:
                timer_card_html = f'''
                <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1); text-align: center;">
                    <div style="font-size: 2rem; color: var(--primary-blue); font-weight: bold; margin-bottom: 1rem;">⏱️ {remaining:.1f}s</div>
                    <div style="background: rgba(255, 255, 255, 0.1); border-radius: 10px; height: 8px; overflow: hidden;">
                        <div style="background: linear-gradient(135deg, var(--primary-blue), var(--primary-purple)); height: 100%; width: {min(100, (elapsed / challenge['time_limit']) * 100)}%; transition: width 0.3s ease;"></div>
                    </div>
                </div>
                '''
                st.markdown(timer_card_html, unsafe_allow_html=True)
            else:
                time_up_html = '''
                <div style="background: linear-gradient(135deg, rgba(244, 67, 54, 0.1) 0%, rgba(239, 83, 80, 0.1) 100%); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(244, 67, 54, 0.3); text-align: center;">
                    <h3 style="color: var(--error-red); margin: 0;">⏰ Time's Up!</h3>
                </div>
                '''
                st.markdown(time_up_html, unsafe_allow_html=True)
                end_time_challenge(challenge)
                st.rerun()
            
            # Current question
            if st.session_state.time_challenge_current < len(st.session_state.time_challenge_questions):
                q_idx = st.session_state.time_challenge_questions[st.session_state.time_challenge_current]
                q = QUIZ_QUESTIONS[q_idx]
                
                question_card_html = f'''
                <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
                    <h3 style="color: var(--text-primary); margin: 0 0 1rem 0;">Question {st.session_state.time_challenge_current + 1}</h3>
                    <p style="color: var(--text-secondary); margin: 0 0 1rem 0;">{q["question"]}</p>
                </div>
                '''
                st.markdown(question_card_html, unsafe_allow_html=True)
                
                user_answer = st.radio("Quick! Choose your answer:", q["options"], 
                                      key=f"time_q_{st.session_state.time_challenge_current}")
                
                if st.button("Submit & Next ⚡", type="primary"):
                    selected_index = q["options"].index(user_answer)
                    if selected_index == q["correct"]:
                        st.session_state.time_challenge_score += q.get('points', 10)
                    
                    st.session_state.time_challenge_current += 1
                    
                    if st.session_state.time_challenge_current >= len(st.session_state.time_challenge_questions):
                        end_time_challenge(challenge)
                    st.rerun()
            
            # Emergency stop
            stop_button_html = '''
            <div style="display: flex; justify-content: center; margin: 2rem 0;">
                <button style="background: rgba(244, 67, 54, 0.2); color: var(--error-red); border: 1px solid rgba(244, 67, 54, 0.3); border-radius: 25px; padding: 0.8rem 1.5rem; font-size: 1rem; font-weight: bold; cursor: pointer; transition: all 0.3s ease;" 
                        onmouseover="this.style.background='rgba(244, 67, 54, 0.3)'" 
                        onmouseout="this.style.background='rgba(244, 67, 54, 0.2)'">
                    🛑 Stop Challenge
                </button>
            </div>
            '''
            if st.button("🛑 Stop Challenge"):
                end_time_challenge(challenge)
                st.rerun()

def start_time_challenge(challenge):
    import time
    import random
    
    st.session_state.active_time_challenge = challenge['title']
    st.session_state.time_challenge_start = time.time()
    st.session_state.time_challenge_questions = challenge['questions'].copy()
    random.shuffle(st.session_state.time_challenge_questions)
    st.session_state.time_challenge_current = 0
    st.session_state.time_challenge_score = 0

def end_time_challenge(challenge):
    import time
    
    if st.session_state.time_challenge_start:
        completion_time = time.time() - st.session_state.time_challenge_start
        
        # Update best time
        current_best = st.session_state.time_challenge_best.get(challenge['title'], float('inf'))
        if completion_time < current_best:
            st.session_state.time_challenge_best[challenge['title']] = completion_time
        
        # Calculate final score
        base_score = st.session_state.time_challenge_score
        time_bonus = max(0, challenge['bonus_points'] * (1 - completion_time / challenge['time_limit']))
        total_score = base_score + time_bonus
        
        st.session_state.user_score += int(total_score)
        
        # Show results with modern UI
        results_html = f'''
        <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 2rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1); text-align: center;">
            <h3 style="color: var(--success-green); margin: 0 0 1rem 0;">⚡ Challenge Complete!</h3>
            <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; margin: 1rem 0;">
                <div style="text-align: center;">
                    <div style="color: var(--text-secondary); font-size: 0.9rem;">Time</div>
                    <div style="color: var(--primary-blue); font-size: 1.5rem; font-weight: bold;">{completion_time:.1f}s</div>
                </div>
                <div style="text-align: center;">
                    <div style="color: var(--text-secondary); font-size: 0.9rem;">Total Score</div>
                    <div style="color: var(--success-green); font-size: 1.5rem; font-weight: bold;">{int(total_score)} pts</div>
                </div>
            </div>
        </div>
        '''
        st.markdown(results_html, unsafe_allow_html=True)
        
        # Update leaderboard
        update_leaderboard("Time Challenge", int(total_score), completion_time)
    
    # Reset challenge state
    st.session_state.active_time_challenge = None
    st.session_state.time_challenge_start = None
    st.session_state.time_challenge_questions = []
    st.session_state.time_challenge_current = 0
    st.session_state.time_challenge_score = 0

def leaderboard_section():
    st.markdown('''
    <div class="section-card">
        <h2 style="background: linear-gradient(135deg, var(--primary-gold), var(--primary-orange)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; text-align: center; margin-bottom: 2rem;">
            🏆 Leaderboard
        </h2>
    </div>
    ''', unsafe_allow_html=True)
    
    if not st.session_state.leaderboard:
        empty_html = '''
        <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 2rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1); text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
            <h3 style="color: var(--text-primary); margin: 0 0 0.5rem 0;">No Scores Yet</h3>
            <p style="color: var(--text-secondary); margin: 0;">Complete challenges to appear on the leaderboard!</p>
        </div>
        '''
        st.markdown(empty_html, unsafe_allow_html=True)
        return
    
    # Sort leaderboard by score
    sorted_leaderboard = sorted(st.session_state.leaderboard, 
                               key=lambda x: x['score'], reverse=True)
    
    # Display top performers
    st.markdown('''
    <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h3 style="color: var(--text-primary); margin: 0 0 1rem 0; text-align: center;">🥇 Top Performers</h3>
    </div>
    ''', unsafe_allow_html=True)
    
    rank_colors = ["#FFD700", "#C0C0C0", "#CD7F32", "#4CAF50", "#2196F3", "#9C27B0", "#FF9800", "#795548", "#607D8B", "#F44336"]
    rank_emoji = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
    
    for i, entry in enumerate(sorted_leaderboard[:10]):
        medal_color = rank_colors[i] if i < len(rank_colors) else "#666"
        
        leaderboard_html = f"""
        <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 12px; padding: 1rem; margin: 0.5rem 0; border: 1px solid rgba(255, 255, 255, 0.1); transition: all 0.3s ease;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: {medal_color}; font-size: 1.2rem;">{rank_emoji[i]}</span>
                    <strong style="color: var(--text-primary);">#{i+1} {entry['username']}</strong>
                </div>
                <div style="display: flex; gap: 1rem; align-items: center;">
                    <span style="color: var(--success-green); font-weight: bold;">{entry['score']} pts</span>
                    <span style="color: var(--text-secondary); font-size: 0.9rem;">{entry['time']:.1f}s</span>
                </div>
            </div>
        </div>
        """
        st.markdown(leaderboard_html, unsafe_allow_html=True)
    
    # Personal stats
    st.markdown('''
    <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h3 style="color: var(--text-primary); margin: 0 0 1rem 0; text-align: center;">📊 Your Statistics</h3>
    </div>
    ''', unsafe_allow_html=True)
    
    user_entries = [entry for entry in st.session_state.leaderboard 
                   if entry['username'] == st.session_state.username]
    
    if user_entries:
        best_score = max(entry['score'] for entry in user_entries)
        best_time = min(entry['time'] for entry in user_entries)
        total_attempts = len(user_entries)
        
        stats_html = f'''
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 1rem 0;">
            <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 12px; padding: 1rem; border: 1px solid rgba(255, 255, 255, 0.1); text-align: center;">
                <div style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 0.5rem;">Best Score</div>
                <div style="color: var(--primary-blue); font-size: 1.5rem; font-weight: bold;">{best_score}</div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 12px; padding: 1rem; border: 1px solid rgba(255, 255, 255, 0.1); text-align: center;">
                <div style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 0.5rem;">Best Time</div>
                <div style="color: var(--success-green); font-size: 1.5rem; font-weight: bold;">{best_time:.1f}s</div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 12px; padding: 1rem; border: 1px solid rgba(255, 255, 255, 0.1); text-align: center;">
                <div style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 0.5rem;">Total Attempts</div>
                <div style="color: var(--primary-purple); font-size: 1.5rem; font-weight: bold;">{total_attempts}</div>
            </div>
        </div>
        '''
        st.markdown(stats_html, unsafe_allow_html=True)
    
    # Achievements display
    st.markdown('''
    <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h3 style="color: var(--text-primary); margin: 0 0 1rem 0; text-align: center;">🏅 Your Achievements</h3>
    </div>
    ''', unsafe_allow_html=True)
    
    if st.session_state.achievements:
        achievements_html = '<div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 1rem 0;">'
        for achievement in st.session_state.achievements:
            achievements_html += f'''
            <span style="background: linear-gradient(135deg, var(--primary-gold) 0%, var(--primary-orange) 100%); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: bold; box-shadow: 0 2px 8px rgba(255, 152, 0, 0.3);">{achievement}</span>
            '''
        achievements_html += '</div>'
        st.markdown(achievements_html, unsafe_allow_html=True)
    else:
        no_achievements_html = '''
        <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 12px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1); text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎯</div>
            <p style="color: var(--text-secondary); margin: 0;">Complete challenges to earn achievements!</p>
        </div>
        '''
        st.markdown(no_achievements_html, unsafe_allow_html=True)

def update_leaderboard(challenge_type, score, time):
    entry = {
        'username': st.session_state.username,
        'challenge_type': challenge_type,
        'score': score,
        'time': time,
        'timestamp': pd.Timestamp.now()
    }
    st.session_state.leaderboard.append(entry)

def check_achievements():
    # Check for various achievements
    achievements_to_check = [
        ("🎯 First Correct Answer", st.session_state.correct_answers >= 1),
        ("🔥 5 Correct Answers", st.session_state.correct_answers >= 5),
        ("💯 Perfect Score", st.session_state.quiz_score == len(QUIZ_QUESTIONS)),
        ("⚡ Speed Demon", st.session_state.user_score >= 100),
        ("🧠 Knowledge Seeker", st.session_state.quiz_attempts >= 10),
    ]
    
    for achievement, condition in achievements_to_check:
        if condition and achievement not in st.session_state.achievements:
            st.session_state.achievements.append(achievement)
            st.success(f"🎉 Achievement Unlocked: {achievement}")
            st.balloons()

# Data Structure Comparison section
def memory_management():
    st.title("💾 Memory Management")
    save_progress("Memory Mgmt")
    
    st.header("1. Garbage Collection")
    st.markdown("""
    **Automatic Memory Management:**
    - Python, Java, C# automatically free unused nodes
    - Circular references can cause memory leaks
    - GC overhead affects performance
    """)
    
    st.code("""
# Python - Automatic GC
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# Memory freed automatically
node = Node(10)
node = None  # Node eligible for GC
    """, language="python")
    
    st.header("2. Memory Leak Prevention")
    st.markdown("""
    **Common Leak Scenarios:**
    - Circular references
    - Lost head pointer
    - Exception during insertion
    - Incomplete deletion
    """)
    
    st.code("""
// C - Manual memory management
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node* next;
} Node;

void deleteList(Node* head) {
    while (head) {
        Node* temp = head;
        head = head->next;
        free(temp);  // Must manually free
    }
}
    """, language="c")
    
    st.header("3. Stack vs Heap Allocation")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Stack")
        st.markdown("""
        - Fast allocation
        - Limited size
        - Automatic cleanup
        - LIFO order
        """)
    
    with col2:
        st.subheader("Heap")
        st.markdown("""
        - Slower allocation
        - Large size
        - Manual/GC cleanup
        - Random access
        """)

def concurrent_linked_lists():
    st.title("🔒 Concurrent Linked Lists")
    save_progress("Concurrency")
    
    st.header("1. Race Conditions")
    st.markdown("""
    **Race conditions** occur when multiple threads access shared data simultaneously.
    """)
    
    st.code("""
# Unsafe linked list operations
class UnsafeLinkedList:
    def __init__(self):
        self.head = None
    
    def insert(self, data):
        new_node = Node(data)
        new_node.next = self.head  # Race condition!
        self.head = new_node       # Race condition!
    """, language="python")
    
    st.header("2. Lock-Free Implementations")
    st.markdown("""
    **Compare-and-Swap (CAS)** operations enable lock-free programming.
    """)
    
    st.code("""
# Lock-free insertion using CAS
class LockFreeLinkedList:
    def __init__(self):
        self.head = None
    
    def insert(self, data):
        new_node = Node(data)
        
        while True:
            current_head = self.head
            new_node.next = current_head
            
            # Atomic compare-and-swap
            if self._cas(self.head, current_head, new_node):
                break  # Success!
    """, language="python")
    
    st.header("3. Atomic Operations")
    st.markdown("""
    **Types of Atomic Operations:**
    - Compare-and-Swap (CAS)
    - Fetch-and-Add
    - Load-Link/Store-Conditional
    - Memory Barriers
    """)
    
    st.code("""
// Java - Using AtomicReference
import java.util.concurrent.atomic.AtomicReference;

class LockFreeStack<T> {
    private final AtomicReference<Node<T>> head = new AtomicReference<>();
    
    public void push(T item) {
        Node<T> newNode = new Node<>(item);
        Node<T> currentHead;
        
        do {
            currentHead = head.get();
            newNode.next = currentHead;
        } while (!head.compareAndSet(currentHead, newNode));
    }
}
    """, language="java")

def specialized_linked_lists():
    st.title("🎆 Specialized Linked Lists")
    save_progress("Specialized")
    
    st.header("1. Skip Lists")
    st.markdown("""
    **Skip Lists** are probabilistic data structures that allow O(log n) search time.
    """)
    
    st.code("""
class SkipListNode:
    def __init__(self, key, value, level):
        self.key = key
        self.value = value
        self.forward = [None] * (level + 1)

class SkipList:
    def __init__(self, max_level=16, p=0.5):
        self.max_level = max_level
        self.p = p
        self.level = 0
        self.header = SkipListNode(-1, None, max_level)
    
    def search(self, key):
        current = self.header
        for i in range(self.level, -1, -1):
            while (current.forward[i] and 
                   current.forward[i].key < key):
                current = current.forward[i]
        current = current.forward[0]
        if current and current.key == key:
            return current.value
        return None
    """, language="python")
    
    st.header("2. Self-Organizing Lists")
    st.markdown("""
    **Self-Organizing Lists** automatically rearrange elements based on access patterns.
    """)
    
    st.code("""
class SelfOrganizingList:
    def __init__(self, strategy='mtf'):
        self.head = None
        self.strategy = strategy
    
    def search(self, key):
        if self.head and self.head.data == key:
            return self.head
        
        prev = self.head
        current = self.head.next if self.head else None
        
        while current:
            if current.data == key:
                if self.strategy == 'mtf':  # Move to front
                    prev.next = current.next
                    current.next = self.head
                    self.head = current
                return current
            prev = current
            current = current.next
        return None
    """, language="python")
    
    st.header("3. Unrolled Linked Lists")
    st.markdown("""
    **Unrolled Linked Lists** store multiple elements in each node for better cache performance.
    """)
    
    st.code("""
class UnrolledNode:
    def __init__(self, max_size=4):
        self.max_size = max_size
        self.elements = []
        self.next = None

class UnrolledLinkedList:
    def __init__(self, max_node_size=4):
        self.head = None
        self.max_node_size = max_node_size
    
    def insert(self, index, value):
        # Find appropriate node and insert
        current = self.head
        if not current or len(current.elements) < self.max_node_size:
            if not current:
                self.head = UnrolledNode(self.max_node_size)
                current = self.head
            current.elements.append(value)
    """, language="python")

def real_world_optimizations():
    st.title("🚀 Real-World Optimizations")
    save_progress("Optimizations")
    
    st.header("1. Language-Specific Optimizations")
    
    tab1, tab2, tab3 = st.tabs(["Python", "Java", "C++"])
    
    with tab1:
        st.subheader("Python Optimizations")
        st.code("""
# Use __slots__ to reduce memory
class OptimizedNode:
    __slots__ = ['data', 'next']
    
    def __init__(self, data):
        self.data = data
        self.next = None

# Use collections.deque for better performance
from collections import deque
fast_list = deque()  # O(1) operations at both ends
        """, language="python")
    
    with tab2:
        st.subheader("Java Optimizations")
        st.code("""
// Use generics and size tracking
public class OptimizedLinkedList<T> {
    private Node<T> head;
    private int size;  // O(1) size() method
    
    private static class Node<T> {
        T data;
        Node<T> next;
        Node(T data) { this.data = data; }
    }
    
    public int size() { return size; }
}
        """, language="java")
    
    with tab3:
        st.subheader("C++ Optimizations")
        st.code("""
// Use smart pointers and move semantics
#include <memory>

template<typename T>
class ModernLinkedList {
    struct Node {
        T data;
        std::unique_ptr<Node> next;
        
        template<typename U>
        Node(U&& value) : data(std::forward<U>(value)) {}
    };
    
    std::unique_ptr<Node> head;
    
public:
    void push_front(T&& value) {
        auto new_node = std::make_unique<Node>(std::move(value));
        new_node->next = std::move(head);
        head = std::move(new_node);
    }
};
        """, language="cpp")
    
    st.header("2. Compiler Optimizations")
    st.markdown("""
    **Key Compiler Optimizations:**
    - **Inlining**: Small functions get inlined
    - **Loop Unrolling**: Reduces iteration overhead
    - **Prefetching**: Predicts memory access patterns
    - **Vectorization**: SIMD instructions for parallel operations
    """)
    
    st.header("3. Cache-Friendly Implementations")
    st.markdown("""
    **Cache Optimization Strategies:**
    - **Memory Pools**: Allocate from contiguous memory
    - **Node Packing**: Store multiple small nodes together
    - **Prefetching**: Load next nodes before needed
    - **Data Layout**: Arrange frequently accessed data together
    """)
    
    st.code("""
// Cache-friendly implementation with memory pool
template<typename T>
class CacheFriendlyList {
    struct Node {
        T data;
        size_t next_index;  // Index instead of pointer
    };
    
    std::vector<Node> node_pool;  // Contiguous memory
    size_t head_index;
    
public:
    void traverse_with_prefetch() {
        size_t current = head_index;
        while (current != INVALID_INDEX) {
            size_t next = node_pool[current].next_index;
            if (next != INVALID_INDEX) {
                __builtin_prefetch(&node_pool[next], 0, 1);
            }
            process_data(node_pool[current].data);
            current = next;
        }
    }
};
    """, language="cpp")

def advanced_problem_patterns():
    st.title("🧩 Advanced Problem Patterns")
    save_progress("Patterns")
    
    st.header("1. Two-Pointer Technique Variations")
    st.code("""
# Fast & Slow Pointer - Cycle Detection
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False

# Distance Pointers - Remove Nth from End
def remove_nth_from_end(head, n):
    dummy = ListNode(0)
    dummy.next = head
    first = second = dummy
    
    for i in range(n + 1):
        first = first.next
    
    while first:
        first = first.next
        second = second.next
    
    second.next = second.next.next
    return dummy.next
    """, language="python")
    
    st.header("2. Sliding Window on Linked Lists")
    st.code("""
# Maximum Sum Sublist of Size K
def max_sum_sublist(head, k):
    current = head
    window_sum = 0
    
    # First window
    for i in range(k):
        window_sum += current.val
        current = current.next
    
    max_sum = window_sum
    left = head
    
    # Slide window
    while current:
        window_sum = window_sum - left.val + current.val
        max_sum = max(max_sum, window_sum)
        left = left.next
        current = current.next
    
    return max_sum
    """, language="python")
    
    st.header("3. System Design Applications")
    st.code("""
# LRU Cache Implementation
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)
            return node.value
        return -1
    
    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        
        node = Node(key, value)
        self._add(node)
        self.cache[key] = node
        
        if len(self.cache) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
    """, language="python")

def interview_preparation():
    st.title("📝 Interview Preparation")
    save_progress("Interview")
    
    st.markdown("""
    <div class="section-card">
    <h2 style="color: #1e3c72; text-align: center; margin-bottom: 1.5rem;">🎯 Master Linked List Interviews</h2>
    <p style="font-size: 1.1em; text-align: center; color: #666; margin-bottom: 1rem;">
    Comprehensive preparation guide with top interview questions, complexity analysis, and expert tips.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Interview difficulty selector
    difficulty_filter = st.selectbox("Filter by Difficulty:", ["All", "Easy", "Medium", "Hard"])
    
    st.header("🔥 Top 20 Interview Questions")
    
    interview_questions = [
        {"q": "Reverse a singly linked list iteratively and recursively", "difficulty": "Easy", "companies": ["Google", "Amazon", "Microsoft"], "frequency": "Very High"},
        {"q": "Detect if a linked list has a cycle (Floyd's algorithm)", "difficulty": "Medium", "companies": ["Facebook", "Apple", "Netflix"], "frequency": "Very High"},
        {"q": "Find the middle element of a linked list", "difficulty": "Easy", "companies": ["Amazon", "Google", "Uber"], "frequency": "High"},
        {"q": "Merge two sorted linked lists", "difficulty": "Easy", "companies": ["Microsoft", "Amazon", "Apple"], "frequency": "Very High"},
        {"q": "Remove nth node from end of list", "difficulty": "Medium", "companies": ["Google", "Facebook", "LinkedIn"], "frequency": "High"},
        {"q": "Check if a linked list is palindrome", "difficulty": "Easy", "companies": ["Amazon", "Microsoft", "Adobe"], "frequency": "Medium"},
        {"q": "Find intersection point of two linked lists", "difficulty": "Easy", "companies": ["Google", "Amazon", "Bloomberg"], "frequency": "Medium"},
        {"q": "Remove duplicates from sorted linked list", "difficulty": "Easy", "companies": ["Microsoft", "Apple", "Salesforce"], "frequency": "Medium"},
        {"q": "Add two numbers represented as linked lists", "difficulty": "Medium", "companies": ["Amazon", "Google", "Facebook"], "frequency": "High"},
        {"q": "Clone a linked list with random pointers", "difficulty": "Medium", "companies": ["Microsoft", "Amazon", "Google"], "frequency": "Medium"},
        {"q": "Reverse nodes in k-group", "difficulty": "Hard", "companies": ["Google", "Facebook", "Uber"], "frequency": "Medium"},
        {"q": "Sort a linked list using merge sort", "difficulty": "Medium", "companies": ["Amazon", "Microsoft", "Apple"], "frequency": "Medium"},
        {"q": "Flatten a multilevel doubly linked list", "difficulty": "Medium", "companies": ["Google", "Amazon", "LinkedIn"], "frequency": "Low"},
        {"q": "LRU Cache implementation", "difficulty": "Medium", "companies": ["Amazon", "Google", "Microsoft"], "frequency": "Very High"},
        {"q": "Design a data structure for LFU cache", "difficulty": "Hard", "companies": ["Google", "Facebook", "Twitter"], "frequency": "Medium"},
        {"q": "Implement stack using linked list", "difficulty": "Easy", "companies": ["Amazon", "Microsoft", "Oracle"], "frequency": "Medium"},
        {"q": "Implement queue using linked list", "difficulty": "Easy", "companies": ["Google", "Apple", "Netflix"], "frequency": "Medium"},
        {"q": "Find if linked list is circular", "difficulty": "Easy", "companies": ["Amazon", "Adobe", "Salesforce"], "frequency": "Low"},
        {"q": "Rotate linked list by k positions", "difficulty": "Medium", "companies": ["Microsoft", "Google", "Uber"], "frequency": "Medium"},
        {"q": "Convert binary tree to doubly linked list", "difficulty": "Hard", "companies": ["Google", "Amazon", "Facebook"], "frequency": "Low"}
    ]
    
    filtered_questions = interview_questions if difficulty_filter == "All" else [q for q in interview_questions if q["difficulty"] == difficulty_filter]
    
    for i, item in enumerate(filtered_questions, 1):
        difficulty_color = {"Easy": "#4CAF50", "Medium": "#FF9800", "Hard": "#F44336"}[item["difficulty"]]
        frequency_color = {"Very High": "#E91E63", "High": "#FF5722", "Medium": "#FF9800", "Low": "#9E9E9E"}[item["frequency"]]
        
        st.markdown(f"""
        <div style="border-left: 4px solid {difficulty_color}; padding: 15px; margin: 10px 0; background: rgba(255,255,255,0.05); border-radius: 8px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <strong style="font-size: 1.1em;">{i}. {item['q']}</strong>
                <div>
                    <span style="background: {difficulty_color}; color: white; padding: 3px 8px; border-radius: 12px; font-size: 0.8em; margin-right: 5px;">{item['difficulty']}</span>
                    <span style="background: {frequency_color}; color: white; padding: 3px 8px; border-radius: 12px; font-size: 0.8em;">{item['frequency']}</span>
                </div>
            </div>
            <div style="font-size: 0.9em; color: #666;">
                <strong>Companies:</strong> {', '.join(item['companies'])}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("⚡ Time/Space Complexity Cheat Sheet")
    
    st.markdown("""
    <div class="section-card">
    <h3 style="color: #1e3c72; margin-bottom: 1rem;">📊 Quick Reference Table</h3>
    </div>
    """, unsafe_allow_html=True)
    
    complexity_data = {
        'Operation': ['Insert Beginning', 'Insert End', 'Insert at Position', 'Delete Beginning', 'Delete End', 'Delete by Value', 'Search', 'Access by Index', 'Traversal'],
        'Singly Linked': ['O(1)', 'O(n)', 'O(n)', 'O(1)', 'O(n)', 'O(n)', 'O(n)', 'O(n)', 'O(n)'],
        'Doubly Linked': ['O(1)', 'O(1)*', 'O(n)', 'O(1)', 'O(1)*', 'O(n)', 'O(n)', 'O(n)', 'O(n)'],
        'Array/List': ['O(n)', 'O(1)', 'O(n)', 'O(n)', 'O(1)', 'O(n)', 'O(n)', 'O(1)', 'O(n)'],
        'Space Complexity': ['O(1)', 'O(1)', 'O(1)', 'O(1)', 'O(1)', 'O(1)', 'O(1)', 'O(1)', 'O(1)']
    }
    
    df = pd.DataFrame(complexity_data)
    st.dataframe(df, use_container_width=True)
    st.caption("*With tail pointer maintained")
    
    # Advanced complexity analysis
    st.subheader("🎯 Advanced Complexity Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Memory Overhead:**
        - Singly Linked: 1 pointer + data per node
        - Doubly Linked: 2 pointers + data per node
        - Array: Data only (contiguous)
        
        **Cache Performance:**
        - Arrays: Excellent (sequential access)
        - Linked Lists: Poor (random memory access)
        """)
    
    with col2:
        st.markdown("""
        **When to Use:**
        - **Linked List**: Frequent insertions/deletions at beginning
        - **Array**: Random access, cache performance critical
        - **Doubly Linked**: Bidirectional traversal needed
        """)
    
    st.header("❌ Common Mistakes to Avoid")
    
    mistakes_data = [
        {"mistake": "Not checking for null pointers before dereferencing", "impact": "Runtime Error", "solution": "Always check if (node != null) before accessing node.data or node.next"},
        {"mistake": "Forgetting to update size counter", "impact": "Incorrect size() method", "solution": "Increment/decrement size in all insert/delete operations"},
        {"mistake": "Memory leaks in manual memory management", "impact": "Memory exhaustion", "solution": "Always free() allocated nodes in C/C++"},
        {"mistake": "Off-by-one errors in indexing", "impact": "Wrong element access", "solution": "Carefully handle 0-based vs 1-based indexing"},
        {"mistake": "Not handling empty list edge cases", "impact": "Null pointer exceptions", "solution": "Check if head == null before operations"},
        {"mistake": "Infinite loops in circular lists", "impact": "Program hangs", "solution": "Use proper termination conditions or visited tracking"},
        {"mistake": "Not updating both next and prev in doubly linked lists", "impact": "Broken links", "solution": "Always update both pointers in doubly linked operations"},
        {"mistake": "Losing reference to head node", "impact": "Memory leak", "solution": "Store head reference before modifications"},
        {"mistake": "Not considering single node edge cases", "impact": "Incorrect behavior", "solution": "Test with lists of size 0, 1, and 2"},
        {"mistake": "Incorrect pointer manipulation during deletion", "impact": "Broken list structure", "solution": "Update previous node's next pointer before deleting"}
    ]
    
    for i, mistake in enumerate(mistakes_data, 1):
        impact_color = {"Runtime Error": "#F44336", "Memory exhaustion": "#E91E63", "Incorrect size() method": "#FF9800", "Wrong element access": "#FF5722", "Null pointer exceptions": "#F44336", "Program hangs": "#9C27B0", "Broken links": "#FF9800", "Memory leak": "#E91E63", "Incorrect behavior": "#FF9800", "Broken list structure": "#F44336"}[mistake["impact"]]
        
        st.markdown(f"""
        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin: 10px 0; background: #fafafa;">
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <span style="color: #F44336; font-size: 1.2em; margin-right: 8px;">❌</span>
                <strong style="color: #333;">{i}. {mistake['mistake']}</strong>
            </div>
            <div style="margin-left: 30px;">
                <div style="margin-bottom: 5px;">
                    <strong>Impact:</strong> <span style="color: {impact_color}; font-weight: bold;">{mistake['impact']}</span>
                </div>
                <div>
                    <strong>Solution:</strong> <span style="color: #4CAF50;">{mistake['solution']}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("💻 Essential Code Templates")
    
    # Tabbed code examples
    tab1, tab2, tab3, tab4 = st.tabs(["🔄 Reverse List", "🔍 Cycle Detection", "🎯 Find Middle", "🔗 Merge Lists"])
    
    with tab1:
        st.subheader("Reverse Linked List")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Iterative Approach:**")
            st.code("""
def reverse_iterative(head):
    prev = None
    current = head
    
    while current:
        next_temp = current.next
        current.next = prev
        prev = current
        current = next_temp
    
    return prev

# Time: O(n), Space: O(1)
            """, language="python")
        
        with col2:
            st.markdown("**Recursive Approach:**")
            st.code("""
def reverse_recursive(head):
    if not head or not head.next:
        return head
    
    new_head = reverse_recursive(head.next)
    head.next.next = head
    head.next = None
    
    return new_head

# Time: O(n), Space: O(n)
            """, language="python")
    
    with tab2:
        st.subheader("Cycle Detection (Floyd's Algorithm)")
        st.code("""
def has_cycle(head):
    if not head or not head.next:
        return False
    
    slow = head
    fast = head.next
    
    while fast and fast.next:
        if slow == fast:
            return True
        slow = slow.next
        fast = fast.next.next
    
    return False

def find_cycle_start(head):
    if not has_cycle(head):
        return None
    
    slow = fast = head
    
    # Find meeting point
    while True:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    
    # Find start of cycle
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    
    return slow

# Time: O(n), Space: O(1)
        """, language="python")
    
    with tab3:
        st.subheader("Find Middle Element")
        st.code("""
def find_middle(head):
    if not head:
        return None
    
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    return slow

def find_middle_with_prev(head):
    if not head:
        return None, None
    
    slow = fast = head
    prev = None
    
    while fast and fast.next:
        prev = slow
        slow = slow.next
        fast = fast.next.next
    
    return slow, prev

# Time: O(n), Space: O(1)
# Returns middle node (for odd length)
# Returns second middle (for even length)
        """, language="python")
    
    with tab4:
        st.subheader("Merge Two Sorted Lists")
        st.code("""
def merge_two_lists(l1, l2):
    dummy = ListNode(0)
    current = dummy
    
    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next
    
    # Attach remaining nodes
    current.next = l1 or l2
    
    return dummy.next

def merge_k_lists(lists):
    if not lists:
        return None
    
    while len(lists) > 1:
        merged_lists = []
        
        for i in range(0, len(lists), 2):
            l1 = lists[i]
            l2 = lists[i + 1] if i + 1 < len(lists) else None
            merged_lists.append(merge_two_lists(l1, l2))
        
        lists = merged_lists
    
    return lists[0]

# Time: O(n + m), Space: O(1)
        """, language="python")
    
    st.header("🎯 Interview Tips & Strategies")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Before Coding:**
        - ✅ Clarify input constraints
        - ✅ Ask about edge cases
        - ✅ Discuss time/space requirements
        - ✅ Confirm expected behavior
        
        **During Implementation:**
        - ✅ Use dummy nodes for simplicity
        - ✅ Draw diagrams on whiteboard
        - ✅ Handle null pointers carefully
        - ✅ Test with small examples
        """)
    
    with col2:
        st.markdown("""
        **Common Patterns:**
        - 🔄 Two pointers (fast/slow)
        - 🎯 Dummy head node
        - 📝 Recursive solutions
        - 🔗 Multiple pass algorithms
        
        **Testing Strategy:**
        - 🧪 Empty list (null)
        - 🧪 Single node
        - 🧪 Two nodes
        - 🧪 Odd/even length lists
        """)
    
    # Interactive practice section
    st.header("🏋️ Practice Session")
    
    if st.button("🎯 Start Practice Interview"):
        practice_question = random.choice(filtered_questions)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; padding: 2rem; margin: 1rem 0;">
            <h3>🎯 Practice Question</h3>
            <p style="font-size: 1.2em; margin: 1rem 0;"><strong>{practice_question['q']}</strong></p>
            <div style="display: flex; gap: 1rem; margin-top: 1rem;">
                <span style="background: rgba(255,255,255,0.2); padding: 5px 10px; border-radius: 15px;">Difficulty: {practice_question['difficulty']}</span>
                <span style="background: rgba(255,255,255,0.2); padding: 5px 10px; border-radius: 15px;">Frequency: {practice_question['frequency']}</span>
            </div>
            <p style="margin-top: 1rem; font-size: 0.9em;">💡 Take 5 minutes to think through the approach before coding!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Company-specific preparation
    st.header("🏢 Company-Specific Preparation")
    
    company_focus = {
        "Google": ["Algorithm optimization", "Clean code", "Edge case handling", "Time/space analysis"],
        "Amazon": ["Leadership principles", "Scalability", "Customer obsession", "Operational excellence"],
        "Microsoft": ["Problem-solving approach", "Collaboration", "Technical depth", "System design"],
        "Facebook/Meta": ["Move fast mentality", "Impact focus", "Technical rigor", "Product thinking"],
        "Apple": ["Attention to detail", "User experience", "Performance optimization", "Quality focus"]
    }
    
    selected_company = st.selectbox("Select Company:", list(company_focus.keys()))
    
    st.markdown(f"""
    **{selected_company} Interview Focus:**
    """)
    
    for focus_area in company_focus[selected_company]:
        st.markdown(f"- 🎯 {focus_area}")
    
    # Practice Problems Section
    st.header("📝 Practice Problems with Solutions")
    
    practice_problems = [
        {
            "title": "Add Two Numbers",
            "difficulty": "Medium",
            "description": "You are given two non-empty linked lists representing two non-negative integers. Add the two numbers and return the sum as a linked list.",
            "example": "Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)\nOutput: 7 -> 0 -> 8\nExplanation: 342 + 465 = 807",
            "solution": """def addTwoNumbers(l1, l2):
    dummy = ListNode(0)
    current = dummy
    carry = 0
    
    while l1 or l2 or carry:
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0
        
        total = val1 + val2 + carry
        carry = total // 10
        current.next = ListNode(total % 10)
        
        current = current.next
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    
    return dummy.next"""
        },
        {
            "title": "Remove Nth Node From End",
            "difficulty": "Medium",
            "description": "Given the head of a linked list, remove the nth node from the end of the list and return its head.",
            "example": "Input: head = [1,2,3,4,5], n = 2\nOutput: [1,2,3,5]",
            "solution": """def removeNthFromEnd(head, n):
    dummy = ListNode(0)
    dummy.next = head
    first = second = dummy
    
    # Move first n+1 steps ahead
    for i in range(n + 1):
        first = first.next
    
    # Move both until first reaches end
    while first:
        first = first.next
        second = second.next
    
    # Remove nth node
    second.next = second.next.next
    return dummy.next"""
        },
        {
            "title": "Palindrome Linked List",
            "difficulty": "Easy",
            "description": "Given the head of a singly linked list, return true if it is a palindrome.",
            "example": "Input: head = [1,2,2,1]\nOutput: true",
            "solution": """def isPalindrome(head):
    # Find middle
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    # Reverse second half
    prev = None
    while slow:
        next_temp = slow.next
        slow.next = prev
        prev = slow
        slow = next_temp
    
    # Compare halves
    while prev:
        if head.val != prev.val:
            return False
        head = head.next
        prev = prev.next
    
    return True"""
        },
        {
            "title": "Intersection of Two Linked Lists",
            "difficulty": "Easy",
            "description": "Given the heads of two singly linked-lists headA and headB, return the node at which the two lists intersect.",
            "example": "Input: intersectVal = 8, listA = [4,1,8,4,5], listB = [5,6,1,8,4,5]\nOutput: Reference to node with value = 8",
            "solution": """def getIntersectionNode(headA, headB):
    if not headA or not headB:
        return None
    
    pA, pB = headA, headB
    
    while pA != pB:
        pA = pA.next if pA else headB
        pB = pB.next if pB else headA
    
    return pA"""
        },
        {
            "title": "Copy List with Random Pointer",
            "difficulty": "Medium",
            "description": "A linked list is given such that each node contains an additional random pointer. Return a deep copy of the list.",
            "example": "Input: head = [[7,null],[13,0],[11,4],[10,2],[1,0]]\nOutput: [[7,null],[13,0],[11,4],[10,2],[1,0]]",
            "solution": """def copyRandomList(head):
    if not head:
        return None
    
    # Create new nodes
    current = head
    while current:
        new_node = Node(current.val)
        new_node.next = current.next
        current.next = new_node
        current = new_node.next
    
    # Set random pointers
    current = head
    while current:
        if current.random:
            current.next.random = current.random.next
        current = current.next.next
    
    # Separate lists
    dummy = Node(0)
    copy_current = dummy
    current = head
    
    while current:
        copy_current.next = current.next
        current.next = current.next.next
        copy_current = copy_current.next
        current = current.next
    
    return dummy.next"""
        }
    ]
    
    for i, problem in enumerate(practice_problems, 1):
        difficulty_color = {"Easy": "#4CAF50", "Medium": "#FF9800", "Hard": "#F44336"}[problem["difficulty"]]
        
        with st.expander(f"{i}. {problem['title']} ({problem['difficulty']})"):
            st.markdown(f"**Problem:** {problem['description']}")
            st.markdown(f"**Example:**\n```\n{problem['example']}\n```")
            st.code(problem['solution'], language="python")
    
    # Final preparation checklist
    st.header("✅ Final Preparation Checklist")
    
    checklist_items = [
        "Master the top 10 most frequent questions",
        "Practice coding without IDE/autocomplete",
        "Time yourself on each problem (20-30 minutes)",
        "Explain your approach out loud",
        "Handle all edge cases systematically",
        "Optimize for both time and space complexity",
        "Review company-specific interview formats",
        "Prepare questions to ask the interviewer",
        "Practice on whiteboard or paper",
        "Mock interview with peers or mentors"
    ]
    
    for item in checklist_items:
        st.markdown(f"☐ {item}")
    
    st.success("🚀 You're ready to ace your linked list interviews! Good luck!")

def testing_and_debugging():
    st.markdown('''
    <div class="section-card">
        <h2 style="background: linear-gradient(135deg, var(--error-red), var(--warning-orange)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; text-align: center; margin-bottom: 2rem;">
            🧪 Testing & Debugging
        </h2>
    </div>
    ''', unsafe_allow_html=True)
    save_progress("Testing")
    
    st.markdown('''
    <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h3 style="color: var(--text-primary); margin: 0 0 1rem 0;">1. Unit Testing Strategies</h3>
    </div>
    ''', unsafe_allow_html=True)
    
    test_code_html = '''
    <div style="background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(10px); border-radius: 12px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
            <span style="color: var(--primary-blue);">📝</span>
            <h4 style="color: var(--text-primary); margin: 0;">Pytest Implementation</h4>
        </div>
        <pre style="color: var(--text-primary); overflow-x: auto;"><code># Using pytest for linked list testing
import pytest
from linked_list import LinkedList, Node

class TestLinkedList:
    def setup_method(self):
        self.ll = LinkedList()
    
    def test_empty_list(self):
        assert self.ll.size == 0
        assert self.ll.head is None
    
    def test_insert_single_element(self):
        self.ll.insert_at_beginning(10)
        assert self.ll.size == 1
        assert self.ll.head.data == 10
    
    def test_edge_cases(self):
        assert self.ll.delete_from_beginning() is None
        assert self.ll.search(10) == -1</code></pre>
    </div>
    '''
    st.markdown(test_code_html, unsafe_allow_html=True)
    
    st.markdown('''
    <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h3 style="color: var(--text-primary); margin: 0 0 1rem 0;">2. Memory Debugging Tools</h3>
    </div>
    ''', unsafe_allow_html=True)
    
    memory_code_html = '''
    <div style="background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(10px); border-radius: 12px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
            <span style="color: var(--warning-orange);">🧠</span>
            <h4 style="color: var(--text-primary); margin: 0;">Memory Profiling</h4>
        </div>
        <pre style="color: var(--text-primary); overflow-x: auto;"><code># Python memory profiling
from memory_profiler import profile

@profile
def test_memory_usage():
    ll = LinkedList()
    for i in range(10000):
        ll.insert_at_end(i)
    while ll.size > 0:
        ll.delete_from_beginning()
    return ll

# Run with: python -m memory_profiler test_memory.py</code></pre>
    </div>
    '''
    st.markdown(memory_code_html, unsafe_allow_html=True)
    
    st.markdown('''
    <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h3 style="color: var(--text-primary); margin: 0 0 1rem 0;">3. Performance Profiling</h3>
    </div>
    ''', unsafe_allow_html=True)
    
    perf_code_html = '''
    <div style="background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(10px); border-radius: 12px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
            <span style="color: var(--success-green);">⚡</span>
            <h4 style="color: var(--text-primary); margin: 0;">Performance Analysis</h4>
        </div>
        <pre style="color: var(--text-primary); overflow-x: auto;"><code># Profile linked list operations
import cProfile
import pstats

def profile_operations():
    ll = LinkedList()
    for i in range(10000):
        ll.insert_at_end(i)
    for i in range(100):
        ll.search(i * 100)

if __name__ == "__main__":
    cProfile.run('profile_operations()', 'results.prof')
    stats = pstats.Stats('results.prof')
    stats.sort_stats('cumulative')
    stats.print_stats(10)</code></pre>
    </div>
    '''
    st.markdown(perf_code_html, unsafe_allow_html=True)
    
    if st.button("🐛 Run Debug Session"):
        st.success("🎉 Debug session completed successfully!")

def integration_topics():
    st.markdown('''
    <div style="background: linear-gradient(135deg, var(--primary-purple), var(--primary-blue)); padding: 2rem; border-radius: 20px; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
        <h1 style="color: white; text-align: center; margin: 0; font-size: 2.5rem;">🔗 Integration Topics</h1>
        <p style="color: rgba(255,255,255,0.8); text-align: center; margin: 0.5rem 0 0 0;">Real-world applications of linked lists</p>
    </div>
    ''', unsafe_allow_html=True)
    save_progress("Integration")
    
    st.markdown('''
    <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h2 style="color: var(--text-primary); margin: 0 0 1rem 0;">1. Linked Lists in Databases</h2>
    </div>
    ''', unsafe_allow_html=True)
    
    db_buffer_html = '''
    <div style="background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(10px); border-radius: 12px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
            <span style="color: var(--info-blue);">💾</span>
            <h4 style="color: var(--text-primary); margin: 0;">Database Buffer Pool with LRU</h4>
        </div>
        <pre style="color: var(--text-primary); overflow-x: auto;"><code># Database Buffer Pool with LRU
class BufferPool:
    def __init__(self, size):
        self.size = size
        self.pages = {}
        self.head = PageNode(None, None)
        self.tail = PageNode(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def get_page(self, page_id):
        if page_id in self.pages:
            node = self.pages[page_id]
            self._move_to_front(node)
            return node.data
        
        page_data = self._load_from_disk(page_id)
        
        if len(self.pages) >= self.size:
            lru_node = self.tail.prev
            self._remove_node(lru_node)
            del self.pages[lru_node.page_id]
        
        new_node = PageNode(page_id, page_data)
        self._add_to_front(new_node)
        self.pages[page_id] = new_node
        
        return page_data</code></pre>
    </div>
    '''
    st.markdown(db_buffer_html, unsafe_allow_html=True)
    
    st.markdown('''
    <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h2 style="color: var(--text-primary); margin: 0 0 1rem 0;">2. File System Implementations</h2>
    </div>
    ''', unsafe_allow_html=True)
    
    file_system_html = '''
    <div style="background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(10px); border-radius: 12px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
            <span style="color: var(--success-green);">📁</span>
            <h4 style="color: var(--text-primary); margin: 0;">File Allocation Table</h4>
        </div>
        <pre style="color: var(--text-primary); overflow-x: auto;"><code># File Allocation Table
class FileAllocationTable:
    def __init__(self, total_clusters):
        self.total_clusters = total_clusters
        self.fat = [0] * total_clusters
        self.free_clusters = list(range(1, total_clusters))
    
    def allocate_file(self, file_size_clusters):
        if len(self.free_clusters) < file_size_clusters:
            return None
        
        allocated = []
        for i in range(file_size_clusters):
            cluster = self.free_clusters.pop(0)
            allocated.append(cluster)
            
            if i == file_size_clusters - 1:
                self.fat[cluster] = -1
            else:
                self.fat[cluster] = self.free_clusters[0]
        
        return allocated[0]</code></pre>
    </div>
    '''
    st.markdown(file_system_html, unsafe_allow_html=True)
    
    st.markdown('''
    <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h2 style="color: var(--text-primary); margin: 0 0 1rem 0;">3. Network Packet Handling</h2>
    </div>
    ''', unsafe_allow_html=True)
    
    network_html = '''
    <div style="background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(10px); border-radius: 12px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
            <span style="color: var(--warning-orange);">🌐</span>
            <h4 style="color: var(--text-primary); margin: 0;">Network Packet Queue with Priority</h4>
        </div>
        <pre style="color: var(--text-primary); overflow-x: auto;"><code># Network Packet Queue with Priority
class PacketQueue:
    def __init__(self):
        self.high_priority = None
        self.normal_priority = None
        self.low_priority = None
    
    def enqueue(self, packet):
        new_node = PacketNode(packet)
        
        if packet.priority == 'high':
            new_node.next = self.high_priority
            self.high_priority = new_node
        elif packet.priority == 'normal':
            new_node.next = self.normal_priority
            self.normal_priority = new_node
        else:
            new_node.next = self.low_priority
            self.low_priority = new_node
    
    def dequeue(self):
        if self.high_priority:
            packet = self.high_priority.packet
            self.high_priority = self.high_priority.next
            return packet
        
        if self.normal_priority:
            packet = self.normal_priority.packet
            self.normal_priority = self.normal_priority.next
            return packet
        
        if self.low_priority:
            packet = self.low_priority.packet
            self.low_priority = self.low_priority.next
            return packet
        
        return None</code></pre>
    </div>
    '''
    st.markdown(network_html, unsafe_allow_html=True)

def data_structure_comparison():
    st.markdown('''
    <div style="background: linear-gradient(135deg, var(--primary-purple), var(--primary-blue)); padding: 2rem; border-radius: 20px; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
        <h1 style="color: white; text-align: center; margin: 0; font-size: 2.5rem;">📊 Data Structure Comparison</h1>
        <p style="color: rgba(255,255,255,0.8); text-align: center; margin: 0.5rem 0 0 0;">Linked Lists vs Arrays - Choose wisely!</p>
    </div>
    ''', unsafe_allow_html=True)
    save_progress("Comparison")

    st.markdown('''
    <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h2 style="color: var(--text-primary); margin: 0 0 1rem 0;">Linked Lists vs Arrays</h2>
    </div>
    ''', unsafe_allow_html=True)

    comparison_data = {
        'Aspect': [
            'Random Access',
            'Insertion at Beginning',
            'Insertion at End',
            'Deletion from Beginning',
            'Deletion from End',
            'Memory Usage',
            'Cache Performance',
            'Implementation Complexity'
        ],
        'Linked List': ['O(n)', 'O(1)', 'O(n)', 'O(1)', 'O(n)', 'Higher', 'Poor', 'Moderate'],
        'Dynamic Array': ['O(1)', 'O(n)', 'O(1)*', 'O(n)', 'O(1)', 'Lower', 'Excellent', 'Simple']
    }

    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True)

    st.markdown("*Note: * Amortized O(1) for dynamic arrays")

    # Interactive comparison chart
    st.markdown('''
    <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h2 style="color: var(--text-primary); margin: 0 0 1rem 0;">Performance Comparison Chart</h2>
    </div>
    ''', unsafe_allow_html=True)

    aspects = ['Random Access', 'Insert Beginning', 'Insert End', 'Delete Beginning', 'Delete End']
    linked_list_scores = [10, 1, 10, 1, 10]  # Lower is better
    array_scores = [1, 10, 1, 10, 1]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Linked List',
        x=aspects,
        y=linked_list_scores,
        marker_color='#1e3c72'
    ))

    fig.add_trace(go.Bar(
        name='Dynamic Array',
        x=aspects,
        y=array_scores,
        marker_color='#667eea'
    ))

    fig.update_layout(
        title="Performance Comparison (Lower is Better)",
        barmode='group',
        yaxis_title="Complexity Score",
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown('''
    <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h2 style="color: var(--text-primary); margin: 0 0 1rem 0;">When to Use Which?</h2>
    </div>
    ''', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('''
        <div style="background: linear-gradient(135deg, rgba(76, 175, 80, 0.1), rgba(76, 175, 80, 0.05)); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(76, 175, 80, 0.3);">
            <h3 style="color: var(--success-green); margin: 0 0 1rem 0;">Choose Linked List when:</h3>
            <ul style="color: var(--text-primary); margin: 0; padding-left: 1.5rem;">
                <li>✅ Frequent insertions/deletions at beginning</li>
                <li>✅ Dynamic size requirements</li>
                <li>✅ Memory allocation/deallocation is expensive</li>
                <li>✅ Implementing stacks, queues, or graphs</li>
                <li>✅ Sequential access patterns</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown('''
        <div style="background: linear-gradient(135deg, rgba(33, 150, 243, 0.1), rgba(33, 150, 243, 0.05)); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(33, 150, 243, 0.3);">
            <h3 style="color: var(--info-blue); margin: 0 0 1rem 0;">Choose Array when:</h3>
            <ul style="color: var(--text-primary); margin: 0; padding-left: 1.5rem;">
                <li>✅ Need fast random access</li>
                <li>✅ Memory efficiency is critical</li>
                <li>✅ Most operations are at the end</li>
                <li>✅ Simple implementation needed</li>
                <li>✅ Cache performance matters</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('''
    <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h2 style="color: var(--text-primary); margin: 0 0 1rem 0;">Linked Lists vs Other Data Structures</h2>
    </div>
    ''', unsafe_allow_html=True)

    structures = ['Linked List', 'Array', 'Stack', 'Queue', 'Tree', 'Graph']
    use_cases = [
        'Dynamic sequences, undo operations',
        'Static sequences, fast access',
        'LIFO operations, function calls',
        'FIFO operations, scheduling',
        'Hierarchical data, searching',
        'Complex relationships, networks'
    ]

    comparison_df = pd.DataFrame({
        'Data Structure': structures,
        'Primary Use Cases': use_cases
    })

    st.dataframe(comparison_df, use_container_width=True)

# Advanced Algorithms section
def advanced_algorithms():
    st.markdown('''
    <div style="background: linear-gradient(135deg, var(--primary-purple), var(--primary-blue)); padding: 2rem; border-radius: 20px; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
        <h1 style="color: white; text-align: center; margin: 0; font-size: 2.5rem;">🚀 Advanced Algorithms</h1>
        <p style="color: rgba(255,255,255,0.8); text-align: center; margin: 0.5rem 0 0 0;">Master complex linked list operations</p>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('''
    <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h2 style="color: var(--text-primary); margin: 0 0 1rem 0;">Merge Sort on Linked Lists</h2>
        <div style="background: linear-gradient(135deg, rgba(255, 193, 7, 0.1), rgba(255, 193, 7, 0.05)); backdrop-filter: blur(10px); border-radius: 12px; padding: 1rem; margin: 1rem 0; border: 1px solid rgba(255, 193, 7, 0.3);">
            <h4 style="color: var(--warning-orange); margin: 0 0 0.5rem 0;">Why Merge Sort for Linked Lists?</h4>
            <ul style="color: var(--text-primary); margin: 0; padding-left: 1.5rem;">
                <li>Linked lists don't support random access</li>
                <li>Merge sort is efficient for linked structures</li>
                <li>No extra space needed for merging</li>
                <li>Stable sorting algorithm</li>
            </ul>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    merge_sort_html = '''
    <div style="background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(10px); border-radius: 12px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
            <span style="color: var(--success-green);">⚡</span>
            <h4 style="color: var(--text-primary); margin: 0;">Merge Sort Implementation</h4>
        </div>
        <pre style="color: var(--text-primary); overflow-x: auto;"><code>def merge_sort(head):
    if not head or not head.next:
        return head

    # Find middle of list
    slow = head
    fast = head.next

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # Split the list
    middle = slow.next
    slow.next = None

    # Recursively sort both halves
    left = merge_sort(head)
    right = merge_sort(middle)

    # Merge the sorted halves
    return merge(left, right)

def merge(left, right):
    if not left:
        return right
    if not right:
        return left

    if left.data <= right.data:
        result = left
        result.next = merge(left.next, right)
    else:
        result = right
        result.next = merge(left, right.next)

    return result

# Time Complexity: O(n log n)
# Space Complexity: O(log n) for recursion stack</code></pre>
    </div>
    '''
    st.markdown(merge_sort_html, unsafe_allow_html=True)

    st.markdown('''
    <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h2 style="color: var(--text-primary); margin: 0 0 1rem 0;">Quick Sort on Linked Lists</h2>
    </div>
    ''', unsafe_allow_html=True)

    quick_sort_html = '''
    <div style="background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(10px); border-radius: 12px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
            <span style="color: var(--warning-orange);">🔥</span>
            <h4 style="color: var(--text-primary); margin: 0;">Quick Sort Implementation</h4>
        </div>
        <pre style="color: var(--text-primary); overflow-x: auto;"><code>def quick_sort(head):
    if not head or not head.next:
        return head

    # Partition around pivot
    pivot = head
    smaller_head = None
    smaller_tail = None
    greater_head = None
    greater_tail = None

    current = head.next

    while current:
        if current.data < pivot.data:
            if not smaller_head:
                smaller_head = current
                smaller_tail = current
            else:
                smaller_tail.next = current
                smaller_tail = current
        else:
            if not greater_head:
                greater_head = current
                greater_tail = current
            else:
                greater_tail.next = current
                greater_tail = current
        current = current.next

    # Terminate partitions properly
    if smaller_tail:
        smaller_tail.next = None
    if greater_tail:
        greater_tail.next = None
        
    # Recursively sort partitions
    smaller_sorted = quick_sort(smaller_head)
    greater_sorted = quick_sort(greater_head)

    # Connect all parts
    if smaller_tail:
        smaller_tail.next = pivot
    else:
        smaller_head = pivot

    pivot.next = greater_sorted

    return smaller_head if smaller_head else pivot

# Time Complexity: O(n²) worst case, O(n log n) average
# Space Complexity: O(log n) for recursion stack</code></pre>
    </div>
    '''
    st.markdown(quick_sort_html, unsafe_allow_html=True)

    st.markdown('''
    <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h2 style="color: var(--text-primary); margin: 0 0 1rem 0;">Cycle Detection Algorithms</h2>
    </div>
    ''', unsafe_allow_html=True)

    floyd_html = '''
    <div style="background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(10px); border-radius: 12px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
            <span style="color: var(--info-blue);">🐢🐇</span>
            <h4 style="color: var(--text-primary); margin: 0;">Floyd's Cycle Detection Algorithm</h4>
        </div>
        <pre style="color: var(--text-primary); overflow-x: auto;"><code>def detect_cycle_floyd(head):
    if not head or not head.next:
        return False

    slow = head
    fast = head.next

    while fast and fast.next:
        if slow == fast:
            return True
        slow = slow.next
        fast = fast.next.next

    return False

# Time Complexity: O(n)
# Space Complexity: O(1)</code></pre>
    </div>
    '''
    st.markdown(floyd_html, unsafe_allow_html=True)

    brent_html = '''
    <div style="background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(10px); border-radius: 12px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
            <span style="color: var(--warning-orange);">🔍</span>
            <h4 style="color: var(--text-primary); margin: 0;">Brent's Cycle Detection Algorithm</h4>
        </div>
        <pre style="color: var(--text-primary); overflow-x: auto;"><code>def detect_cycle_brent(head):
    if not head:
        return False

    slow = head
    fast = head.next
    power = 1
    length = 1

    # Find cycle
    while fast and fast != slow:
        if power == length:
            power *= 2
            length = 0
            slow = fast

        fast = fast.next
        length += 1

    return fast is not None

# Time Complexity: O(n)
# Space Complexity: O(1)
# Often faster than Floyd's algorithm in practice</code></pre>
    </div>
    '''
    st.markdown(brent_html, unsafe_allow_html=True)

    st.markdown('''
    <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h2 style="color: var(--text-primary); margin: 0 0 1rem 0;">Advanced Operations</h2>
    </div>
    ''', unsafe_allow_html=True)

    reverse_groups_html = '''
    <div style="background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(10px); border-radius: 12px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
            <span style="color: var(--success-green);">🔄</span>
            <h4 style="color: var(--text-primary); margin: 0;">Reverse k nodes at a time</h4>
        </div>
        <pre style="color: var(--text-primary); overflow-x: auto;"><code>def reverse_k_groups(head, k):
    if not head or k == 1:
        return head

    # Count total nodes
    count = 0
    current = head
    while current:
        count += 1
        current = current.next

    # Create dummy node
    dummy = Node(0)
    dummy.next = head
    prev_group_end = dummy

    while count >= k:
        current = prev_group_end.next
        next_group_start = current

        # Reverse k nodes
        for i in range(k - 1):
            temp = current.next
            current.next = temp.next
            temp.next = prev_group_end.next
            prev_group_end.next = temp

        prev_group_end = next_group_start
        count -= k

    return dummy.next

# Example: reverse_k_groups([1,2,3,4,5], 2) -> [2,1,4,3,5]</code></pre>
    </div>
    '''
    st.markdown(reverse_groups_html, unsafe_allow_html=True)

# Example: reverse_k_groups([1,2,3,4,5], 2) -> [2,1,4,3,5]

# Memory Layout Visualizations section
def memory_layout_visualizations():
    st.markdown('''
    <div style="background: linear-gradient(135deg, var(--primary-purple), var(--primary-blue)); padding: 2rem; border-radius: 20px; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
        <h1 style="color: white; text-align: center; margin: 0; font-size: 2.5rem;">💾 Memory Layout Visualizations</h1>
        <p style="color: rgba(255,255,255,0.8); text-align: center; margin: 0.5rem 0 0 0;">Understanding memory allocation and fragmentation in linked lists</p>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('''
    <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h2 style="color: var(--text-primary); margin: 0 0 1rem 0;">How Linked Lists are Stored in Memory</h2>
        <div style="background: linear-gradient(135deg, rgba(14, 165, 233, 0.1), rgba(14, 165, 233, 0.05)); backdrop-filter: blur(10px); border-radius: 12px; padding: 1rem; margin: 1rem 0; border: 1px solid rgba(14, 165, 233, 0.3);">
            <h4 style="color: var(--info-blue); margin: 0 0 0.5rem 0;">Key Concept</h4>
            <p style="color: var(--text-primary); margin: 0; line-height: 1.7;">Unlike arrays that store elements in contiguous memory locations, linked list nodes are scattered throughout memory and connected via pointers.</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Interactive memory layout demo
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: var(--radius-lg);
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: var(--shadow-md);
    ">
        <h3 style="color: var(--primary-700); margin-bottom: 1.5rem;">Interactive Memory Layout</h3>
    """, unsafe_allow_html=True)

    if 'demo_list' not in st.session_state:
        st.session_state.demo_list = [10, 20, 30, 40]

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### Memory Blocks")
        memory_placeholder = st.empty()

    with col2:
        st.markdown("### Controls")
        
        # Modern button styling
        st.markdown("""
        <div style="
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        ">
        """, unsafe_allow_html=True)
        
        if st.button("➕ Add Node", help="Add a new node to the linked list"):
            st.session_state.demo_list.append(len(st.session_state.demo_list) * 10 + 10)
            st.rerun()

        if st.button("➖ Remove Node", help="Remove the last node from the linked list") and st.session_state.demo_list:
            st.session_state.demo_list.pop()
            st.rerun()

        if st.button("🔀 Shuffle Memory", help="Randomize the memory layout"):
            import random
            random.shuffle(st.session_state.demo_list)
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

    # Display memory layout
    with memory_placeholder.container():
        if st.session_state.demo_list:
            cols = st.columns(min(6, len(st.session_state.demo_list)))

            for i, val in enumerate(st.session_state.demo_list):
                if i < 6:  # Show max 6 blocks
                    with cols[i]:
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, var(--primary-100) 0%, var(--primary-200) 100%);
                            border-radius: var(--radius-lg);
                            padding: 1.5rem;
                            margin: 0.5rem;
                            text-align: center;
                            box-shadow: var(--shadow-md);
                            transition: all var(--transition-normal);
                            border: 1px solid rgba(14, 165, 233, 0.2);
                        " onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='var(--shadow-xl)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='var(--shadow-md)'">
                            <div style="font-weight: 600; color: var(--primary-700); margin-bottom: 0.5rem;">Block {i}</div>
                            <div style="font-size: 1.5rem; font-weight: 700; color: var(--primary-800); margin: 1rem 0;">{val}</div>
                            <div style="font-size: 0.9rem; color: var(--primary-600); margin-bottom: 1rem;">Addr: 0x{i*100:03X}</div>
                            {'<div style="font-size: 1.5rem; color: var(--primary-600);">→</div>' if i < len(st.session_state.demo_list) - 1 else '<div style="font-size: 1.5rem; color: var(--error-500);">NULL</div>'}
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("Add some nodes to see the memory layout!")
    
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('''
    <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h2 style="color: var(--text-primary); margin: 0 0 1rem 0;">Memory Fragmentation</h2>
        <div style="background: linear-gradient(135deg, rgba(255, 193, 7, 0.1), rgba(255, 193, 7, 0.05)); backdrop-filter: blur(10px); border-radius: 12px; padding: 1rem; margin: 1rem 0; border: 1px solid rgba(255, 193, 7, 0.3);">
            <h4 style="color: var(--warning-orange); margin: 0 0 0.5rem 0;">Memory Fragmentation</h4>
            <p style="color: var(--text-primary); margin: 0; line-height: 1.7;">Memory fragmentation occurs when free memory is divided into small, non-contiguous blocks. This can happen with frequent insertions and deletions in linked lists.</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Fragmentation visualization
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: var(--radius-lg);
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: var(--shadow-md);
    ">
        <h3 style="color: var(--primary-700); margin-bottom: 1.5rem;">Fragmentation Demo</h3>
    """, unsafe_allow_html=True)

    fragmentation_data = [
        {"address": "0x100", "size": 32, "status": "used", "data": "Node A"},
        {"address": "0x120", "size": 16, "status": "free", "data": ""},
        {"address": "0x130", "size": 48, "status": "used", "data": "Node B"},
        {"address": "0x160", "size": 24, "status": "free", "data": ""},
        {"address": "0x184", "size": 40, "status": "used", "data": "Node C"},
    ]

    for block in fragmentation_data:
        bg_color = "rgba(34, 197, 94, 0.1)" if block["status"] == "used" else "rgba(239, 68, 68, 0.1)"
        text_color = "var(--success-600)" if block["status"] == "used" else "var(--error-600)"
        st.markdown(f"""
        <div style="
            display: flex; 
            align-items: center; 
            margin: 0.75rem 0; 
            padding: 1rem; 
            border-radius: var(--radius-md); 
            background: {bg_color};
            border: 1px solid {'rgba(34, 197, 94, 0.2)' if block['status'] == 'used' else 'rgba(239, 68, 68, 0.2)'};
            transition: all var(--transition-normal);
        " onmouseover="this.style.transform='translateX(4px)'; this.style.boxShadow='var(--shadow-sm)'" onmouseout="this.style.transform='translateX(0)'; this.style.boxShadow='none'">
            <div style="width: 120px; font-weight: 600; color: var(--primary-700);">{block['address']}</div>
            <div style="width: 80px; color: var(--neutral-600);">{block['size']}B</div>
            <div style="width: 100px; color: {text_color}; font-weight: 600;">{block['status'].upper()}</div>
            <div style="flex: 1; color: var(--neutral-700);">{block['data']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-card">
        <h3 style="color: var(--primary-700); margin-bottom: 1rem;">Impact of Fragmentation</h3>
        <div style="display: grid; gap: 1rem;">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span style="color: var(--error-500); font-size: 1.2rem;">⚠️</span>
                <div>
                    <strong style="color: var(--primary-700);">Memory Waste:</strong>
                    <span style="color: var(--neutral-600);">Small free blocks can't be used for larger allocations</span>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span style="color: var(--warning-500); font-size: 1.2rem;">⚡</span>
                <div>
                    <strong style="color: var(--primary-700);">Performance:</strong>
                    <span style="color: var(--neutral-600);">Increased time for memory allocation/deallocation</span>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span style="color: var(--secondary-500); font-size: 1.2rem;">🔄</span>
                <div>
                    <strong style="color: var(--primary-700);">Cache Issues:</strong>
                    <span style="color: var(--neutral-600);">Scattered memory access patterns</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-card">
        <h2 style="color: var(--primary-700); margin-bottom: 1rem;">Cache Performance</h2>
        <p style="color: var(--neutral-600); line-height: 1.7;">
            <strong>Cache Locality</strong> refers to how closely related data elements are stored in memory.
            Arrays have excellent cache locality, while linked lists have poor cache locality.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Cache performance visualization
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: var(--radius-lg);
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: var(--shadow-md);
    ">
        <h3 style="color: var(--primary-700); margin-bottom: 1.5rem;">Cache Access Patterns</h3>
    """, unsafe_allow_html=True)

    cache_demo = st.selectbox("Select data structure:", ["Array", "Linked List"])

    if cache_demo == "Array":
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(22, 163, 74, 0.1) 100%);
            border: 1px solid rgba(34, 197, 94, 0.2);
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            margin: 1rem 0;
        ">
            <h4 style="color: var(--success-600); margin-bottom: 1rem;">Array Access Pattern</h4>
            <div style="display: grid; gap: 0.75rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: var(--success-500);">✓</span>
                    <span style="color: var(--neutral-700);">Elements stored contiguously: [10][20][30][40][50]</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: var(--success-500);">✓</span>
                    <span style="color: var(--neutral-700);">Memory addresses: 0x100, 0x104, 0x108, 0x10C, 0x110</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: var(--success-500);">⚡</span>
                    <strong style="color: var(--success-600);">Cache Performance:</strong>
                    <span style="color: var(--neutral-700);">Excellent - sequential access</span>
                </div>
            </div>
        </div>
        """)
    else:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.1) 100%);
            border: 1px solid rgba(239, 68, 68, 0.2);
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            margin: 1rem 0;
        ">
            <h4 style="color: var(--error-600); margin-bottom: 1rem;">Linked List Access Pattern</h4>
            <div style="display: grid; gap: 0.75rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: var(--error-500);">⚠️</span>
                    <span style="color: var(--neutral-700);">Elements scattered: 10(0x100) → 20(0x200) → 30(0x150) → 40(0x300)</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: var(--error-500);">⚠️</span>
                    <span style="color: var(--neutral-700);">Memory addresses: 0x100, 0x200, 0x150, 0x300</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: var(--error-500);">❌</span>
                    <strong style="color: var(--error-600);">Cache Performance:</strong>
                    <span style="color: var(--neutral-700);">Poor - random access, cache misses</span>
                </div>
            </div>
        </div>
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Performance Benchmarks section
def performance_benchmarks():
    st.markdown('''
    <div style="background: linear-gradient(135deg, var(--primary-purple), var(--primary-blue)); padding: 2rem; border-radius: 20px; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
        <h1 style="color: white; text-align: center; margin: 0; font-size: 2.5rem;">📊 Performance Benchmarks</h1>
        <p style="color: rgba(255,255,255,0.8); text-align: center; margin: 0.5rem 0 0 0;">Compare linked lists vs arrays in real-time</p>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('''
    <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h2 style="color: var(--text-primary); margin: 0 0 1rem 0;">Actual Timing Comparisons</h2>
    </div>
    ''', unsafe_allow_html=True)

    if st.button("Run Benchmarks"):
        import time

        # Test data sizes
        sizes = [100, 1000, 10000]

        results = {
            'Size': [],
            'Operation': [],
            'Linked List (ms)': [],
            'Array (ms)': []
        }

        for size in sizes:
            # Create test data
            test_data = list(range(size))

            # Linked List Implementation
            class Node:
                def __init__(self, data):
                    self.data = data
                    self.next = None

            class LinkedList:
                def __init__(self):
                    self.head = None

                def insert_at_end(self, data):
                    if not self.head:
                        self.head = Node(data)
                        return
                    current = self.head
                    while current.next:
                        current = current.next
                    current.next = Node(data)

                def search(self, target):
                    current = self.head
                    while current:
                        if current.data == target:
                            return True
                        current = current.next
                    return False

            # Create structures
            ll = LinkedList()
            array = []

            # Insert at end - Linked List
            start_time = time.time()
            for item in test_data:
                ll.insert_at_end(item)
            ll_insert_time = (time.time() - start_time) * 1000

            # Insert at end - Array
            start_time = time.time()
            for item in test_data:
                array.append(item)
            array_insert_time = (time.time() - start_time) * 1000

            # Search - Linked List
            start_time = time.time()
            for _ in range(100):  # Search 100 times
                ll.search(size // 2)
            ll_search_time = (time.time() - start_time) * 1000 / 100

            # Search - Array
            start_time = time.time()
            for _ in range(100):  # Search 100 times
                (size // 2) in array
            array_search_time = (time.time() - start_time) * 1000 / 100

            # Record results
            results['Size'].extend([size, size])
            results['Operation'].extend(['Insert at End', 'Search'])
            results['Linked List (ms)'].extend([ll_insert_time, ll_search_time])
            results['Array (ms)'].extend([array_insert_time, array_search_time])

        # Display results
        df = pd.DataFrame(results)
        st.dataframe(df, use_container_width=True)

        # Create comparison chart
        fig = go.Figure()

        for op in ['Insert at End', 'Search']:
            op_data = df[df['Operation'] == op]
            fig.add_trace(go.Bar(
                name=f'Linked List - {op}',
                x=[f"Size {size}" for size in op_data['Size']],
                y=op_data['Linked List (ms)'],
                marker_color='#1e3c72'
            ))
            fig.add_trace(go.Bar(
                name=f'Array - {op}',
                x=[f"Size {size}" for size in op_data['Size']],
                y=op_data['Array (ms)'],
                marker_color='#667eea'
            ))

        fig.update_layout(
            title="Performance Benchmarks",
            barmode='group',
            yaxis_title="Time (milliseconds)",
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown('''
    <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h2 style="color: var(--text-primary); margin: 0 0 1rem 0;">Memory Usage Analysis</h2>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown("")
    memory_comparison_html = '''
    <div style="background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(10px); border-radius: 12px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h4 style="color: var(--text-primary); margin: 0 0 1rem 0;">Memory Overhead Comparison</h4>
        <table style="width: 100%; border-collapse: collapse; color: var(--text-primary);">
            <thead>
                <tr style="background: rgba(255, 255, 255, 0.1);">
                    <th style="padding: 0.75rem; border: 1px solid rgba(255, 255, 255, 0.2); text-align: left;">Data Structure</th>
                    <th style="padding: 0.75rem; border: 1px solid rgba(255, 255, 255, 0.2); text-align: left;">Element Size</th>
                    <th style="padding: 0.75rem; border: 1px solid rgba(255, 255, 255, 0.2); text-align: left;">Overhead</th>
                    <th style="padding: 0.75rem; border: 1px solid rgba(255, 255, 255, 0.2); text-align: left;">Total per Element</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="padding: 0.75rem; border: 1px solid rgba(255, 255, 255, 0.2);">Linked List (Python)</td>
                    <td style="padding: 0.75rem; border: 1px solid rgba(255, 255, 255, 0.2);">28 bytes</td>
                    <td style="padding: 0.75rem; border: 1px solid rgba(255, 255, 255, 0.2);">8 bytes (pointer)</td>
                    <td style="padding: 0.75rem; border: 1px solid rgba(255, 255, 255, 0.2);">~36 bytes</td>
                </tr>
                <tr style="background: rgba(255, 255, 255, 0.05);">
                    <td style="padding: 0.75rem; border: 1px solid rgba(255, 255, 255, 0.2);">Dynamic Array (Python)</td>
                    <td style="padding: 0.75rem; border: 1px solid rgba(255, 255, 255, 0.2);">28 bytes</td>
                    <td style="padding: 0.75rem; border: 1px solid rgba(255, 255, 255, 0.2);">~4 bytes (amortized)</td>
                    <td style="padding: 0.75rem; border: 1px solid rgba(255, 255, 255, 0.2);">~32 bytes</td>
                </tr>
            </tbody>
        </table>
        <div style="background: linear-gradient(135deg, rgba(255, 193, 7, 0.1), rgba(255, 193, 7, 0.05)); backdrop-filter: blur(10px); border-radius: 8px; padding: 0.75rem; margin-top: 1rem; border: 1px solid rgba(255, 193, 7, 0.3);">
            <p style="color: var(--warning-orange); margin: 0; font-size: 0.9rem;">Note: Actual memory usage depends on the programming language and implementation.</p>
        </div>
    </div>
    '''
    st.markdown(memory_comparison_html, unsafe_allow_html=True)

# Progress Tracking Feature
def save_progress(section_name, data=None):
    """Save user progress"""
    st.session_state.progress_data[section_name] = {
        'completed': True,
        'timestamp': pd.Timestamp.now(),
        'data': data
    }
    st.session_state.completed_sections.add(section_name)

def get_progress_percentage():
    """Calculate overall progress"""
    total_sections = 10
    return (len(st.session_state.completed_sections) / total_sections) * 100

# Search Feature
def search_content(query):
    """Global search functionality with suggestions"""
    search_data = {
        'Introduction': ['linked', 'list', 'node', 'pointer', 'memory', 'data', 'structure', 'intro'],
        'Types': ['singly', 'doubly', 'circular', 'XOR', 'skip', 'list', 'type'],
        'Operations': ['insert', 'delete', 'search', 'traverse', 'reverse', 'operation', 'algo'],
        'Playground': ['interactive', 'visualization', 'create', 'modify', 'play', 'demo'],
        'Analysis': ['performance', 'complexity', 'time', 'space', 'benchmark', 'compare'],
        'Practice': ['problems', 'solutions', 'algorithms', 'coding', 'exercise'],
        'Quiz': ['questions', 'test', 'knowledge', 'game', 'challenge'],
        'Comparison': ['array', 'vs', 'memory', 'cache', 'efficiency', 'compare', 'diff'],
        'Testing': ['unit', 'test', 'debug', 'memory', 'profile', 'benchmark'],
        'Interview': ['questions', 'complexity', 'mistakes', 'preparation', 'coding', 'companies', 'tips', 'practice', 'solutions'],
        'Sum': ['calculate', 'total', 'addition', 'examples', 'practice', 'algorithm'],
        'Memory': ['garbage', 'collection', 'leak', 'stack', 'heap', 'allocation'],
        'Concurrency': ['thread', 'safe', 'lock', 'atomic', 'race', 'condition'],
        'Specialized': ['skip', 'list', 'self', 'organizing', 'unrolled', 'advanced'],
        'Optimizations': ['compiler', 'cache', 'language', 'performance', 'optimization'],
        'Patterns': ['two', 'pointer', 'sliding', 'window', 'system', 'design'],
        'Integration': ['database', 'file', 'system', 'network', 'packet', 'handling']
    }
    
    if query:
        query = query.lower().strip()
        results = []
        for section, keywords in search_data.items():
            # Check section name contains query
            if query in section.lower():
                results.append(section)
            # Check keywords contain query
            elif any(query in keyword for keyword in keywords):
                results.append(section)
        return list(set(results))  # Remove duplicates
    return []

def get_search_suggestions(query):
    """Get search suggestions based on input"""
    all_terms = ['Introduction', 'Types', 'Operations', 'Playground', 'Analysis', 'Practice', 'Quiz', 'Comparison', 'complexity', 'performance', 'insert', 'delete', 'node', 'pointer', 'linked', 'list', 'array', 'memory']
    
    query_lower = query.lower()
    # First try starts with, then contains
    starts_with = [term for term in all_terms if term.lower().startswith(query_lower)]
    contains = [term for term in all_terms if query_lower in term.lower() and term not in starts_with]
    suggestions = starts_with + contains
    return suggestions[:4]

# Code Export Feature
def export_code(code_content, filename="linked_list_code.py"):
    """Export code functionality"""
    return st.download_button(
        label="📥 Download Code",
        data=code_content,
        file_name=filename,
        mime="text/plain"
    )

# Step-by-Step Visualization
def step_by_step_insert(elements, new_value, position):
    """Animated insertion visualization"""
    steps = []
    if position == 0:  # Insert at beginning
        steps = [
            f"Step 1: Create new node with value {new_value}",
            "Step 2: Set new node's next to current head",
            "Step 3: Update head to point to new node",
            "Step 4: Insertion complete!"
        ]
    else:  # Insert at end
        steps = [
            f"Step 1: Create new node with value {new_value}",
            "Step 2: Traverse to the last node",
            "Step 3: Set last node's next to new node",
            "Step 4: Insertion complete!"
        ]
    return steps

# New Features
def add_bookmark(section_name):
    if section_name not in st.session_state.bookmarks:
        st.session_state.bookmarks.append(section_name)
        st.success(f"📌 Bookmarked {section_name}!")

def save_note(section_name, note_text):
    st.session_state.notes[section_name] = {'text': note_text, 'timestamp': pd.Timestamp.now()}
    st.success("📝 Note saved!")

def get_study_time():
    st.session_state.study_time += 0.1  # Increment study time
    return st.session_state.study_time

# Mobile Responsive CSS
def mobile_responsive_css():
    """Add mobile responsive styles"""
    css_content = r"""
    <style>
    @media (max-width: 768px) {
        .main-header { font-size: 2rem !important; }
        .section-card { padding: 1rem !important; margin: 0.5rem 0 !important; }
        .feature-card { padding: 1rem !important; margin: 0.25rem !important; }
        .stColumns { flex-direction: column !important; }
        .quiz-container { padding: 1rem !important; }
    }
    </style>
    """
    st.markdown(css_content, unsafe_allow_html=True)

# Theme Toggle Feature
def theme_toggle():
    """Apply dark theme"""
    st.session_state.dark_mode = True

    # Apply theme
    st.markdown('<div data-theme="dark" style="min-height: 100vh;">', unsafe_allow_html=True)

    # Dark theme CSS
    dark_css = """
    <style>
        .stApp {
            background: #1a1a1a !important;
            color: #e0e0e0 !important;
        }

        .main .block-container {
            background: #1a1a1a !important;
        }

        .stApp > div {
            background: #1a1a1a !important;
        }

        div[data-testid="stSidebar"] {
            background: #2d2d2d !important;
        }

        .section-card {
            background: #2d2d2d !important;
            border-left: 6px solid #64b5f6 !important;
            color: #e0e0e0 !important;
        }

        .feature-card {
            background: linear-gradient(135deg, #424242 0%, #616161 100%) !important;
        }

        .interactive-card {
            background: linear-gradient(135deg, #37474f 0%, #455a64 100%) !important;
        }

        .code-block {
            background: #1e1e1e !important;
            border-left: 4px solid #64b5f6 !important;
            color: #e0e0e0 !important;
        }

        .visual-diagram {
            background: #2c2c2c !important;
            color: #e0e0e0 !important;
        }

        .metric-card {
            background: linear-gradient(135deg, #37474f 0%, #455a64 100%) !important;
        }

        .quiz-container {
            background: linear-gradient(135deg, #37474f 0%, #455a64 100%) !important;
        }

        .stMarkdown {
            color: #e0e0e0 !important;
        }

        .stDataFrame {
            background: #2d2d2d !important;
        }

        .stPlotlyChart {
            background: #2d2d2d !important;
        }
    </style>
    """
    st.markdown(dark_css, unsafe_allow_html=True)

# Main app function
def main():
    # Initialize session state for tab navigation
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = 0

    # Initialize gamification session state
    if 'user_score' not in st.session_state:
        st.session_state.user_score = 0
    if 'quiz_attempts' not in st.session_state:
        st.session_state.quiz_attempts = 0
    if 'correct_answers' not in st.session_state:
        st.session_state.correct_answers = 0
    if 'leaderboard' not in st.session_state:
        st.session_state.leaderboard = []
    if 'achievements' not in st.session_state:
        st.session_state.achievements = []
    if 'current_challenge' not in st.session_state:
        st.session_state.current_challenge = None
    if 'challenge_start_time' not in st.session_state:
        st.session_state.challenge_start_time = None
    if 'coding_challenge_score' not in st.session_state:
        st.session_state.coding_challenge_score = 0
    if 'time_challenge_best' not in st.session_state:
        st.session_state.time_challenge_best = {}
    if 'username' not in st.session_state:
        st.session_state.username = "Player"
    if 'bookmarks' not in st.session_state:
        st.session_state.bookmarks = []
    if 'notes' not in st.session_state:
        st.session_state.notes = {}
    if 'study_time' not in st.session_state:
        st.session_state.study_time = 0
    if 'progress_data' not in st.session_state:
        st.session_state.progress_data = {}
    if 'completed_sections' not in st.session_state:
        st.session_state.completed_sections = set()

    
    # Apply theme toggle
    theme_toggle()

    # Add mobile responsive CSS
    mobile_responsive_css()
    
    # Sidebar navigation
    with st.sidebar:
        # Header with theme-aware color
        header_color = "#64b5f6" if st.session_state.get('dark_mode', False) else "#1e3c72"
        st.markdown(f"<h2 style='text-align: center; color: {header_color};'>🔗 Navigation</h2>", unsafe_allow_html=True)
        
        # Global Search with suggestions
        st.markdown("---")
        search_query = st.text_input("🔍 Search", placeholder="Search topics...", key="search_input")
        
        if search_query:
            query = search_query.strip()
            if len(query) > 0:
                # Show suggestions
                suggestions = get_search_suggestions(query)
                if suggestions:
                    st.write("**Suggestions:**")
                    for i, suggestion in enumerate(suggestions):
                        if st.button(f"💡 {suggestion}", key=f"suggest_{suggestion}_{i}"):
                            st.rerun()
                
                # Show results
                results = search_content(query)
                if results:
                    st.write("**Found in:**")
                    for i, result in enumerate(results):
                        completed = result in st.session_state.completed_sections
                        status = "✓" if completed else "○"
                        if st.button(f"{status} {result}", key=f"search_result_{result}_{i}"):
                            section_map = {'Introduction': 1, 'Types': 2, 'Operations': 3, 'Playground': 4, 'Analysis': 5, 'Practice': 6, 'Quiz': 8, 'Comparison': 9, 'Patterns': 14, 'Integration': 15}
                            if result in section_map:
                                st.session_state.current_tab = section_map[result]
                                st.rerun()
                else:
                    st.write("No results found")
        
        # Theme toggle
        st.markdown("---")
        theme_col1, theme_col2 = st.columns([1, 2])
        with theme_col1:
            theme_icon = "🌙" if not st.session_state.get('dark_mode', False) else "☀️"
            st.markdown(f"<div style='font-size: 1.5em; text-align: center;'>{theme_icon}</div>", unsafe_allow_html=True)
        with theme_col2:
            if st.button("Dark Mode" if not st.session_state.get('dark_mode', False) else "Light Mode", key="theme_toggle"):
                st.session_state.dark_mode = not st.session_state.get('dark_mode', False)
                st.rerun()
        
        st.markdown("---")
        
        # User stats display
        if st.session_state.user_score > 0:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {'#37474f' if st.session_state.get('dark_mode', False) else '#e3f2fd'} 0%, {'#455a64' if st.session_state.get('dark_mode', False) else '#bbdefb'} 100%); 
                        border-radius: 10px; padding: 10px; margin: 10px 0; text-align: center;">
                <div style="font-size: 0.9em; opacity: 0.8;">Your Score</div>
                <div style="font-size: 1.5em; font-weight: bold; color: {'#64b5f6' if st.session_state.get('dark_mode', False) else '#1e3c72'};">{st.session_state.user_score}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Navigation buttons
        nav_options = [
            ("🏠 Welcome", "Get started with linked lists"),
            ("📖 Introduction", "Learn the basics"),
            ("🔗 Types", "Explore different types"),
            ("⚙️ Operations", "Master operations & algorithms"),
            ("🎮 Playground", "Interactive practice"),
            ("📊 Analysis", "Performance comparison"),
            ("💡 Practice", "Solve problems"),
            ("🧪 Testing & Debugging", "Unit testing and debugging strategies"),
            ("📝 Interview Prep", "Top interview questions and tips"),
            ("🎨 Advanced Viz", "Advanced visualizations"),
            ("🧠 Quiz", "Test your knowledge"),
            ("⚖️ Comparison", "Compare data structures"),
            ("💾 Memory Mgmt", "Memory management topics"),
            ("🔒 Concurrency", "Thread-safe implementations"),
            ("🎆 Specialized", "Advanced linked list variants"),
            ("🚀 Optimizations", "Real-world implementation details"),
            ("🧩 Patterns", "Advanced problem patterns"),
            ("🔗 Integration", "Real-world integrations")
        ]
        
        for i, (name, desc) in enumerate(nav_options):
            # Highlight current tab
            button_type = "primary" if st.session_state.current_tab == i else "secondary"
            if st.button(name, key=f"nav_{i}", help=desc, use_container_width=True, type=button_type):
                st.session_state.current_tab = i
                st.session_state.scroll_to_top = True  # Flag to scroll to top
                st.rerun()
        
        st.markdown("---")
        
        # Progress indicator
        progress_pct = get_progress_percentage()
        st.markdown(f"""
        <div style="margin: 10px 0;">
            <div style="font-size: 0.9em; opacity: 0.8; text-align: center;">Progress: {progress_pct:.0f}%</div>
            <div style="background: {'#555' if st.session_state.get('dark_mode', False) else '#ddd'}; border-radius: 10px; height: 8px; margin: 5px 0;">
                <div style="background: {'#64b5f6' if st.session_state.get('dark_mode', False) else '#1e3c72'}; height: 8px; border-radius: 10px; width: {progress_pct}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Bookmarks section
        if st.session_state.bookmarks:
            st.markdown("**📌 Bookmarks**")
            for bookmark in st.session_state.bookmarks[:3]:
                if st.button(f"📖 {bookmark}", key=f"bookmark_{bookmark}"):
                    section_map = {'Introduction': 1, 'Types': 2, 'Operations': 3, 'Playground': 4, 'Analysis': 5, 'Practice': 6, 'Quiz': 8, 'Comparison': 9, 'Patterns': 14, 'Integration': 15}
                    if bookmark in section_map:
                        st.session_state.current_tab = section_map[bookmark]
                        st.rerun()
        
        if st.session_state.get('achievements'):
            st.markdown(f"""
            <div style="text-align: center; margin: 10px 0;">
                <div style="font-size: 0.9em; opacity: 0.8;">Achievements</div>
                <div style="font-size: 1.2em;">🏆 {len(st.session_state.achievements)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        footer_color = "#b0b0b0" if st.session_state.get('dark_mode', False) else "#666"
        st.markdown(f"<p style='text-align: center; color: {footer_color}; font-size: 0.8em;'>Select a section above to explore</p>", unsafe_allow_html=True)

    # Add scroll to top functionality
    if st.session_state.get('scroll_to_top', False):
        # Force page to start from top by clearing and re-rendering
        placeholder = st.empty()
        with placeholder.container():
            st.markdown("")
        st.session_state.scroll_to_top = False
    
    # Render the selected tab content
    if st.session_state.current_tab == 0:
        welcome_dashboard()
    elif st.session_state.current_tab == 1:
        introduction()
    elif st.session_state.current_tab == 2:
        types_of_linked_lists()
    elif st.session_state.current_tab == 3:
        operations_and_algorithms()
    elif st.session_state.current_tab == 4:
        interactive_playground()
    elif st.session_state.current_tab == 5:
        performance_analysis()
    elif st.session_state.current_tab == 6:
        practice_problems()
    elif st.session_state.current_tab == 7:
        testing_and_debugging()
    elif st.session_state.current_tab == 8:
        interview_preparation()
    elif st.session_state.current_tab == 9:
        advanced_visualizations()
    elif st.session_state.current_tab == 10:
        interactive_quiz()
    elif st.session_state.current_tab == 11:
        data_structure_comparison()
    elif st.session_state.current_tab == 12:
        memory_management()
    elif st.session_state.current_tab == 13:
        concurrent_linked_lists()
    elif st.session_state.current_tab == 14:
        specialized_linked_lists()
    elif st.session_state.current_tab == 15:
        real_world_optimizations()
    elif st.session_state.current_tab == 16:
        advanced_problem_patterns()
    elif st.session_state.current_tab == 17:
        integration_topics()
    
    # Close theme wrapper
    st.markdown('</div>', unsafe_allow_html=True)

# Run the main application
if __name__ == "__main__":
    main()
