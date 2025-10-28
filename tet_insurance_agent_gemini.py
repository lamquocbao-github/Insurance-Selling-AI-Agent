import streamlit as st
import google.generativeai as genai
from datetime import datetime, timedelta
import json
import numpy as np
from typing import List, Dict, Any
import pickle
import os

# Page configuration
st.set_page_config(
    page_title="Tet Insurance AI Agent - Gemini Powered",
    page_icon="🧧",
    layout="wide"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'customer_profile' not in st.session_state:
    st.session_state.customer_profile = None
if 'current_phase' not in st.session_state:
    st.session_state.current_phase = "pre-tet"
if 'short_term_memory' not in st.session_state:
    st.session_state.short_term_memory = []
if 'conversation_summary' not in st.session_state:
    st.session_state.conversation_summary = ""
if 'gemini_model' not in st.session_state:
    st.session_state.gemini_model = None


class SimpleEmbedding:
    """Simple embedding using character-level features for semantic similarity"""
    
    @staticmethod
    def embed_text(text: str) -> np.ndarray:
        """Create a simple embedding vector from text"""
        # Normalize text
        text = text.lower().strip()
        
        # Character frequency vector (a-z, 0-9, common Vietnamese characters)
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789 àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ'
        vector = np.zeros(len(chars) + 10)  # Extra features
        
        # Character frequencies
        for i, char in enumerate(chars):
            vector[i] = text.count(char) / max(len(text), 1)
        
        # Additional features
        vector[-10] = len(text) / 100.0  # Length
        vector[-9] = text.count(' ') / max(len(text), 1)  # Word density
        vector[-8] = 1 if 'bảo hiểm' in text else 0
        vector[-7] = 1 if 'giá' in text or 'price' in text else 0
        vector[-6] = 1 if 'tết' in text or 'tet' in text else 0
        vector[-5] = 1 if 'du lịch' in text or 'travel' in text else 0
        vector[-4] = 1 if 'tai nạn' in text or 'accident' in text else 0
        vector[-3] = 1 if 'gia đình' in text or 'family' in text else 0
        vector[-2] = 1 if 'claim' in text or 'bồi thường' in text else 0
        vector[-1] = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        
        return vector
    
    @staticmethod
    def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)


