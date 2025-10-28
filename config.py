# Configuration file for Tet Insurance AI Agent
# Customize these settings to match your business needs

# App Settings
APP_TITLE = "Tet Insurance AI Agent Demo"
APP_ICON = "🧧"
COMPANY_NAME = "ABC Insurance Vietnam"

# Tet Season Dates (customize based on actual Tet calendar)
TET_2025_DATE = "2025-01-29"  # Actual Tet date
PRE_TET_START = "2024-12-15"
PRE_TET_END = "2025-01-28"
TET_PEAK_START = "2025-01-22"
TET_PEAK_END = "2025-02-05"
POST_TET_START = "2025-02-06"

# Discount Settings
TET_PEAK_DISCOUNT = 0.30  # 30% discount during peak
EARLY_BIRD_DISCOUNT = 0.15  # 15% discount for pre-Tet
BUNDLE_DISCOUNT = 0.20  # 20% discount for multiple products

# Response Time Settings
TARGET_RESPONSE_TIME = 30  # seconds
CLAIM_CALLBACK_TIME = 30  # minutes

# Payment Methods
PAYMENT_METHODS = ["MoMo", "ZaloPay", "VNPay", "Bank Transfer"]

# Messaging Platforms
SUPPORTED_PLATFORMS = ["Zalo", "Facebook Messenger", "Website Chat", "Mobile App"]

# Agent Behavior
DEFAULT_TONE = "friendly"  # casual, friendly, formal, professional
USE_EMOJIS = True
MAX_RECOMMENDATIONS = 3
AUTO_FOLLOW_UP_DAYS = 3

# Product Catalog
PRODUCT_CATEGORIES = [
    "Travel Insurance",
    "Motor Insurance", 
    "Health Insurance",
    "Life Insurance",
    "Accident Insurance",
    "Property Insurance"
]

# Customer Segments
CUSTOMER_SEGMENTS = [
    "young_professional",
    "family",
    "senior",
    "business_owner",
    "student"
]

# Vietnamese Language Settings
LANGUAGE = "vi"  # Vietnamese
FALLBACK_LANGUAGE = "en"  # English

# Cultural Customization
USE_FORMAL_GREETINGS_FOR_SENIORS = True
INCLUDE_LUCKY_NUMBERS = True  # 8, 9 considered lucky
AVOID_UNLUCKY_NUMBERS = True  # 4 considered unlucky

# Analytics
TRACK_CONVERSIONS = True
TRACK_ENGAGEMENT = True
TRACK_RESPONSE_TIME = True

# Feature Flags
ENABLE_QUICK_QUOTE = True
ENABLE_CLAIM_SUPPORT = True
ENABLE_PRODUCT_RECOMMENDATIONS = True
ENABLE_MULTI_CHANNEL_SYNC = True
ENABLE_GAMIFICATION = False  # Lì xì (red envelope) features

# Compliance
GDPR_COMPLIANT = True
REQUIRE_CONSENT = True
DATA_RETENTION_DAYS = 365

# Demo Mode Settings
DEMO_MODE = True
SIMULATE_PAYMENT = True
SIMULATE_CLAIMS = True
SHOW_DEBUG_INFO = False
