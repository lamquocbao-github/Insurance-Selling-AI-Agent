import streamlit as st
import json
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="Tet Insurance AI Agent Demo",
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
if 'conversation_context' not in st.session_state:
    st.session_state.conversation_context = {}

# Customer profiles database
CUSTOMER_PROFILES = {
    "young_professional": {
        "name": "Minh Nguyen",
        "age": 28,
        "segment": "Young Professional",
        "tone": "casual",
        "greeting": "Chào Minh! 🧧",
        "has_motor": True,
        "has_health": False,
        "has_life": False,
        "income": "high",
        "travel_history": ["Da Nang", "Phu Quoc"],
        "tet_plans": "Traveling home to Vinh (300km)"
    },
    "family": {
        "name": "Linh Tran",
        "age": 35,
        "segment": "Family with Kids",
        "tone": "friendly",
        "greeting": "Chúc mừng năm mới chị Linh!",
        "has_motor": True,
        "has_health": True,
        "has_life": False,
        "income": "medium",
        "family_size": 4,
        "children": 2,
        "tet_plans": "Hosting family gathering"
    },
    "senior": {
        "name": "Tuấn Lê",
        "age": 55,
        "segment": "Senior/Retiree",
        "tone": "formal",
        "greeting": "Kính chúc quý khách năm mới an khang thịnh vượng",
        "has_motor": True,
        "has_health": True,
        "has_life": True,
        "income": "medium",
        "tet_plans": "Visiting children in Saigon"
    },
    "business_owner": {
        "name": "Hùng Pham",
        "age": 42,
        "segment": "Small Business Owner",
        "tone": "professional",
        "greeting": "Chào anh Hùng! Chúc năm mới phát tài phát lộc!",
        "has_motor": True,
        "has_health": True,
        "has_life": False,
        "income": "high",
        "business": "Restaurant",
        "tet_plans": "Business trip to Hanoi"
    }
}

# Tet timeline phases
TET_PHASES = {
    "pre-tet": {
        "name": "Pre-Tet Planning",
        "dates": "Mid-December to Late January",
        "focus": "Preparation, Protection, Smart Spending",
        "offers": "Early bird discounts, Bundle deals"
    },
    "tet-peak": {
        "name": "Tet Holiday Peak",
        "dates": "1 week before to 1 week after Tet",
        "focus": "Emergency support, Quick purchase",
        "offers": "Flash sales, Instant coverage, 24/7 claims"
    },
    "post-tet": {
        "name": "Post-Tet Season",
        "dates": "February onwards",
        "focus": "New year resolutions, Claim follow-ups",
        "offers": "Renewal reminders, Year-long protection"
    }
}

# Insurance products
INSURANCE_PRODUCTS = {
    "travel_domestic": {
        "name": "Domestic Travel Insurance",
        "price": 150000,
        "coverage": "50,000,000 VND",
        "duration": "Per trip (up to 15 days)"
    },
    "travel_international": {
        "name": "International Travel Insurance",
        "price": 500000,
        "coverage": "100,000,000 VND",
        "duration": "Annual coverage"
    },
    "motor_extension": {
        "name": "Motor Insurance Highway Extension",
        "price": 250000,
        "coverage": "Extended distance + passengers",
        "duration": "30 days"
    },
    "family_health": {
        "name": "Family Health Package",
        "price": 3500000,
        "coverage": "Up to 500,000,000 VND",
        "duration": "Annual"
    },
    "accident": {
        "name": "Personal Accident Insurance",
        "price": 300000,
        "coverage": "200,000,000 VND",
        "duration": "Annual"
    },
    "life_savings": {
        "name": "Life + Savings Insurance",
        "price": 5000000,
        "coverage": "1,000,000,000 VND + Returns",
        "duration": "Annual premium"
    }
}

