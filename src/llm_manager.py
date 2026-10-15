import os
from typing import Optional, Tuple
from dotenv import load_dotenv

# Ensure environment is loaded
load_dotenv()

_active_llm = None
_active_provider = "mock"
_active_model = "Rule-based Fallback Engine"

def get_active_llm():
    """Returns the configured LLM instance, or None if in fallback mode."""
    global _active_llm, _active_provider, _active_model
    
    if _active_llm is not None:
        return _active_llm
    
    # OpenAI
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    if openai_key and not openai_key.startswith("your_") and not openai_key == "sk-...":
        try:
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2, api_key=openai_key, timeout=8)
            _active_llm = llm
            _active_provider = "OpenAI"
            _active_model = "gpt-4o-mini"
            return llm
        except Exception as e:
            print(f"[LLM Manager] Error loading OpenAI: {e}")

    # Gemini
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")
    gemini_key = gemini_key.strip() if gemini_key else ""
    if gemini_key and not gemini_key.startswith("your_"):
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2, google_api_key=gemini_key, timeout=8)
            _active_llm = llm
            _active_provider = "Google Gemini"
            _active_model = "gemini-1.5-flash"
            return llm
        except Exception as e:
            print(f"[LLM Manager] Error loading Gemini: {e}")

    _active_llm = None
    _active_provider = "Mock Engine"
    _active_model = "Rule-based Fallback"
    return None

def get_ai_status() -> dict:
    """Returns current AI connectivity metadata."""
    llm = get_active_llm()
    return {
        "connected": llm is not None,
        "provider": _active_provider,
        "model": _active_model,
        "has_openai_key": bool(os.getenv("OPENAI_API_KEY") and not os.getenv("OPENAI_API_KEY").startswith("your_")),
        "has_gemini_key": bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
    }

def verify_and_save_key(provider: str, api_key: str) -> Tuple[bool, str]:
    """Tests the API key and persists it to .env if valid."""
    api_key = api_key.strip()
    if not api_key:
        return False, "API key cannot be empty."

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(base_dir, ".env")
    
    if provider.lower() == "openai":
        try:
            from langchain_openai import ChatOpenAI
            test_llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key, timeout=10)
            test_res = test_llm.invoke("Reply with 'OK'")
            
            # Persist to environment and file
            os.environ["OPENAI_API_KEY"] = api_key
            _update_env_file(env_path, "OPENAI_API_KEY", api_key)
            get_active_llm()
            return True, f"Successfully connected to OpenAI (gpt-4o-mini)!"
        except Exception as e:
            err = str(e)
            if "Incorrect API key" in err or "invalid_api_key" in err:
                return False, "Invalid OpenAI API key. Please check your key at platform.openai.com."
            elif "insufficient_quota" in err:
                return False, "OpenAI API key has exceeded its quota or has no credits available."
            return False, f"OpenAI connection error: {err[:120]}"

    elif provider.lower() in ["gemini", "google"]:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            test_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, timeout=10)
            test_res = test_llm.invoke("Reply with 'OK'")
            
            os.environ["GEMINI_API_KEY"] = api_key
            os.environ["GOOGLE_API_KEY"] = api_key
            _update_env_file(env_path, "GEMINI_API_KEY", api_key)
            get_active_llm()
            return True, f"Successfully connected to Google Gemini (gemini-1.5-flash)!"
        except Exception as e:
            return False, f"Gemini connection error: {str(e)[:120]}"

    return False, f"Unknown provider: {provider}"

def _update_env_file(filepath: str, key_name: str, key_value: str):
    """Updates or appends a key in the .env file."""
    lines = []
    found = False
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            lines = f.readlines()
            
    new_lines = []
    for line in lines:
        if line.strip().startswith(f"{key_name}="):
            new_lines.append(f"{key_name}={key_value}\n")
            found = True
        else:
            new_lines.append(line)
            
    if not found:
        new_lines.append(f"{key_name}={key_value}\n")
        
    with open(filepath, "w") as f:
        f.writelines(new_lines)
