# AI Agents with Gemini and Pydantic Structured Outputs

Technical guide for building AI agents using Google Gemini with Pydantic for type-safe structured outputs.

## Dependencies

```toml
# pyproject.toml
[project]
dependencies = [
    "google-genai>=1.0.0",
    "pydantic>=2.0.0",
]
```

```bash
uv add google-genai pydantic
```

## Environment

```bash
# .env
GEMINI_API_KEY=your_api_key_here
```

## How Structured Outputs Work

Gemini can return JSON that conforms to a Pydantic schema. You pass the schema to the API, and Gemini constrains its output to match that structure exactly.

```python
from google import genai
from google.genai import types
from pydantic import BaseModel


class PizzaOrder(BaseModel):
    size: str
    toppings: list[str]
    quantity: int
    special_instructions: str


client = genai.Client(api_key="your_key")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="I want a large pepperoni pizza with extra cheese, make it 2 please",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=PizzaOrder,
    ),
)

# response.text is valid JSON matching PizzaOrder schema
order = PizzaOrder.model_validate_json(response.text)
print(order.size)      # "large"
print(order.toppings)  # ["pepperoni", "extra cheese"]
print(order.quantity)  # 2
```

## Recommended Architecture

```
your_app/
  agents/
    __init__.py       # Export all agents
    base.py           # BaseAgent with Gemini integration
    order_agent.py    # Specific agent
    support_agent.py  # Another agent
  schemas/
    __init__.py
    outputs.py        # Pydantic output schemas
```

## Defining Output Schemas

```python
# schemas/outputs.py
from decimal import Decimal
from pydantic import BaseModel


class OrderOutput(BaseModel):
    """What the agent extracts from an order request."""
    items: list[str]
    total_price: Decimal
    delivery_address: str
    estimated_time_minutes: int


class SupportOutput(BaseModel):
    """What the agent produces for support queries."""
    category: str  # "billing", "technical", "general"
    summary: str
    suggested_response: str
    escalate: bool
```

## Base Agent Class

```python
# agents/base.py
import logging
import os
import time

from google import genai
from google.genai import types
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class AgentError(Exception):
    """Base exception for agent errors."""
    pass


class GeminiAPIError(AgentError):
    """Raised when Gemini API calls fail after retries."""
    pass


class InvalidOutputError(AgentError):
    """Raised when response doesn't match schema."""
    pass


class BaseAgent:
    """Base class for AI agents with structured output.
    
    Subclasses must:
    1. Set `output_schema` to a Pydantic model
    2. Implement `_build_prompt()` to construct the prompt
    """

    output_schema: type[BaseModel]  # Subclasses MUST define this
    model_name: str = "gemini-2.0-flash"
    max_retries: int = 3
    retry_delay: float = 1.0

    def __init__(self, context: dict):
        """Initialize with context data for prompt building."""
        self.context = context
        self._client: genai.Client | None = None
        self._configure_client()

    def _configure_client(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise AgentError("GEMINI_API_KEY environment variable not set")
        self._client = genai.Client(api_key=api_key)

    def _build_prompt(self) -> str:
        """Build the prompt string. Subclasses must implement."""
        raise NotImplementedError("Subclasses must implement _build_prompt()")

    def _parse_response(self, response_text: str) -> BaseModel:
        """Parse JSON response into Pydantic model."""
        try:
            return self.output_schema.model_validate_json(response_text)
        except Exception as e:
            raise InvalidOutputError(f"Failed to parse response: {e}") from e

    def generate(self) -> BaseModel:
        """Call Gemini and return validated structured output.
        
        Returns:
            Instance of output_schema with validated data.
            
        Raises:
            GeminiAPIError: If API fails after all retries.
            InvalidOutputError: If response doesn't match schema.
        """
        prompt = self._build_prompt()
        last_error = None

        for attempt in range(self.max_retries):
            try:
                response = self._client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=self.output_schema,
                    ),
                )

                if not response.text:
                    raise GeminiAPIError("Empty response from API")

                return self._parse_response(response.text)

            except InvalidOutputError:
                raise  # Don't retry validation errors

            except Exception as e:
                last_error = e
                logger.warning(f"Attempt {attempt + 1}/{self.max_retries} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (2 ** attempt))

        raise GeminiAPIError(f"Failed after {self.max_retries} attempts: {last_error}")
```

