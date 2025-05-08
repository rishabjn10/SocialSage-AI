from enum import Enum
from typing import List, Optional
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from logger import log_step_details

# Uncomment the following line to use an example of a custom tool
# from marketing_posts.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from pydantic import BaseModel, Field

class ContentTypeEnum(str, Enum):
    INFORMATIONAL = "informational"
    JOKE = "joke"
    MEME = "meme"
    RANDOM_THOUGHT = "random_thought"
    LEARNING_SNIPPET = "learning_snippet"
    TRENDING_ANALYSIS = "trending_analysis"
    QUESTION_BASED = "question_based"
    PROMOTIONAL = "promotional"
    BEHIND_THE_SCENES = "behind_the_scenes"

class VisualTypeEnum(str, Enum):
    TEXT_WITH_VISUALS = "text_with_visuals"
    MEME = "meme"
    PICTOGRAPH = "pictograph"
    INFOGRAPHIC_SNIPPET = "infographic_snippet"
    PHOTO = "photo"
    SHORT_ANIMATION = "short_animation"
    DATA_VISUALIZATION = "data_visualization"
    CAROUSEL_TEXT_SLIDES = "carousel_text_slides"
    NO_VISUAL_NEEDED = "no_visual_needed"

# --- Input and Intermediate Models for Agent 1 (Input Validator & Profiler) ---

class UserWorkflowInput(BaseModel):
    """Schema for the initial input to the workflow."""
    domain_name: str = Field(..., description="The industry or domain of focus (e.g., 'Artificial Intelligence', 'Renewable Energy').")
    skill_sets: List[str] = Field(..., description="User's key skills (e.g., ['Python', 'Machine Learning', 'Project Management']).")
    country: str = Field(..., description="User's country for localization of trends if applicable (e.g., 'India').")
    target_audience: str = Field(..., description="Description of the target audience on LinkedIn (e.g., 'Tech recruiters and hiring managers in the USA', 'Fellow data scientists interested in MLOps').")

class ParsedUserInputData(BaseModel):
    """Schema for validated and structured user inputs (Output of T01)."""
    domain_name: str
    skill_sets: List[str]
    country: str
    target_audience_description: str

class ProfileWithKeywords(ParsedUserInputData):
    """Schema for user profile including generated research keywords (Output of T02)."""
    parsed_keywords_for_research: List[str] = Field(..., description="Keywords derived from inputs for research.")

# --- Models for Agent 2 (Trend & Content Research) ---

class NewsSnippet(BaseModel):
    """Represents a brief news item found during research."""
    title: str
    summary: str
    source_url: Optional[str] = None

class ResearchFindings(BaseModel):
    """Schema for the output of the research task (T03)."""
    trending_topics: List[str] = Field(default_factory=list, description="List of current trending topics.")
    relevant_news: List[NewsSnippet] = Field(default_factory=list, description="List of relevant news snippets.")
    popular_hashtags: List[str] = Field(default_factory=list, description="List of popular and relevant hashtags.")
    common_questions_asked: List[str] = Field(default_factory=list, description="Common questions the target audience is asking.")
    engaging_content_formats: List[str] = Field(default_factory=list, description="Observed engaging content formats in the domain.")

# --- Models for Agent 3 (Content Strategy & Planning) ---

class ContentPostOutline(BaseModel):
    """Schema for a single planned post within the content series."""
    post_id: str = Field(..., description="Unique identifier for the post plan (e.g., 'post_1').")
    theme_idea: str = Field(..., description="The core idea or topic for the post.")
    content_type: ContentTypeEnum = Field(..., description="Type of content to create.")
    key_message: str = Field(..., description="The main takeaway or message of the post.")
    preliminary_hashtags: List[str] = Field(default_factory=list, description="Initial list of suggested hashtags.")

class ContentPlan(BaseModel):
    """Schema for the overall content plan (Output of T04)."""
    posts: List[ContentPostOutline] = Field(..., description="A series of planned post outlines.")

# --- Models for Agent 4 (Post Generation) ---