class KnowledgeBase:
    """Knowledge base with semantic search capabilities"""
    
    def __init__(self):
        self.documents = []
        self.embeddings = []
        self.embedding_model = SimpleEmbedding()
    
    def add_document(self, doc_id: str, content: str, metadata: Dict[str, Any] = None):
        """Add a document to the knowledge base"""
        embedding = self.embedding_model.embed_text(content)
        
        self.documents.append({
            'id': doc_id,
            'content': content,
            'metadata': metadata or {},
            'timestamp': datetime.now().isoformat()
        })
        self.embeddings.append(embedding)
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Search for relevant documents using semantic similarity"""
        if not self.documents:
            return []
        
        query_embedding = self.embedding_model.embed_text(query)
        
        # Calculate similarities
        similarities = []
        for i, doc_embedding in enumerate(self.embeddings):
            similarity = self.embedding_model.cosine_similarity(query_embedding, doc_embedding)
            similarities.append((i, similarity))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return top-k results
        results = []
        for i, score in similarities[:top_k]:
            result = self.documents[i].copy()
            result['similarity_score'] = score
            results.append(result)
        
        return results
    
    def get_all_documents(self) -> List[Dict[str, Any]]:
        """Get all documents in the knowledge base"""
        return self.documents


class ShortTermMemory:
    """Short-term memory for conversation context"""
    
    def __init__(self, max_items: int = 10):
        self.max_items = max_items
        self.items = []
    
    def add(self, item_type: str, content: str, metadata: Dict[str, Any] = None):
        """Add an item to short-term memory"""
        memory_item = {
            'type': item_type,
            'content': content,
            'metadata': metadata or {},
            'timestamp': datetime.now().isoformat()
        }
        
        self.items.append(memory_item)
        
        # Keep only the most recent items
        if len(self.items) > self.max_items:
            self.items = self.items[-self.max_items:]
    
    def get_recent(self, n: int = 5) -> List[Dict[str, Any]]:
        """Get the n most recent items"""
        return self.items[-n:] if self.items else []
    
    def get_by_type(self, item_type: str) -> List[Dict[str, Any]]:
        """Get all items of a specific type"""
        return [item for item in self.items if item['type'] == item_type]
    
    def summarize(self) -> str:
        """Generate a summary of short-term memory"""
        if not self.items:
            return "No recent conversation history."
        
        summary_parts = []
        
        # Group by type
        for item_type in ['user_intent', 'product_interest', 'concern', 'decision']:
            items = self.get_by_type(item_type)
            if items:
                latest = items[-1]
                summary_parts.append(f"{item_type}: {latest['content']}")
        
        return " | ".join(summary_parts) if summary_parts else "Recent conversation context available."
    
    def clear(self):
        """Clear all items from memory"""
        self.items = []


class TetInsuranceAgent:
    """AI Agent with Gemini LLM, knowledge base, and memory"""
    
    def __init__(self, gemini_api_key: str, customer_profile: Dict, current_phase: str):
        self.profile = customer_profile
        self.phase = current_phase
        
        # Initialize Gemini
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Initialize knowledge base and memory
        self.knowledge_base = KnowledgeBase()
        self.short_term_memory = ShortTermMemory(max_items=10)
        
        # Load customer historical data
        self._load_customer_history()
        
        # Load insurance product knowledge
        self._load_product_knowledge()
    
    def _load_customer_history(self):
        """Load customer historical data into knowledge base"""
        profile = self.profile
        
        # Purchase history
        if profile.get('has_motor'):
            self.knowledge_base.add_document(
                'history_motor',
                f"Customer {profile['name']} has motor insurance. Purchased 6 months ago. No claims filed. Regular premium payer.",
                {'category': 'purchase_history', 'product': 'motor'}
            )
        
        if profile.get('has_health'):
            self.knowledge_base.add_document(
                'history_health',
                f"Customer has health insurance for family of {profile.get('family_size', 1)}. Active policy. Used for annual checkups.",
                {'category': 'purchase_history', 'product': 'health'}
            )
        
        if profile.get('has_life'):
            self.knowledge_base.add_document(
                'history_life',
                f"Customer has life insurance policy worth 500 million VND. Beneficiary: family members.",
                {'category': 'purchase_history', 'product': 'life'}
            )
        
        # Interaction history
        self.knowledge_base.add_document(
            'interaction_last_tet',
            f"Last Tet, customer {profile['name']} inquired about travel insurance but didn't purchase. Mentioned budget concerns.",
            {'category': 'interaction_history', 'event': 'last_tet'}
        )
        
        # Behavioral data
        if profile.get('travel_history'):
            travels = ', '.join(profile['travel_history'])
            self.knowledge_base.add_document(
                'behavior_travel',
                f"Customer loves traveling. Recent destinations: {travels}. Travels 2-3 times per year. Prefers domestic destinations.",
                {'category': 'behavior', 'interest': 'travel'}
            )
        
        # Demographics and preferences
        self.knowledge_base.add_document(
            'profile_demographics',
            f"{profile['name']}, {profile['age']} years old, {profile['segment']}. Income level: {profile.get('income', 'medium')}. Tet plans: {profile.get('tet_plans', 'Not specified')}",
            {'category': 'demographics'}
        )
        
        # Communication preferences
        self.knowledge_base.add_document(
            'profile_communication',
            f"Customer prefers {profile['tone']} communication style. Responds well to personalized offers. Active on Zalo and Facebook.",
            {'category': 'communication'}
        )
    
    def _load_product_knowledge(self):
        """Load insurance product information into knowledge base"""
        
        products = {
            'travel_domestic': {
                'name': 'Domestic Travel Insurance',
                'description': 'Comprehensive coverage for travel within Vietnam. Covers medical emergencies, trip cancellation, lost baggage, and 24/7 assistance.',
                'price': 150000,
                'coverage': 50000000,
                'best_for': 'Weekend trips, Tet travel to hometown, domestic vacations'
            },
            'travel_international': {
                'name': 'International Travel Insurance',
                'description': 'Full protection for overseas travel. Includes medical coverage up to 100 million VND, emergency evacuation, and trip interruption.',
                'price': 500000,
                'coverage': 100000000,
                'best_for': 'ASEAN travel, long-distance flights, adventure trips'
            },
            'motor_extension': {
                'name': 'Motor Insurance Highway Extension',
                'description': 'Extends your motor insurance for long-distance travel. Covers highway accidents, passenger protection, and roadside assistance.',
                'price': 250000,
                'coverage': 'Extended distance + 3 passengers',
                'best_for': 'Tet journey home, long road trips, highway travel'
            },
            'family_health': {
                'name': 'Family Health Package',
                'description': 'Complete health coverage for entire family. Includes annual checkups, hospitalization, outpatient care, and dental.',
                'price': 3500000,
                'coverage': 500000000,
                'best_for': 'Families with children, comprehensive protection, peace of mind'
            },
            'accident': {
                'name': 'Personal Accident Insurance',
                'description': 'Protection against accidents resulting in injury or death. Covers medical expenses, disability benefits, and death benefits.',
                'price': 300000,
                'coverage': 200000000,
                'best_for': 'Active lifestyle, motorbike riders, additional protection'
            },
            'life_savings': {
                'name': 'Life Insurance with Savings',
                'description': 'Dual benefit policy combining life protection with savings. Guaranteed returns plus insurance coverage for family.',
                'price': 5000000,
                'coverage': '1 billion VND + investment returns',
                'best_for': 'Long-term planning, wealth building, family security'
            }
        }
        
        for product_id, product_info in products.items():
            content = f"{product_info['name']}: {product_info['description']} Price: {product_info['price']:,} VND. Coverage: {product_info['coverage']}. Best for: {product_info['best_for']}"
            
            self.knowledge_base.add_document(
                f'product_{product_id}',
                content,
                {'category': 'product', 'product_id': product_id, **product_info}
            )
        
        # Tet-specific knowledge
        tet_knowledge = {
            'tet_travel_peak': 'During Tet, traffic accidents increase by 40%. Highway travel is especially risky. Extended motor insurance is crucial.',
            'tet_family_gathering': 'Tet is time for family reunion. Many people host large gatherings, increasing health risks. Family health packages popular.',
            'tet_gift_insurance': 'Insurance as Tet gift is becoming popular. Shows care for loved ones. Life insurance and health insurance most gifted.',
            'tet_budget': 'People receive bonuses before Tet. Good time to invest in insurance. Many willing to spend on protection.',
            'tet_discount': f'Special Tet promotions available. {self._get_phase_discount()}% discount during {self.phase} phase.'
        }
        
        for knowledge_id, content in tet_knowledge.items():
            self.knowledge_base.add_document(
                knowledge_id,
                content,
                {'category': 'tet_insights'}
            )
    
    def _get_phase_discount(self) -> int:
        """Get discount percentage based on current phase"""
        if self.phase == "tet-peak":
            return 30
        elif self.phase == "pre-tet":
            return 15
        else:
            return 10
    
    def _get_phase_context(self) -> str:
        """Get context about current Tet phase"""
        phase_contexts = {
            "pre-tet": "We are in the Pre-Tet planning phase (Mid-December to Late January). Focus on preparation and early bird offers. Customers are planning their Tet activities.",
            "tet-peak": "We are in the Tet Holiday Peak (1 week before to 1 week after Tet). This is urgent time with flash sales and instant coverage needs. Customers are actively traveling and celebrating.",
            "post-tet": "We are in the Post-Tet season (February onwards). Focus on follow-ups, renewals, and new year resolutions. Customers are back to normal routine."
        }
        return phase_contexts.get(self.phase, "")
    
    def _build_context(self, user_message: str) -> str:
        """Build context from knowledge base and memory"""
        
        # Search knowledge base for relevant information
        relevant_docs = self.knowledge_base.search(user_message, top_k=5)
        
        # Build context string
        context_parts = []
        
        # Add customer profile context
        context_parts.append(f"CUSTOMER PROFILE: {self.profile['name']}, {self.profile['age']} years old, {self.profile['segment']}")
        
        # Add phase context
        context_parts.append(f"TET PHASE: {self._get_phase_context()}")
        
        # Add relevant knowledge
        if relevant_docs:
            context_parts.append("RELEVANT CUSTOMER HISTORY & KNOWLEDGE:")
            for doc in relevant_docs:
                if doc['similarity_score'] > 0.1:  # Only include relevant matches
                    context_parts.append(f"- {doc['content']}")
        
        # Add short-term memory
        recent_memory = self.short_term_memory.get_recent(5)
        if recent_memory:
            context_parts.append("RECENT CONVERSATION:")
            for memory in recent_memory:
                context_parts.append(f"- {memory['type']}: {memory['content']}")
        
        return "\n".join(context_parts)
    
    def _create_system_prompt(self) -> str:
        """Create system prompt for Gemini"""
        
        prompt = f"""You are an AI insurance agent for a Vietnamese insurance company, specializing in Tet (Lunar New Year) season.

