import re
import random
import time
from typing import *
import logging

logger = logging.getLogger(__name__)

Message = Dict[str, Any]

def get_backdoor_components(response: str) -> Optional[Tuple[str, str, str]]:
    """Get the correct solution, backdoor code, fail input, and failure hint from the response"""
    correct_solution = re.findall(r'<correct_solution>(.+)</correct_solution>', response, re.DOTALL)
    if len(correct_solution) == 0:
        return None
    correct_solution_extracted = correct_solution[-1]   
    
    fail_input = re.findall(r'<fail_input>(.+)</fail_input>', response, re.DOTALL)
    if len(fail_input) == 0:
        return None
    fail_input_extracted = fail_input[-1]
    
    failure_hint = re.findall(r'<failure_hint>(.+)</failure_hint>', response, re.DOTALL)
    if len(failure_hint) == 0:
        return (correct_solution_extracted, fail_input_extracted, "No hint found")
    failure_hint_extracted = failure_hint[-1]
    
    backdoor_code = re.findall(r'<subtly_wrong_solution>(.+)</subtly_wrong_solution>', response, re.DOTALL)
    if len(backdoor_code) == 0:
        return None
    backdoor_code_extracted = backdoor_code[-1]
    
    return correct_solution_extracted, fail_input_extracted, failure_hint_extracted, backdoor_code_extracted
    
def exponential_backoff(attempt):
    wait_time = min(300, (2 ** attempt) + random.uniform(0, 1))
    logger.info(f"Rate limit hit. Waiting {wait_time:.2f} seconds (attempt {attempt})")
    time.sleep(wait_time)

MODEL_COSTS = {
    "gpt-4o": {"input": 2.5, "output": 10, "cached_input": 1.25},  # per 1M tokens
    "gpt-4o-mini": {"input": 0.15, "output": 0.6, "cached_input": 0.075},
    "o1": {"input": 15, "output": 60, "cached_input": 7.5},
    "o3-mini": {"input": 1.1, "output": 4.4, "cached_input": 0.55},
    # Add other models as needed
}