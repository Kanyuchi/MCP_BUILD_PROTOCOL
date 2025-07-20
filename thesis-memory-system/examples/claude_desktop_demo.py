from thesis_memory.manager import ThesisManager
from thesis_memory.claude_desktop import ClaudeDesktopIntegration

def simulate_claude_conversation():
    # Initialize the system
    manager = ThesisManager("sqlite:///thesis_demo.db")
    claude = ClaudeDesktopIntegration(manager)

    # Create a methodology section
    methodology = manager.create_section(
        title="Methodology",
        content="Initial methodology section content..."
    )

    # Add VoC framework
    voc = manager.add_framework(
        name="Varieties of Capitalism",
        description="Framework for comparing market economies",
        key_concepts=["institutional complementarities", "coordination mechanisms"],
        primary_authors=["Peter A. Hall", "David Soskice"]
    )

    # Add some citations
    manager.add_citation(
        key="hall2001varieties",
        title="Varieties of Capitalism",
        authors=["Peter A. Hall", "David Soskice"],
        year=2001,
        source_type="book"
    )

    # Simulate a conversation with Claude
    print("\nStarting conversation with Claude...")
    print("-" * 50)

    # 1. Get initial context
    context = claude.create_context_prompt("Methodology")
    print("Initial Context for Claude:")
    print(context)

    # 2. Simulate Claude's response
    claude_response = """
    Based on the current methodology section and the Varieties of Capitalism framework, 
    here are my suggestions:

    New insight: The institutional complementarities in Germany's CME may create both 
    opportunities and barriers for sustainable transformation.

    Methodology decision: Adopt a mixed-methods approach combining institutional 
    analysis with case studies.

    Framework application: Use VoC's coordination mechanisms concept to analyze how 
    different institutional arrangements affect sustainability transitions.

    Would you like me to elaborate on any of these points?
    """
    print("\nClaude's Response:")
    print(claude_response)

    # 3. Process Claude's response
    print("\nProcessing Claude's response...")
    claude.process_claude_response("Methodology", claude_response)

    # 4. Save the conversation memory
    conversation = [
        {"role": "system", "content": context},
        {"role": "assistant", "content": claude_response}
    ]
    claude.save_session_memory("Methodology", conversation)

    # 5. Get recommendations for new content
    new_content = """
    The analysis will focus on how different institutional arrangements in liberal 
    and coordinated market economies affect their approach to sustainability transitions.
    Particular attention will be paid to the role of coordination mechanisms and 
    institutional complementarities in shaping transition pathways.
    """
    recommendations = claude.get_section_recommendations(new_content)
    
    print("\nRecommendations for new content:")
    print("-" * 50)
    if recommendations.get('frameworks'):
        print("\nRelevant Frameworks:")
        for rec in recommendations['frameworks']:
            print(f"- {rec['framework']}")
            print(f"  Matching concepts: {', '.join(rec['matching_concepts'])}")

    # 6. Load previous conversation
    print("\nLoading previous conversation...")
    previous_conversation = claude.load_session_memory("Methodology")
    if previous_conversation:
        print("Found previous conversation with", len(previous_conversation), "messages")

    # Clean up
    manager.close()

if __name__ == "__main__":
    simulate_claude_conversation() 