import time
import functools
from typing import Callable, Any, Tuple
import json

def estimate_tokens(text: str) -> int:
    """
    Mock token estimator logic (from original nodes.py).
    1 token ~ 4 characters.
    """
    return len(str(text)) // 4

def measure_latency_tokens(func: Callable[..., Any]) -> Callable[..., Tuple[Any, float, int]]:
    """
    A decorator that measures execution latency and estimates tokens for LLM generation functions.
    It wraps functions that return results, modifying the return type to append (result, latency_ms, tokens).
    
    Assumes the function arguments contain the prompt/history to measure input tokens, 
    and the function result is the raw LLM output or json object to measure output tokens.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Tuple[Any, float, int]:
        start_time = time.time()
        
        # Calculate input text size roughly by stringifying arguments
        # It's a simplistic estimation similar to the original manual one.
        input_text = " ".join(str(arg) for arg in args) + " ".join(str(v) for v in kwargs.values())
        
        # Execute the original function
        result = func(*args, **kwargs)
        
        latency = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Ensure we only stringify the direct result for token counting, 
        # avoid duplicating counting if the decorated function already returned (result, lat, tok)
        if isinstance(result, tuple) and len(result) == 3 and isinstance(result[1], float) and isinstance(result[2], int):
            # If the inner function still manually returned tuple, just pass it through
            return result
            
        output_text = json.dumps(result) if isinstance(result, dict) else str(result)
        
        tokens = estimate_tokens(input_text + output_text)
        
        return result, latency, tokens
        
    return wrapper
