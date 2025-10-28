# 🧧 Tet Insurance AI Agent Demo

A comprehensive Streamlit-based demo of an AI Agent for insurance marketing during Vietnam's Tet (Lunar New Year) season.

## Features

### 1. ✨ Personalization Engine
- **Customer Profile Recognition**: Automatically adapts to different customer segments
  - Young Professional
  - Family with Kids
  - Senior/Retiree
  - Small Business Owner
- **Tone Adaptation**: Adjusts language formality based on customer age and preferences
- **Context-Aware Recommendations**: Smart product suggestions based on customer profile and needs

### 2. 📅 Seasonality Awareness
- **Tet Timeline Automation**: Three distinct phases
  - Pre-Tet Planning (Mid-December to Late January)
  - Tet Holiday Peak (1 week before to 1 week after)
  - Post-Tet Season (February onwards)
- **Dynamic Pricing**: Automatic discounts during peak Tet period
- **Cultural Moment Triggers**: Special offers aligned with Vietnamese customs

### 3. ⚡ Tactical Support Functions
- **Quick Quote Generator**: Instant travel insurance quotes (30 seconds)
- **Simple Decision Tree**: Natural conversation flow for product recommendations
- **Claim Fast-Track**: Emergency claim support with step-by-step guidance
- **Multi-Channel Simulation**: Mimics Zalo, Facebook Messenger, and web chat

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Run the application**
```bash
streamlit run tet_insurance_agent.py
```

3. **Access the demo**
The application will automatically open in your browser at `http://localhost:8501`

## Usage Guide

### Getting Started

1. **Select Customer Profile** (Left Sidebar)
   - Choose from 4 pre-defined customer personas
   - Each has different insurance needs and communication preferences
   - View detailed profile information in the expandable section

2. **Choose Tet Phase** (Left Sidebar)
   - Pre-Tet Planning: Early preparation phase with bundle deals
   - Tet Holiday Peak: Active holiday period with flash sales (30% discount)
   - Post-Tet Season: Follow-up and renewal phase

3. **Start Conversation**
   - Click "Generate Recommendations" for AI-initiated outreach
   - Use sample prompts for quick testing
   - Type custom messages in the chat input

### Sample Conversation Flows

#### Example 1: Travel Insurance
```
User: "Tôi muốn đi du lịch Thái Lan"
Agent: Generates instant quote with coverage details and purchase option
```

#### Example 2: Emergency Claim
```
User: "Tôi bị tai nạn, giúp tôi với"
Agent: Provides step-by-step claim filing process with photo upload instructions
```

#### Example 3: Price Inquiry
```
User: "Giá bảo hiểm xe máy bao nhiêu?"
Agent: Shows relevant products with pricing and Tet special offers
```

## Key Components

### Customer Profiles
- **Young Professional**: Travel-focused, casual tone, motor insurance holder
- **Family with Kids**: Family protection needs, friendly tone, health insurance
- **Senior**: Formal tone, comprehensive coverage, visiting family focus
- **Business Owner**: Professional tone, business protection needs

### Insurance Products
1. Domestic Travel Insurance (150,000 VND)
2. International Travel Insurance (500,000 VND/year)
3. Motor Insurance Extension (250,000 VND)
4. Family Health Package (3,500,000 VND/year)
5. Personal Accident Insurance (300,000 VND/year)
6. Life + Savings Insurance (5,000,000 VND/year)

### AI Agent Capabilities

#### Personalization
- Recognizes customer segment automatically
- Adapts greeting style (casual/formal/friendly)
- Remembers conversation context
- Provides relevant product recommendations

#### Seasonality
- Phase-based messaging strategy
- Automatic discount application during peak Tet
- Cultural sensitivity in communication
- Timeline-triggered offers

#### Tactical Support
- Quick quote generation (< 30 seconds)
- Emergency claim handling
- Payment gateway simulation
- Decision tree logic for recommendations

## Technical Architecture

### Main Components

1. **TetInsuranceAgent Class**
   - Core AI agent logic
   - Response generation engine
   - Recommendation system
   - Quote calculator

2. **Session State Management**
   - Conversation history
   - Customer profile tracking
   - Context preservation

3. **UI Layout**
   - Sidebar: Configuration and quick actions
   - Main area: Chat interface
   - Right panel: Product catalog and feature list

## Customization

### Adding New Customer Profiles
Edit the `CUSTOMER_PROFILES` dictionary in the code:
```python
CUSTOMER_PROFILES["new_segment"] = {
    "name": "Customer Name",
    "age": 30,
    "segment": "Segment Name",
    "tone": "casual/formal/friendly",
    # ... other attributes
}
```

### Adding New Products
Edit the `INSURANCE_PRODUCTS` dictionary:
```python
INSURANCE_PRODUCTS["product_key"] = {
    "name": "Product Name",
    "price": 100000,
    "coverage": "Coverage amount",
    "duration": "Duration"
}
```

### Modifying Tet Phases
Edit the `TET_PHASES` dictionary to adjust timing and messaging strategy.

## Features Demonstration

### 1. Personalization in Action
- Switch between customer profiles to see tone adaptation
- Notice how recommendations change based on profile
- Observe different greeting styles

### 2. Seasonality Awareness
- Compare prices between Pre-Tet and Tet-Peak phases
- See messaging changes across phases
- Notice cultural elements in responses

### 3. Tactical Support
- Test quick quote generation with travel inquiries
- Simulate claim process with accident keywords
- Experience natural conversation flow

## Metrics Tracked

The demo tracks:
- Total messages exchanged
- Current Tet phase
- Customer profile being simulated
- Conversation context

## Best Practices Demonstrated

1. **Simple, Fast, Personal**: Responses within 30 seconds
2. **Culturally Aware**: Vietnamese language, Tet customs, family focus
3. **Context Retention**: Remembers conversation history
4. **Escalation Ready**: Identifies complex scenarios for human handoff

## Limitations (Demo)

- Payment gateway links are simulated
- Photo upload for claims is simulated
- Actual insurance policy generation not included
- No real-time API integrations

## Production Considerations

For production deployment, you would need:
1. Integration with actual insurance systems
2. Real payment gateway (MoMo, ZaloPay)
3. CRM system integration
4. Multi-language NLP model
5. Security and compliance measures
6. Analytics and reporting dashboard
7. Human agent escalation workflow
8. Multi-channel deployment (Zalo, Facebook, Website)

## Support

For questions or issues with the demo:
- Check the code comments for detailed explanations
- Review sample prompts for usage examples
- Experiment with different profile and phase combinations

## License

This is a demonstration project for educational purposes.

---

**Built with ❤️ for Vietnamese Insurance Industry**
