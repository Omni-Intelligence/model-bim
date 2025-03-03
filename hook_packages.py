
import sys
import os

# Add package directories to path at runtime
package_dirs = ['xhtml2pdf', 'markdown2', 'tkinterweb', 'tkinterdnd2']
for pkg in package_dirs:
    pkg_path = os.path.join(sys._MEIPASS, pkg)
    if os.path.exists(pkg_path) and pkg_path not in sys.path:
        sys.path.insert(0, pkg_path)
        print(f"Added {pkg_path} to path")