class DraftedPostContent(BaseModel):
    """Schema for the output of the post drafting task (T05)."""
    linkedin_post_body: str = Field(..., description="The drafted text for the LinkedIn post.")
    final_hashtags: List[str] = Field(default_factory=list, description="Finalized list of hashtags for the post.")

# --- Models for Agent 5 (Visual Content & Prompt Generation) ---

class VisualConcept(BaseModel):
    """Schema for the suggested visual concept (Output of T06)."""
    visual_type: VisualTypeEnum = Field(..., description="Suggested type of visual.")
    visual_description: str = Field(..., description="Brief description of the visual's content and style.")

class TextToMediaPrompt(BaseModel):
    """Schema for the generated text-to-media prompt (Output of T07)."""
    prompt: str = Field(..., description="The detailed prompt for a text-to-image/video generation tool.")

# --- Models for Agent 6 (Orchestrator & Final Output) ---
# This combines outputs from Agent 4 and 5 for a single post.

class VisualSuggestionForPost(BaseModel):
    """Consolidated visual suggestion for a single post."""
    visual_type: VisualTypeEnum = Field(..., description="Type of visual recommended.")
    description: str = Field(..., description="Brief description of the visual concept and style.")
    text_to_media_prompt: Optional[str] = Field(None, description="Prompt for a text-to-image/video tool. Can be empty if 'no_visual_needed'.")

class LinkedInPostDetail(BaseModel):
    """Schema for the detailed structure of a single finalized LinkedIn post (Output of T08)."""
    post_id: str = Field(..., description="Unique identifier for the post.")
    theme: str = Field(..., description="The core theme or topic of the post (derived from ContentPostOutline.theme_idea).")
    content_type: ContentTypeEnum = Field(..., description="Type of content for the post.")
    linkedin_post_body: str = Field(..., description="The full text content for the LinkedIn post.")
    hashtags: List[str] = Field(default_factory=list, description="Finalized hashtags for the post.")
    visual_suggestion: VisualSuggestionForPost

class LinkedInPostSeriesPlan(BaseModel):
    """The final output schema for the entire workflow (Output of T09)."""
    user_inputs: UserWorkflowInput = Field(..., description="The initial inputs provided by the user for this series.")
    post_series: List[LinkedInPostDetail] = Field(
        ..., description="An array of planned LinkedIn posts with all details."
    )

class ContentTypeEnum(str, Enum):
    INFORMATIONAL = "informational"
    JOKE = "joke"
    MEME = "meme"
    RANDOM_THOUGHT = "random_thought"
    LEARNING_SNIPPET = "learning_snippet"
    TRENDING_ANALYSIS = "trending_analysis"
    QUESTION_BASED = "question_based"
    PROMOTIONAL = "promotional"
    BEHIND_THE_SCENES = "behind_the_scenes"

class VisualTypeEnum(str, Enum):
    TEXT_WITH_VISUALS = "text_with_visuals"
    MEME = "meme"
    PICTOGRAPH = "pictograph"
    INFOGRAPHIC_SNIPPET = "infographic_snippet"
    PHOTO = "photo"
    SHORT_ANIMATION = "short_animation"
    DATA_VISUALIZATION = "data_visualization"
    CAROUSEL_TEXT_SLIDES = "carousel_text_slides"
    NO_VISUAL_NEEDED = "no_visual_needed"

class NewsSnippet(BaseModel):
    title: str = Field(..., description="Title of the news item.")
    summary: str = Field(..., description="Brief summary of the news.")
    source_url: Optional[str] = Field(None, description="Optional URL to the news source.")

class ResearchFindings(BaseModel):
    """Detailed research findings for content strategy."""
    trending_topics: List[str] = Field(default_factory=list, description="List of current trending topics.")
    relevant_news: List[NewsSnippet] = Field(default_factory=list, description="List of relevant news snippets.")
    popular_hashtags: List[str] = Field(default_factory=list, description="List of popular and relevant hashtags.")
    common_questions_asked: List[str] = Field(default_factory=list, description="Common questions or pain points of the target audience.")
    engaging_content_formats: List[str] = Field(default_factory=list, description="Observed engaging content formats for this domain/audience.")

