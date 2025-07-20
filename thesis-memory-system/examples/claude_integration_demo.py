from thesis_memory.database.manager import ThesisMemoryManager
from thesis_memory.claude_integration import ClaudeMemoryInterface
from thesis_memory.models.research import FindingType, ResearchNote, ResearchFinding

def main():
    # Initialize the system
    manager = ThesisMemoryManager("sqlite:///thesis_demo.db")
    claude_interface = ClaudeMemoryInterface(manager)

    # Set up some initial data
    # Add Varieties of Capitalism framework
    voc = manager.add_framework(
        name="Varieties of Capitalism",
        description="Theoretical framework for comparing different types of market economies",
        key_concepts=["institutional complementarities", "coordination mechanisms", "comparative advantage"],
        primary_authors=["Peter A. Hall", "David Soskice"]
    )

    # Create a methodology section
    methodology = manager.add_section(
        title="Methodology",
        content="This chapter outlines the research methodology..."
    )

    # Add a research note and finding
    note = ResearchNote(
        title="Institutional Analysis Approach",
        content="Using comparative institutional analysis to examine differences between UK and German approaches",
        section_id=methodology.id,
        framework_id=voc.id
    )
    manager.session.add(note)

    finding = ResearchFinding(
        note_id=note.id,
        type=FindingType.INSIGHT,
        description="Institutional complementarities appear stronger in coordinated market economies",
        evidence="Based on preliminary analysis of policy documents",
        implications="May explain divergent approaches to sustainable transformation",
        confidence_level=4
    )
    manager.session.add(finding)
    manager.session.commit()

    # Demonstrate Claude integration
    print("\nGenerating context-aware prompt for Claude:")
    print("-" * 50)
    prompt = claude_interface.create_section_prompt("Methodology")
    print(prompt)

    # Simulate Claude's response
    claude_response = """
    Based on the methodology section's context and the Varieties of Capitalism framework, 
    I suggest the following additions:

    New insight: The institutional complementarities in Germany's CME may create both 
    opportunities and barriers for sustainable transformation, requiring a nuanced analysis 
    of how existing coordination mechanisms can be leveraged or adapted.

    Would you like me to elaborate on this insight or explore other aspects of the 
    methodology?
    """

    print("\nSimulating Claude's response:")
    print("-" * 50)
    print(claude_response)

    # Update memory system based on Claude's response
    print("\nUpdating memory system with Claude's insights...")
    claude_interface.update_from_claude_response("Methodology", claude_response)

    # Get framework recommendations for new content
    new_content = """
    The analysis reveals how different institutional arrangements in liberal and 
    coordinated market economies affect their approach to sustainability transitions.
    The coordination mechanisms and institutional complementarities play a crucial role.
    """

    print("\nGetting framework recommendations for new content:")
    print("-" * 50)
    recommendations = claude_interface.get_framework_recommendations(new_content)
    for rec in recommendations:
        print(f"Framework: {rec['framework']}")
        print(f"Matching concepts: {', '.join(rec['matching_concepts'])}")
        print(f"Relevance score: {rec['relevance']:.2f}\n")

    # Clean up
    manager.close()

if __name__ == "__main__":
    main() 