from thesis_memory.database.manager import ThesisMemoryManager

def main():
    # Initialize the memory manager
    manager = ThesisMemoryManager("sqlite:///thesis_demo.db")

    # Add Varieties of Capitalism framework
    voc = manager.add_framework(
        name="Varieties of Capitalism",
        description="Theoretical framework for comparing different types of market economies",
        key_concepts=["institutional complementarities", "coordination mechanisms", "comparative advantage"],
        primary_authors=["Peter A. Hall", "David Soskice"]
    )

    # Add some concepts to VoC framework
    manager.add_framework_concept(
        framework_id=voc.id,
        name="Institutional Complementarities",
        description="How institutions in different spheres of the economy complement each other",
        operationalization="Analysis of institutional interactions across spheres",
        measurement_approach="Qualitative comparative analysis, Case studies"
    )

    # Add Behavioral Economics framework
    be = manager.add_framework(
        name="Behavioral Economics",
        description="Study of psychological, social, and emotional factors in economic decision-making",
        key_concepts=["bounded rationality", "heuristics", "cognitive biases"],
        primary_authors=["Daniel Kahneman", "Amos Tversky"]
    )

    # Create thesis sections
    methodology = manager.add_section(
        title="Methodology",
        content="This chapter outlines the research methodology..."
    )

    # Link frameworks to sections
    manager.link_framework_to_section(
        framework_id=voc.id,
        section_id=methodology.id,
        application_context="Using VoC to structure institutional analysis",
        key_insights="Institutional complementarities guide methodology design"
    )

    # Update section status
    manager.update_section_status(
        section_id=methodology.id,
        status="reviewed",
        lock=True
    )

    # Demonstrate retrieval
    methodology_frameworks = manager.get_section_frameworks(methodology.id)
    print("\nFrameworks linked to Methodology section:")
    for framework in methodology_frameworks:
        print(f"- {framework.name}")

    # Clean up
    manager.close()

if __name__ == "__main__":
    main() 