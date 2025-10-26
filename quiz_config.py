# Quiz Configuration
# Extracted quiz questions for better maintainability

QUIZ_QUESTIONS = [
    {
        "question": "What is the time complexity of inserting an element at the beginning of a singly linked list?",
        "options": ["O(1)", "O(n)", "O(log n)", "O(n²)"],
        "correct": 0,
        "explanation": "Inserting at the beginning requires only updating the head pointer, which is O(1) time."
    },
    {
        "question": "Which of the following is NOT an advantage of linked lists over arrays?",
        "options": ["Dynamic size", "Efficient random access", "No memory waste", "Flexible structure"],
        "correct": 1,
        "explanation": "Linked lists have poor random access (O(n)) compared to arrays (O(1))."
    },
    {
        "question": "In a doubly linked list, each node contains:",
        "options": ["Only data", "Data and one pointer", "Data and two pointers", "Data and three pointers"],
        "correct": 2,
        "explanation": "Doubly linked list nodes contain data, a previous pointer, and a next pointer."
    },
    {
        "question": "What is the space complexity of a singly linked list with n elements?",
        "options": ["O(1)", "O(n)", "O(n²)", "O(log n)"],
        "correct": 1,
        "explanation": "Each node requires O(1) space, so n nodes require O(n) space."
    },
    {
        "question": "Which algorithm is commonly used to detect cycles in a linked list?",
        "options": ["Quick Sort", "Merge Sort", "Floyd's Cycle Detection", "Binary Search"],
        "correct": 2,
        "explanation": "Floyd's Cycle Detection algorithm uses two pointers moving at different speeds."
    },
    {
        "question": "What is the main advantage of a doubly linked list over a singly linked list?",
        "options": ["Less memory usage", "Bidirectional traversal", "Simpler implementation", "Faster insertion at end"],
        "correct": 1,
        "explanation": "Doubly linked lists allow traversal in both directions."
    },
    {
        "question": "Which linked list type has the last node pointing back to the first node?",
        "options": ["Singly linked list", "Doubly linked list", "Circular linked list", "XOR linked list"],
        "correct": 2,
        "explanation": "Circular linked lists form a loop by pointing the last node to the first."
    },
    {
        "question": "What is the time complexity of searching for an element in a linked list?",
        "options": ["O(1)", "O(n)", "O(log n)", "O(n²)"],
        "correct": 1,
        "explanation": "Searching requires traversing the list, which is O(n)."
    },
    {
        "question": "Which operation is typically O(1) in a linked list?",
        "options": ["Insertion at beginning", "Searching", "Traversal", "Deletion by value"],
        "correct": 0,
        "explanation": "Insertion at the beginning is constant time."
    },
    {
        "question": "What is a common use case for circular linked lists?",
        "options": ["Undo functionality", "Round-robin scheduling", "Browser history", "Polynomial representation"],
        "correct": 1,
        "explanation": "Circular linked lists are used in round-robin scheduling."
    }
]