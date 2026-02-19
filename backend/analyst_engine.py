from backend.market_events import MARKET_EVENTS
import streamlit as st

class FinancialAnalyst:
    def __init__(self, current_event=None, persona=None, round_num=1, total_value=1000000):
        self.event = current_event
        self.persona = persona
        self.round = round_num
        self.value = total_value
        
    def get_context_advice(self, query):
        query = query.lower()
        
        # 1. Intent: Definitions
        definitions = {
            "repo rate": "The rate at which the RBI lends money to commercial banks. A higher rate usually controls inflation but slows growth.",
            "cvar": "Conditional Value at Risk. It measures the 'tail risk' of a portfolio, specifically the average loss in the worst-case scenarios.",
            "nbfc": "Non-Banking Financial Companies. They provide banking services without holding a full banking license, often more agile but higher risk.",
            "twin deficit": "A situation where a country has both a fiscal deficit (spending > revenue) and a current account deficit (imports > exports).",
            "fii": "Foreign Institutional Investors. Large entities like pension funds or insurance companies from other countries investing in India."
        }
        
        for key in definitions:
            if key in query:
                return f"INSTITUTIONAL DEFINTION: {definitions[key]}"

        # 2. Intent: Historical Context
        if "happened" in query or "history" in query or "past" in query:
            if self.event:
                return f"HISTORICAL AUDIT: {self.event['description']} {self.event.get('recovery', '')}"
            return "Please select a market event to analyze historical context."

        # 3. Intent: Strategic Guidance
        if "help" in query or "rebalance" in query or "strategy" in query or "what should i do" in query:
            if not self.event:
                return "Strategic guidance is most effective once a market scenario is active. Please select an event."
            
            impact = self.event['impact']
            safe_havens = [k for k, v in impact.items() if v >= 0]
            crashing = [k for k, v in impact.items() if v < -0.2]
            
            advice = f"REBALANCING LOGIC (R{self.round}): Based on the {self.event['title']}, we are seeing significant pressure on {', '.join(crashing)}. "
            if self.persona:
                p_name = self.persona.get('player_name', 'Strategist')
                advice += f"For your profile ({p_name}), I recommend prioritizing {', '.join(safe_havens)} to preserve capital. "
            
            return advice

        # Default Response
        return "I am monitoring the current terminal state. You can ask me about market definitions, strategic rebalancing, or historical event context."

def get_quick_questions(event):
    if not event:
        return ["What is Repo Rate?", "Explain CVAR", "How to rebalance?"]
    
    return [
        f"How will this affect my {list(event['impact'].keys())[0]}?",
        "Tell me about the historical recovery.",
        "Strategic advice for this scenario."
    ]
