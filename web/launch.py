#!/usr/bin/env python3
"""
Launcher for Video Compressor Web Interface.
Checks dependencies and starts the server.
"""

import subprocess
import sys
import os

def check_and_install_flask():
    """Check if Flask is installed, install if needed."""
    try:
        import flask
        print(f"✓ Flask {flask.__version__} is installed")
        return True
    except ImportError:
        print("Flask is not installed. Attempting to install...")

        try:
            # Try installing Flask
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install',
                'flask', 'werkzeug', '--quiet'
            ])
            print("✓ Flask installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("✗ Failed to install Flask automatically")
            print("\nPlease install Flask manually:")
            print("  python3 -m pip install flask werkzeug")
            print("\nOr use Homebrew:")
            print("  brew install python-flask")
            return False

def main():
    print("=" * 60)
    print("Video Compressor Web Interface - Launcher")
    print("=" * 60)
    print()

    # Check Flask
    if not check_and_install_flask():
        return 1

    print()
    print("Starting server...")
    print("=" * 60)
    print()

    # Change to web directory
    web_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(web_dir)

    # Import and run the app
    try:
        # Add parent directory to path for SDK imports
        sys.path.insert(0, os.path.join(web_dir, '..', 'src'))

        # Import app
        from app import app

        print("Server starting at: http://localhost:5000")
        print("Press Ctrl+C to stop")
        print("=" * 60)
        print()

        # Run Flask app
        app.run(debug=True, host='0.0.0.0', port=5000)

    except KeyboardInterrupt:
        print("\nServer stopped")
        return 0
    except Exception as e:
        print(f"\n✗ Error starting server: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
