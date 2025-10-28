# 🧧 Tet Insurance AI Agent - Gemini Powered

An advanced AI Agent for Vietnamese insurance marketing powered by Google's Gemini LLM, featuring semantic search, knowledge retrieval, and dynamic memory management.

## 🌟 Key Features

### 1. **Gemini LLM Integration**
- **Dynamic Response Generation**: No hard-coded sentences, all responses generated naturally by Gemini
- **Context-Aware**: Understands nuanced customer needs and responds appropriately
- **Cultural Intelligence**: Vietnamese language support with cultural awareness
- **Adaptive Tone**: Automatically adjusts communication style (casual/formal/friendly)

### 2. **Knowledge Layer with Semantic Search**
The agent maintains a comprehensive knowledge base with semantic search capabilities:

#### Customer Historical Data
- **Purchase History**: Past insurance policies, payment patterns, claims history
- **Interaction History**: Previous conversations, inquiries, abandoned purchases
- **Behavioral Data**: Travel patterns, lifestyle preferences, family information
- **Demographics**: Age, occupation, income level, family structure
- **Communication Preferences**: Preferred tone, channel preferences, response patterns

#### Product Knowledge
- Complete insurance product catalog with detailed descriptions
- Coverage details, pricing, best use cases
- Tet-specific insights and seasonal knowledge
- Competitive advantages and unique selling points

#### Semantic Search Engine
- Vector-based similarity matching for relevant context retrieval
- Retrieves top-K most relevant documents for each query
- Automatic relevance scoring and filtering
- Fast in-memory search without external dependencies

### 3. **Short-Term Memory System**
Dynamic conversation memory that makes the agent truly interactive:

- **Intent Tracking**: Recognizes and remembers user intentions (pricing, travel, claims)
- **Decision History**: Tracks customer's interest, agreements, and concerns
- **Concern Detection**: Identifies objections and hesitations
- **Context Continuity**: Maintains conversation flow across multiple turns
- **Automatic Summarization**: Generates conversation summaries for quick context

### 4. **Personalization Engine**
- **Profile-Based Adaptation**: Responses tailored to customer segment
- **Historical Context**: References past interactions naturally
- **Proactive Recommendations**: Suggests products based on profile and needs
- **Cultural Sensitivity**: Respects Vietnamese customs and Tet traditions

### 5. **Seasonality Awareness**
- **Phase-Specific Messaging**: Adapts strategy for Pre-Tet, Peak, and Post-Tet
- **Dynamic Pricing**: Automatic discount application based on phase
- **Urgency Creation**: Natural time-based urgency without being pushy
- **Cultural Moments**: Aligned with Vietnamese customs and expectations

## 🏗️ Architecture

```
User Input
    ↓
Semantic Search → Knowledge Base (Customer History + Products + Insights)
    ↓
Context Builder → Combines: Profile + Relevant Docs + Memory
    ↓
Gemini LLM → Generates Natural Response
    ↓
Memory Manager → Updates Short-Term Memory
    ↓
Response to User
```

## 📋 Prerequisites

- **Python 3.8+**
- **Gemini API Key** (Free from Google AI Studio)