ROLE & PERSONALITY:
- Friendly, helpful, and culturally aware Vietnamese insurance advisor
- Communication tone: {self.profile['tone']} (adapt accordingly)
- Use appropriate Vietnamese greetings and expressions
- Be empathetic and understanding of customer needs
- Focus on family protection and Tet traditions

CURRENT SITUATION:
- Tet Phase: {self.phase}
- Discount Available: {self._get_phase_discount()}%
- Customer Segment: {self.profile['segment']}

OBJECTIVES:
1. Understand customer needs through natural conversation
2. Provide personalized insurance recommendations based on their profile and history
3. Be proactive about Tet-related risks and opportunities
4. Handle inquiries about pricing, coverage, and claims
5. Create urgency during peak periods while being respectful

GUIDELINES:
- Always reference customer's historical data when relevant
- Mention specific Tet plans and adapt recommendations accordingly
- Use Vietnamese language naturally (mix with English for technical terms if needed)
- Be concise but warm in responses
- Focus on value and protection, not just selling
- Address concerns with empathy
- For claims, prioritize safety first, then process

IMPORTANT CULTURAL NOTES:
- Tet is about family, reunion, and fresh starts
- Insurance is increasingly seen as showing care for loved ones
- Lucky numbers (8, 9) and avoiding unlucky (4) matters to some customers
- Gifting insurance during Tet is becoming popular