class TetInsuranceAgent:
    def __init__(self, customer_profile, current_phase):
        self.profile = customer_profile
        self.phase = current_phase
    
    def generate_greeting(self):
        """Generate personalized Tet greeting"""
        greeting = self.profile['greeting']
        
        if self.phase == "pre-tet":
            return f"{greeting} Tết đang đến gần! Bạn đã chuẩn bị gì chưa? 🎊"
        elif self.phase == "tet-peak":
            return f"{greeting} Chúc mừng năm mới! 🧧 Tôi có thể giúp gì cho bạn?"
        else:
            return f"{greeting} Chúc bạn năm mới thật nhiều sức khỏe và thành công! 🎉"
    
    def analyze_needs(self):
        """Analyze customer needs based on profile"""
        recommendations = []
        
        # Travel-based recommendations
        if "Traveling" in self.profile.get('tet_plans', '') or "trip" in self.profile.get('tet_plans', '').lower():
            if not self.profile.get('has_travel'):
                recommendations.append({
                    "type": "travel",
                    "reason": f"Bạn đang có kế hoạch: {self.profile['tet_plans']}",
                    "products": ["travel_domestic", "motor_extension"]
                })
        
        # Family protection
        if self.profile.get('family_size', 0) > 2 and not self.profile.get('has_life'):
            recommendations.append({
                "type": "family",
                "reason": "Bảo vệ gia đình trong dịp Tết",
                "products": ["family_health", "life_savings"]
            })
        
        # Motor insurance extension
        if self.profile.get('has_motor') and "km" in self.profile.get('tet_plans', '').lower():
            recommendations.append({
                "type": "motor",
                "reason": "Hành trình dài cần bảo vệ tốt hơn",
                "products": ["motor_extension", "accident"]
            })
        
        # Business protection
        if self.profile.get('business'):
            recommendations.append({
                "type": "business",
                "reason": "Bảo vệ doanh nghiệp trong dịp nghỉ Tết",
                "products": ["accident", "life_savings"]
            })
        
        return recommendations
    
    def generate_product_recommendation(self, product_key):
        """Generate product recommendation message"""
        product = INSURANCE_PRODUCTS[product_key]
        
        if self.phase == "tet-peak":
            discount = 0.3
            special_price = int(product['price'] * (1 - discount))
            return f"""
🎊 **TẾT SPECIAL - {product['name']}**

Giá thường: {product['price']:,} VND
🎁 GIÁ TẾT: **{special_price:,} VND** (Giảm {int(discount*100)}%)

✅ Bảo hiểm: {product['coverage']}
✅ Thời hạn: {product['duration']}
⏰ Ưu đãi chỉ trong hôm nay!

Bạn có muốn tôi chuẩn bị gói này không?
"""
        else:
            return f"""
📋 **{product['name']}**

💰 Giá: {product['price']:,} VND
✅ Bảo hiểm: {product['coverage']}
✅ Thời hạn: {product['duration']}

Bạn quan tâm đến gói này không?
"""
    
    def generate_quick_quote(self, destination, duration=5):
        """Generate quick travel insurance quote"""
        if destination.lower() in ["thailand", "singapore", "malaysia", "philippines"]:
            base_price = 180000
            product_type = "travel_international"
        else:
            base_price = 120000
            product_type = "travel_domestic"
        
        total_price = base_price * (duration / 5)
        
        return f"""
✈️ **Báo giá nhanh - Bảo hiểm du lịch**

📍 Điểm đến: {destination}
📅 Thời gian: {duration} ngày
💰 Giá: **{int(total_price):,} VND**
🛡️ Bảo hiểm: 50,000,000 VND

Bao gồm:
✅ Y tế khẩn cấp
✅ Hành lý thất lạc
✅ Hủy chuyến bay
✅ Hỗ trợ 24/7

Muốn mua ngay không? Chỉ mất 1 phút! ⚡
"""

    def handle_claim_request(self):
        """Handle insurance claim process"""
        return """
🚨 **Hỗ trợ bồi thường ngay lập tức**

Tôi sẽ giúp bạn xử lý nhanh:

**Bước 1:** Bạn có an toàn chứ? Cần liên hệ khẩn cấp không?

**Bước 2:** Vui lòng chụp ảnh:
📸 Thiệt hại/vết thương
📸 Biển số xe (nếu tai nạn giao thông)
📸 Địa điểm xảy ra

**Bước 3:** Gửi ảnh cho tôi ngay

**Bước 4:** Tôi sẽ đăng ký hồ sơ và chuyên viên sẽ gọi cho bạn trong 30 phút

Bạn có thể gửi ảnh cho tôi bây giờ không?
"""

    def generate_response(self, user_input):
        """Generate contextual response based on user input"""
        user_input_lower = user_input.lower()
        
        # Claim handling
        if any(word in user_input_lower for word in ["tai nạn", "accident", "claim", "bồi thường", "bảo hiểm"]):
            return self.handle_claim_request()
        
        # Travel inquiry
        if any(word in user_input_lower for word in ["du lịch", "travel", "đi", "trip"]):
            # Try to extract destination
            destinations = ["thailand", "singapore", "da nang", "nha trang", "phu quoc", "ha noi", "sai gon"]
            found_destination = None
            for dest in destinations:
                if dest in user_input_lower:
                    found_destination = dest.title()
                    break
            
            if found_destination:
                return self.generate_quick_quote(found_destination)
            else:
                return "Tuyệt! Bạn dự định đi đâu trong dịp Tết? Tôi sẽ báo giá bảo hiểm du lịch ngay cho bạn! ✈️"
        
        # Price inquiry
        if any(word in user_input_lower for word in ["giá", "price", "bao nhiêu", "cost"]):
            recommendations = self.analyze_needs()
            if recommendations:
                product_key = recommendations[0]['products'][0]
                return self.generate_product_recommendation(product_key)
            else:
                return "Bạn quan tâm đến loại bảo hiểm nào? Tôi có thể báo giá:\n- Du lịch\n- Xe máy\n- Sức khỏe gia đình\n- Tai nạn cá nhân"
        
        # Positive responses
        if any(word in user_input_lower for word in ["yes", "có", "ok", "được", "đồng ý", "sure"]):
            return """
Tuyệt vời! 🎉

Tôi sẽ chuẩn bị hồ sơ cho bạn. Thanh toán qua:
💳 MoMo
💳 ZaloPay
💳 Chuyển khoản ngân hàng

Bạn muốn thanh toán bằng cách nào?

[Trong demo thực tế, đây sẽ là link thanh toán]
"""
        
        # Negative responses
        if any(word in user_input_lower for word in ["no", "không", "cancel", "thôi"]):
            return "Không sao! Nếu cần gì, cứ nhắn cho tôi nhé. Chúc bạn một mùa Tết vui vẻ! 🧧"
        
        # Default contextual response
        recommendations = self.analyze_needs()
        if recommendations:
            rec = recommendations[0]
            product_key = rec['products'][0]
            return f"""
Tôi hiểu rồi! 

{rec['reason']}, tôi nghĩ bạn nên xem xét:

{self.generate_product_recommendation(product_key)}
"""
        else:
            return "Tôi có thể giúp gì cho bạn? Hãy cho tôi biết về kế hoạch Tết của bạn! 🎊"