## 🚀 Installation & Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements_gemini.txt
```

### Step 2: Get Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Copy your API key

### Step 3: Run the Application

```bash
streamlit run tet_insurance_agent_gemini.py
```

### Step 4: Enter API Key

1. Application opens in browser
2. Enter your Gemini API key in the sidebar
3. Select customer profile and Tet phase
4. Start chatting!

## 💡 Usage Guide

### Quick Start

1. **Configure Settings** (Left Sidebar)
   - Enter Gemini API key
   - Select customer profile (4 personas available)
   - Choose Tet season phase
   - View profile and phase details

2. **Start Conversation**
   - Click "Generate Proactive Message" for AI-initiated outreach
   - Use sample prompts for quick testing
   - Type custom messages for natural conversation

3. **Explore Advanced Features**
   - Click "View Knowledge Base" to see all stored information
   - Click "View Memory" to inspect conversation context
   - Monitor statistics in real-time

### Sample Conversations

#### Example 1: Travel Insurance Inquiry
```
User: Tôi muốn đi du lịch Thái Lan dịp Tết
Agent: [Gemini generates natural response about]:
- Acknowledges travel plans
- References customer's travel history
- Suggests international travel insurance
- Provides personalized pricing
- Mentions Tet special discount
- Asks about trip duration
```

#### Example 2: Family Protection
```
User: Tôi có 3 người trong gia đình, cần bảo hiểm gì?
Agent: [Gemini considers]:
- Family size from profile
- Current health insurance status
- Tet family gathering context
- Budget from historical data
- Recommends family health package
```

#### Example 3: Price Negotiation
```
User: Có vẻ hơi đắt
Agent: [Gemini responds with]:
- Empathy for budget concerns
- Value explanation
- Tet discount offering
- Bundle options
- Payment flexibility
```

## 🧠 How Knowledge & Memory Work

### Knowledge Base Structure

**Customer Historical Data:**
```python
{
  "id": "history_motor",
  "content": "Customer has motor insurance. Purchased 6 months ago...",
  "metadata": {
    "category": "purchase_history",
    "product": "motor"
  }
}
```

**Semantic Search:**
- User query: "Tôi muốn đi du lịch"
- Searches knowledge base using vector similarity
- Returns relevant documents about:
  - Customer's travel history
  - Travel insurance products
  - Past travel inquiries
  - Tet travel insights

### Short-Term Memory

**Memory Types:**
- `user_intent`: What the customer wants
- `product_interest`: Products mentioned/viewed
- `concern`: Objections or hesitations
- `decision`: Agreements or purchase signals
- `conversation`: General context

**Automatic Updates:**
```python
User: "Giá bao nhiêu?"
→ Memory stores: user_intent = "Asking about pricing"

User: "OK, tôi quan tâm"
→ Memory stores: decision = "Customer showing interest"
```

## 🔧 Technical Components

### 1. SimpleEmbedding Class
- Character-level text vectorization
- Vietnamese language support
- Cosine similarity calculation
- Fast, lightweight, no external models needed

### 2. KnowledgeBase Class
```python
kb = KnowledgeBase()
kb.add_document(id, content, metadata)
results = kb.search(query, top_k=5)
```

### 3. ShortTermMemory Class
```python
memory = ShortTermMemory(max_items=10)
memory.add(type, content, metadata)
recent = memory.get_recent(n=5)
summary = memory.summarize()
```

### 4. TetInsuranceAgent Class
- Main orchestrator
- Integrates all components
- Manages Gemini communication
- Builds context dynamically

## 🎨 Customization

### Adding New Customer Profiles

```python
customer_profiles["new_profile"] = {
    "name": "Name",
    "age": 30,
    "segment": "Segment",
    "tone": "casual/formal/friendly",
    "has_motor": True/False,
    "has_health": True/False,
    "has_life": True/False,
    "income": "low/medium/high",
    "travel_history": ["Place1", "Place2"],
    "tet_plans": "Description of plans"
}
```

### Modifying Knowledge Base

Edit the `_load_customer_history()` and `_load_product_knowledge()` methods in the `TetInsuranceAgent` class to add more historical data or product information.

### Adjusting Memory Settings

```python
# Change memory capacity
memory = ShortTermMemory(max_items=20)  # Default: 10

