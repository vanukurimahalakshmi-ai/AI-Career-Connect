import os
import json
import requests
from flask import current_app

class MistralService:
    def __init__(self, api_key=None, model=None):
        self.api_key = api_key or os.environ.get('MISTRAL_API_KEY', '')
        self.model = model or os.environ.get('MISTRAL_MODEL', 'mistral-small-latest')
        self.api_url = "https://api.mistral.ai/v1/chat/completions"

    def _call_mistral(self, system_prompt, user_prompt, temperature=0.7):
        """Sends chat request to Mistral API with fallback to built-in simulation."""
        if not self.api_key or self.api_key.strip() == '':
            return None  # Trigger mock fallback

        headers = {
            "Authorization": f"Bearer {self.api_key.strip()}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature,
            "response_format": {"type": "json_object"}
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=12)
            if response.status_code == 200:
                res_data = response.json()
                content = res_data['choices'][0]['message']['content']
                return json.loads(content)
        except Exception as e:
            print(f"[MistralService] API call notice: {e}. Using simulated response engine.")

        return None

    def generate_interview_question(self, role, topic, level):
        """Generates a technical/behavioral mock interview question."""
        system_prompt = "You are a Senior Principal Interviewer at a top AI technology company. Generate a relevant technical or behavioral question in JSON format."
        user_prompt = f"Role: {role}, Topic: {topic}, Experience Level: {level}. Return JSON with key 'question' and key 'hints'."

        result = self._call_mistral(system_prompt, user_prompt)
        if result and 'question' in result:
            return result

        # Mock Fallback Questions based on topic & role
        questions = {
            "Technical Behavioral & Architecture": f"Can you walk me through a challenging architectural decision you made while working as a {role}? How did you handle trade-offs between performance and maintainability?",
            "System Design & Scalability": f"Design a high-throughput real-time AI recommendation system for a platform with 10 million daily active users. What database and caching strategies would you employ?",
            "Coding & Algorithms": "Explain the time and space complexity trade-offs between using a hash map vs a binary search tree for fast lookup in a memory-constrained application.",
            "AI & Machine Learning": "How do you mitigate model hallucinations and optimize latency when deploying LLM inference pipelines in production?"
        }
        question_text = questions.get(topic, f"Explain a major technical project you led as a {role} and how you measured its business impact.")
        return {
            "question": question_text,
            "hints": ["Focus on metrics and quantitative results", "Use the STAR method (Situation, Task, Action, Result)", "Mention concurrency or system bottlenecks if applicable"]
        }

    def evaluate_interview_response(self, question, candidate_answer, role):
        """Evaluates candidate response and returns score + feedback."""
        system_prompt = "You are a Senior Technical Hiring Manager. Evaluate the candidate's interview answer and return JSON with 'score' (number 0-100), 'feedback' (detailed string), and 'key_takeaways' (array of strings)."
        user_prompt = f"Question: {question}\nCandidate Answer: {candidate_answer}\nTarget Role: {role}"

        result = self._call_mistral(system_prompt, user_prompt)
        if result and 'score' in result:
            return result

        # Smart fallback evaluation calculation
        word_count = len(candidate_answer.split())
        score = min(95, max(60, 65 + (word_count // 5)))
        
        feedback = f"Great response! You covered key aspects relevant to {role}. "
        if word_count < 25:
            feedback += "Consider elaborating further on specific technical implementations and metrics achieved."
        else:
            feedback += "Your technical terminology and structure were strong. Adding specific metrics will elevate your answer even further."

        return {
            "score": score,
            "feedback": feedback,
            "key_takeaways": [
                "Good technical context",
                "Clear communication structure",
                "Recommend incorporating quantitative metrics"
            ]
        }

    def analyze_resume(self, resume_text, target_role):
        """Analyzes resume text against a target job role."""
        system_prompt = "You are an Executive Career Coach and Resume Auditor. Evaluate the resume text against the target role and return JSON."
        user_prompt = f"Target Role: {target_role}\nResume Content:\n{resume_text}\nReturn JSON with keys 'match_score' (0-100), 'strengths' (array of strings), 'missing_skills' (array of strings), and 'recommendations' (array of strings)."

        result = self._call_mistral(system_prompt, user_prompt)
        if result and 'match_score' in result:
            return result

        # Fallback simulation
        return {
            "match_score": 82,
            "strengths": [
                "Strong background in software engineering fundamentals",
                "Demonstrated hands-on experience with modern backend APIs",
                "Clear project delivery track record"
            ],
            "missing_skills": [
                "Vector Databases (Pinecone/ChromaDB)",
                "System design for distributed AI inference",
                "CI/CD pipeline automation for MLOps"
            ],
            "recommendations": [
                f"Highlight specific project outcomes related to {target_role}",
                "Add quantifiable metrics (e.g., 'Improved performance by 35%')",
                "Include certifications or project portfolios in generative AI/Flask APIs"
            ]
        }

    def generate_career_roadmap(self, target_role, current_level):
        """Generates a structured career progression roadmap."""
        system_prompt = "You are an AI Career Strategist. Generate a step-by-step career path roadmap in JSON format."
        user_prompt = f"Target Role: {target_role}, Current Level: {current_level}. Return JSON with 'roadmap_title' and 'milestones' (array of objects with 'title', 'timeframe', 'skills', 'description')."

        result = self._call_mistral(system_prompt, user_prompt)
        if result and 'milestones' in result:
            return result

        return {
            "roadmap_title": f"Mastery Roadmap: Transition to {target_role}",
            "milestones": [
                {
                    "title": "Phase 1: Core Foundation & API Mastery",
                    "timeframe": "Month 1 - 2",
                    "skills": ["Flask", "SQLite/SQLAlchemy", "RESTful Design", "Python Async"],
                    "description": "Master clean software architecture, database indexing, and robust REST API design."
                },
                {
                    "title": "Phase 2: AI & LLM Integration",
                    "timeframe": "Month 3 - 4",
                    "skills": ["Mistral API", "LangChain/LlamaIndex", "Embeddings", "STT/TTS"],
                    "description": "Build end-to-end intelligent voice and text applications integrating Mistral AI and speech models."
                },
                {
                    "title": "Phase 3: Production System Design & MLOps",
                    "timeframe": "Month 5 - 6",
                    "skills": ["Docker", "Redis Caching", "CI/CD", "Monitoring"],
                    "description": "Deploy scalable applications with automated testing, rate limiting, and observability."
                }
            ]
        }
