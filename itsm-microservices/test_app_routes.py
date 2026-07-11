#!/usr/bin/env python
import sys
sys.path.insert(0, '.')

from src.main import app

print("[INFO] App loaded")
print(f"[INFO] Total routes: {len(app.routes)}")

auth_routes = [r for r in app.routes if hasattr(r, 'path') and '/auth' in r.path]
print(f"[INFO] Auth routes found: {len(auth_routes)}")

for route in auth_routes:
    print(f"  - {route.path}")

if not auth_routes:
    print("[ERROR] NO AUTH ROUTES FOUND!")
    print("\n[INFO] All routes:")
    for route in app.routes:
        if hasattr(route, 'path'):
            print(f"  - {route.path}")
