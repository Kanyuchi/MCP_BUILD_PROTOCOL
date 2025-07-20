from datetime import datetime, timedelta
from thesis_memory.manager import ThesisManager

def main():
    # Initialize the thesis manager
    manager = ThesisManager("sqlite:///thesis_demo.db")

    # 1. Add theoretical frameworks
    voc = manager.add_framework(
        name="Varieties of Capitalism",
        description="Theoretical framework for comparing different types of market economies",
        key_concepts=["institutional complementarities", "coordination mechanisms", "comparative advantage"],
        primary_authors=["Peter A. Hall", "David Soskice"]
    )

    # 2. Add citations
    hall_citation = manager.add_citation(
        key="hall2001varieties",
        title="Varieties of Capitalism: The Institutional Foundations of Comparative Advantage",
        authors=["Peter A. Hall", "David Soskice"],
        year=2001,
        source_type="book"
    )

    # 3. Create thesis section
    methodology = manager.create_section(
        title="Methodology",
        content="This chapter outlines the research methodology..."
    )

    # 4. Add reviewer
    reviewer = manager.add_reviewer(
        name="Prof. Smith",
        email="smith@university.edu",
        role="supervisor",
        expertise=["institutional economics", "comparative political economy"]
    )

    # 5. Create research milestone
    milestone = manager.create_milestone(
        title="Literature Review",
        description="Review of VoC literature and institutional analysis approaches",
        phase="LITERATURE_REVIEW",
        planned_start=datetime.now(),
        planned_end=datetime.now() + timedelta(days=30)
    )

    # 6. Add smart suggestion
    suggestion = manager.add_smart_suggestion(
        section_id=methodology.id,
        type="METHODOLOGY",
        title="Consider Mixed Methods Approach",
        description="Combine institutional analysis with case studies for deeper insights"
    )

    # 7. Document research decision
    decision = manager.add_research_decision(
        type="METHODOLOGY",
        title="Mixed Methods Selection",
        description="Decision to use mixed methods approach",
        rationale="Enables both broad institutional comparison and detailed case analysis"
    )

    # 8. Create export template
    template = manager.create_export_template(
        name="LaTeX Methodology Template",
        format="LATEX",
        template_content="\\section{Methodology}\n\\subsection{Research Approach}"
    )

    # 9. Get section status
    status = manager.get_section_status(methodology.id)
    print("\nSection Status:")
    print("-" * 50)
    print(f"Title: {status['basic_info']['title']}")
    print(f"Status: {status['basic_info']['status']}")
    print(f"Version: {status['basic_info']['version']}")

    # 10. Get research progress
    progress = manager.get_research_progress()
    print("\nResearch Progress:")
    print("-" * 50)
    for milestone in progress['milestones']:
        print(f"Milestone: {milestone['title']}")
        print(f"Status: {milestone['status']}")
        print(f"Progress: {milestone['progress']*100:.1f}%")

    # Clean up
    manager.close()

if __name__ == "__main__":
    main() 