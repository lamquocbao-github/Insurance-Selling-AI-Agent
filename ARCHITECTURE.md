# Technical Architecture - Tet Insurance AI Agent

## System Overview

This document provides detailed technical information about the AI Agent architecture, components, and implementation details.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                       (Streamlit UI)                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   TetInsuranceAgent                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            Conversation Handler                       │  │
│  │  • Receives user input                               │  │
│  │  • Orchestrates components                           │  │
│  │  • Returns generated response                        │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                    │
│         ┌───────────────┼───────────────┐                   │
│         ▼               ▼               ▼                   │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │  Knowledge  │ │   Memory    │ │   Context   │          │
│  │    Base     │ │   Manager   │ │   Builder   │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
│         │               │               │                   │
│         └───────────────┴───────────────┘                   │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Prompt Constructor                       │  │
│  │  • System prompt                                     │  │
│  │  • Customer context                                  │  │
│  │  • Retrieved knowledge                               │  │
│  │  • Memory summary                                    │  │
│  │  • User message                                      │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Gemini API (LLM)                          │
│  • Model: gemini-pro                                        │
│  • Temperature: Default                                     │
│  • Max tokens: Auto                                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Generated Response                          │
│  • Natural language                                         │
│  • Context-aware                                            │
│  • Culturally appropriate                                   │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. SimpleEmbedding Class

**Purpose**: Create vector representations of text for semantic similarity comparison

**Implementation**:
```python
class SimpleEmbedding:
    - embed_text(text: str) -> np.ndarray
    - cosine_similarity(vec1, vec2) -> float
```

**Features**:
- Character-frequency based vectorization
- Vietnamese character support (àáảãạăắằẳẵặâấầẩẫậèéẻẽẹê...)
- Additional semantic features:
  - Text length normalization
  - Word density
  - Insurance-specific keywords (bảo hiểm, giá, tết, du lịch, etc.)
  - Claim-related terms
  - Family-related terms
- Fast, in-memory computation
- No external model dependencies

**Vector Dimensions**: ~90 dimensions
- 82 character frequencies (a-z, 0-9, Vietnamese)
- 10 semantic features

**Performance**:
- Embedding generation: <1ms per text
- Similarity calculation: <0.1ms per comparison

### 2. KnowledgeBase Class

**Purpose**: Store and retrieve relevant information using semantic search

**Implementation**:
```python
class KnowledgeBase:
    - add_document(doc_id, content, metadata)
    - search(query, top_k=3) -> List[Document]
    - get_all_documents() -> List[Document]
```

**Data Structure**:
```python
{
    "id": "unique_identifier",
    "content": "document text content",
    "metadata": {
        "category": "purchase_history|behavior|product|tet_insights",
        "product": "motor|health|life|travel",
        "timestamp": "ISO datetime"
    },
    "embedding": [0.1, 0.3, ...],  # 90-dim vector
    "similarity_score": 0.85  # When returned from search
}
```

**Categories**:
1. **purchase_history**: Past insurance policies
2. **interaction_history**: Previous conversations
3. **behavior**: Travel patterns, preferences
4. **demographics**: Age, occupation, family
5. **communication**: Tone, channel preferences
6. **product**: Insurance product details
7. **tet_insights**: Seasonal knowledge

**Search Algorithm**:
1. Convert query to embedding vector
2. Calculate cosine similarity with all documents
3. Sort by similarity score (descending)
4. Return top-K results above threshold (0.1)

**Scalability**:
- Current: Linear search (O(n))
- For production: Use FAISS, Pinecone, or Weaviate
- Supports ~1000 documents efficiently
- For 10,000+: Migrate to vector database

### 3. ShortTermMemory Class

**Purpose**: Maintain conversation context and track conversation dynamics

**Implementation**:
```python
class ShortTermMemory:
    - add(item_type, content, metadata)
    - get_recent(n=5) -> List[MemoryItem]
    - get_by_type(item_type) -> List[MemoryItem]
    - summarize() -> str
    - clear()
```

**Memory Types**:
- `user_intent`: Customer's goal (pricing, travel, claim)
- `product_interest`: Products mentioned or viewed
- `concern`: Objections or hesitations
- `decision`: Agreement signals or purchase intent
- `conversation`: General context

**Memory Item Structure**:
```python
{
    "type": "user_intent",
    "content": "Asking about travel insurance",
    "metadata": {
        "query": "original user message",
        "urgent": False
    },
    "timestamp": "2025-01-15T10:30:00"
}
```

**Memory Management**:
- Max items: 10 (configurable)
- FIFO eviction: Oldest items removed
- Recency bias: Recent items weighted higher
- Type-based retrieval: Get all items of specific type