# Streamlit UI
def main():
    st.title("🧧 Tet Insurance AI Agent Demo")
    st.markdown("*Tư vấn bảo hiểm thông minh cho mùa Tết*")
    
    # Sidebar - Configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Customer Profile Selection
        st.subheader("👤 Customer Profile")
        profile_options = {
            "Young Professional (28)": "young_professional",
            "Family with Kids (35)": "family",
            "Senior/Retiree (55)": "senior",
            "Business Owner (42)": "business_owner"
        }
        
        selected_profile = st.selectbox(
            "Select Customer",
            options=list(profile_options.keys())
        )
        
        profile_key = profile_options[selected_profile]
        st.session_state.customer_profile = CUSTOMER_PROFILES[profile_key]
        
        # Display profile details
        with st.expander("📋 Profile Details"):
            profile = st.session_state.customer_profile
            st.write(f"**Name:** {profile['name']}")
            st.write(f"**Age:** {profile['age']}")
            st.write(f"**Segment:** {profile['segment']}")
            st.write(f"**Tet Plans:** {profile['tet_plans']}")
            st.write(f"**Current Insurance:**")
            st.write(f"- Motor: {'✅' if profile['has_motor'] else '❌'}")
            st.write(f"- Health: {'✅' if profile['has_health'] else '❌'}")
            st.write(f"- Life: {'✅' if profile['has_life'] else '❌'}")
        
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
        
        # Display phase details
        phase_info = TET_PHASES[st.session_state.current_phase]
        with st.expander("📊 Phase Details"):
            st.write(f"**Period:** {phase_info['dates']}")
            st.write(f"**Focus:** {phase_info['focus']}")
            st.write(f"**Offers:** {phase_info['offers']}")
        
        st.divider()
        
        # Quick Actions
        st.subheader("⚡ Quick Actions")
        
        if st.button("🎯 Generate Recommendations", use_container_width=True):
            agent = TetInsuranceAgent(
                st.session_state.customer_profile,
                st.session_state.current_phase
            )
            recommendations = agent.analyze_needs()
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": agent.generate_greeting()
            })
            
            if recommendations:
                rec_message = "Dựa trên hồ sơ của bạn, tôi có một số đề xuất:\n\n"
                for i, rec in enumerate(recommendations, 1):
                    rec_message += f"**{i}. {rec['reason']}**\n"
                    for product_key in rec['products'][:2]:
                        product = INSURANCE_PRODUCTS[product_key]
                        rec_message += f"   - {product['name']}: {product['price']:,} VND\n"
                    rec_message += "\n"
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": rec_message
                })
        
        if st.button("🔄 Reset Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.divider()
        
        # Statistics
        st.subheader("📈 Demo Statistics")
        st.metric("Messages", len(st.session_state.messages))
        st.metric("Current Phase", st.session_state.current_phase.replace("-", " ").title())
    
    # Main Chat Interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 Chat Interface")
        
        # Display chat messages
        chat_container = st.container(height=500)
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # Chat input
        user_input = st.chat_input("Type your message here...")
        
        if user_input:
            # Add user message
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
            
            # Generate AI response
            agent = TetInsuranceAgent(
                st.session_state.customer_profile,
                st.session_state.current_phase
            )
            
            response = agent.generate_response(user_input)
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })
            
            st.rerun()
        
        # Sample prompts
        st.markdown("**💡 Try these prompts:**")
        sample_prompts = [
            "Tôi muốn đi du lịch Thái Lan",
            "Giá bảo hiểm xe máy bao nhiêu?",
            "Tôi bị tai nạn, giúp tôi với",
            "Có gói nào cho gia đình không?"
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
                    
                    agent = TetInsuranceAgent(
                        st.session_state.customer_profile,
                        st.session_state.current_phase
                    )
                    
                    response = agent.generate_response(prompt)
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response
                    })
                    
                    st.rerun()
    
    with col2:
        st.subheader("📦 Available Products")
        
        for product_key, product in INSURANCE_PRODUCTS.items():
            with st.expander(f"💼 {product['name']}"):
                st.write(f"**Price:** {product['price']:,} VND")
                st.write(f"**Coverage:** {product['coverage']}")
                st.write(f"**Duration:** {product['duration']}")
                
                if st.session_state.current_phase == "tet-peak":
                    discount_price = int(product['price'] * 0.7)
                    st.success(f"🎁 Tet Special: {discount_price:,} VND (30% off)")
        
        st.divider()
        
        st.subheader("🎯 Agent Features")
        st.markdown("""
        **✅ Personalization**
        - Customer profile recognition
        - Tone adaptation
        - Context-aware responses
        
        **✅ Seasonality Awareness**
        - Tet timeline phases
        - Cultural moment triggers
        - Travel pattern detection
        
        **✅ Tactical Support**
        - Quick quote generator
        - Multi-channel sync
        - Claim fast-track
        - Decision tree logic
        """)

if __name__ == "__main__":
    main()