Remember: You're not just selling insurance, you're helping families protect what matters most during the most important holiday of the year."""

        return prompt
    
    def generate_response(self, user_message: str) -> str:
        """Generate response using Gemini with context"""
        
        # Build context from knowledge base and memory
        context = self._build_context(user_message)
        
        # Create full prompt
        system_prompt = self._create_system_prompt()
        
        full_prompt = f"""{system_prompt}

{context}

USER MESSAGE: {user_message}

Provide a helpful, natural response. Be specific and reference the customer's context when relevant. Keep response concise (2-4 sentences for simple queries, longer for complex ones)."""

        try:
            # Generate response using Gemini
            response = self.model.generate_content(full_prompt)
            
            generated_text = response.text
            
            # Update short-term memory
            self._update_memory(user_message, generated_text)
            
            return generated_text
            
        except Exception as e:
            return f"Xin lỗi, tôi gặp chút vấn đề kỹ thuật. Bạn có thể thử lại không? (Error: {str(e)})"
    
    def _update_memory(self, user_message: str, agent_response: str):
        """Update short-term memory based on conversation"""
        
        user_lower = user_message.lower()
        
        # Detect user intent and store in memory
        if any(word in user_lower for word in ['giá', 'price', 'bao nhiêu', 'cost']):
            self.short_term_memory.add('user_intent', 'Asking about pricing', {'query': user_message})
        
        if any(word in user_lower for word in ['du lịch', 'travel', 'đi']):
            self.short_term_memory.add('user_intent', 'Interested in travel insurance', {'query': user_message})
        
        if any(word in user_lower for word in ['tai nạn', 'accident', 'claim']):
            self.short_term_memory.add('user_intent', 'Needs claim support', {'query': user_message, 'urgent': True})
        
        if any(word in user_lower for word in ['yes', 'có', 'ok', 'được', 'đồng ý']):
            self.short_term_memory.add('decision', 'Customer showing interest/agreement', {'response': user_message})
        
        if any(word in user_lower for word in ['no', 'không', 'expensive', 'đắt']):
            self.short_term_memory.add('concern', 'Customer has concerns or objections', {'response': user_message})
        
        # Store general conversation context
        self.short_term_memory.add('conversation', f"User: {user_message} | Agent: {agent_response[:100]}...")
    
    def get_proactive_message(self) -> str:
        """Generate proactive outreach message"""
        
        context = self._build_context("generate proactive Tet greeting and recommendation")
        system_prompt = self._create_system_prompt()
        
        prompt = f"""{system_prompt}

{context}

Generate a warm, personalized proactive message to reach out to this customer for Tet season. 
- Start with appropriate Vietnamese Tet greeting
- Reference their specific situation or Tet plans
- Suggest 1-2 relevant insurance products
- Create natural urgency based on the current phase
- Keep it friendly and not too salesy (3-5 sentences)"""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Chúc mừng năm mới! 🧧 (Error generating message: {str(e)})"