# Modify what gets stored
# Edit _update_memory() method to track different patterns
```

### Customizing System Prompt

Edit the `_create_system_prompt()` method to modify:
- Agent personality
- Communication guidelines
- Cultural considerations
- Business rules

## 📊 What Makes This Different

### Compared to Hard-Coded Agents:
❌ **Hard-Coded**: Limited responses, feels robotic
✅ **Gemini-Powered**: Infinite variety, natural conversations

❌ **Hard-Coded**: Can't handle unexpected questions
✅ **Gemini-Powered**: Adapts to any query contextually

❌ **Hard-Coded**: Same response for similar questions
✅ **Gemini-Powered**: Unique responses based on full context

### Semantic Search vs. Keyword Search:
❌ **Keyword**: "travel" only matches exact word
✅ **Semantic**: Understands "đi du lịch", "trip", "vacation"

❌ **Keyword**: No understanding of meaning
✅ **Semantic**: Finds conceptually related information

### Memory-Enabled vs. Stateless:
❌ **Stateless**: Forgets previous conversation
✅ **Memory-Enabled**: Builds on previous context

❌ **Stateless**: Repeats questions
✅ **Memory-Enabled**: Natural conversation flow

## 🎯 Use Cases Demonstrated

1. **Proactive Outreach**: AI-generated personalized Tet greetings
2. **Product Recommendation**: Context-aware suggestions
3. **Price Inquiry**: Dynamic pricing with justification
4. **Objection Handling**: Empathetic concern resolution
5. **Claim Support**: Emergency assistance with empathy
6. **Cross-Selling**: Natural upsell opportunities
7. **Seasonal Campaigns**: Phase-appropriate messaging

## 🔒 Privacy & Security

- API keys stored in session only
- No data persisted to disk
- Knowledge base rebuilt each session
- Memory cleared on reset
- GDPR-compliant design ready

## 📈 Performance Considerations

### Response Time:
- Semantic search: <100ms
- Context building: <50ms
- Gemini generation: 1-3 seconds
- Total: ~2-4 seconds per message

### Scalability:
- Current: In-memory, single user
- Production: Add vector database (Pinecone, Weaviate)
- Production: Add Redis for memory persistence
- Production: Add caching layer

## 🚀 Production Deployment Checklist

- [ ] Integrate with real CRM system
- [ ] Connect to actual insurance database
- [ ] Add vector database for semantic search at scale
- [ ] Implement Redis for memory persistence
- [ ] Add authentication & authorization
- [ ] Set up monitoring & analytics
- [ ] Implement rate limiting
- [ ] Add conversation logging
- [ ] Create admin dashboard
- [ ] Set up A/B testing
- [ ] Deploy on cloud (GCP, AWS, Azure)
- [ ] Add multi-channel support (Zalo API, Facebook API)
- [ ] Implement human handoff workflow
- [ ] Add payment gateway integration
- [ ] Create reporting system

## 🐛 Troubleshooting

### "Invalid API Key" Error
- Verify key is correct
- Check Google AI Studio quota
- Ensure internet connection

### Slow Responses
- Check internet speed
- Gemini API may be rate-limited
- Consider caching common queries

### Memory Not Updating
- Check console for errors
- Verify session state is preserved
- Reset and try again

### Irrelevant Search Results
- Tune similarity threshold
- Add more relevant documents
- Improve embedding method

## 📚 Additional Resources

- [Gemini API Documentation](https://ai.google.dev/docs)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Vietnamese NLP Resources](https://github.com/VinAIResearch)

## 🤝 Contributing

This is a demonstration project. For production use:
1. Review and enhance security measures
2. Add comprehensive error handling
3. Implement proper testing
4. Add monitoring and observability
5. Scale infrastructure appropriately

## 📄 License

Demo project for educational purposes.

## 🎉 Key Takeaways

This agent demonstrates:
✅ **Natural Conversations**: No robotic responses
✅ **Contextual Intelligence**: Understands full situation
✅ **Memory-Enabled**: Builds on previous context
✅ **Semantic Understanding**: Beyond keyword matching
✅ **Cultural Awareness**: Vietnamese language & customs
✅ **Dynamic Personalization**: Each response unique
✅ **Production-Ready Architecture**: Scalable design

---

**Built with ❤️ for Vietnamese Insurance Industry**
**Powered by Google Gemini AI**
