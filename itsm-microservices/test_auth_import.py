#!/usr/bin/env python
import sys
sys.path.insert(0, '.')

try:
    from src.auth.api import router
    print("[OK] Import successful")
    print(f"[OK] Router: {router}")
    print(f"[OK] Routes: {[r.path for r in router.routes]}")
except Exception as e:
    print(f"[ERROR] Import failed: {e}")
    import traceback
    traceback.print_exc()
