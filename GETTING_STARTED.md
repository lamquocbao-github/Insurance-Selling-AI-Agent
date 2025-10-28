# 🚀 Getting Started - Quick Guide

## Welcome! 👋

You have successfully received the complete Tet Insurance AI Agent package. This guide will get you up and running in minutes.

---

## 📦 What You Have

**14 Files Total:**

### Applications (2):
1. `tet_insurance_agent.py` - Hard-coded version
2. `tet_insurance_agent_gemini.py` - Gemini-powered version ⭐

### Documentation (5):
1. `INDEX.md` - **START HERE** - Complete package overview
2. `README.md` - Hard-coded version guide
3. `README_GEMINI.md` - Gemini version guide (recommended)
4. `ARCHITECTURE.md` - Technical deep-dive
5. `COMPARISON.md` - Feature comparison

### Quick Start Scripts (4):
1. `start.sh` - Run hard-coded (Mac/Linux)
2. `start.bat` - Run hard-coded (Windows)
3. `start_gemini.sh` - Run Gemini (Mac/Linux)
4. `start_gemini.bat` - Run Gemini (Windows)

### Configuration (3):
1. `requirements.txt` - Hard-coded dependencies
2. `requirements_gemini.txt` - Gemini dependencies
3. `config.py` - Settings file

---

## ⚡ Quick Start (Choose Your Path)

### Path A: Simple Demo (2 minutes)

**No API key needed, works offline**

```bash
# Install
pip install streamlit

# Run
streamlit run tet_insurance_agent.py
```

Then:
1. Select a customer profile
2. Choose Tet phase
3. Try sample prompts
4. See template-based responses

### Path B: AI-Powered Demo (5 minutes) ⭐ RECOMMENDED

**Requires free Gemini API key**

1. **Get API Key** (2 minutes):
   - Visit: https://makersuite.google.com/app/apikey
   - Sign in with Google
   - Click "Create API Key"
   - Copy the key

2. **Install & Run** (3 minutes):
   ```bash
   # Install dependencies
   pip install -r requirements_gemini.txt
   
   # Run application
   streamlit run tet_insurance_agent_gemini.py
   ```

3. **Configure**:
   - Paste API key in sidebar
   - Select customer profile
   - Choose Tet phase

4. **Experience AI**:
   - Natural conversations
   - Semantic search
   - Memory system
   - View knowledge base

---

## 🎯 What to Try First

### In Hard-Coded Version:
1. ✅ Generate recommendations (button in sidebar)
2. ✅ Try sample prompts
3. ✅ Switch between customer profiles
4. ✅ Change Tet phases
5. ✅ Notice template responses

### In Gemini Version:
1. ✅ Generate proactive message (AI-created)
2. ✅ Ask unexpected questions
3. ✅ View knowledge base (see what AI knows)
4. ✅ View memory (see conversation context)
5. ✅ Try multi-turn conversations
6. ✅ Notice dynamic responses

---

## 💡 Try These Conversations

Copy and paste these into the chat:

### Basic:
```
Tôi muốn đi du lịch Thái Lan dịp Tết
```

### Complex:
```
Tôi có 3 người trong gia đình, con 5 tuổi, vợ 32 tuổi. 
Cần bảo hiểm gì cho Tết?
```

### Price Negotiation:
```
Giá có vẻ hơi cao, có thể giảm không?
```

### Unexpected:
```
Nếu tôi bị tai nạn ở nước ngoài thì sao?
```

---

## 🔍 Understanding the Difference

**Type the same question in both versions:**

**Question:** "Tôi muốn bảo hiểm cho chuyến về quê"

**Hard-Coded Response:**
- Template-based
- Same every time
- Generic information
- Fixed structure

**Gemini Response:**
- AI-generated
- Unique each time
- References your profile
- Asks follow-up questions
- Natural conversation

**Try it yourself to see the difference!**

---

## 📚 Next Steps

### After Quick Start:

1. **Read INDEX.md** (5 minutes)
   - Complete overview
   - Feature comparison
   - Use case recommendations

2. **Read COMPARISON.md** (10 minutes)
   - Detailed examples
   - Side-by-side comparison
   - When to use which version

3. **Explore Architecture** (Optional, 15 minutes)
   - Read ARCHITECTURE.md
   - Understand how it works
   - Learn about components

### For Implementation:

1. **Customize Profiles**
   - Edit customer profiles in code
   - Add your own insurance products
   - Modify Tet phases

