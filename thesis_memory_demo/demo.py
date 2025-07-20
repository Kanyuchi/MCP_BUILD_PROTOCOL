import os
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Initialize SQLAlchemy
Base = declarative_base()

class Framework(Base):
    """Theoretical framework model."""
    __tablename__ = 'frameworks'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    description = Column(Text)
    key_concepts = Column(Text)  # JSON array
    primary_authors = Column(Text)  # JSON array
    created_at = Column(DateTime, default=datetime.utcnow)

class ThesisSection(Base):
    """Thesis section model."""
    __tablename__ = 'thesis_sections'

    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    content = Column(Text)
    status = Column(String(20), default='draft')
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Memory:
    """Simple memory system for thesis writing."""

    def __init__(self, db_path="thesis_memory.db"):
        self.engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_framework(self, name, description, key_concepts, primary_authors):
        """Add a theoretical framework."""
        framework = Framework(
            name=name,
            description=description,
            key_concepts=json.dumps(key_concepts),
            primary_authors=json.dumps(primary_authors)
        )
        self.session.add(framework)
        self.session.commit()
        return framework

    def add_section(self, title, content=None):
        """Add a thesis section."""
        section = ThesisSection(
            title=title,
            content=content
        )
        self.session.add(section)
        self.session.commit()
        return section

    def get_section_context(self, title):
        """Get context for a thesis section."""
        section = self.session.query(ThesisSection).filter_by(title=title).first()
        if not section:
            return None

        return {
            "title": section.title,
            "status": section.status,
            "version": section.version,
            "content": section.content
        }

    def create_claude_prompt(self, section_title):
        """Create a context-aware prompt for Claude."""
        context = self.get_section_context(section_title)
        if not context:
            return "Section not found."

        frameworks = self.session.query(Framework).all()
        
        prompt = [
            f"You are assisting with the thesis section: {context['title']}",
            f"Current status: {context['status']} (Version {context['version']})",
            "\nTheoretical Frameworks available:"
        ]

        for framework in frameworks:
            concepts = json.loads(framework.key_concepts)
            authors = json.loads(framework.primary_authors)
            prompt.append(f"- {framework.name}")
            prompt.append(f"  Key concepts: {', '.join(concepts)}")
            prompt.append(f"  Authors: {', '.join(authors)}")

        return "\n".join(prompt)

def main():
    # Initialize memory system
    memory = Memory()

    # Add Varieties of Capitalism framework
    voc = memory.add_framework(
        name="Varieties of Capitalism",
        description="Framework for comparing different types of market economies",
        key_concepts=["institutional complementarities", "coordination mechanisms", "comparative advantage"],
        primary_authors=["Peter A. Hall", "David Soskice"]
    )

    # Add methodology section
    methodology = memory.add_section(
        title="Methodology",
        content="This chapter outlines the research methodology..."
    )

    # Get context-aware prompt for Claude
    prompt = memory.create_claude_prompt("Methodology")
    
    print("\nContext-aware prompt for Claude:")
    print("-" * 50)
    print(prompt)

if __name__ == "__main__":
    main() 