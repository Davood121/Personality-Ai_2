"""
Setup script for the AI Personality Learning System
"""
import os
import sys
import subprocess
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = [
        "memory",
        "logs",
        "exports"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"  ✓ Created {directory}/")
    
    print("✅ All directories created!")

def setup_environment():
    """Set up environment file"""
    print("🔧 Setting up environment...")
    
    if not os.path.exists('.env'):
        # Copy example env file
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("  ✓ Created .env file from template")
            print("  ⚠️  Please edit .env file and add your API keys!")
        else:
            # Create basic .env file
            with open('.env', 'w') as f:
                f.write("# AI Personality Learning System Environment Variables\n")
                f.write("# Add your API keys here\n\n")
                f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
                f.write("GOOGLE_API_KEY=your_google_api_key_here\n")
                f.write("GOOGLE_CSE_ID=your_google_custom_search_engine_id_here\n")
            print("  ✓ Created basic .env file")
            print("  ⚠️  Please edit .env file and add your API keys!")
    else:
        print("  ✓ .env file already exists")

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing module imports...")
    
    modules = [
        'personality_engine',
        'web_searcher', 
        'question_generator',
        'memory_system',
        'learning_engine',
        'main_ai'
    ]
    
    failed_imports = []
    
    for module in modules:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"❌ Failed to import: {', '.join(failed_imports)}")
        return False
    else:
        print("✅ All modules imported successfully!")
        return True

def create_run_scripts():
    """Create convenient run scripts"""
    print("📝 Creating run scripts...")
    
    # Windows batch file
    with open('run_ai.bat', 'w') as f:
        f.write('@echo off\n')
        f.write('echo Starting AI Personality Learning System...\n')
        f.write('python main_ai.py\n')
        f.write('pause\n')
    
    # Unix shell script
    with open('run_ai.sh', 'w') as f:
        f.write('#!/bin/bash\n')
        f.write('echo "Starting AI Personality Learning System..."\n')
        f.write('python main_ai.py\n')
    
    # Make shell script executable on Unix systems
    if os.name != 'nt':
        os.chmod('run_ai.sh', 0o755)
    
    print("  ✓ Created run_ai.bat (Windows)")
    print("  ✓ Created run_ai.sh (Unix/Linux/Mac)")

def display_usage_instructions():
    """Display usage instructions"""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    print()
    print("📋 NEXT STEPS:")
    print("1. Edit the .env file and add your API keys:")
    print("   - OpenAI API key (optional, for advanced features)")
    print("   - Google Custom Search API key (for web searching)")
    print("   - Google Custom Search Engine ID")
    print()
    print("2. Run the AI system:")
    print("   • Continuous learning: python main_ai.py")
    print("   • Interactive mode:   python main_ai.py interactive")
    print("   • Single cycle:       python main_ai.py single")
    print("   • Limited cycles:     python main_ai.py 10")
    print()
    print("3. Or use the convenience scripts:")
    print("   • Windows: run_ai.bat")
    print("   • Unix/Linux/Mac: ./run_ai.sh")
    print()
    print("🔗 API SETUP HELP:")
    print("• Google Custom Search: https://developers.google.com/custom-search/v1/introduction")
    print("• OpenAI API: https://platform.openai.com/api-keys")
    print()
    print("🤖 The AI will:")
    print("• Generate infinite questions about personality")
    print("• Search the web for answers")
    print("• Store knowledge in memory files")
    print("• Evolve its learning strategy over time")
    print("• Develop its own personality traits")
    print()
    print("📁 Files created in:")
    print("• memory/ - Knowledge and learning data")
    print("• logs/ - System logs (future use)")
    print("• exports/ - Data exports (future use)")
    print()
    print("Happy learning! 🧠✨")

def main():
    """Main setup function"""
    print("🚀 Setting up AI Personality Learning System...")
    print()
    
    # Step 1: Create directories
    create_directories()
    print()
    
    # Step 2: Install requirements
    if not install_requirements():
        print("❌ Setup failed at package installation")
        return False
    print()
    
    # Step 3: Setup environment
    setup_environment()
    print()
    
    # Step 4: Test imports
    if not test_imports():
        print("❌ Setup failed at import testing")
        return False
    print()
    
    # Step 5: Create run scripts
    create_run_scripts()
    print()
    
    # Step 6: Display instructions
    display_usage_instructions()
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
