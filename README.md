# TDS Quiz Solver — Final Project Submission

This repository contains the complete implementation of my API solver for the TDS Quiz evaluation.  
It follows the project requirements exactly:  
• Uses a public API endpoint  
• Accepts POST quiz tasks  
• Solves multi-step quiz flows  
• Supports CSV, PDF, table scraping, and LLM-based reasoning  
• Submits answers back within the required time limit  
• Includes defender & attacker prompts  
• Licensed under MIT  
• Compatible with HuggingFace Spaces (CPU Basic)

---

## 📌 API Endpoint Specification

### **POST /**  
Your endpoint must accept:

```json
{
  "email": "your email",
  "secret": "your secret",
  "url": "quiz url"
}