**Auto-Detection Patterns**:
```python
Pricing inquiry: ['giá', 'price', 'bao nhiêu', 'cost']
Travel intent: ['du lịch', 'travel', 'đi']
Claim request: ['tai nạn', 'accident', 'claim']
Agreement: ['yes', 'có', 'ok', 'được', 'đồng ý']
Objection: ['no', 'không', 'expensive', 'đắt']
```

### 4. TetInsuranceAgent Class

**Purpose**: Main orchestrator that integrates all components and manages Gemini interaction

**Key Methods**:

#### `__init__(gemini_api_key, customer_profile, current_phase)`
- Initializes Gemini model
- Creates knowledge base and memory
- Loads customer history
- Loads product knowledge

#### `_load_customer_history()`
Populates knowledge base with:
- Purchase history (motor, health, life insurance)
- Interaction history (past conversations)
- Behavioral data (travel patterns)
- Demographics (age, segment, income)
- Communication preferences (tone, channels)

#### `_load_product_knowledge()`
Adds to knowledge base:
- 6 insurance products with full details
- Coverage amounts and pricing
- Best use cases
- Tet-specific insights

#### `_build_context(user_message) -> str`
Constructs context string by:
1. Extracting customer profile summary
2. Adding current Tet phase information
3. Performing semantic search (top-5 docs)
4. Including short-term memory (last 5 items)
5. Combining into formatted context

#### `_create_system_prompt() -> str`
Generates comprehensive system prompt with:
- Agent role and personality
- Communication guidelines
- Current situation (phase, discounts)
- Objectives and tasks
- Cultural considerations
- Vietnamese language instructions

#### `generate_response(user_message) -> str`
Main response generation flow:
1. Build context from knowledge + memory
2. Create system prompt
3. Construct full prompt
4. Call Gemini API
5. Parse response
6. Update short-term memory
7. Return response

#### `_update_memory(user_message, agent_response)`
Analyzes conversation and stores:
- Detected user intent
- Product interests
- Concerns or objections
- Decision signals
- General conversation context

#### `get_proactive_message() -> str`
Generates outreach message by:
1. Building full customer context
2. Providing "proactive outreach" instruction
3. Letting Gemini create personalized greeting
4. Returning natural, warm message

## Data Flow

### Conversation Flow

```
1. User types message
   ↓
2. Message added to session history
   ↓
3. TetInsuranceAgent.generate_response() called
   ↓
4. Semantic search retrieves relevant docs
   ↓
5. Context builder combines:
   - Customer profile
   - Retrieved knowledge
   - Short-term memory
   - Current phase info
   ↓
6. System prompt created with:
   - Agent personality
   - Guidelines
   - Cultural notes
   ↓
7. Full prompt constructed:
   System + Context + User Message
   ↓
8. Gemini API called
   ↓
9. Response generated
   ↓
10. Memory updated with conversation
   ↓
11. Response displayed to user
```

### Knowledge Retrieval Flow

```
User message: "Tôi muốn đi du lịch Thái Lan"
   ↓
Embedding created: [0.05, 0.12, 0.08, ...]
   ↓
Similarity calculated with all docs
   ↓
Top matches:
1. "Customer loves traveling... Thailand" (0.82)
2. "International travel insurance..." (0.75)
3. "Tet travel peak season..." (0.68)
   ↓
Documents added to context
   ↓
Gemini uses this context to respond
```

## Gemini Integration

### Model Configuration

```python
model = genai.GenerativeModel('gemini-pro')
```

**Model**: gemini-pro
- Most capable Gemini model
- Good at Vietnamese language
- Natural conversation ability
- Context window: ~30K tokens

**Parameters** (using defaults):
- Temperature: 0.7 (balanced creativity)
- Top-p: 0.95 (nucleus sampling)
- Top-k: 40 (diversity)
- Max output tokens: Auto

### Prompt Engineering

**Structure**:
```
[System Prompt]
- Agent role and personality
- Guidelines and objectives
- Cultural considerations

[Context]
- Customer profile
- Tet phase information
- Retrieved knowledge (top-5 docs)
- Short-term memory (last 5 items)

[User Message]
- Current user input

[Instruction]
- Response guidelines
- Length guidance
- Context usage instruction
```

**Token Budget**:
- System prompt: ~800 tokens
- Context: ~1,200 tokens
- User message: ~100 tokens
- Response: ~500 tokens
- Total: ~2,600 tokens per turn

### Error Handling

```python
try:
    response = model.generate_content(prompt)
    return response.text
except Exception as e:
    return f"Xin lỗi, tôi gặp vấn đề kỹ thuật. (Error: {str(e)})"
```

## Session Management

### Streamlit Session State

```python
st.session_state = {
    'messages': [
        {'role': 'user', 'content': '...'},
        {'role': 'assistant', 'content': '...'}
    ],
    'customer_profile': {...},
    'current_phase': 'pre-tet',
    'short_term_memory': [...],
    'api_key_validated': True,
    'gemini_model': <model_object>
}
```