## Implementing a Specific Agent

```python
# agents/order_agent.py
from agents.base import BaseAgent
from schemas.outputs import OrderOutput


class OrderAgent(BaseAgent):
    """Extracts structured order data from natural language."""

    output_schema = OrderOutput

    def _build_prompt(self) -> str:
        customer_message = self.context["message"]
        menu_items = self.context.get("menu", [])
        
        menu_text = "\n".join(f"- {item}" for item in menu_items)

        return f"""Extract order details from this customer message.

AVAILABLE MENU:
{menu_text}

CUSTOMER MESSAGE:
{customer_message}

Extract:
- items: list of items ordered
- total_price: calculated total
- delivery_address: where to deliver
- estimated_time_minutes: realistic estimate"""
```

## Using an Agent

```python
from agents.order_agent import OrderAgent

context = {
    "message": "Hi, I'd like 2 large pizzas and a coke delivered to 123 Main St",
    "menu": ["Small Pizza $10", "Large Pizza $15", "Coke $3", "Salad $8"],
}

agent = OrderAgent(context)
result = agent.generate()

# result is a validated OrderOutput instance
print(result.items)                  # ["Large Pizza", "Large Pizza", "Coke"]
print(result.total_price)            # Decimal("33.00")
print(result.delivery_address)       # "123 Main St"
print(result.estimated_time_minutes) # 30
```

## Dynamic Output Schemas

When an agent needs different output structures based on context:

```python
class FlexibleAgent(BaseAgent):
    """Agent that switches schema based on task type."""

    output_schema = DefaultOutput  # Fallback

    def __init__(self, context: dict):
        super().__init__(context)
        
        task_type = context.get("task_type")
        if task_type == "order":
            self.output_schema = OrderOutput
        elif task_type == "support":
            self.output_schema = SupportOutput
        elif task_type == "feedback":
            self.output_schema = FeedbackOutput
```

## Available Models

| Model | Best For | Speed | Cost |
|-------|----------|-------|------|
| `gemini-2.0-flash` | General use, good balance | Fast | Low |
| `gemini-2.0-flash-lite` | High volume, simple tasks | Fastest | Lowest |
| `gemini-2.5-pro-preview-06-05` | Complex reasoning | Slow | Higher |

Override in subclass:

```python
class ComplexReasoningAgent(BaseAgent):
    model_name = "gemini-2.5-pro-preview-06-05"
```

## Error Handling

```python
from agents.base import AgentError, GeminiAPIError, InvalidOutputError

try:
    result = agent.generate()
except InvalidOutputError as e:
    # Response didn't match schema - likely a prompt issue
    logger.error(f"Schema validation failed: {e}")
except GeminiAPIError as e:
    # API failed after retries - check key/quota/network
    logger.error(f"API error: {e}")
except AgentError as e:
    # Base error (e.g., missing API key)
    logger.error(f"Agent error: {e}")
```

## Testing Agents

```python
from unittest.mock import MagicMock, patch

def test_order_agent():
    context = {"message": "1 large pizza to 123 Main St", "menu": ["Large Pizza $15"]}
    
    mock_response = MagicMock()
    mock_response.text = '''{
        "items": ["Large Pizza"],
        "total_price": "15.00",
        "delivery_address": "123 Main St",
        "estimated_time_minutes": 25
    }'''
    
    with patch.object(OrderAgent, '_configure_client'):
        agent = OrderAgent(context)
        agent._client = MagicMock()
        agent._client.models.generate_content.return_value = mock_response
        
        result = agent.generate()
        
        assert result.items == ["Large Pizza"]
        assert result.delivery_address == "123 Main St"
```

## Key Principles

1. **Structured Output**: Always define Pydantic schemas - never parse free-form text
2. **Minimal Context**: Pass only what the agent needs, not entire application state
3. **Single Responsibility**: Each agent does one thing well
4. **Retry Logic**: Handle transient API failures with exponential backoff
5. **Type Safety**: The schema guarantees the shape of your data
