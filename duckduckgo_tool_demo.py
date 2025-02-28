from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from pydantic_ai.agent import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool
from pydantic import BaseModel, Field

class SearchResult(BaseModel):
    title: str = Field(..., description='The title of the search result.')
    href: str = Field(..., description='The URL of the search result.')
    body: str = Field(..., description='The body of the search result.')

class SearchResults(BaseModel):
    results: list[SearchResult] = Field(..., description='The search results.')

duckduckgo_agent = Agent(
    name='DuckDuckGo Search Agent',
    model=OpenAIModel('gpt-4o-mini'),
    tools=[duckduckgo_search_tool()],
    result_type=SearchResults,
    system_prompt='Use DuckDuckGo search for any giving query and return the results.',
)

prompt = 'List the top 3 most popular programming language in 2024'
response = duckduckgo_agent.run_sync(prompt)

if isinstance(response.data, SearchResults):
    for result in response.data.results:
        print(result.title)
        print(result.href)
        print(result.body)
        print()