from typing import Optional, List
from pydantic_ai.agent import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.common_tools.tavily import tavily_search_tool
from pydantic import BaseModel, Field

class SearchResult(BaseModel):
    title: str = Field(..., description='The title of the search result.')
    url: str = Field(..., description='The URL of the search result.', alias='href')
    content: str = Field(..., description='A snippet or summary of the content.', alias='body')
    score: Optional[float] = Field(None, description='Relevance score of the result.')
    raw_content: Optional[str] = Field(None, description='Full raw content if available.')

class SearchResults(BaseModel):
    query: str = Field(..., description='The original search query.')
    answer: str = Field(..., description='An AI-generated answer based on the search results.')
    images: List[str] = Field(default_factory=list, description='URLs of relevant images, if any.')
    results: List[SearchResult] = Field(..., description='The search results.')
    response_time: str = Field(..., description='Time taken to process the request.')

duckduckgo_agent = Agent(
    name='Tavily Search Agent',
    model=OpenAIModel('gpt-4o-mini'),
    tools=[tavily_search_tool(api_key='<tavily api key>')],
    result_type=SearchResults,
    system_prompt='Use Tavily search for any giving query and return the results',
)

prompt = 'Give me the 3 latest news for Apple'
response = duckduckgo_agent.run_sync(prompt)

if isinstance(response.data, SearchResults):
    print(response.data.answer)
    print(response.data.response_time)
    print(response.data.query)
    print('---' * 10)
    for result in response.data.results:
        print(result.title)
        print(result.url)
        print(result.content)
        print(result.score)
        print(result.raw_content)
        print('---' * 10)