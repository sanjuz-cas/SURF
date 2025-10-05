"""
SURF Setup Script
================
Automated setup for SURF Customer Feedback Agent

This script will:
1. Check Python version
2. Create virtual environment
3. Install dependencies
4. Setup .env file
5. Verify database connection
"""

import os
import sys
import subprocess
from pathlib import Path


def print_banner():
    """Display setup banner."""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   🌊 SURF - Customer Feedback Agent Setup                ║
    ║   Strategic User Retention & Feedback                    ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)


def check_python_version():
    """Check if Python version is 3.9 or higher."""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print(f"❌ Python 3.9+ required. Current: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def create_venv():
    """Create virtual environment."""
    print("\n📦 Creating virtual environment...")
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("⚠️  Virtual environment already exists. Skipping.")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False


def get_venv_python():
    """Get path to Python in virtual environment."""
    if sys.platform == "win32":
        return Path("venv/Scripts/python.exe")
    return Path("venv/bin/python")


def install_dependencies():
    """Install Python dependencies."""
    print("\n📚 Installing dependencies...")
    python_path = get_venv_python()
    
    try:
        subprocess.run(
            [str(python_path), "-m", "pip", "install", "--upgrade", "pip"],
            check=True
        )
        subprocess.run(
            [str(python_path), "-m", "pip", "install", "-r", "requirements.txt"],
            check=True
        )
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def setup_env_file():
    """Setup .env file from .env.example."""
    print("\n⚙️  Setting up environment configuration...")
    
    if Path(".env").exists():
        print("⚠️  .env file already exists. Skipping.")
        return True
    
    if not Path(".env.example").exists():
        print("❌ .env.example not found")
        return False
    
    try:
        with open(".env.example", "r") as src:
            content = src.read()
        with open(".env", "w") as dst:
            dst.write(content)
        print("✅ .env file created from template")
        print("⚠️  IMPORTANT: Edit .env and add your API keys and database credentials")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env: {e}")
        return False


def create_directories():
    """Create necessary directories."""
    print("\n📁 Creating directories...")
    directories = ["logs"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Directories created")
    return True


def display_next_steps():
    """Display next steps for the user."""
    print("\n" + "="*70)
    print("🎉 SETUP COMPLETE!")
    print("="*70)
    print("\n📋 Next Steps:\n")
    print("1. Edit the .env file with your credentials:")
    print("   - OPENAI_API_KEY")
    print("   - Database credentials (DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)")
    print("   - Slack webhook URL (optional)")
    print("\n2. Setup PostgreSQL database:")
    print("   createdb surf_feedback_db")
    print("   psql -d surf_feedback_db -f db/init_schema.sql")
    print("\n3. Activate virtual environment:")
    if sys.platform == "win32":
        print("   .\\venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("\n4. Run SURF:")
    print("   python backend/main.py")
    print("\n5. Or run in dry-run mode to test configuration:")
    print("   python backend/main.py --dry-run")
    print("\n" + "="*70)
    print("📚 Documentation: README.md")
    print("❓ Issues: https://github.com/sanjuz-cas/SURF/issues")
    print("="*70 + "\n")


def main():
    """Main setup function."""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_venv():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup .env file
    if not setup_env_file():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        sys.exit(1)
    
    # Display next steps
    display_next_steps()


if __name__ == "__main__":
    main()
