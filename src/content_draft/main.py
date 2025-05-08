import sys
from content_draft.crew import LinkedInMarketingCrew
from dotenv import load_dotenv

load_dotenv(override=True)

def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    domain_name = input("Enter your domain name (e.g., Artificial Intelligence): ")
    skill_sets_raw = input("Enter your key skill sets (comma-separated, e.g., Python, Machine Learning): ")
    target_audience = input("Describe your target audience (e.g., Tech recruiters in the USA): ")
    country = input("Enter your country (e.g., India): ")

    skill_sets = [skill.strip() for skill in skill_sets_raw.split(',')]
    
    # inputs = {
    #     'domain_name': domain_name,
    #     'skill_sets': skill_sets, # Pass as a list
    #     'target_audience': target_audience,
    #     'country': country
    # }
    
    inputs = {
    "domain_name": "Agentic AI and LLM Solutions",
    "skill_sets": [
        "AI Engineering",
        "Agentic AI Development",
        "Software Development (Custom Solutions)",
        "Large Language Models (LLM)",
        "Technical Leadership",
        "Software Architecture",
        "Storytelling (Technical & Startup Narratives)",
        "Startup Case Studies & Roadmapping"
    ],
    "target_audience": "Tech audience (developers, students, AI enthusiasts) and random people who are interested in knwoing about AI's unique use cases reshaping industries. Content should showcase deep trend flow, technical expertise, innovative AI vision, startup case studies, and future technology roadmaps, long term vision ideas based on current market trends.",
    "country": "India"
}
    
    # inputs = {
    #     "domain_name": "",
    #     "skill_sets": [],
    #     "country": "",
    #     "target_audience": [
    #         "Tech entrepreneurs and investors in Southeast Asia,"
    #         "HR professionals looking for talent development insights"
    #     ],
    # }
    
    LinkedInMarketingCrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'customer_domain': 'crewai.com',
        'project_description': """
CrewAI, a leading provider of multi-agent systems, aims to revolutionize marketing automation for its enterprise clients. This project involves developing an innovative marketing strategy to showcase CrewAI's advanced AI-driven solutions, emphasizing ease of use, scalability, and integration capabilities. The campaign will target tech-savvy decision-makers in medium to large enterprises, highlighting success stories and the transformative potential of CrewAI's platform.

Customer Domain: AI and Automation Solutions
Project Overview: Creating a comprehensive marketing campaign to boost awareness and adoption of CrewAI's services among enterprise clients.
"""
    }
    try:
        LinkedInMarketingCrew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "train":
        train()
    else:
        run()