2. **Extend Knowledge Base**
   - Add more customer history
   - Include product details
   - Add seasonal insights

3. **Deploy**
   - Choose deployment platform
   - Set up monitoring
   - Configure scaling

---

## 🆘 Troubleshooting

### "Module not found" Error
```bash
pip install -r requirements_gemini.txt
```

### "Invalid API Key" Error
- Verify you copied the complete key
- Check at: https://makersuite.google.com/app/apikey
- Make sure you have internet connection

### "Port already in use" Error
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Application Won't Start
```bash
# Check Python version (need 3.8+)
python --version

# Reinstall dependencies
pip install --upgrade -r requirements_gemini.txt
```

---

## 💰 Costs

### Hard-Coded Version:
- **Setup:** FREE
- **Running:** FREE
- **Deployment:** FREE (Streamlit Cloud free tier)

### Gemini Version:
- **Setup:** FREE (free API key)
- **Running:** ~$0.01-0.02 per conversation
- **Free Tier:** 60 requests per minute
- **Deployment:** ~$5-20/month (Streamlit Cloud or Cloud Run)

**Example:** 1,000 conversations/month = ~$10-20

---

## 🎓 Learning Path

### Beginner (You are here):
- ✅ Run hard-coded version
- ✅ Try Gemini version
- ✅ Compare experiences
- ⬜ Read documentation

### Intermediate:
- ⬜ Customize profiles
- ⬜ Add new products
- ⬜ Modify knowledge base
- ⬜ Test different scenarios

### Advanced:
- ⬜ Deploy to production
- ⬜ Integrate with CRM
- ⬜ Add payment gateway
- ⬜ Implement analytics
- ⬜ Scale infrastructure

---

## 🎯 Key Takeaways

After trying both versions, you'll understand:

1. ✅ **Hard-coded = Fast to build**, but limited and robotic
2. ✅ **Gemini = More setup**, but natural and intelligent
3. ✅ **Semantic search** finds relevant info by meaning
4. ✅ **Memory system** enables coherent conversations
5. ✅ **Knowledge base** provides context for AI
6. ✅ **Dynamic responses** feel more human

---

## 📞 Support

### Documentation:
- **INDEX.md** - Complete overview
- **README_GEMINI.md** - Detailed guide
- **ARCHITECTURE.md** - Technical details
- **COMPARISON.md** - Feature comparison

### Code:
- All code is commented
- Class docstrings included
- Method explanations provided
- Examples in comments

### Community:
- Streamlit docs: https://docs.streamlit.io
- Gemini docs: https://ai.google.dev/docs
- Stack Overflow: Tag with "streamlit" and "gemini"

---

## ✨ Best Practices

### When Testing:
1. Try both versions with same questions
2. Test edge cases and unexpected queries
3. Switch between customer profiles
4. Change Tet phases to see adaptation
5. Check knowledge base viewer
6. Inspect memory system

### When Customizing:
1. Start with config.py for simple changes
2. Add to knowledge base before modifying code
3. Test after each change
4. Keep backup of working version
5. Document your modifications

### When Deploying:
1. Test thoroughly in development
2. Set up proper monitoring
3. Implement error handling
4. Configure rate limiting
5. Plan for scaling

---

## 🎉 You're Ready!

**Time Investment:**
- Quick demo: 2 minutes
- Full exploration: 30 minutes
- Deep understanding: 2 hours
- Production ready: 1 week

**What You Can Build:**
- Insurance chatbot
- Customer service assistant
- Sales qualification tool
- Lead generation system
- Product recommendation engine

**Start Now:**
```bash
# Simple version
streamlit run tet_insurance_agent.py

# AI version
streamlit run tet_insurance_agent_gemini.py
```

---

## 📝 Checklist

- [ ] Installed Python 3.8+
- [ ] Installed dependencies
- [ ] Tried hard-coded version
- [ ] Got Gemini API key
- [ ] Tried Gemini version
- [ ] Compared both versions
- [ ] Read INDEX.md
- [ ] Read COMPARISON.md
- [ ] Explored knowledge base
- [ ] Inspected memory system
- [ ] Tested custom scenarios
- [ ] Reviewed documentation
- [ ] Ready to customize!

---

**Welcome to the future of insurance marketing! 🚀**

**Questions? Start with INDEX.md for complete overview!**

🧧 Chúc mừng năm mới! 🎊