**Lifecycle**:
1. Session starts: Initialize empty state
2. User configures: Profile and phase selected
3. Conversation begins: Messages accumulate
4. Memory updates: After each turn
5. Reset: Clears messages and memory
6. Session ends: State discarded

## Performance Optimization

### Current Implementation

- **Embedding**: Character-based, fast (~1ms)
- **Search**: Linear scan, acceptable for <1000 docs
- **Memory**: In-memory, instant access
- **Context**: Constructed per turn (~50ms)

### Production Optimizations

1. **Vector Database**
   - Migrate to FAISS, Pinecone, or Weaviate
   - Approximate nearest neighbor search
   - Sub-millisecond retrieval

2. **Caching**
   - Cache frequent queries
   - Cache embeddings
   - Cache system prompts
   - Use Redis for distributed cache

3. **Batching**
   - Batch multiple searches
   - Batch embedding generation
   - Reduce API calls

4. **Async Processing**
   - Async Gemini calls
   - Parallel knowledge retrieval
   - Non-blocking UI updates

## Security Considerations

### Current Implementation

- API keys in session only (not persisted)
- No data written to disk
- Knowledge base rebuilt each session
- Memory cleared on reset

### Production Requirements

1. **API Key Management**
   - Store in environment variables
   - Use secret management (AWS Secrets, GCP Secret Manager)
   - Rotate keys regularly
   - Monitor usage and quota

2. **Data Privacy**
   - Encrypt customer data at rest
   - Encrypt data in transit (HTTPS)
   - Anonymize PII where possible
   - Implement data retention policies

3. **Access Control**
   - Authentication (OAuth, JWT)
   - Authorization (RBAC)
   - Audit logging
   - Rate limiting per user

4. **Compliance**
   - GDPR: Right to erasure, data portability
   - Vietnamese data laws
   - Insurance industry regulations
   - PCI DSS for payment data

## Scalability Plan

### Current Limitations

- Single user per session
- No data persistence
- Limited to ~1000 documents
- Synchronous processing

### Scaling Strategy

**Phase 1: Multi-User** (100 concurrent users)
- Add Redis for session management
- PostgreSQL for customer data
- Load balancer (Nginx)
- Multiple Streamlit instances

**Phase 2: High Performance** (1000+ users)
- Vector database (Pinecone/Weaviate)
- Microservices architecture
- Message queue (RabbitMQ/Kafka)
- Distributed caching

**Phase 3: Enterprise** (10,000+ users)
- Kubernetes orchestration
- Auto-scaling
- Multiple regions
- CDN for static assets
- Advanced monitoring (Datadog, New Relic)

## Monitoring & Observability

### Metrics to Track

**Performance**:
- Response time (p50, p95, p99)
- Gemini API latency
- Search latency
- Error rate

**Business**:
- Conversation starts
- Messages per conversation
- Conversion rate
- Customer satisfaction

**Technical**:
- API usage and quota
- Memory usage
- CPU utilization
- Cache hit rate

### Logging Strategy

```python
{
    "timestamp": "2025-01-15T10:30:00Z",
    "user_id": "customer_123",
    "session_id": "session_456",
    "event": "message_sent",
    "message_length": 45,
    "response_time_ms": 2340,
    "knowledge_docs_retrieved": 5,
    "memory_items_used": 3,
    "gemini_tokens": 850
}
```

## Testing Strategy

### Unit Tests
- SimpleEmbedding: Vector generation, similarity
- KnowledgeBase: Add, search, retrieval
- ShortTermMemory: Add, retrieve, summarize
- Context building logic

### Integration Tests
- End-to-end conversation flow
- Knowledge retrieval accuracy
- Memory persistence
- Gemini API integration

### User Acceptance Tests
- Response quality
- Cultural appropriateness
- Personalization accuracy
- Error handling

## Deployment Architecture

### Development
```
Local Machine
  ├── Streamlit Dev Server
  ├── Gemini API (Cloud)
  └── In-Memory Storage
```

### Production
```
Cloud Infrastructure (GCP/AWS)
  ├── Load Balancer
  ├── App Servers (Kubernetes)
  │   └── Streamlit + Agent Code
  ├── Vector Database (Pinecone)
  ├── Redis Cache
  ├── PostgreSQL (Customer Data)
  ├── Google Cloud Storage (Logs)
  └── Monitoring (Datadog)
```

## Future Enhancements

1. **Voice Integration**: Support voice input/output
2. **Multi-Language**: Full English support
3. **Advanced Analytics**: Conversation insights
4. **A/B Testing**: Test different prompts
5. **Reinforcement Learning**: Learn from feedback
6. **Sentiment Analysis**: Detect customer emotions
7. **Automated Follow-ups**: Schedule reminders
8. **Integration Hub**: Connect to CRM, policy systems

---

**Document Version**: 1.0
**Last Updated**: 2025-01-15
**Author**: AI Architecture Team
