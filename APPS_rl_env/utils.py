import re
import random
import time
from typing import *
import logging

logger = logging.getLogger(__name__)

Message = Dict[str, Any]

def extract_honest_code(messages: List[Message]) -> Optional[str]:
    """Extract the honest code from the messages"""
    message = messages[-1]
    assert message["role"] == "assistant"
    code = re.findall(r'<cpp>(.+)</cpp>', message["content"], re.DOTALL)
    if len(code) == 0:
        return None
    # Return the last code block
    return code[-1]

def get_backdoor_components(response: str) -> Optional[Tuple[str, str, str]]:
    """Get the backdoor code, fail input, and failure hint from the response"""
    backdoor_code = re.findall(r'<subtly_wrong_solution>(.+)</subtly_wrong_solution>', response, re.DOTALL)
    if len(backdoor_code) == 0:
        return None
    backdoor_code_extracted = backdoor_code[-1]   
    
    fail_input = re.findall(r'<fail_input>(.+)</fail_input>', response, re.DOTALL)
    if len(fail_input) == 0:
        return None
    fail_input_extracted = fail_input[-1]
    
    failure_hint = re.findall(r'<failure_hint>(.+)</failure_hint>', response, re.DOTALL)
    if len(failure_hint) == 0:
        return (backdoor_code_extracted, fail_input_extracted, "No hint found")
    failure_hint_extracted = failure_hint[-1]
    
    return backdoor_code_extracted, fail_input_extracted, failure_hint_extracted
    
def exponential_backoff(attempt):
    wait_time = min(300, (2 ** attempt) + random.uniform(0, 1))
    logger.info(f"Rate limit hit. Waiting {wait_time:.2f} seconds (attempt {attempt})")
    time.sleep(wait_time)