def init_gemini_model(api_key: str):
    """Initialize Gemini model with API key"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        # Test the model
        test_response = model.generate_content("Say hello")
        return model, None
    except Exception as e:
        return None, str(e)


# Streamlit UI
def main():
    st.title("🧧 Tet Insurance AI Agent - Gemini Powered")
    st.markdown("*AI Agent với Gemini LLM, Knowledge Base & Memory*")
    
    # Sidebar - Configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Gemini API Key
        st.subheader("🔑 Gemini API")
        gemini_api_key = st.text_input(
            "Enter Gemini API Key",
            type="password",
            help="Get your API key from https://makersuite.google.com/app/apikey"
        )
        
        if gemini_api_key:
            if 'api_key_validated' not in st.session_state:
                model, error = init_gemini_model(gemini_api_key)
                if error:
                    st.error(f"❌ Invalid API key: {error}")
                    st.session_state.api_key_validated = False
                else:
                    st.success("✅ API key validated!")
                    st.session_state.gemini_model = model
                    st.session_state.api_key_validated = True
        else:
            st.warning("⚠️ Please enter Gemini API key to use the agent")
            st.info("Get free API key at: https://makersuite.google.com/app/apikey")
        
        st.divider()
        
        # Customer Profile Selection
        st.subheader("👤 Customer Profile")
        
        customer_profiles = {
            "Minh (28) - Young Professional": {
                "name": "Minh Nguyen",
                "age": 28,
                "segment": "Young Professional",
                "tone": "casual",
                "has_motor": True,
                "has_health": False,
                "has_life": False,
                "income": "high",
                "travel_history": ["Da Nang", "Phu Quoc"],
                "tet_plans": "Traveling home to Vinh (300km)"
            },
            "Linh (35) - Family with Kids": {
                "name": "Linh Tran",
                "age": 35,
                "segment": "Family with Kids",
                "tone": "friendly",
                "has_motor": True,
                "has_health": True,
                "has_life": False,
                "income": "medium",
                "family_size": 4,
                "children": 2,
                "travel_history": ["Vung Tau", "Nha Trang"],
                "tet_plans": "Hosting family gathering at home"
            },
            "Tuấn (55) - Senior": {
                "name": "Tuấn Lê",
                "age": 55,
                "segment": "Senior/Retiree",
                "tone": "formal",
                "has_motor": True,
                "has_health": True,
                "has_life": True,
                "income": "medium",
                "travel_history": ["Dalat", "Ha Noi"],
                "tet_plans": "Visiting children in Saigon"
            },
            "Hùng (42) - Business Owner": {
                "name": "Hùng Pham",
                "age": 42,
                "segment": "Small Business Owner",
                "tone": "professional",
                "has_motor": True,
                "has_health": True,
                "has_life": False,
                "income": "high",
                "business": "Restaurant",
                "travel_history": ["Singapore", "Bangkok"],
                "tet_plans": "Business trip to Hanoi, then family vacation"
            }
        }
        
        selected_profile_name = st.selectbox(
            "Select Customer",
            options=list(customer_profiles.keys())
        )
        
        st.session_state.customer_profile = customer_profiles[selected_profile_name]
        
        # Display profile details
        with st.expander("📋 Profile Details"):
            profile = st.session_state.customer_profile
            st.write(f"**Name:** {profile['name']}")
            st.write(f"**Age:** {profile['age']}")
            st.write(f"**Segment:** {profile['segment']}")
            st.write(f"**Tone:** {profile['tone']}")
            st.write(f"**Tet Plans:** {profile['tet_plans']}")
            st.write(f"**Travel History:** {', '.join(profile.get('travel_history', []))}")
            st.write(f"**Current Insurance:**")
            st.write(f"- Motor: {'✅' if profile.get('has_motor') else '❌'}")
            st.write(f"- Health: {'✅' if profile.get('has_health') else '❌'}")
            st.write(f"- Life: {'✅' if profile.get('has_life') else '❌'}")
        
        st.divider()
        
        # Tet Phase Selection
        st.subheader("📅 Tet Season Phase")
        phase_options = {
            "Pre-Tet Planning": "pre-tet",
            "Tet Holiday Peak": "tet-peak",
            "Post-Tet Season": "post-tet"
        }
        
        selected_phase = st.selectbox(
            "Select Phase",
            options=list(phase_options.keys())
        )
        
        st.session_state.current_phase = phase_options[selected_phase]
        
        # Display phase info
        phase_info = {
            "pre-tet": {"discount": "15%", "focus": "Planning & Preparation"},
            "tet-peak": {"discount": "30%", "focus": "Urgent Coverage & Flash Sales"},
            "post-tet": {"discount": "10%", "focus": "Renewals & Resolutions"}
        }
        
        current_phase_info = phase_info[st.session_state.current_phase]
        st.info(f"**Discount:** {current_phase_info['discount']}\n\n**Focus:** {current_phase_info['focus']}")
        
        st.divider()
        
        # Quick Actions
        st.subheader("⚡ Quick Actions")
        
        if st.button("🎯 Generate Proactive Message", use_container_width=True):
            if not gemini_api_key or not st.session_state.get('api_key_validated'):
                st.error("Please enter valid Gemini API key first!")
            else:
                with st.spinner("Generating personalized message..."):
                    agent = TetInsuranceAgent(
                        gemini_api_key,
                        st.session_state.customer_profile,
                        st.session_state.current_phase
                    )
                    
                    proactive_msg = agent.get_proactive_message()
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": proactive_msg
                    })
                    
                    st.rerun()
        
        if st.button("📊 View Knowledge Base", use_container_width=True):
            if not gemini_api_key or not st.session_state.get('api_key_validated'):
                st.error("Please enter valid Gemini API key first!")
            else:
                agent = TetInsuranceAgent(
                    gemini_api_key,
                    st.session_state.customer_profile,
                    st.session_state.current_phase
                )
                
                docs = agent.knowledge_base.get_all_documents()
                
                st.session_state.show_knowledge = True
                st.session_state.knowledge_docs = docs
        
        if st.button("🧠 View Memory", use_container_width=True):
            st.session_state.show_memory = True
        
        if st.button("🔄 Reset Conversation", use_container_width=True):
            st.session_state.messages = []
            st.session_state.short_term_memory = []
            st.session_state.conversation_summary = ""
            st.rerun()
        
        st.divider()
        
        # Statistics
        st.subheader("📈 Statistics")
        st.metric("Total Messages", len(st.session_state.messages))
        st.metric("Memory Items", len(st.session_state.get('short_term_memory', [])))
        st.metric("Current Phase", st.session_state.current_phase.replace("-", " ").title())
    
    # Main Chat Interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 Chat with AI Agent")
        
        # Display chat messages
        chat_container = st.container(height=500)
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # Chat input
        if gemini_api_key and st.session_state.get('api_key_validated'):
            user_input = st.chat_input("Nhắn tin với AI Agent...")
            
            if user_input:
                # Add user message
                st.session_state.messages.append({
                    "role": "user",
                    "content": user_input
                })
                
                # Generate AI response
                with st.spinner("Agent đang suy nghĩ..."):
                    agent = TetInsuranceAgent(
                        gemini_api_key,
                        st.session_state.customer_profile,
                        st.session_state.current_phase
                    )
                    
                    # Update agent's short-term memory from session
                    if st.session_state.short_term_memory:
                        agent.short_term_memory.items = st.session_state.short_term_memory
                    
                    response = agent.generate_response(user_input)
                    
                    # Save updated memory to session
                    st.session_state.short_term_memory = agent.short_term_memory.items
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response
                    })
                
                st.rerun()
        else:
            st.info("👆 Please enter your Gemini API key in the sidebar to start chatting")
        
        # Sample prompts
        if gemini_api_key and st.session_state.get('api_key_validated'):
            st.markdown("**💡 Thử các câu hỏi này:**")
            sample_prompts = [
                "Tôi muốn đi du lịch Thái Lan dịp Tết",
                "Giá bảo hiểm xe máy cho chuyến về quê bao nhiêu?",
                "Tôi có 3 người trong gia đình, cần bảo hiểm gì?",
                "Có gói nào phù hợp với kế hoạch Tết của tôi không?"
            ]
            
            prompt_cols = st.columns(2)
            for i, prompt in enumerate(sample_prompts):
                with prompt_cols[i % 2]:
                    if st.button(prompt, key=f"prompt_{i}", use_container_width=True):
                        # Simulate user input
                        st.session_state.messages.append({
                            "role": "user",
                            "content": prompt
                        })
                        
                        with st.spinner("Agent đang suy nghĩ..."):
                            agent = TetInsuranceAgent(
                                gemini_api_key,
                                st.session_state.customer_profile,
                                st.session_state.current_phase
                            )
                            
                            if st.session_state.short_term_memory:
                                agent.short_term_memory.items = st.session_state.short_term_memory
                            
                            response = agent.generate_response(prompt)
                            
                            st.session_state.short_term_memory = agent.short_term_memory.items
                            
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": response
                            })
                        
                        st.rerun()
    
    with col2:
        st.subheader("🎯 Agent Capabilities")
        
        st.markdown("""
        **✨ Powered by Gemini AI**
        - Dynamic response generation
        - Context-aware conversations
        - Natural language understanding
        
        **📚 Knowledge Layer**
        - Customer purchase history
        - Behavioral patterns
        - Product catalog
        - Tet insights
        - Semantic search
        
        **🧠 Memory System**
        - Short-term conversation memory
        - Intent tracking
        - Decision history
        - Concern detection
        
        **🎭 Personalization**
        - Profile-based responses
        - Tone adaptation
        - Cultural awareness
        - Context retrieval
        """)
        
        st.divider()
        
        st.subheader("💡 How It Works")
        
        st.markdown("""
        1. **User Input** → Message sent
        2. **Semantic Search** → Relevant knowledge retrieved
        3. **Context Building** → Profile + History + Memory
        4. **Gemini LLM** → Generates natural response
        5. **Memory Update** → Stores conversation context
        """)
    
    # Knowledge Base Viewer (Modal)
    if st.session_state.get('show_knowledge'):
        st.divider()
        st.subheader("📚 Knowledge Base Contents")
        
        docs = st.session_state.get('knowledge_docs', [])
        
        # Group by category
        categories = {}
        for doc in docs:
            category = doc['metadata'].get('category', 'other')
            if category not in categories:
                categories[category] = []
            categories[category].append(doc)
        
        for category, category_docs in categories.items():
            with st.expander(f"📁 {category.replace('_', ' ').title()} ({len(category_docs)} documents)"):
                for doc in category_docs:
                    st.markdown(f"**{doc['id']}**")
                    st.text(doc['content'])
                    st.caption(f"Added: {doc['timestamp']}")
                    st.divider()
        
        if st.button("Close Knowledge Base"):
            st.session_state.show_knowledge = False
            st.rerun()
    
    # Memory Viewer (Modal)
    if st.session_state.get('show_memory'):
        st.divider()
        st.subheader("🧠 Short-Term Memory")
        
        memory_items = st.session_state.get('short_term_memory', [])
        
        if memory_items:
            for i, item in enumerate(reversed(memory_items), 1):
                with st.expander(f"Memory {i}: {item['type']}"):
                    st.write(f"**Type:** {item['type']}")
                    st.write(f"**Content:** {item['content']}")
                    st.write(f"**Time:** {item['timestamp']}")
                    if item.get('metadata'):
                        st.write(f"**Metadata:** {item['metadata']}")
        else:
            st.info("No memory items yet. Start a conversation!")
        
        if st.button("Close Memory View"):
            st.session_state.show_memory = False
            st.rerun()


if __name__ == "__main__":
    main()