class ContentPostOutline(BaseModel):
    """Plan for a single LinkedIn post."""
    post_id: str = Field(..., description="Unique identifier for the post plan (e.g., 'post_20250509_xyz').")
    theme_idea: str = Field(..., description="The core idea or topic for the post.")
    content_type: ContentTypeEnum = Field(..., description="Type of content to create.")
    key_message: str = Field(..., description="The main takeaway or message of the post.")
    preliminary_hashtags: List[str] = Field(default_factory=list, description="Initial list of suggested hashtags.")

class VisualSuggestion(BaseModel):
    """Details for the suggested visual element."""
    visual_type: VisualTypeEnum = Field(..., description="Type of visual recommended.")
    description: str = Field(..., description="Brief description of the visual concept, style, and key elements.")
    text_to_media_prompt: str = Field(..., description="Detailed prompt for a text-to-image/video tool to generate the visual.")

class LinkedInPostDetail(BaseModel):
    """Complete details for a single LinkedIn post, ready for generation or review."""
    post_id: str = Field(..., description="Unique identifier from the content plan.")
    theme: str = Field(..., description="The core theme or topic of the post.")
    content_type: ContentTypeEnum = Field(..., description="Type of content for the post.")
    linkedin_post_body: str = Field(..., description="The full text content for the LinkedIn post.")
    hashtags: List[str] = Field(default_factory=list, description="Finalized list of suggested hashtags for the post.")
    visual_suggestion: VisualSuggestion = Field(..., description="Comprehensive visual suggestion including the generation prompt.")


@CrewBase
class LinkedInMarketingCrew():
    """LinkedInMarketingCrew for generating engaging LinkedIn posts"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        # Initialize any tools if they require API keys or specific setup here
        # For SerperDevTool, an API key is usually set via environment variable SERPER_API_KEY
        self.serper_tool = SerperDevTool()
        self.scrape_tool = ScrapeWebsiteTool()
        # You could also pass API keys or other configs to tools if needed:
        # self.serper_tool = SerperDevTool(api_key="YOUR_SERPER_API_KEY")

    @agent
    def trend_research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['trend_research_agent'],
            tools=[self.serper_tool, self.scrape_tool],
            verbose=True,
            # memory=False, # memory is False by default if not set in config
            allow_delegation=False # Explicitly set, though False is default
        )

    @agent
    def content_strategy_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['content_strategy_agent'],
            tools=[self.serper_tool], # Strategist might also use search for quick checks or ideation
            verbose=True,
            allow_delegation=False
        )

    @agent
    def linkedin_post_creator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['linkedin_post_creator_agent'],
            verbose=True,
            allow_delegation=False
            # No specific tools listed for this agent, relies on LLM's creative capabilities
        )

    @task
    def research_and_profiling_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_and_profiling_task'],
            agent=self.trend_research_agent(),
            output_json=ResearchFindings # Expect Pydantic model as output
        )

    @task
    def content_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_planning_task'],
            agent=self.content_strategy_agent(),
            context=[self.research_and_profiling_task()], # Depends on research
            output_json=ContentPostOutline # Expect Pydantic model as output
        )

    @task
    def linkedin_post_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['linkedin_post_generation_task'],
            agent=self.linkedin_post_creator_agent(),
            context=[self.content_planning_task(), self.research_and_profiling_task()], # Needs plan and optionally full research for context
            output_json=LinkedInPostDetail # Expect Pydantic model as output
        )

    @crew
    def crew(self) -> Crew:
        """Creates the LinkedInMarketingCrew"""
        return Crew(
            agents=self.agents,  # Uses agents defined with @agent decorator
            tasks=self.tasks,    # Uses tasks defined with @task decorator
            process=Process.sequential,
            verbose=True,
            memory=True, # Enable memory for the crew if you want agents to remember previous interactions in the same run
            task_callback=log_step_details # Optional: function to call after each task
        )
