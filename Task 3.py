"""
simple_ai_chatbot.py

A lightweight local "AI" chatbot with simple NLP (no external models).
- Uses fuzzy matching to respond from a knowledge base.
- Lets you teach the bot new Q->A pairs interactively.
- Saves learned knowledge to knowledge.json and chat logs to chat_log.txt.

How to use:
- Run in IDLE (File -> New File -> paste -> Save as simple_ai_chatbot.py -> F5)
- Type messages into the IDLE shell.
- Commands:
    help                - show built-in commands
    show                - display loaded Q->A pairs
    save                - save knowledge immediately
    exit                - quit the chatbot
    teach: Q => A        - teach a new mapping in one line
Example teach command:
    teach: What is AI? => AI stands for Artificial Intelligence.
"""

import json
import os
import re
import difflib
from datetime import datetime

KB_FILENAME = "knowledge.json"
LOG_FILENAME = "chat_log.txt"

# -------------------- Utilities --------------------
def preprocess(text: str) -> str:
    """Lowercase, strip, remove extra whitespace and some punctuation."""
    text = text.lower().strip()
    # replace some punctuation with spaces, keep alphanumerics and basic punctuation
    text = re.sub(r"[^\w\s\?']", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

def similarity(a: str, b: str) -> float:
    """Return a fuzzy similarity score between 0 and 1 using difflib."""
    return difflib.SequenceMatcher(None, a, b).ratio()

def load_knowledge(filename=KB_FILENAME):
    """Load knowledge base from JSON file (list of {'q':..., 'a':...})."""
    if not os.path.exists(filename):
        # default starter knowledge
        starter = [
            {"q": "hello", "a": "Hello! How can I help you today?"},
            {"q": "hi", "a": "Hi there! Ask me anything or type 'help' for commands."},
            {"q": "how are you", "a": "I'm a bot — always ready to help! How are you?"},
            {"q": "what is your name", "a": "I'm a simple NLP chatbot created to help you learn."},
            {"q": "help", "a": "Type your question. Commands: help, show, save, exit, teach: Q => A"}
        ]
        save_knowledge(starter, filename)
        return starter
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                print("Knowledge file format invalid — resetting to starter knowledge.")
                return []
    except Exception as e:
        print("Failed to load knowledge:", e)
        return []

def save_knowledge(kb, filename=KB_FILENAME):
    """Save knowledge base to JSON file."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(kb, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print("Error saving knowledge:", e)
        return False

def append_log(user, bot_resp):
    """Append one line to chat log with timestamp."""
    ts = datetime.now().isoformat(sep=" ", timespec="seconds")
    try:
        with open(LOG_FILENAME, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] USER: {user}\n")
            f.write(f"[{ts}] BOT: {bot_resp}\n")
    except Exception:
        pass

# -------------------- Core chatbot --------------------
class SimpleChatbot:
    def __init__(self):
        self.kb = load_knowledge()
        # store preprocessed questions for faster matching
        self.kb_pre = [(preprocess(item["q"]), item["a"]) for item in self.kb]

    def find_best_answer(self, user_text, min_score=0.55):
        """Find the best matching Q in knowledge base using fuzzy similarity."""
        u = preprocess(user_text)
        best_score = 0.0
        best_answer = None
        best_q = None
        for q_pre, a in self.kb_pre:
            score = similarity(u, q_pre)
            if score > best_score:
                best_score = score
                best_answer = a
                best_q = q_pre
        return best_score, best_q, best_answer

    def teach(self, question, answer):
        """Teach the bot a new Q->A pair and persist it."""
        q = question.strip()
        a = answer.strip()
        if not q or not a:
            return False, "Question and answer must be non-empty."
        # check duplicate
        for item in self.kb:
            if preprocess(item["q"]) == preprocess(q):
                return False, "I already have a similar question in my knowledge base."
        new = {"q": q, "a": a}
        self.kb.append(new)
        self.kb_pre.append((preprocess(q), a))
        saved = save_knowledge(self.kb)
        if saved:
            return True, "Learned successfully and saved to knowledge."
        else:
            return True, "Learned successfully but failed to save to disk."

    def handle(self, user_text):
        """Main handler: process user text and return bot response and flag learned(boolean)."""
        text = user_text.strip()
        if not text:
            return "Please type something.", False

        # Check for commands
        if text.lower() == "help":
            return ("Commands:\n"
                    " - help : show this message\n"
                    " - show : list known questions\n"
                    " - save : save knowledge to disk\n"
                    " - exit : quit chatbot\n"
                    " - teach: Q => A  (teach a new mapping in one line)\n"
                    "You can also ask normal questions.", False)

        if text.lower() == "show":
            lines = ["Known Q->A pairs:"]
            for i, item in enumerate(self.kb, 1):
                lines.append(f"{i}. Q: {item['q']}  =>  A: {item['a']}")
            return "\n".join(lines), False

        if text.lower() == "save":
            ok = save_knowledge(self.kb)
            return ("Knowledge saved." if ok else "Failed to save knowledge."), False

        if text.lower() == "exit":
            return "exit", False

        # Inline teach format: teach: question => answer
        teach_match = re.match(r"^\s*teach\s*:\s*(.+?)\s*=>\s*(.+)$", text, flags=re.IGNORECASE)
        if teach_match:
            q = teach_match.group(1).strip()
            a = teach_match.group(2).strip()
            ok, msg = self.teach(q, a)
            return msg, ok

        # Normal Q: find best answer
        score, matched_q, answer = self.find_best_answer(text)
        # debug: print(score)
        if score >= 0.70:
            return answer + f"\n\n( matched: {matched_q} — score {score:.2f} )", False
        elif score >= 0.55 and answer:
            # provide probable answer but ask for confirmation/feedback
            return (answer + f"\n\n( I'm somewhat confident — matched: {matched_q} — score {score:.2f} )\n"
                    "If this is not correct, you can teach me the right answer using:\n"
                    "teach: your question => correct answer"), False
        else:
            # fallback: ask to teach
            fallback = ("I don't have a good answer for that yet.\n"
                        "You can teach me in one line like:\n"
                        "teach: Your question text => The answer you want me to give\n"
                        "Or type 'help' for commands.")
            return fallback, False

# -------------------- Run loop --------------------
def chat_loop():
    print("Simple NLP Chatbot (type 'help' for commands, 'exit' to quit)\n")
    bot = SimpleChatbot()
    while True:
        try:
            user = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting. Goodbye!")
            break

        response, learned = bot.handle(user)
        if response == "exit":
            print("Bot: Goodbye! (chat saved)")
            break

        print("Bot:", response)
        append_log(user, response)

# -------------------- Entry point --------------------
if __name__ == "__main__":
    chat_loop()
