#!/usr/bin/env python3
"""
Test script for OpenAI API Key
This script tests if your OpenAI API key is working correctly
"""

import os
import sys
from dotenv import load_dotenv

def load_api_key():
    """Load OpenAI API key from .env file or environment"""
    load_dotenv()
    
    # Try to get API key from .env file or environment
    api_key = "sk-qrstefghuvwxabcdqrstefghuvwxabcdqrstefgh"
    
    if not api_key:
        print("❌ OPENAI_API_KEY not found!")
        print("📝 Please add your OpenAI API key to .env file:")
        print("   OPENAI_API_KEY=your_openai_api_key_here")
        print("🔗 Get your API key from: https://platform.openai.com/api-keys")
        return None
    
    if api_key.startswith("sk-uvwxijklmnop1234uvwxijklmnop1234uvwxijkl"):
        print("❌ Please replace the placeholder with your actual OpenAI API key!")
        return None
    
    return api_key

def test_openai_connection(api_key):
    """Test OpenAI API connection"""
    try:
        import openai
        print("✅ OpenAI library imported successfully")
        
        # Set up the client
        client = openai.OpenAI(api_key=api_key)
        print("✅ OpenAI client initialized")
        
        # Test with a simple chat completion
        print("🔄 Testing API connection...")
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say 'Hello, OpenAI API is working!' in one sentence."}
            ],
            max_tokens=50,
            temperature=0.7
        )
        
        answer = response.choices[0].message.content
        print(f"✅ API Response: {answer}")
        
        # Test embeddings (optional)
        try:
            print("🔄 Testing embeddings...")
            embedding_response = client.embeddings.create(
                model="text-embedding-ada-002",
                input="Test embedding"
            )
            
            embedding_length = len(embedding_response.data[0].embedding)
            print(f"✅ Embeddings working! Vector length: {embedding_length}")
            
        except Exception as e:
            print(f"⚠️ Embeddings test failed: {e}")
        
        return True
        
    except ImportError:
        print("❌ OpenAI library not installed!")
        print("💡 Install it with: pip install openai")
        return False
        
    except openai.AuthenticationError:
        print("❌ Authentication failed! Check your API key.")
        print("🔗 Get a valid API key from: https://platform.openai.com/api-keys")
        return False
        
    except openai.RateLimitError:
        print("❌ Rate limit exceeded! Please try again later.")
        return False
        
    except openai.APIError as e:
        print(f"❌ OpenAI API error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def check_account_info(api_key):
    """Check account information and usage"""
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        
        print("\n📊 Account Information:")
        print("🔄 Checking account details...")
        
        # Note: The new OpenAI API doesn't have direct account info endpoints
        # We can only test if the key works with actual API calls
        print("✅ API key is valid and working!")
        print("💡 For detailed usage info, visit: https://platform.openai.com/usage")
        
    except Exception as e:
        print(f"⚠️ Could not fetch account info: {e}")

def main():
    """Main test function"""
    print("🔑 OpenAI API Key Test")
    print("=" * 40)
    
    # Load API key
    api_key = load_api_key()
    if not api_key:
        sys.exit(1)
    
    print(f"✅ API Key loaded: {api_key[:8]}...{api_key[-4:]}")
    
    # Test connection
    if test_openai_connection(api_key):
        print("\n🎉 OpenAI API test successful!")
        check_account_info(api_key)
        
        print("\n💡 Next steps:")
        print("   - Your OpenAI API key is working correctly")
        print("   - You can now use it in your applications")
        print("   - Check usage at: https://platform.openai.com/usage")
        
    else:
        print("\n❌ OpenAI API test failed!")
        print("💡 Please check your API key and try again")
        sys.exit(1)

if __name__ == "__main__":
    main() 